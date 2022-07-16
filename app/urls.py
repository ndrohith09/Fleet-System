from django.urls import path , include 
from app.views import * 

urlpatterns = [ 
    path('camera/', CameraView.as_view() , name='camera'),
    path('fleet/',FleetView.as_view() , name='fleet'),
    path('fleet-in-out/',FleetEntryExit.as_view() , name='fleet-in-out'),
    path('fleet-details/',FleetDetails.as_view() , name='fleet-details'),
    path('fleet-live/',FleetLiveActivity.as_view() , name='fleet-live'),
]