from django.db import models

# Create your models here.
class Server(models.Model):
    name = models.CharField(max_length=100)
    ip_address = models.CharField(max_length = 15)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name 
    
class ServerMetric(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    cpu_usage=models.FloatField()
    memory_usage = models.FloatField()
    disk_usage=models.FloatField()
    network_in = models.FloatField()
    network_out = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering =['-timestamp']

    def __str__(self):
            return f"{self.server.name} at {self.timestamp}"
    