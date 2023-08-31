import datetime
import os
import sys

from data_extractor import DataExtractor
from dotenv import dotenv_values
from influx_client import InfluxClient
from intervals import Intervals

try:
    # Load .env
    config = dotenv_values(".env")
    INFLUXDB_TOKEN = config["INFLUXDB_TOKEN"]
    INFLUXDB_ORG = config["INFLUXDB_ORG"]
    INFLUXDB_URL = config["INFLUXDB_URL"]
    INFLUXDB_BUCKET = config["INFLUXDB_BUCKET"]
    INTERVALS_ATHLETE_ID = config["INTERVALS_ATHLETE_ID"]
    INTERVALS_API_KEY = config["INTERVALS_API_KEY"]


except Exception as e:
    print("Error loading .env:", e)
    INFLUXDB_TOKEN = os.environ["INFLUXDB_TOKEN"]
    INFLUXDB_ORG = os.environ["INFLUXDB_ORG"]
    INFLUXDB_URL = os.environ["INFLUXDB_URL"]
    INFLUXDB_BUCKET = os.environ["INFLUXDB_BUCKET"]
    INTERVALS_ATHLETE_ID = os.environ["INTERVALS_ATHLETE_ID"]
    INTERVALS_API_KEY = os.environ["INTERVALS_API_KEY"]

start_date = ""
reset = False

if len(sys.argv) == 2:
    try:
        start_date = datetime.date.fromisoformat(sys.argv[1])
    except Exception as e:
        exit(e)
if len(sys.argv) == 3:
    try:
        start_date = datetime.date.fromisoformat(sys.argv[1])
        reset = True
    except Exception as e:
        exit(e)
if len(sys.argv) > 3:
    exit("Too many params. Only 0 or 1 are allowed")

if start_date == "":
    start_date = datetime.datetime.now().date()
end_date = datetime.datetime.now().date()

intervals = Intervals(INTERVALS_ATHLETE_ID, INTERVALS_API_KEY)
influx = InfluxClient(
    INFLUXDB_URL, INFLUXDB_TOKEN, INFLUXDB_ORG, INFLUXDB_BUCKET, reset
)
extractor = DataExtractor(intervals, influx, start_date, end_date)


# def convert_pace(time):
#     try:
#         time = float((float(3600 / (float(time) * 3.6))) / 60)
#         res = time - int(time)
#         res = round(res * 0.6, 2)
#         if res == 0.6:
#             time = int(time) + 1
#             res = 0
#         return float(int(time) + res)
#     except:
#         return time


# def convert_speed(time):
#     try:
#         return float(float(time) * 3.6)
#     except:
#         return time


#### ATHLETE
# ride, run, swim, other = intervals.athlete(INTERVALS_ATHLETE_ID)
# print(ride)
# exit()

#### WELLNESS
extractor.wellness()
extractor.activities()
extractor.streams()
