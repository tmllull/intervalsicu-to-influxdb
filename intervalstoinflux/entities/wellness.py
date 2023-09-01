class Wellness(dict):
    fields = [
        "id",
        "ctl",
        "atl",
        "rampRate",
        "ctlLoad",
        "atlLoad",
        "sportInfo",
        "updated",
        "weight",
        "restingHR",
        "hrv",
        "hrvSDNN",
        "menstrualPhase",
        "menstrualPhasePredicted",
        "kcalConsumed",
        "sleepSecs",
        "sleepScore",
        "sleepQuality",
        "avgSleepingHR",
        "soreness",
        "fatigue",
        "stress",
        "mood",
        "motivation",
        "injury",
        "spO2",
        "systolic",
        "diastolic",
        "hydration",
        "hydrationVolume",
        "readiness",
        "baevskySI",
        "bloodGlucose",
        "lactate",
        "bodyFat",
        "abdomen",
        "vo2max",
        "comments",
    ]

    def __init__(self, **kwargs):
        dict.__init__(self, **kwargs)

    def sport_info(self, wellness):
        # TODO: to be implemented
        return
