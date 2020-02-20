import base64
import json
import os

from pyojo.common.decorator import try_exec
from pyojo.utils import object_convert


class ConfigBase:
    _protect_fields = []
    _config_path = None

    def _protect_encode(self, x):
        return object_convert.dump_b64_data(x)[::-1]

    def _protect_decode(self, x):
        return object_convert.load_b64_data(x)[::-1]

    @try_exec()
    def load(self):
        if os.path.exists(self._config_path):
            with open(self._config_path, 'r') as io:
                config = json.load(io)
                for f in self._protect_fields:
                    config[f] = self._protect_decode(config[f])
                object_convert.dict_to_object(config, self, new_fields=False)

    @try_exec()
    def save(self):
        with open(self._config_path, 'w') as io:
            config = object_convert.object_to_dict(self)
            for f in self._protect_fields:
                config[f] = base64.b64encode(config[f].encode()).decode()[::-1]
            json.dump(config, io, indent='  ')

    def clear(self):
        if os.path.exists(self._config_path):
            os.unlink(self._config_path)
