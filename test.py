import os, time
from influxdb_client_3 import InfluxDBClient3, Point

token = "Z9c01qUww-s96EMMruucTBA1AkA4DlPqgrFN-SCNwQ3M2LMbvd6-Z8aZ---a7_HZy7JExiGQTC8d_gmsuap6wQ=="
org = "BBS"
host = "https://eu-central-1-1.aws.cloud2.influxdata.com"

client = InfluxDBClient3(host=host, token=token, org=org)

database="Temperatur"

data = {
  "point1": {
    "location": "Wert",
    "species": "bees",
    "count": 23,
  }
}

for key in data:
  point = (
    Point("census")
    .tag("location", data[key]["location"])
    .field(data[key]["species"], data[key]["count"])
  )
  client.write(database=database, record=point)
  time.sleep(1) # separate points by 1 second

print("Complete. Return to the InfluxDB UI.")
