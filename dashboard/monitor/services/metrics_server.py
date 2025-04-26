from concurrent import futures 
import grpc 
import time 
from django.core.cache import cache 
from channels.layers import get_channel_layer 
from asgiref.sync import async_to_sync 
from . import metrics_pb2_grpc , metrics_pb2 
from ..models import Server, ServerMetric 

class MetricsService(metrics_pb2_grpc.MetricsServiceServicer):
    def ReportMetrics(self, request, context):
        try: 
            server = Server.objects.get(id=request.server_id)

            #Save metrics to db 
            metric = ServerMetric.objects.create(
                server = server,
                cpu_usage = request.cpu_usage,
                memory_usage = request.memory_usage,
                disk_usage = request.disk_usage,
                network_in = request.network_in ,
                network_out = request.network_out 
            )

            #Prepare data for WebSocket broadcast
            metrics_data = {
                'server_id': str(server.id),
                'server_name': server.name,
                'cpu_usage': request.cpu_usage,
                'memory_usage': request.memory_usage,
                'disk_usage': request.disk_usage,
                'network_in': request.network_in,
                'network_out': request.network_out,
                'timestamp': metric.timestamp.isoformat(),
            }

            #Cache the latest metrics 
            cache.set('latest_metrics',metrics_data,timeout = 300)

            #Broadcast to WebSocket clients 
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send) (
                "metrics",
                {
                    "type": "send.metrics",
                    "metrics": metrics_data 
                }
            )

            return metrics_pb2.MetricResponse(
                succces = True,
                message="Metrics recorded successfully"
            )
        except Server.DoesNotExist:
            return metrics_pb2.MetricsResponse(
                success=False,
                message='Server not found'
            )
        except Exception as e:
            return metrics_pb2.MetricsResponse(
                success=False,
                message=str(e)
            )
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    metrics_pb2_grpc.add_MetricsServiceServicer_to_server(
        MetricsService(),server

    )
    server.add_insecure_port('[::]:50051') 
    server.start()
    try: 
        while True: 
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()