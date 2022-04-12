from mopidy import backend, audio
from .utils import Utils
import logging
import requests
logger = logging.getLogger("mopidy")


class MopidyPlaybackProvider(backend.PlaybackProvider):
    def __init__(self, backend, audio, url):
        super().__init__(audio, backend)
        self._url = url

    def translate_uri(self, uri: str):
        logger.error('translate')
        logger.error(uri)
        uri = Utils.uri_to_master(uri)
        return self._url+uri;
#        payload = {
#          "method": "core.playback.translate_uri",
#          "jsonrpc": "2.0",
#          "params": {"uri":uri},
#          "id": 0,
#        }
#        response = requests.post(self._url, json=payload).json()
#        return response['result']
