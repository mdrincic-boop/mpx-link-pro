import numpy as np
from collections import deque


class AudioProcessor:
    def __init__(self, samplerate=192000):
        self.samplerate = samplerate
        self.agc_enabled = False
        self.limiter_enabled = False
        self.target_level = 0.7
        self.attack_time = 0.005
        self.release_time = 0.1
        self.current_gain = 1.0

        self.attack_coef = np.exp(-1.0 / (self.samplerate * self.attack_time))
        self.release_coef = np.exp(-1.0 / (self.samplerate * self.release_time))

    def apply_agc(self, audio_data: np.ndarray) -> np.ndarray:
        if not self.agc_enabled:
            return audio_data

        output = np.copy(audio_data).astype(np.float32)

        for i in range(len(output)):
            input_level = np.abs(output[i]).max()

            if input_level > self.current_gain * self.target_level:
                self.current_gain = self.attack_coef * self.current_gain + (1 - self.attack_coef) * (self.target_level / (input_level + 1e-10))
            else:
                self.current_gain = self.release_coef * self.current_gain + (1 - self.release_coef) * 1.0

            output[i] *= self.current_gain

        return output

    def apply_limiter(self, audio_data: np.ndarray, threshold: float = 0.95) -> np.ndarray:
        if not self.limiter_enabled:
            return audio_data

        output = np.copy(audio_data).astype(np.float32)
        output = np.clip(output, -threshold, threshold)

        return output

    def process(self, audio_data: np.ndarray) -> np.ndarray:
        audio_float = audio_data.astype(np.float32) / 32768.0

        audio_float = self.apply_agc(audio_float)
        audio_float = self.apply_limiter(audio_float)

        return (audio_float * 32768.0).astype(np.int16)


class FFTAnalyzer:
    def __init__(self, samplerate=192000, fft_size=8192):
        self.samplerate = samplerate
        self.fft_size = fft_size
        self.window = np.hanning(fft_size)
        self.buffer = deque(maxlen=fft_size)

    def add_samples(self, audio_data: np.ndarray):
        mono = audio_data[:, 0] if audio_data.ndim > 1 else audio_data
        self.buffer.extend(mono.flatten())

    def get_spectrum(self):
        if len(self.buffer) < self.fft_size:
            return None, None

        data = np.array(list(self.buffer)[-self.fft_size:])
        windowed = data * self.window

        fft_result = np.fft.rfft(windowed)
        magnitude = np.abs(fft_result)
        magnitude_db = 20 * np.log10(magnitude + 1e-10)

        freqs = np.fft.rfftfreq(self.fft_size, 1.0 / self.samplerate)

        return freqs, magnitude_db

    def get_pilot_tone_level(self) -> float:
        freqs, magnitude_db = self.get_spectrum()
        if freqs is None:
            return -60.0

        pilot_freq = 19000
        tolerance = 100

        mask = (freqs >= pilot_freq - tolerance) & (freqs <= pilot_freq + tolerance)
        if np.any(mask):
            return np.max(magnitude_db[mask])

        return -60.0

    def get_subcarrier_level(self) -> float:
        freqs, magnitude_db = self.get_spectrum()
        if freqs is None:
            return -60.0

        subcarrier_freq = 38000
        tolerance = 200

        mask = (freqs >= subcarrier_freq - tolerance) & (freqs <= subcarrier_freq + tolerance)
        if np.any(mask):
            return np.max(magnitude_db[mask])

        return -60.0


class PeakHolder:
    def __init__(self, hold_time=1.0, decay_rate=20.0):
        self.hold_time = hold_time
        self.decay_rate = decay_rate
        self.peak_left = -60.0
        self.peak_right = -60.0
        self.peak_time_left = 0
        self.peak_time_right = 0

    def update(self, left_db: float, right_db: float):
        current_time = time.time()

        if left_db > self.peak_left:
            self.peak_left = left_db
            self.peak_time_left = current_time
        elif current_time - self.peak_time_left > self.hold_time:
            self.peak_left -= self.decay_rate * 0.1
            self.peak_left = max(self.peak_left, left_db)

        if right_db > self.peak_right:
            self.peak_right = right_db
            self.peak_time_right = current_time
        elif current_time - self.peak_time_right > self.hold_time:
            self.peak_right -= self.decay_rate * 0.1
            self.peak_right = max(self.peak_right, right_db)

        return self.peak_left, self.peak_right


import time
