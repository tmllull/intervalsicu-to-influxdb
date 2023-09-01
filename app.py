import argparse
import datetime
import os

from data_extractor import DataExtractor
from dotenv import dotenv_values
from influx_client import InfluxClient
from intervals import Intervals

try:
    # Load env variables
    config = dotenv_values(".env")
    INFLUXDB_TOKEN = config.get("INFLUXDB_TOKEN", os.environ.get("INFLUXDB_TOKEN"))
    INFLUXDB_ORG = config.get("INFLUXDB_ORG", os.environ.get("INFLUXDB_ORG"))
    INFLUXDB_URL = config.get("INFLUXDB_URL", os.environ.get("INFLUXDB_URL"))
    INFLUXDB_BUCKET = config.get("INFLUXDB_BUCKET", os.environ.get("INFLUXDB_BUCKET"))
    INFLUXDB_TIMEOUT = config.get(
        "INFLUXDB_TIMEOUT", os.environ.get("INFLUXDB_TIMEOUT")
    )
    INTERVALS_ATHLETE_ID = config.get(
        "INTERVALS_ATHLETE_ID", os.environ.get("INTERVALS_ATHLETE_ID")
    )
    INTERVALS_API_KEY = config.get(
        "INTERVALS_API_KEY", os.environ.get("INTERVALS_API_KEY")
    )

except Exception as e:
    exit(e)

# Arg parser
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

# Init instances
intervals = Intervals(INTERVALS_ATHLETE_ID, INTERVALS_API_KEY)
influx = InfluxClient(
    INFLUXDB_URL, INFLUXDB_TOKEN, INFLUXDB_ORG, INFLUXDB_BUCKET, reset
)
extractor = DataExtractor(intervals, influx, start_date, end_date)

# Main process
extractor.wellness()
extractor.activities()
if not no_streams:
    extractor.streams()
