import time
import threading
from collections import deque
from typing import Dict, Optional


class StreamMonitor:
    def __init__(self):
        self.packets_sent = 0
        self.packets_received = 0
        self.packets_lost = 0
        self.bytes_sent = 0
        self.bytes_received = 0
        self.latency_samples = deque(maxlen=100)
        self.quality_samples = deque(maxlen=100)
        self.start_time = None
        self.lock = threading.Lock()
        self.last_sequence = -1

    def start(self):
        self.start_time = time.time()

    def record_packet_sent(self, size: int):
        with self.lock:
            self.packets_sent += 1
            self.bytes_sent += size

    def record_packet_received(self, size: int, sequence: Optional[int] = None):
        with self.lock:
            self.packets_received += 1
            self.bytes_received += size

            if sequence is not None and self.last_sequence >= 0:
                expected = self.last_sequence + 1
                if sequence > expected:
                    self.packets_lost += (sequence - expected)

            if sequence is not None:
                self.last_sequence = sequence

    def record_latency(self, latency_ms: float):
        with self.lock:
            self.latency_samples.append(latency_ms)

    def record_quality(self, quality_percent: float):
        with self.lock:
            self.quality_samples.append(quality_percent)

    def get_stats(self) -> Dict:
        with self.lock:
            uptime = time.time() - self.start_time if self.start_time else 0

            avg_latency = sum(self.latency_samples) / len(self.latency_samples) if self.latency_samples else 0
            max_latency = max(self.latency_samples) if self.latency_samples else 0
            min_latency = min(self.latency_samples) if self.latency_samples else 0

            avg_quality = sum(self.quality_samples) / len(self.quality_samples) if self.quality_samples else 100

            total_packets = self.packets_sent if self.packets_sent > 0 else self.packets_received
            packet_loss_rate = (self.packets_lost / total_packets * 100) if total_packets > 0 else 0

            bitrate = (self.bytes_sent * 8 / uptime) if uptime > 0 else 0

            return {
                'uptime': uptime,
                'packets_sent': self.packets_sent,
                'packets_received': self.packets_received,
                'packets_lost': self.packets_lost,
                'packet_loss_rate': packet_loss_rate,
                'bytes_sent': self.bytes_sent,
                'bytes_received': self.bytes_received,
                'bitrate': bitrate,
                'avg_latency': avg_latency,
                'max_latency': max_latency,
                'min_latency': min_latency,
                'avg_quality': avg_quality
            }

    def reset(self):
        with self.lock:
            self.packets_sent = 0
            self.packets_received = 0
            self.packets_lost = 0
            self.bytes_sent = 0
            self.bytes_received = 0
            self.latency_samples.clear()
            self.quality_samples.clear()
            self.start_time = None
            self.last_sequence = -1
