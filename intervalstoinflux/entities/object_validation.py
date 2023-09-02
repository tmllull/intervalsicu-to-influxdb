class ObjectValidation(dict):
    def validation(self, expected, actual):
        for key in expected:
            if key not in actual:
                raise KeyError(
                    "Validation failed: field '"
                    + str(key)
                    + "' not found on IntervalsObject"
                )
