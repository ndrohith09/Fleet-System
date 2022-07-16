from django.shortcuts import render
from app.models import *
from app.serializers import *
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from datetime import date, datetime as dtt, time
from django.conf import settings
import requests

"""---------Date Time Format---------"""
dmY = "%d-%m-%Y"
Ymd = '%Y-%m-%d'
Ydm = '%Y-%d-%m'
mdY = "%m-%d-%Y"
IMp = "%I:%M %p"
HMS = "%H:%M:%S"
dBY = "%d %B,%Y"
#dtt.strptime(date.today(), '%Y-%m-%d').strftime(dmY)


def number_plate_model(img):
    number_plate = 'TN10AV0001'
    return number_plate

def decodelocation(lat,lon):
    """
    This function takes lat,lon as paramter and gives a certain json address in Str full address format
    """
    azure_maps_url = "https://atlas.microsoft.com/search/address/reverse/json"
    queryparams = {
        "subscription-key":settings.AZURE_SUBSCRIPTION_KEY,
        "api-version": "1.0",
        "query": f"{lat},{lon}"
    }
    reverse_code = requests.get(url=azure_maps_url,params=queryparams)
    geo_data = reverse_code.json()
    return geo_data

def check_fleet_authorization(fleet_id):
    """
    This function takes fleet_id as parameter and checks if the fleet is authorized or not
    """
    fleet = FleetModel.objects.filter(id=fleet_id).first()
    if fleet is None:
        return {
            "access" : False,
            "message" : "Fleet number not found in database. Unauthorized vehicle detected"
        }
    if fleet.access == True:
        return {
            "access" : True,
            "message" : "Fleet is authorize"
        }
    else:
        return {
            "access" : False,
            "message" : "Fleet number not authorized. Your fleet has been blocked by the administrative"
        }


class CameraView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        '''
        This function of POST method is used to add a new Camera to the database.
        '''
        data = request.data
        number = data.get('number', None)
        latitude = data.get('latitude', None)
        longitude = data.get('longitude', None)
        gate_number = data.get('gate_number', None)
        entry = data.get('entry', None)

        val_arr = [None, '']
        val_bool = [True, False]

        if number in val_arr or latitude in val_arr or longitude in val_arr or gate_number in val_arr:
            return Response({'msg': 'Please fill all the fields'}, status=status.HTTP_404_NOT_FOUND)

        if entry not in val_bool:
            return Response({'msg': 'Please fill all the fields bool'}, status=status.HTTP_404_NOT_FOUND)

        '''check_cam_number'''
        cameras = Camera.objects.filter(number=number).first()
        if cameras is not None:
            return Response({'msg': 'Camera already exists'}, status=status.HTTP_404_NOT_FOUND)

        try:
            new_cam = Camera.objects.create(
                number=number,
                latitude=latitude,
                longitude=longitude,
                gate_number=gate_number,
                entry=entry
            )
            return Response({'msg': 'Camera added successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'msg': 'Error adding camera', 'data': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        '''
        This function of GET method is used to get all the cameras from the database.
        query_params:
            id : get a specific camera by ***number***
        '''
        id = request.query_params.get('number', None)

        json_data = []

        if id is not None:
            camera = Camera.objects.filter(id=id).first()
            if camera is None:
                return Response({'msg': 'Camera not found'}, status=status.HTTP_404_NOT_FOUND)

            json_data.append({
                'id': camera.id,
                'number': camera.number,
                'latitude': camera.latitude,
                'longitude': camera.longitude,
                'gate_number': camera.gate_number,
                'entry': camera.entry,
                'available': camera.available
            })

        else:
            camera = Camera.objects.all()
            for cam in camera:
                json_data.append({
                    'id': cam.id,
                    'number': cam.number,
                    'latitude': cam.latitude,
                    'longitude': cam.longitude,
                    'gate_number': cam.gate_number,
                    'entry': cam.entry,
                    'available': cam.available
                })

        return Response({'msg': 'Cameras retrieved successfully', 'data': json_data}, status=status.HTTP_200_OK)

    def put(self, request):
        '''
            This function of PUT method is used to update a camera in the database.
            data:
                id : get a specific camera by id
        '''
        data = request.data
        id = data.get('id', None)
        latitude = data.get('latitude', None)
        longitude = data.get('longitude', None)
        gate_number = data.get('gate_number', None)
        entry = data.get('entry', None)
        available = data.get('available', None)
        access = data.get('access', None)

        val_arr = [None, '']
        val_bool = [True, False]

        if id in val_arr:
            return Response({'msg': 'Please provide camera id'}, status=status.HTTP_404_NOT_FOUND)

        get_cam = Camera.objects.filter(id=id).first()
        if get_cam is None:
            return Response({'msg': 'Camera not found'}, status=status.HTTP_404_NOT_FOUND)

        """Update the data"""
        if latitude is not None:
            get_cam.latitude = latitude

        if longitude is not None:
            get_cam.longitude = longitude

        if gate_number is not None:
            get_cam.gate_number = gate_number

        if entry is not None and entry in val_bool:
            get_cam.entry = entry

        if available is not None and available in val_bool:
            get_cam.available = available

        if access is not None and access in val_bool:
            get_cam.access = access

        get_cam.save()
        return Response({'msg': 'Camera updated successfully'}, status=status.HTTP_200_OK)


class FleetView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        '''create a new vehicle'''

        data = request.data
        asset_id = data.get('asset_id', None)
        asset_name = data.get('asset_name', None)
        number_plate = data.get('number_plate', None)
        driver_name = data.get('driver_name', None)

        val_arr = [None, '']

        if asset_id in val_arr or asset_name in val_arr or number_plate in val_arr or driver_name in val_arr:
            return Response({'msg': 'Please fill all the fields'}, status=status.HTTP_404_NOT_FOUND)

        '''check_vehicle_number'''
        chk_vh = FleetModel.objects.filter(
            Q(number_plate=number_plate) | Q(asset_id=asset_id)).first()
        if chk_vh is not None:
            return Response({'msg': 'Vehicle already exists'}, status=status.HTTP_404_NOT_FOUND)

        try:
            new_vh = FleetModel.objects.create(
                asset_id=asset_id,
                asset_name=asset_name,
                number_plate=number_plate,
                driver_name=driver_name,
                logs=[]
            )
            return Response({'msg': 'Vehicle added successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'msg': 'Error adding vehicle', 'data': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        """
            Get the particular vehicle information 
            query_params:
                asset_id : get a specific vehicle by id
        """
        data = request.data
        asset_id = data.get('asset_id', None)

        json_data = []

        val_arr = [None, '']

        if asset_id in val_arr:
            fleets = FleetModel.objects.all()

            for fleet in fleets:
                json_data.append({
                    'id': fleet.id,
                    'asset_id': fleet.asset_id,
                    'asset_name': fleet.asset_name,
                    'number_plate': fleet.number_plate,
                    'driver_name': fleet.driver_name,
                    'access': fleet.access,
                    'logs': fleet.logs
                })

        else:
            fleet = FleetModel.objects.filter(asset_id=asset_id).first()
            if fleet is None:
                return Response({'msg': 'Vehicle not found'}, status=status.HTTP_404_NOT_FOUND)

            json_data.append({
                'id': fleet.id,
                'asset_id': fleet.asset_id,
                'asset_name': fleet.asset_name,
                'number_plate': fleet.number_plate,
                'driver_name': fleet.driver_name,
                'access': fleet.access,
                'logs': fleet.logs
            })

        return Response({'msg': 'Vehicles retrieved successfully', 'data': json_data}, status=status.HTTP_200_OK)

    def put(self, request):
        ''''
            updating the vehicle views
            query_params:
                asset_id : get a specific vehicle by id
        '''

        data = request.data
        asset_id = data.get('asset_id', None)

        val_arr = [None, '']
        val_bool = [True, False]

        if asset_id in val_arr:
            return Response({'msg': 'Please provide vehicle id'}, status=status.HTTP_404_NOT_FOUND)

        get_vh = FleetModel.objects.filter(asset_id=asset_id).first()
        if get_vh is None:
            return Response({'msg': 'Vehicle not found'}, status=status.HTTP_404_NOT_FOUND)

        asset_name = data.get('asset_name', None)
        driver_name = data.get('driver_name', None)
        access = data.get('access', None)

        if asset_name not in val_arr:
            get_vh.asset_name = asset_name

        if driver_name not in val_arr:
            get_vh.driver_name = driver_name

        if access in val_bool:
            get_vh.access = access

        get_vh.save()
        return Response({'msg': 'Vehicle updated successfully'}, status=status.HTTP_200_OK)


class FleetEntryExit(APIView):
    authentication_classes = []
    permission_classes = []

    location_data = {
        "full_address" : "",
        "locality" : "",
        "pincode" : ""
    }
    log_data = {
        'time': '',
        'gate': '',
        'camera': '',
        'latitude': '',
        'longitude': '',
        'location': ''
    }
    default_logs = {
        'in_unit': True,
        'entry': [],
        'exit': [],
        'updated_at': str(dtt.now()),
        'date': str(date.today())
    }

    def post(self, request):
        """
            Entry of a fleet
            ---------------------------
            form_data:
                img : get a specific vehicle image from react
                camera_number : get a specific camera by number
            --------------------------
            Process the model and then return then numberplates of the fleets
        """

        camera_number = request.data.get('camera_number', None)
        img = request.data.get('img', None)

        val_arr = [None, '']

        if img in val_arr:
            return Response({'msg': 'Please provide image'}, status=status.HTTP_404_NOT_FOUND)

        if camera_number in val_arr:
            return Response({'msg': 'Please provide camera number'}, status=status.HTTP_404_NOT_FOUND)

        '''Processing the image here'''
        vh_plate = number_plate_model("test")
        if vh_plate in val_arr:
            return Response({'msg': 'Model didnt process the image properly'}, status=status.HTTP_404_NOT_FOUND)

        get_vh = FleetModel.objects.filter(number_plate=vh_plate).first()
        if get_vh is None:
            return Response({'msg': 'Vehicle not found'}, status=status.HTTP_404_NOT_FOUND)
        serializers = FleetSerializer(get_vh, context={'request': request})

        """-------------------Checking the camera number exists or not-------------------"""
        get_camera = Camera.objects.filter(number=camera_number).first()
        if get_camera is None:
            return Response({'msg': 'Camera not found'}, status=status.HTTP_404_NOT_FOUND)
        serializers_camera = CameraSerializer(get_camera, context={'request': request})

        """-------------------
            Checking the vehicle authorization here.
            If entry cam:
                Unauthorized vehicle is entering into unit
            else:
                Unauthorized vehicle is exiting from unit
            --------------------
        """
        check_access = check_fleet_authorization(get_vh.id)
        if check_access['status'] == False:
            if serializers_camera['entry'] == True:
                return Response({'msg': 'Unauthorized vehicle is entering into unit','msg':check_access['msg']}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'msg': 'Unauthorized vehicle is exiting from unit','msg':check_access['msg']}, status=status.HTTP_404_NOT_FOUND)
        

        """--------------------Get the logs of current date.First check if the logs are empty 
            or not.If empty, then create a new log.If not empty, 
            then get the logs of current date.-------------------------
        """
        if len(serializers['logs']) == 0:
            serializers['logs'].append(self.default_logs)

        now_date = str(date.today())
        now_index = None

        #Time Complexity raising to peaks area less than O(1) <= x <= O(n)
        for i, log in enumerate(serializers['logs']):
            if log['date'] == now_date:
                now_index = i
                break

        if now_index is None:
            serializers['logs'].append(self.default_logs)
            now_index = len(serializers['logs']) - 1

        """
            This view is based on entry view , so update the entry view.
            default_logs['in_unit'] = True
            default_logs['entry'] = [{self.log_data}]
            default_logs['updated_at'] = str(dtt.now())
            ------------------------------
            Step-1 : Get the camera data from the camera model using the lat,lon
            Step-2 : Process the lat and long to get the location in address
            Step-3 : Update the entry view
            --------------------------------
            log_data = {
                'time': '',
                'gate': '',
                'camera': '',
                'latitude': '',
                'longitude': '',
                'location': {
                    "full_address" : "",
                    "locality" : "",
                    "pincode" : "",
                }
            }
        """
        #Azure location Maps
        geo_data = decodelocation(serializers_camera['latitude'],serializers_camera['longitude'])
        zipcode = geo_data['addresses'][0]['address']['postalCode']
        zipcode = zipcode.replace(" ","")
        freeformaddress = geo_data['addresses'][0]['address']['freeformAddress']
        city = geo_data['addresses'][0]['address']['localName']

        #Location Data
        loc_data = self.location_data
        loc_data['full_address'] = freeformaddress
        loc_data['locality'] = city
        loc_data['pincode'] = zipcode
        
        #Log Data
        now_time = dtt.now()
        log_data = self.log_data
        log_data['time'] = now_time.strftime(HMS) #dtt.strptime(date.today(), '%Y-%m-%d').strftime(dmY)
        log_data['gate'] = serializers_camera['gate_number']
        log_data['camera'] = serializers_camera['number']
        log_data['latitude'] = serializers_camera['latitude']
        log_data['longitude'] = serializers_camera['longitude']
        log_data['location'] = loc_data

        #Update the entry view
        if serializers_camera['entry'] == True:
            serializers['logs'][now_index]['in_unit'] = True
            serializers['logs'][now_index]['entry'].append(log_data)
        else:
            serializers['logs'][now_index]['in_unit'] = False
            serializers['logs'][now_index]['exit'].append(log_data)
        serializers['logs'][now_index]['updated_at'] = str(dtt.now())


        #Update the database
        get_vh.logs = serializers['logs']
        get_vh.save()

        return Response({'msg': 'Vehicle entry successful', 'number_plate': vh_plate}, status=status.HTTP_200_OK)
           

