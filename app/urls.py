from django.urls import path , include 
from app.views import * 

urlpatterns = [ 
    path('', home, name='index'),
    path('logs/', logs, name='logs'),
    path('camera/', addCamera, name='camera'),
    path('vehicle/', addVehicle, name='vehicle'),
    path('activity-logs/' , activity_logs, name='activity_logs'),
]