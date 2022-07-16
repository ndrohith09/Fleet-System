from django.shortcuts import render
from torch import rand
from app.models import FleetModel , Camera ,ActivityLog
from datetime import datetime
import uuid , random

# Create your views here.

def home(request):
    # Camera.objects.all().delete()
    return render(request, 'index.html')

def addVehicle(request):
    if request.method == 'POST':
        assetid = request.POST.get('assetid')
        assetName = request.POST.get('assetName')
        numberPlate = request.POST.get('numberPlate')
        driverName = request.POST.get('driverName') 
                                
        count = random.randint(0,10)

        # save to database
        FleetModel.objects.create( 
            id = str(uuid.uuid4())[:7] + str(count+1)[:1],
            assetid = assetid , 
            assetName = assetName , 
            numberPlate = numberPlate , 
            driverName = driverName ,  
        ) 
        return render(request, 'vehicle.html', {'message': 'Successfully added'})
        
    return render(request, 'vehicle.html')

def addCamera(request):
    if request.method == 'POST': 
        number = request.POST.get('number')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        gate_number = request.POST.get('gate_number')
        
        count = random.randint(0,10)

        # save to database
        Camera.objects.create(  
            id = str(uuid.uuid4())[:7] + str(count+1)[:1],
            number = number , 
            latitude = latitude , 
            longitude = longitude , 
            gate_number = gate_number , 
        ) 
        return render(request, 'camera.html', {'message': 'Successfully added'})
        
    return render(request, 'camera.html')


def logs(request):
    # create vechicle log 
    # number_plate = request.POST.get('number_plate') 
    # camera_num = request.POST.get('camera')  

    number_plate = "TN10AB1234" 
    camera_num = 1 

    # get camera data 
    camera_data = Camera.objects.filter(number=camera_num).first()
    vehicle_data = FleetModel.objects.filter(numberPlate=number_plate).first() 

    if vehicle_data is not None: 
        authorized  = True
    else :
        authorized = False

    if camera_num.startswith('ENTRY'):
        logs = {
            'entry' : True ,
            'entry_time' : datetime.now() , 
            'exit_time' : "",
            'gate_number' : camera_data.gate_number , 
            'camera_number' : camera_data.number , 
            'latitude' : camera_data.latitude ,
            'longitude' : camera_data.longitude , 
            'authorized' : authorized
        }

        # add logs to Fleet Model 
        vehicle_data.logs = logs
        vehicle_data.save() 

        # add logs to Activity Log 
        ActivityLog.objects.create(
            activity = logs
        )
    else : 
        logs = {
            'entry' : False ,
            'exit_time' : datetime.now() , 
            'entry_time' : "",
            'gate_number' : camera_data.gate_number , 
            'camera_number' : camera_data.number , 
            'latitude' : camera_data.latitude ,
            'longitude' : camera_data.longitude , 
            'authorized' : authorized
        }
            
        # add logs to Fleet Model
        vehicle_data.logs = logs
        vehicle_data.save() 

        # add logs to Activity Log
        ActivityLog.objects.create(
            activity = logs
        )

    return render(request, 'logs.html')

def activity_logs(request):
    logs = ActivityLog.objects.all()
    return render(request, 'activity.html', {'logs': logs})