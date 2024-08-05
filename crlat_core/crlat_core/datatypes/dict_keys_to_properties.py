
class DictKeysToProperties(object):
    def __init__(self, **entries):
        for key, value in entries.items():
            value2 = (DictKeysToProperties(**value) if isinstance(value, dict) else value)
            self.__dict__[key] = value2

    def __getitem__(self, item, default=None):
        return getattr(self, item, default)

    def items(self):
        return self.__dict__.items()

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def get(self, item, default=None):
        """ D.get(k[,d]) -> D[k] if k in D, else d.  d defaults to None. """
        return self.__getitem__(item, default)
