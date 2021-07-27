import time
from prometheus_client import start_http_server, Gauge
from pythonping import ping
from multiprocessing import Process


def ping_ip4():
    # Create the metrics that will be picked up by Prometheus - response time in ms,
    # and whether the most recent ping has failed
    s = Gauge('current_response_time', 'Response time in ms for 4.4.4.4')
    failed = Gauge('check_request_failed', 'Has a request failed for 4.4.4.4')

    # Start the webserver for Prometheus to scrape
    start_http_server(8001)
    name = "4.4.4.4"
    print("Pinging", name)

    # Ping indefinitely. Update the response time metric appropriately by trying to extract the response time.
    # If that isn't possible, the ping has failed and that metric needs to be updated
    while True:
        obj = ping(name, verbose=True, count=1)
        ms = str(obj).split()
        size = len(ms[6])
        try:
            s.set(ms[30:34])
            print("Response time(ms):",ms[6][:size-2])
            failed.set(0)
        except:
            print("No reply from",name)
            failed.set(1)

        # Run every 15 seconds to be in line with scrape interval
        time.sleep(15)

def ping_ip8():
    # Create the metrics that will be picked up by Prometheus - response time in ms,
    # and whether the most recent ping has failed
    s = Gauge('current_response_time', 'Response time in ms for 8.8.8.8')
    failed = Gauge('check_request_failed', 'Has a request failed for 8.8.8.8')

    # Start the webserver for Prometheus to scrape
    start_http_server(8002)
    name = "8.8.8.8"
    print("Pinging", name)

    # Ping indefinitely. Update the response time metric appropriately by trying to extract the response time.
    # If that isn't possible, the ping has failed and that metric needs to be updated
    while True:
        obj = ping(name, verbose=True, count=1)
        ms = str(obj).split()
        size = len(ms[6])
        try:
            s.set(ms[30:34])
            print("Response time(ms):",ms[6][:size-2])
            failed.set(0)
        except:
            print("No reply from",name)
            failed.set(1)

        # Run every 15 seconds to be in line with scrape interval
        time.sleep(15)



if __name__ == '__main__':
    # Start the pinging processes in parallel
    four = Process(target=ping_ip4)
    eight = Process(target=ping_ip8)
    four.start()
    eight.start()



