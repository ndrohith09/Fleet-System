from django.urls import path , include 
from app.views import * 

urlpatterns = [ 
    path('camera/', CameraView.as_view() , name='camera'),
    path('fleet/',FleetView.as_view() , name='fleet'),
]