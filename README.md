# Intervals.icu to influxDB
This script exports some data from [intervals.icu](https://intervals.icu) to [influxDB](https://www.influxdata.com/), so you can create your own dashboards, for example with [Grafana](https://grafana.com/). To retreive the information the official [intervals.icu API](https://intervals.icu/api/v1/docs/swagger-ui/index.html) is used.

The following screenshots are an example with Grafana:

![Grafana Dashboard example](screenshots/image.png)
![Alt text](screenshots/image2.png)
## Exported data
Not all information is exported. This project has been created to extract only data from activities or wellness (sleep, VO2Max, etc.), and not all fields are saved (soreness, injury or systolic, for example, are not exported -for now-). Besides, information about data account (like email, location, preferences, etc.), calendar or workouts are not retreived neither.

Currently the following data is exported:
- **Wellness**: this data contains information like sleep time and quality, act/ctl or VO2Max
- \***Activities**: general information about every activity, like elapsed time, time in zones (hr or pace), distance, average pace/hr, etc.
- \*\****Streams***: streams contains detailed information about activities, like hr/pace for every second.

\* Common data is stored (time, distance, hr...). Specific data for every activity type (like pool distance for Swim, for example) is not stored. (Next steps)

\*\* Like activities, for now I'm working on Run streams. Another activity types streams are not exported (next steps)



## How to use
This script can be used with Docker or directly from code (with Python).

1. Download or clone this repository

2. Create a `.env` file on the root folder with the following values:

```
INFLUXDB_TOKEN=
INFLUXDB_ORG=
INFLUXDB_URL=
INFLUXDB_BUCKET=
INFLUXDB_TIMEOUT=10000
INTERVALS_ATHLETE_ID=
INTERVALS_API_KEY=
```

### Docker

1. Compile the image:

```
docker build --tag intervals-to-influxdb .
```

2. Run a new container with the created image:

```
docker run -it --rm intervals-to-influxdb app.py [start_date] [reset]
```

Examples:
```
# First run
docker run -it --rm intervals-to-influxdb app.py 2023-01-01

# Update data from specific date (august)
docker run -it --rm intervals-to-influxdb app.py 2023-08-01

# Retreive data for today
docker run -it --rm intervals-to-influxdb app.py

# Reset buket (start_date is required)
docker run -it --rm intervals-to-influxdb app.py 2023-01-01 reset
```

If you want to run with a cron job, use the following commad (recommended use without date, to get only the new data):

```
docker run --rm intervals-to-influxdb app.py
```

### Directly with Python
1. Install dependencies:

```
pip install -r requirements.txt
```

2. Run the script
```
python app.py [start_date] [reset]
```

Examples:
```
# First run
python app.py 2023-01-01

# Update data from specific date (august)
python app.py 2023-08-01

# Retreive data for today
python app.py

# Reset buket (start_date is required)
python app.py 2023-01-01 reset
```

### Params
If you set [start_date], all data from this date until today will be retreived. If not, only data for today. If you set [reset], the bucket on influxDB will be removed before start the process (this param must be on the second place, so if you want to get only the current day data and reset de bucket, you must to pass today date).

If no bucket exists when run the script, a new one will be created.