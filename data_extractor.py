import datetime

from influx_client import InfluxClient
from intervals import Intervals
from objects.ride import Ride
from objects.run import Run
from objects.swim import Swim
from objects.wellness import Wellness
from objects.yoga import Yoga


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
        for item in wellness_list:
            wellness = Wellness(**item)
            day_data = {}
            day_data["fields"] = []
            day_data["tags"] = []
            fields = {}
            tags = {}
            tags["day"] = wellness["id"]
            day_data["measurement"] = "wellness"
            for key, value in wellness.items():
                if key != "sportInfo":
                    fields[key] = value
                    if key == "ctl":
                        ctl = value
                    if key == "atl":
                        atl = value
            fields["form"] = ctl - atl
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
        for i, item in enumerate(activities_list):
            activity_data = {}
            activity_data["fields"] = []
            activity_data["tags"] = []
            activity_data["measurement"] = "activity"
            tags = {}
            tags["type"] = item["type"]
            tags["id"] = item["id"]
            tags["start_date"] = datetime.datetime.strptime(
                item["start_date_local"], "%Y-%m-%dT%H:%M:%S"
            ).strftime("%Y-%m-%d")
            fields = {}
            if item["type"] == "Run":
                fields = Run().extract_data(item)
            elif item["type"] == "Ride":
                fields = Ride().extract_data(item)
            elif item["type"] == "Swim":
                fields = Swim().extract_data(item)
            elif item["type"] == "Yoga":
                fields = Yoga().extract_data(item)
            else:
                continue
            activity_data["fields"] = fields
            activity_data["tags"] = tags
            activity_data["time"] = int(
                datetime.datetime.strptime(
                    item["start_date_local"], "%Y-%m-%dT%H:%M:%S"
                ).timestamp()
            )
            data.append(activity_data)
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
                if i > 1 and i % 20 == 0:
                    self._influx.write_data(data)
                    data = []
                    print(i, "of", len(activities), "saved")
                elif i == len(activities) - 1:
                    self._influx.write_data(data)
                    print(i + 1, "of", len(activities), "saved")
            except Exception as e:
                print("Error on activity ", activity, ":", e)
