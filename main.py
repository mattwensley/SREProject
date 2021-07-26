import time
from prometheus_client import start_http_server, Gauge
from pythonping import ping
from multiprocessing import Process


def ping_ip4():
    s = Gauge('current_response_time', 'Response time in ms for 4.4.4.4')
    failed = Gauge('check_request_failed', 'Has a request failed for 4.4.4.4')
    start_http_server(8001)
    name = "4.4.4.4"
    print("Pinging", name)
    while True:
        obj = ping(name, verbose=True, count=1)
        ms = str(obj)
        try:
            s.set(ms[30:35])
            print("Response time(ms):",ms[30:35])
            failed.set(0)
        except:
            print("No reply from",name)
            failed.set(1)
        time.sleep(3)

def ping_ip8():
    s = Gauge('current_response_time', 'Response time in ms for 8.8.8.8')
    failed = Gauge('check_request_failed', 'Has a request failed for 8.8.8.8')
    start_http_server(8002)
    name = "8.8.8.8"
    print("Pinging", name)
    while True:
        obj = ping(name, verbose=True, count=1)
        ms = str(obj)
        try:
            s.set(ms[30:35])
            print("Response time(ms):",ms[30:35])
            failed.set(0)
        except:
            print("No reply from",name)
            failed.set(1)
        time.sleep(3)



if __name__ == '__main__':
    #start_http_server(8000)
    four = Process(target=ping_ip4)
    eight = Process(target=ping_ip8)
    four.start()
    eight.start()



