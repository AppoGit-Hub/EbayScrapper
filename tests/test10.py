from prometheus_client import start_http_server, Gauge
import random
import time

# Create a metric to track a value
g = Gauge('my_custom_metric', 'Description of my custom metric')

# Start up the server to expose the metrics.
start_http_server(8000)

# Generate some random values for the metric
while True:
    g.set(random.random())
    time.sleep(1)