import argparse
import datetime
import os

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
    INFLUXDB_TIMEOUT = config["INFLUXDB_TIMEOUT"]
    INTERVALS_ATHLETE_ID = config["INTERVALS_ATHLETE_ID"]
    INTERVALS_API_KEY = config["INTERVALS_API_KEY"]

except Exception as e:
    print("Error loading .env:", e)
    INFLUXDB_TOKEN = os.environ["INFLUXDB_TOKEN"]
    INFLUXDB_ORG = os.environ["INFLUXDB_ORG"]
    INFLUXDB_URL = os.environ["INFLUXDB_URL"]
    INFLUXDB_BUCKET = os.environ["INFLUXDB_BUCKET"]
    INFLUXDB_TIMEOUT = os.environ["INFLUXDB_TIMEOUT"]
    INTERVALS_ATHLETE_ID = os.environ["INTERVALS_ATHLETE_ID"]
    INTERVALS_API_KEY = os.environ["INTERVALS_API_KEY"]

# Default values
reset = False
no_streams = False

parser = argparse.ArgumentParser()

parser.add_argument(
    "--no-streams",
    action="store_true",
    help="This flag ignores streams when export data",
)
parser.add_argument(
    "--reset", action="store_true", help="Reset influx bucket (delete and create)"
)
parser.add_argument("--start-date", type=str, help="Start date in format YYYY-MM-DD")
parser.add_argument("--end-date", type=str, help="End date in format YYYY-MM-DD")

args = parser.parse_args()

if args.no_streams:
    no_streams = True
else:
    no_streams = False
if args.reset:
    reset = True
else:
    reset = False
if args.start_date:
    start_date = datetime.date.fromisoformat(args.start_date)
else:
    start_date = datetime.datetime.now().date()
if args.end_date:
    end_date = datetime.date.fromisoformat(args.end_date)
else:
    end_date = datetime.datetime.now().date()


intervals = Intervals(INTERVALS_ATHLETE_ID, INTERVALS_API_KEY)
influx = InfluxClient(
    INFLUXDB_URL, INFLUXDB_TOKEN, INFLUXDB_ORG, INFLUXDB_BUCKET, reset
)
extractor = DataExtractor(intervals, influx, start_date, end_date)

extractor.wellness()
extractor.activities()
if not no_streams:
    extractor.streams()
