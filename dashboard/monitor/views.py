from django.core.cache import cache
from rest_framework import generics,status 
from rest_framework.response import Response 
from rest_framework.throttling import UserRateThrottle 
from .models import Server, ServerMetric 
from .serializers import ServerSerializer, ServerMetricSerializer

class CustomThrottle(UserRateThrottle):
    rate = '100/hour'

class ServerListView(generics.ListCreateAPIView):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    throttle_classes =[CustomThrottle]

class ServerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    throttle_classes = [CustomThrottle]

class ServerMetricsView(generics.ListAPIView):
    serializer_class = ServerMetricSerializer
    throttle_classes = [CustomThrottle]

    def get_queryset(self):
        server_id = self.kwargs['server_id']
        return ServerMetric.objects.filter(server_id= server_id).order_by('-timestamp')[:100]
    
    def list(self,request,*args,**kwargs):
        cache_key = f"server_{self.kwargs['server_id']}_metrics"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)
        
        # If not 
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset,many = True)

        # Cache the response for 1 minute 
        cache.set(cache_key,serializer.data, timeout=60)

        return Response(serializer.data)
    
    