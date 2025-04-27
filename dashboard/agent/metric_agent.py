import grpc 
import psutil 
import time 
import metrics_pb2
import metrics_pb2_grpc
from datetime import datetime

#Config
SERVER_ID = "1"
GRPC_SERVER = "localhost:50051"



def collect_metrics():
    "Gather system metrics using psutil"
    try:
        return metrics_pb2.MetricsRequest(
            server_id = SERVER_ID,
            cpu_usage = psutil.cpu_percent(),
            memory_usage = psutil.virtual_memory().percent,
            disk_usage = psutil.disk_usage('/').percent,
            network_in = psutil.net_io_counters().bytes_recv / 1024,
            network_out=psutil.net_io_counters().bytes_sent / 1024
        )
    except Exception as e: 
        print(f"Error collecting metrics: {str(e)}")
        raise 


    

def run():
    print(f"Starting metric agent for server {SERVER_ID}...")
    while True: 
        try: 
            channel = grpc.insecure_channel(GRPC_SERVER)
            stub = metrics_pb2_grpc.MetricsServiceStub(channel)
            response = stub.ReportMetrics(collect_metrics())
            print(f"[{datetime.now()}] Metrics sent. Response: {response.message}")
        except Exception as e:
            print(f"Error: {str(e)}")
        time.sleep(5)
    
if __name__ == '__main__':
    run()
