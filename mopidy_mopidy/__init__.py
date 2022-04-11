from mopidy import ext, config
import pathlib
from .backend import MopidyMusicBackend

__version__ = '0.1'


class Extension(ext.Extension):
    dist_name = "Mopidy-Mopidy"
    ext_name = "mopidy_mopidy"
    version = __version__

    def get_default_config(self):
        default_config = config.read(pathlib.Path(__file__).parent / "ext.conf")
        return default_config

    def get_config_schema(self):
        schema = super().get_config_schema()
        schema["host"] = config.String()
        return schema

    def validate_config(self, config):
        return True

    def setup(self, registry):
        registry.add("backend", MopidyMusicBackend)
