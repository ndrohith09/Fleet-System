from django.db.models.signals import pre_save
from django.dispatch import receiver
import uuid
from .models import *

@receiver(pre_save,sender=FleetModel)
def create_fleet_id(sender,instance,**kwargs):
    if instance.id in [None,""]:
        count = FleetModel.objects.count()
        id = str(uuid.uuid4())[:7] + str(count+1)[:1]
        res=FleetModel.objects.filter(id=id)
        while res.exists():
            id = str(uuid.uuid4())[:7] + str(count+1)[:1]
        instance.id=id  
    
@receiver(pre_save,sender=Camera)
def create_camera_id(sender,instance,**kwargs):
    if instance.id in [None,""]:
        count = Camera.objects.count()
        id = str(uuid.uuid4())[:7] + str(count+1)[:1]
        res=Camera.objects.filter(id=id)
        while res.exists():
            id = str(uuid.uuid4())[:7] + str(count+1)[:1]
        instance.id=id  
    
