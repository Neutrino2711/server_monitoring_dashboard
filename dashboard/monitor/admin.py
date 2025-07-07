from django.contrib import admin
from .models import Server, ServerMetric

# Register your models here.
@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip_address','description','is_active','created_at')
    list_filter = ('is_active',)
    search_fields = ('name','ip_address',)

@admin.register(ServerMetric)
class ServerMetricAdmin(admin.ModelAdmin):
    list_display = ('server','cpu_usage','memory_usage','disk_usage','network_in','network_out','timestamp')
    list_filter = ('server',)
    date_hierarchy = 'timestamp'


