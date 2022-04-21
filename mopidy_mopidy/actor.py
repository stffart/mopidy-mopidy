
import pykka

from mopidy import exceptions, listener, zeroconf
from mopidy.core import CoreListener
from mopidy_mpd import network, session, uri_mapper
import requests
import logging
import asyncio
from tornado import websocket, ioloop
import json
import signal


logger = logging.getLogger(__name__)

class MasterFrontend(pykka.ThreadingActor, CoreListener):
    def __init__(self, config, core):
        super(MasterFrontend, self).__init__()
        self.core = core
        mst_config = config['mopidy_mopidy']
        self._name = mst_config['name']
        self._ip = mst_config["ip"]
        self._frontend = mst_config["frontend"]
        self._master_url = "http://{}:6680/master/".format(mst_config['master'])
        self._master_ws = "ws://{}:6680/master/socketapi/ws".format(mst_config['master'])
        self._is_active = False
        self._ws_opened = False
        self.loop = asyncio.get_event_loop()
        self.loop.add_signal_handler(signal.SIGTERM, self.stop)
        self.loop.run_until_complete(self.client_connect())

    def stop(self):
       logger.error("stop")
       if self._ws_opened:
         self._ws_opened = False
         self.ws.close()
       else:
         self._ws_opened = False
       for task in asyncio.all_tasks():
          task.cancel()

    @asyncio.coroutine
    def client_connect(self):
        self._registered = False
        try:
          self.ws = yield from websocket.websocket_connect(self._master_ws)
          self.register()
          logger.error("connected to master")
        except:
          logger.error("cannot connect to master")
          yield from asyncio.sleep(10)
          yield from self.client_connect()
        else:
          yield from self.run()

    @asyncio.coroutine
    def run(self):
      self._ws_opened = True
      self.ws.write_message("list")
      while self._ws_opened:
          msg = yield from self.ws.read_message()
          if msg is None:
             if self._ws_opened:
               self._ws_opened = False
               logger.error('connection closed')
               yield from self.client_connect()
          else:
            data = json.loads(msg)
            logger.error(data)
            if data['msg'] == 'devices':
              for device in data['devices']:
                 if data['devices'][device]['name'] == self._name:
                    self.change_active(data['devices'][device]['active'])

    def change_active(self, active):
      if self._is_active != active:
        self._is_active = active
        if not active:
          #replicate tracks from master
          logger.error("replicate")

    def set_active(self):
        payload = {
          "name": self._name,
        }
        logger.error(f"{self._master_url}masterapi/active")
        response = requests.post(f"{self._master_url}masterapi/active", json=payload).json()
        logger.error(response)

    def on_event(self, event, **kwargs):
         if event == 'track_playback_started':
           self.set_active()
         logger.error(event)

    def register(self):
        payload = {
          "name": self._name,
          "url": f"http://{self._ip}:6680/{self._frontend}",
          "ws": f"ws://{self._ip}:6680/mopidy/ws",
        }
        logger.error(f"{self._master_url}masterapi/register")
        response = requests.post(f"{self._master_url}masterapi/register", json=payload).json()
        logger.error(response)
        self._registered = True
