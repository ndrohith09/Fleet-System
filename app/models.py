from django.db import models

# Create your models here.

''' vehicle Model '''


class FleetModel(models.Model):
    id = models.CharField(max_length=256, primary_key=True, unique=True)
    # vehicle machinery number
    asset_id = models.CharField(max_length=10, unique=True, editable=False)
    asset_name = models.CharField(max_length=256, null=True, blank=True)   # vehicle machinery name
    number_plate = models.CharField(max_length=256, null=True, blank=True, unique=True, editable=False)
    driver_name = models.CharField(max_length=256, null=True, blank=True)  # driver name

    '''
    logs = {
        'in_unit': True,
        'entry': [
            {
                'time': '',
                'gate': '',
                'camera': '',
                'latitude': '',
                'longitude': '',
                'location': {
                    "full_address" : "",
                    "locality" : "",
                    "pincode" : ""
                }
            }
        ],
        'exit': [
            {
                'time': '',
                'gate': '',
                'camera': '',
                'latitude': '',
                'longitude': '',
                'location': {
                    "full_address" : "",
                    "locality" : "",
                    "pincode" : ""
                }
            }
        ],
        'updated_at': 'updated_at',
        'date': ''
    }
    '''

    logs = models.JSONField(default=dict, blank=True)
    access = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id + self.asset_id


''' camera Model '''


class Camera(models.Model):
    id = models.CharField(max_length=256, primary_key=True, unique=True)
    number = models.CharField(max_length=50, null=True,blank=True, editable=False, unique=True)
    latitude = models.CharField(max_length=50, null=True, blank=True)  # latitude
    longitude = models.CharField( max_length=50, null=True, blank=True)  # longitude
    gate_number = models.CharField(max_length=50, null=True, blank=True)  # gate number
    entry = models.BooleanField(default=True)  # entry or exit
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id + self.number
