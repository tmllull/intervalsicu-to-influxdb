import datetime

from ..my_utils import MyUtils
from .object_validation import ObjectValidation

utils = MyUtils()


class Athlete(dict):
    fields = ["id", "icu_resting_hr", "icu_weight", "sportSettings", "patata"]

    iterable_fields = ["sportSettings"]

    def __init__(self, validate=False, **kwargs):
        if validate:
            try:
                ObjectValidation().validation(set(Athlete.fields), set(kwargs.keys()))
            except Exception as e:
                exit(e)
        dict.__init__(self, **kwargs)

    def extract_data(self, data):
        fields = {}
        activity = Athlete(**data)
        for key, value in activity.items():
            if key not in self.iterable_fields:
                fields[key] = value
        return fields
