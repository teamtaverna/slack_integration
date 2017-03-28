def fake_creds():
    return {
        'FAKE_CHANNEL': 'C12942JF92'
    }


class FakeClient:
    def __init__(self):
        self.rtm_messages = []

    def rtm_send_message(self, channel, message, attachments=None):
        self.rtm_messages.append((channel, message))


class FakeMessage:
    def __init__(self, client, msg):
        self._client = client
        self._msg = msg

    def reply(self, message):
        # Perhaps a bit unnecessary to do it this way, but it's close to how
        # dispatcher and message actually works
        self._client.rtm_send_message(self._msg['channel'], message)
