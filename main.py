import sys, os
from prometheus_client import start_http_server, Summary0s
from pythonping import ping
from multiprocessing import Process

Responses = Summary('Responses','Number of total responses')
ips = ["8.8.8.8","4.4.4.4"]

def ping_ip(name):
    print("Pinging", name)
    ping(name, verbose=True)


if __name__ == '__main__':
    start_http_server(8000)
    four = Process(target=ping_ip, args=("4.4.4.4",))
    eight = Process(target=ping_ip, args=("8.8.8.8",))
    four.start()
    eight.start()



