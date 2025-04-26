from rest_framework import serializers 
from .models import Server , ServerMetric 

class ServerSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Server
        fields = ['id','name','ip_address','description','is_active']

class ServerMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServerMetric
        fields = '__all__'
        
