import datetime

from influx_client import InfluxClient
from intervals import Intervals


class DataExtractor:
    def __init__(
        self,
        intervals_client: Intervals,
        influx_client: InfluxClient,
        start_date,
        end_date,
    ):
        self._intervals = intervals_client
        self._influx = influx_client
        self._start_date = start_date
        self._end_date = end_date

    def _convert_pace(self, time):
        try:
            time = float((float(3600 / (float(time) * 3.6))) / 60)
            res = time - int(time)
            res = round(res * 0.6, 2)
            if res == 0.6:
                time = int(time) + 1
                res = 0
            return float(int(time) + res)
        except Exception:
            return time

    def _convert_speed(self, time):
        try:
            return float(float(time) * 3.6)
        except Exception:
            return time

    def _get_activities_for_streams(self):
        """Get minumun information about activities like id, type and start_date.
        This information will be used to retreive streams

        Returns:
            list: list with the id, type and start_date information of the activities
        """
        activities_list = self._intervals.activities(self._start_date, self._end_date)
        activities_ids = []
        for activity in activities_list:
            activities_ids.append(
                {
                    "id": activity["id"],
                    "type": activity["type"],
                    "time": activity["start_date_local"],
                }
            )
        return activities_ids

    def wellness(self):
        wellness_list = self._intervals.wellness(self._start_date, self._end_date)
        data = []
        print("Total wellness data for " + str(len(wellness_list)) + " days...")
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
            fields["sleepTime"] = wellness[
                "sleepSecs"
            ]  # secs_to_hours(wellness["sleepSecs"])
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
        self._influx.write_data(data)

    def activities(self):
        activities_list = self._intervals.activities(self._start_date, self._end_date)
        print(
            "Saving activities and zones for "
            + str(len(activities_list))
            + " activities..."
        )
        data = []
        for i, activity in enumerate(activities_list):
            # print(activity["id"])
            # data = []
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
            fields["max_speed"] = self._convert_speed(activity["max_speed"])
            fields["average_speed"] = self._convert_speed(activity["average_speed"])
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
            fields["pace"] = self._convert_pace(activity["pace"])
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
            data.append(activity_data)
            # self._influx.write_data(data)
            if i > 1 and i % 50 == 0:
                self._influx.write_data(data)
                data = []
                print(i, "of", len(activities_list), "saved")
            elif i == len(activities_list) - 1:
                self._influx.write_data(data)
                print(i + 1, "of", len(activities_list), "saved")

    def streams(self):
        streams = []
        activities = self._get_activities_for_streams()
        print("Saving streams for " + str(len(activities)) + " activities...")
        data = []
        for i, activity in enumerate(activities):
            # data = []
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
                ) = self._intervals.activitiy_streams(activity["id"])
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
                    # data = []
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

                        # self._influx.write_data(data)
                if i > 1 and i % 20 == 0:
                    self._influx.write_data(data)
                    data = []
                    print(i, "of", len(activities), "saved")
                elif i == len(activities) - 1:
                    self._influx.write_data(data)
                    print(i + 1, "of", len(activities), "saved")
            except Exception as e:
                print("Error on activity ", activity, ":", e)
