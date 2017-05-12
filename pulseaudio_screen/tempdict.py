import datetime


class TempDict(dict):
    def __init__(self, expiration):
        super().__init__()
        self.expiration = expiration
        self.expirations = {}

    def __setitem__(self, key, value):
        self.expirations[key] = datetime.datetime.now() + datetime.timedelta(seconds=self.expiration)
        return super(TempDict, self).__setitem__(key, value)

    def __getitem__(self, item):
        value = super(TempDict, self).__getitem__(item)
        if datetime.datetime.now() > self.expirations.get(item):
            del self[item]
            raise KeyError
        return value

    def __delitem__(self, key):
        del self.expirations[key]
        return super(TempDict, self).__delitem__(key)
