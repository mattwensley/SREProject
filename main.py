import sys, os, time
from prometheus_client import start_http_server, Summary, Gauge
from pythonping import ping
from multiprocessing import Process


s4 = Summary('current_response_time4','Response time in ms for 4.4.4.4')
failed4 = Gauge('check_request_failed4','Has a request failed for 4.4.4.4')
s8 = Summary('current_response_time8','Response time in ms for 8.8.8.8')
failed8 = Gauge('check_request_failed8','Has a request failed for 8.8.8.8')


def ping_ip4():
    start_http_server(8001)
    name = "4.4.4.4"
    print("Pinging", name)
    while True:
        obj = ping(name, verbose=True, count=1)
        ms = str(obj)
        try:
            s4.observe(ms[30:36])
            print("Response time(ms):",ms[30:36])
            failed4.set(0)
        except:
            print("No reply from",name)
            failed4.set(1)
        time.sleep(3)

def ping_ip8():
    start_http_server(8002)
    name = "8.8.8.8"
    print("Pinging", name)
    while True:
        obj = ping(name, verbose=True, count=1)
        ms = str(obj)
        try:
            s8.observe(ms[30:36])
            print("Response time(ms):",ms[30:36])
            failed8.set(0)
        except:
            print("No reply from",name)
            failed8.set(1)
        time.sleep(3)



if __name__ == '__main__':
    start_http_server(8000)
    four = Process(target=ping_ip4)
    eight = Process(target=ping_ip8)
    four.start()
    eight.start()



