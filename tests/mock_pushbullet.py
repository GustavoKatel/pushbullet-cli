from unittest.mock import MagicMock


class MockPushBullet(object):
    def __init__(self):
        self.push_note = MagicMock()

        self.push_link = MagicMock()

        self.push_file = MagicMock()

        self.devices = []

        self.pushes = []

    def upload_file(self, f, path):
        import os
        return {'filename': os.path.basename(path)}

    def new_device(self, nickname):
        device = MockPushBullet()
        device.nickname = nickname
        self.devices.append(device)
        return device

    def new_push(self, **data):
        import datetime
        created = datetime.datetime(2018, 10, 23, 18, 3, 2)
        try:
            data['created'] = created.timestamp()
        except AttributeError:
            data['created'] = created.strftime('%s.%f')

        self.pushes.append(data)
        return data

    def get_pushes(self, limit=None):
        return self.pushes[::-1][:limit]
