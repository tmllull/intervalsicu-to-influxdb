# Intervals.icu to influxDB
This script exports some data from [intervals.icu](https://intervals.icu) to [influxDB](https://www.influxdata.com/), so you can create your own dashboards, for example with [Grafana](https://grafana.com/). To retreive the information the official [intervals.icu API](https://intervals.icu/api/v1/docs/swagger-ui/index.html) is used.

The following screenshots are an example with Grafana:

![Grafana Dashboard example](docs/screenshots/image.png)
![Grafana Dashboard example2](docs/screenshots/image2.png)
## Exported data
Not all information is exported. This project has been created to extract (for now) only data from activities or wellness (sleep, VO2Max, etc.). Besides, information about data account (like email, location, preferences, etc.), calendar or workouts are not retreived neither (for now).

Currently the following data is exported:
- **Wellness**: this data contains information like sleep time and quality, act/ctl or VO2Max
- **Activities**: general information about every activity, like elapsed time, time in zones (hr or pace), distance, average pace/hr, etc.
- \***Streams**: streams contains detailed information about activities, like hr/pace for every second.

\* Currently working on it.


## How to use
This script can be used with Docker or directly from code (with Python), but in both cases you need to create a .env file with the following information:

```
INFLUXDB_TOKEN=
INFLUXDB_ORG=
INFLUXDB_URL=
INFLUXDB_BUCKET=
INFLUXDB_TIMEOUT=10000
INTERVALS_ATHLETE_ID=
INTERVALS_API_KEY=
```

NOTE: If no bucket exists when run the script, a new one will be created.

### Docker
There are 2 ways to use it.

### From Dockerhub
If you want to use the last image from Dockerhub, just run

```bash
docker run --env-file PATH/TO/FILE -it --rm tmllull/intervals-to-influxdb app.py
```

### From source
If you want to run with Docker using the sorce code, you need to clone the projects and follow the next steps:
1. Compile the image:

```bash
docker build --tag intervals-to-influxdb .
```

2. Run a new container with the created image:

```bash
docker run --env-file PATH/TO/FILE -it --rm intervals-to-influxdb app.py [-h] [--start-date START_DATE] [--end-date END_DATE] [--streams] [--reset]
```

### Examples
```
# First run
docker run -it --rm tmllull/intervals-to-influxdb app.py --start-date 2023-01-01

# Get data from specific date (august)
docker run -it --rm tmllull/intervals-to-influxdb app.py --start-date 2023-08-01

# Retreive data for today
docker run -it --rm tmllull/intervals-to-influxdb app.py

# Retreive data for today with streams
docker run -it --rm tmllull/intervals-to-influxdb app.py --streams

# Reset buket
docker run -it --rm tmllull/intervals-to-influxdb app.py --start-date 2023-01-01 --reset
```

If you want to run with a cron job, use the following commad (recommended use without date, to get only the today's data):

```
docker run --env-file PATH/TO/FILE --rm tmllull/intervals-to-influxdb app.py
```

### Directly with Python
If you want to run it with python, there are 2 options:

### Using pip
To use the pip package, just install the module:

```bash
pip install intervalsicu-to-influxdb
```

Then, just use the `app.py` file.

### Using source code
If you want to run directly from source code, first clone the project, and then:

1. Install dependencies

```
pip install .
```

2. Run the script `app.py`
```
python app.py [-h] [--start-date START_DATE] [--end-date END_DATE] [--streams] [--reset]
```

Examples:
```
# First run
python app.py --start-date 2023-01-01

# Update data from specific date (august)
python app.py --start-date 2023-01-01

# Retreive data for today
python app.py

# Retreive data with streams
python app.py --streams

# Reset buket
python app.py --start-date 2023-01-01 --reset
```

## Options
The following options are available:

```
-h, --help              show this help message and exit
--start-date START_DATE Start date in format YYYY-MM-DD
--end-date END_DATE     End date in format YYYY-MM-DD
--streams               Export streams for the activities
--reset                 Reset influx bucket (delete and create)
```