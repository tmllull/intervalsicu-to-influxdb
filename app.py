import datetime
import os
import sys

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


influx = InfluxClient(
    INFLUXDB_URL, INFLUXDB_TOKEN, INFLUXDB_ORG, INFLUXDB_BUCKET, reset
)
intervals = Intervals(INTERVALS_ATHLETE_ID, INTERVALS_API_KEY)

if start_date == "":
    start_date = datetime.datetime.now().date()
end_date = datetime.datetime.now().date()


def convert_pace(time):
    try:
        time = float((float(3600 / (float(time) * 3.6))) / 60)
        res = time - int(time)
        res = round(res * 0.6, 2)
        if res == 0.6:
            time = int(time) + 1
            res = 0
        return float(int(time) + res)
    except:
        return time


def convert_speed(time):
    try:
        return float(float(time) * 3.6)
    except:
        return time


#### ATHLETE
# ride, run, swim, other = intervals.athlete(INTERVALS_ATHLETE_ID)
# print(ride)
# exit()

#### WELLNESS
wellness_list = intervals.wellness(start_date, end_date)
data = []
print("Total wellness data:", len(wellness_list))
# exit()
for wellness in wellness_list:
    day_data = {}
    day_data["fields"] = []
    day_data["tags"] = []
    fields = {}
    tags = {}
    tags["day"] = wellness["id"]
    day_data["measurement"] = "wellness"
    fields["id"] = wellness["id"]
    fields["ctl"] = wellness["ctl"]
    fields["atl"] = wellness["atl"]
    fields["form"] = int(wellness["ctl"] - wellness["atl"])
    fields["rampRate"] = wellness["rampRate"]
    fields["ctlLoad"] = wellness["ctlLoad"]
    fields["atlLoad"] = wellness["atlLoad"]
    fields["restingHR"] = wellness["restingHR"]
    fields["sleepTime"] = wellness["sleepSecs"]  # secs_to_hours(wellness["sleepSecs"])
    fields["sleepScore"] = wellness["sleepScore"]
    fields["sleepQuality"] = wellness["sleepQuality"]
    fields["vo2max"] = wellness["vo2max"]
    day_data["fields"] = fields
    day_data["tags"] = tags
    day_data["time"] = int(
        datetime.datetime.strptime(wellness["id"], "%Y-%m-%d").timestamp()
    )
    data.append(day_data)

print("Saving wellness...")
influx.write_data(data)


### ACTIVITIES
activities_list = intervals.activities(start_date, end_date)
activities_ids = []
print("Total activities:", len(activities_list))
print("Saving activities and zones...")
for i, activity in enumerate(activities_list):
    # print(activity["id"])
    data = []
    activities_ids.append(
        {
            "id": activity["id"],
            "type": activity["type"],
            "time": activity["start_date_local"],
        }
    )
    activity_data = {}
    activity_data["fields"] = []
    activity_data["tags"] = []
    activity_data["measurement"] = "activity"
    tags = {}
    tags["type"] = activity["type"]
    tags["id"] = activity["id"]
    tags["start_date"] = datetime.datetime.strptime(
        activity["start_date_local"], "%Y-%m-%dT%H:%M:%S"
    ).strftime("%Y-%m-%d")
    fields = {}
    fields["id"] = activity["id"]
    fields["icu_pm_cp"] = activity["icu_pm_cp"]
    fields["icu_pm_w_prime"] = activity["icu_pm_w_prime"]
    fields["icu_pm_p_max"] = activity["icu_pm_p_max"]
    fields["icu_pm_ftp"] = activity["icu_pm_ftp"]
    fields["icu_pm_ftp_secs"] = activity["icu_pm_ftp_secs"]
    fields["icu_pm_ftp_watts"] = activity["icu_pm_ftp_watts"]
    fields["icu_rolling_ftp"] = activity["icu_rolling_ftp"]
    fields["icu_training_load"] = activity["icu_training_load"]
    fields["icu_atl"] = activity["icu_atl"]
    fields["icu_ctl"] = activity["icu_ctl"]
    fields["name"] = activity["name"]
    fields["start_date"] = datetime.datetime.strptime(
        activity["start_date_local"], "%Y-%m-%dT%H:%M:%S"
    ).strftime("%Y-%m-%d")
    fields["start_time"] = datetime.datetime.strptime(
        activity["start_date_local"], "%Y-%m-%dT%H:%M:%S"
    ).strftime("%H:%M")
    fields["distance"] = activity["distance"]
    # convert_to_km(activity["distance"])
    fields["moving_time"] = activity[
        "moving_time"
    ]  # mins_to_hours(activity["moving_time"])
    fields["elapsed_time"] = activity[
        "elapsed_time"
    ]  # mins_to_hours(activity["elapsed_time"])
    fields["total_elevation_gain"] = activity["total_elevation_gain"]
    fields["max_speed"] = convert_speed(activity["max_speed"])
    fields["average_speed"] = convert_speed(activity["average_speed"])
    fields["max_heartrate"] = activity["max_heartrate"]
    fields["average_heartrate"] = activity["average_heartrate"]
    fields["average_cadence"] = activity["average_cadence"]
    fields["calories"] = activity["calories"]
    fields["average_temp"] = activity["average_temp"]
    fields["gap"] = activity["gap"]
    fields["icu_ftp"] = activity["icu_ftp"]
    fields["threshold_pace"] = activity["threshold_pace"]
    fields["lthr"] = activity["lthr"]
    fields["icu_resting_hr"] = activity["icu_resting_hr"]
    fields["icu_weight"] = activity["icu_weight"]
    fields["icu_sweet_spot_min"] = activity["icu_sweet_spot_min"]
    fields["icu_sweet_spot_max"] = activity["icu_sweet_spot_max"]
    fields["trimp"] = activity["trimp"]
    fields["hr_load"] = activity["hr_load"]
    fields["pace_load"] = activity["pace_load"]
    fields["pace"] = convert_pace(activity["pace"])
    fields["icu_intensity"] = activity["icu_intensity"]
    fields["icu_efficiency_factor"] = activity["icu_efficiency_factor"]
    fields["icu_power_hr"] = activity["icu_power_hr"]
    fields["average_stride"] = activity["average_stride"]
    zones = {
        "icu_hr_zone": activity["icu_hr_zones"],
        "pace_zone": activity["pace_zones"],
        "icu_power_zone": activity["icu_power_zones"],
        "icu_zone_time": activity["icu_zone_times"],
        "icu_hr_time": activity["icu_hr_zone_times"],
        "pace_zone_time": activity["pace_zone_times"],
    }
    # print(zones)
    for zone in zones:
        try:
            if zones[zone] is not None:
                if zone != "icu_zone_time":
                    for j, value in enumerate(zones[zone]):
                        fields[zone + "_" + str(j)] = value
                else:
                    for value in zones[zone]:
                        fields[zone + "_" + value["id"]] = value["secs"]
        except Exception as e:
            print(e)
            continue
    activity_data["fields"] = fields
    activity_data["tags"] = tags
    activity_data["time"] = int(
        datetime.datetime.strptime(
            activity["start_date_local"], "%Y-%m-%dT%H:%M:%S"
        ).timestamp()
    )
    # print(activity_data)
    # exit()
    data.append(activity_data)
    influx.write_data(data)
    if i > 1 and i % 10 == 0:
        print(i, "of", len(activities_list), "saved")

# STREAMS
streams = []
print("Saving streams...")
for i, activity in enumerate(activities_ids):
    try:
        (
            time,
            watts,
            cadence,
            heartrate,
            distance,
            altitude,
            latlng,
            velocity_smooth,
            temp,
            torque,
            respiration,
        ) = intervals.activitiy_streams(activity["id"])
        streams = [
            time,
            watts,
            cadence,
            heartrate,
            distance,
            altitude,
            latlng,
            velocity_smooth,
            temp,
            torque,
            respiration,
        ]
        for stream in streams:
            data = []
            if stream != []:
                for j, item in enumerate(stream["data"]):
                    stream_data = {}
                    fields = {}
                    stream_data["fields"] = []
                    stream_data["tags"] = []
                    stream_data["measurement"] = "stream"
                    tags = {}
                    try:
                        fields["value"] = float(item)
                    except Exception as e:
                        fields["value"] = None
                    tags["activity_type"] = activity["type"]
                    tags["activity_id"] = activity["id"]
                    tags["stream_type"] = stream["type"]
                    stream_data["fields"] = fields
                    stream_data["tags"] = tags
                    stream_data["time"] = int(
                        datetime.datetime.strptime(
                            activity["time"], "%Y-%m-%dT%H:%M:%S"
                        ).timestamp()
                        + j
                    )
                    data.append(stream_data)

                influx.write_data(data)
        if i > 1 and i % 10 == 0:
            print(i, "of", len(activities_ids), "saved")
    except Exception as e:
        print("Error on activity ", activity, ":", e)
