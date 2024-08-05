

class DictKeysToProperties(object):
    def __init__(self, **entries):
        for key, value in entries.items():
            value2 = (DictKeysToProperties(**value) if isinstance(value, dict) else value)
            self.__dict__[key] = value2

    def __getitem__(self, item):
        return getattr(self, item)
