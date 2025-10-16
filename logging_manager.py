import json
import csv
import os
from datetime import datetime
from typing import Dict, List
import threading


class SessionLogger:
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        self.current_session = None
        self.session_events = []
        self.lock = threading.Lock()

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

    def start_session(self, session_type: str, config: Dict):
        with self.lock:
            self.current_session = {
                'session_id': datetime.now().strftime("%Y%m%d_%H%M%S"),
                'type': session_type,
                'start_time': datetime.now().isoformat(),
                'config': config,
                'events': []
            }
            self.session_events = []

    def log_event(self, event_type: str, data: Dict):
        if not self.current_session:
            return

        with self.lock:
            event = {
                'timestamp': datetime.now().isoformat(),
                'type': event_type,
                'data': data
            }
            self.session_events.append(event)

    def end_session(self, stats: Dict = None):
        if not self.current_session:
            return

        with self.lock:
            self.current_session['end_time'] = datetime.now().isoformat()
            self.current_session['events'] = self.session_events
            if stats:
                self.current_session['final_stats'] = stats

            self._save_session()
            self.current_session = None
            self.session_events = []

    def _save_session(self):
        if not self.current_session:
            return

        session_id = self.current_session['session_id']
        json_path = os.path.join(self.log_dir, f"{session_id}.json")

        with open(json_path, 'w') as f:
            json.dump(self.current_session, f, indent=2)

    def export_to_csv(self, session_id: str = None):
        if session_id:
            json_path = os.path.join(self.log_dir, f"{session_id}.json")
        else:
            json_path = os.path.join(self.log_dir, f"{self.current_session['session_id']}.json")

        if not os.path.exists(json_path):
            return None

        with open(json_path, 'r') as f:
            session_data = json.load(f)

        csv_path = json_path.replace('.json', '.csv')
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Timestamp', 'Event Type', 'Data'])

            for event in session_data.get('events', []):
                writer.writerow([
                    event['timestamp'],
                    event['type'],
                    json.dumps(event['data'])
                ])

        return csv_path

    def get_sessions(self) -> List[Dict]:
        sessions = []
        for filename in os.listdir(self.log_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.log_dir, filename)
                with open(filepath, 'r') as f:
                    sessions.append(json.load(f))

        return sorted(sessions, key=lambda x: x['start_time'], reverse=True)


class AudioRecorder:
    def __init__(self, record_dir: str = "recordings"):
        self.record_dir = record_dir
        self.is_recording = False
        self.current_file = None
        self.lock = threading.Lock()

        if not os.path.exists(record_dir):
            os.makedirs(record_dir)

    def start_recording(self, direction: str = "incoming"):
        with self.lock:
            if self.is_recording:
                return

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{direction}_{timestamp}.raw"
            self.current_file = open(os.path.join(self.record_dir, filename), 'wb')
            self.is_recording = True

    def write_audio(self, audio_data: bytes):
        with self.lock:
            if self.is_recording and self.current_file:
                self.current_file.write(audio_data)

    def stop_recording(self):
        with self.lock:
            if self.is_recording and self.current_file:
                self.current_file.close()
                self.current_file = None
                self.is_recording = False


class AlertSystem:
    def __init__(self):
        self.alerts = []
        self.callbacks = []
        self.lock = threading.Lock()

    def register_callback(self, callback):
        with self.lock:
            self.callbacks.append(callback)

    def raise_alert(self, severity: str, message: str, details: Dict = None):
        with self.lock:
            alert = {
                'timestamp': datetime.now().isoformat(),
                'severity': severity,
                'message': message,
                'details': details or {}
            }
            self.alerts.append(alert)

            for callback in self.callbacks:
                try:
                    callback(alert)
                except Exception:
                    pass

    def get_alerts(self, severity: str = None) -> List[Dict]:
        with self.lock:
            if severity:
                return [a for a in self.alerts if a['severity'] == severity]
            return list(self.alerts)

    def clear_alerts(self):
        with self.lock:
            self.alerts.clear()
