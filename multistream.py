import threading
import numpy as np
from typing import Dict, List, Optional
from collections import deque


class AudioStream:
    def __init__(self, stream_id: str, name: str):
        self.stream_id = stream_id
        self.name = name
        self.buffer = deque(maxlen=100)
        self.lock = threading.Lock()
        self.enabled = True
        self.volume = 1.0

    def add_audio(self, audio_data: np.ndarray):
        with self.lock:
            if self.enabled:
                self.buffer.append(audio_data)

    def get_audio(self, frames: int) -> Optional[np.ndarray]:
        with self.lock:
            if len(self.buffer) > 0:
                return self.buffer.popleft()
        return None

    def clear(self):
        with self.lock:
            self.buffer.clear()


class AudioMixer:
    def __init__(self, channels: int = 2):
        self.channels = channels
        self.streams: Dict[str, AudioStream] = {}
        self.lock = threading.Lock()

    def add_stream(self, stream_id: str, name: str) -> AudioStream:
        with self.lock:
            if stream_id not in self.streams:
                self.streams[stream_id] = AudioStream(stream_id, name)
            return self.streams[stream_id]

    def remove_stream(self, stream_id: str):
        with self.lock:
            if stream_id in self.streams:
                del self.streams[stream_id]

    def mix(self, frames: int, dtype=np.int16) -> np.ndarray:
        with self.lock:
            output = np.zeros((frames, self.channels), dtype=np.float32)
            active_streams = 0

            for stream in self.streams.values():
                if not stream.enabled:
                    continue

                audio_data = stream.get_audio(frames)
                if audio_data is not None:
                    audio_float = audio_data.astype(np.float32) * stream.volume

                    if len(audio_float) >= frames:
                        output += audio_float[:frames]
                    else:
                        output[:len(audio_float)] += audio_float

                    active_streams += 1

            if active_streams > 1:
                output = output / active_streams

            output = np.clip(output, -32768, 32767)
            return output.astype(dtype)

    def set_stream_volume(self, stream_id: str, volume: float):
        with self.lock:
            if stream_id in self.streams:
                self.streams[stream_id].volume = max(0.0, min(2.0, volume))

    def set_stream_enabled(self, stream_id: str, enabled: bool):
        with self.lock:
            if stream_id in self.streams:
                self.streams[stream_id].enabled = enabled

    def get_streams(self) -> List[AudioStream]:
        with self.lock:
            return list(self.streams.values())


class AudioRouter:
    def __init__(self):
        self.routes: Dict[str, List[str]] = {}
        self.lock = threading.Lock()

    def add_route(self, source_id: str, destination_id: str):
        with self.lock:
            if source_id not in self.routes:
                self.routes[source_id] = []
            if destination_id not in self.routes[source_id]:
                self.routes[source_id].append(destination_id)

    def remove_route(self, source_id: str, destination_id: str):
        with self.lock:
            if source_id in self.routes:
                if destination_id in self.routes[source_id]:
                    self.routes[source_id].remove(destination_id)
                if not self.routes[source_id]:
                    del self.routes[source_id]

    def get_destinations(self, source_id: str) -> List[str]:
        with self.lock:
            return self.routes.get(source_id, []).copy()

    def clear_routes(self, source_id: str = None):
        with self.lock:
            if source_id:
                if source_id in self.routes:
                    del self.routes[source_id]
            else:
                self.routes.clear()


class MultiStreamManager:
    def __init__(self):
        self.mixer = AudioMixer()
        self.router = AudioRouter()
        self.lock = threading.Lock()

    def create_stream(self, stream_id: str, name: str) -> AudioStream:
        return self.mixer.add_stream(stream_id, name)

    def route_audio(self, audio_data: np.ndarray, source_id: str):
        destinations = self.router.get_destinations(source_id)

        if not destinations:
            stream = self.mixer.streams.get(source_id)
            if stream:
                stream.add_audio(audio_data)
        else:
            for dest_id in destinations:
                stream = self.mixer.streams.get(dest_id)
                if stream:
                    stream.add_audio(audio_data)

    def get_mixed_audio(self, frames: int) -> np.ndarray:
        return self.mixer.mix(frames)
