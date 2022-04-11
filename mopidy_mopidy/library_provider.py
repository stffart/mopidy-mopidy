from mopidy import backend, models, config
from .classes import ATrack, AArtist, AAlbum, ARef, APlaylist
from .utils import Utils
import logging
import requests
logger = logging.getLogger("mopidy_mopidy")

class MopidyLibraryProvider(backend.LibraryProvider):
    def __init__(self, url):
        self._url = url
        uri = "mopidymopidy:directory:root"
        name = "Mopidy Master"
        artwork = "yastatic.net/doccenter/images/support.yandex.com/en/music/freeze/fzG5B6KxX0dggCpZn4SQBpnF4GA.png"
        self.root_directory = ARef(type=ARef.PLAYLIST, uri=uri, name=name, artwork=artwork)

    def browse(self, uri):
        uri = Utils.uri_to_master(uri)
        if uri == "root":
          uri = None
        payload = {
          "method": "core.library.browse",
          "jsonrpc": "2.0",
          "params": {"uri":uri},
          "id": 0,
        }
        response = requests.post(self._url, json=payload).json()
        refs = []
        for res in response['result']:
          refs.append(ARef.from_ref(res))
        return refs

    def search(self, query, uris = None, exact = False):
        logger.error('search')
        logger.error(query)
        return sresult

    def lookup(self, uri: str):
        uri = Utils.uri_to_master(uri)
        logger.error(uri)
        payload = {
          "method": "core.library.lookup",
          "jsonrpc": "2.0",
          "params": {"uris":[uri]},
          "id": 0,
        }
        response = requests.post(self._url, json=payload).json()
        tracks = []
        for res in response['result']:
          for track in response['result'][res]:
            track['uri'] = res
            tracks.append( ATrack.from_track(track))
        return tracks

    def get_images(self, uris):
        logger.error('get_images')
        logger.error(uris)
        result = dict()

        return result
