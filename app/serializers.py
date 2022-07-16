from rest_framework.serializers import ModelSerializer
from .models import *

class FleetSerializer(ModelSerializer):
	class Meta:
		model = FleetModel
		fields='__all__'

	def __init__(self, *args, **kwargs):
		super(FleetSerializer, self).__init__(*args, **kwargs) 
		request = self.context.get('request')
		if request and request.method == 'POST':
			self.Meta.depth = 0
		elif request and request.method == 'PUT':
			self.Meta.depth = 0 
		else:
			self.Meta.depth = 4	

class CameraSerializer(ModelSerializer):
	class Meta:
		model = Camera
		fields='__all__'

	def __init__(self, *args, **kwargs):
		super(CameraSerializer, self).__init__(*args, **kwargs) 
		request = self.context.get('request')
		if request and request.method == 'POST':
			self.Meta.depth = 0
		elif request and request.method == 'PUT':
			self.Meta.depth = 0 
		else:
			self.Meta.depth = 4	