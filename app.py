import argparse

from intervalstoinflux.intervals_to_influx import IntervalsToInflux

# Arg parser
parser = argparse.ArgumentParser()

parser.add_argument(
    "--streams",
    action="store_true",
    help="Export streams for the activities",
)
parser.add_argument(
    "--reset", action="store_true", help="Reset influx bucket (delete and create)"
)
parser.add_argument("--start-date", type=str, help="Start date in format YYYY-MM-DD")
parser.add_argument("--end-date", type=str, help="End date in format YYYY-MM-DD")

args = parser.parse_args()

if args.streams:
    streams = True
else:
    streams = False
if args.reset:
    reset = True
else:
    reset = False
if args.start_date:
    start_date = args.start_date
else:
    start_date = None
if args.end_date:
    end_date = args.end_date
else:
    end_date = None


extractor = IntervalsToInflux(start_date, end_date, reset)

# Main process
extractor.wellness()
extractor.activities()
if streams:
    extractor.streams()
