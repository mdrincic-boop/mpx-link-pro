import json
import os
from typing import Dict, List, Optional


class ConfigPreset:
    def __init__(self, name: str, config: Dict):
        self.name = name
        self.config = config

    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'config': self.config
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(data['name'], data['config'])


class ConfigManager:
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.presets: Dict[str, ConfigPreset] = {}
        self.current_config: Dict = self._default_config()
        self.load()

    def _default_config(self) -> Dict:
        return {
            'host': '127.0.0.1',
            'port': 5000,
            'protocol': 'TCP',
            'samplerate': 192000,
            'blocksize': 1024,
            'device': '',
            'agc_enabled': False,
            'limiter_enabled': False,
            'encryption_enabled': False,
            'password': '',
            'shared_secret': '',
            'fec_enabled': False,
            'auto_reconnect': True,
            'reconnect_interval': 2,
            'bandwidth_limit': 0,
            'theme': 'light',
            'system_tray': True
        }

    def save_preset(self, name: str, config: Dict = None):
        if config is None:
            config = self.current_config.copy()

        self.presets[name] = ConfigPreset(name, config)
        self.save()

    def load_preset(self, name: str) -> Optional[Dict]:
        if name in self.presets:
            self.current_config = self.presets[name].config.copy()
            return self.current_config
        return None

    def delete_preset(self, name: str):
        if name in self.presets:
            del self.presets[name]
            self.save()

    def get_presets(self) -> List[str]:
        return list(self.presets.keys())

    def save(self):
        data = {
            'current': self.current_config,
            'presets': {name: preset.to_dict() for name, preset in self.presets.items()}
        }

        with open(self.config_file, 'w') as f:
            json.dump(data, f, indent=2)

    def load(self):
        if not os.path.exists(self.config_file):
            return

        try:
            with open(self.config_file, 'r') as f:
                data = json.load(f)

            self.current_config = data.get('current', self._default_config())

            presets_data = data.get('presets', {})
            self.presets = {
                name: ConfigPreset.from_dict(preset_data)
                for name, preset_data in presets_data.items()
            }
        except Exception:
            pass

    def get(self, key: str, default=None):
        return self.current_config.get(key, default)

    def set(self, key: str, value):
        self.current_config[key] = value

    def reset_to_defaults(self):
        self.current_config = self._default_config()
