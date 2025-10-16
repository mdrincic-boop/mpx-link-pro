import numpy as np
import sounddevice as sd
from typing import List, Tuple


def get_audio_devices() -> Tuple[List[str], List[str]]:
    """Get lists of input and output audio devices."""
    devices = sd.query_devices()
    input_devices = []
    output_devices = []

    for idx, device in enumerate(devices):
        if device['max_input_channels'] > 0:
            input_devices.append(f"{idx}: {device['name']}")
        if device['max_output_channels'] > 0:
            output_devices.append(f"{idx}: {device['name']}")

    return input_devices, output_devices


def calculate_db_fs(audio_data: np.ndarray) -> Tuple[float, float]:
    """
    Calculate dBFS (decibels relative to full scale) for stereo audio.
    Returns: (left_channel_db, right_channel_db)
    """
    if audio_data.size == 0:
        return -60.0, -60.0

    if audio_data.ndim == 1:
        audio_data = audio_data.reshape(-1, 1)

    left_channel = audio_data[:, 0] if audio_data.shape[1] > 0 else np.array([0])
    right_channel = audio_data[:, 1] if audio_data.shape[1] > 1 else left_channel

    left_rms = np.sqrt(np.mean(left_channel**2))
    right_rms = np.sqrt(np.mean(right_channel**2))

    left_db = 20 * np.log10(left_rms) if left_rms > 0 else -60.0
    right_db = 20 * np.log10(right_rms) if right_rms > 0 else -60.0

    left_db = max(left_db, -60.0)
    right_db = max(right_db, -60.0)

    return left_db, right_db


def normalize_db(db_value: float, min_db: float = -60.0, max_db: float = 0.0) -> float:
    """Normalize dB value to 0.0-1.0 range for display."""
    if db_value <= min_db:
        return 0.0
    if db_value >= max_db:
        return 1.0
    return (db_value - min_db) / (max_db - min_db)
