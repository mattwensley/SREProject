import time
from prometheus_client import start_http_server, Gauge
from pythonping import ping
from multiprocessing import Process

def ping_ip(port, ip):
    s = Gauge(f'current_response_time', 'Response time in ms for {ip}')
    failed = Gauge(f'check_request_failed', 'Has a request failed for {ip}')
    start_http_server(port)
    print('Pinging ', ip)
    while True:
        obj = ping(ip, verbose=True, count=1)
        ms = str(obj)
        size = len(ms[6])
        try:
            s.set(ms[6][:size-2])
            print("Response time from [{ip}] (ms):",ms[6][:size-2])
            failed.set(0)
        except Exception as e:
            print("Error from {ip}: ",e)
            failed.set(1)
        # Run every 15 seconds to be in line with scrape interval
        time.sleep(15)

if __name__ == '__main__':
    # Start the pinging processes in parallel
    four = Process(target=ping_ip, args=(8001,"4.4.4.4"))
    eight = Process(target=ping_ip, args=(8002,"8.8.8.8"))
    four.start()
    eight.start()