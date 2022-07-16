from django.db import models

# Create your models here.

''' vehicle Model '''
class FleetModel(models.Model):
    id = models.CharField(max_length=256, primary_key=True,unique=True)
    assetid = models.CharField(max_length=10 , unique=True , editable=False) # vehicle machinery number
    assetName = models.CharField(max_length=256 , null=True , blank=True)   # vehicle machinery name 
    numberPlate = models.CharField(max_length=256 , null=True , blank=True) # 
    driverName = models.CharField(max_length=256 , null=True , blank=True) # driver name
    
    '''
    logs = {
        'entry' : 'true/false',
        'entry_time' : 'entry_time', 
        'exit_time' : 'exit_time', 
        'gate_number' : 'gate_number',
        'camera_number' : 'camera_number',
        'latitude' : 'latitude', 
        'longitude' : 'longitude',
        'updated_at' : 'updated_at',
        'authorized' : 'true/false',
    }
    '''
    
    logs = models.JSONField(default=dict , blank= True)
 
    created_at=models.DateTimeField(auto_now_add=True) 
    def __str__(self):
        return self.id + self.assetid

''' camera Model '''
class Camera(models.Model):
    id = models.CharField(max_length=256, primary_key=True,unique=True) 
    number = models.CharField(max_length=50, null=True , blank=True) # camera number [ ENTRY1 , EXIT2]
    latitude = models.CharField(max_length=50, null=True , blank=True) # latitude 
    longitude = models.CharField(max_length=50, null=True , blank=True) # longitude
    gate_number = models.CharField(max_length=50, null=True , blank=True) # gate number 
    def __str__(self) :
        return self.id + self.number

class ActivityLog(models.Model):
    id = models.CharField(max_length=256, primary_key=True,unique=True) 
    activity = models.JSONField(default=dict , blank= True)