import os
from supabase import create_client, Client
from datetime import datetime
from typing import Dict, List, Optional


class SupabaseManager:
    def __init__(self):
        url = os.environ.get("VITE_SUPABASE_URL")
        key = os.environ.get("VITE_SUPABASE_ANON_KEY")

        self.client: Optional[Client] = None
        self.enabled = False

        if url and key:
            try:
                self.client = create_client(url, key)
                self.enabled = True
            except Exception as e:
                print(f"Failed to initialize Supabase: {e}")

    def log_session(self, session_data: Dict) -> bool:
        if not self.enabled:
            return False

        try:
            config = session_data.get('config', {})
            data = {
                'session_type': session_data.get('type', 'sender'),
                'host': config.get('host', '0.0.0.0'),
                'port': config.get('port', 5000),
                'protocol': config.get('protocol', 'TCP'),
                'sample_rate': config.get('samplerate', 192000),
                'block_size': config.get('blocksize', 1024),
                'started_at': session_data.get('start_time'),
                'ended_at': session_data.get('end_time'),
                'status': 'completed' if session_data.get('end_time') else 'active'
            }

            self.client.table('mpx_sessions').insert(data).execute()
            return True
        except Exception as e:
            print(f"Failed to log session: {e}")
            return False

    def get_sessions(self, limit: int = 50) -> List[Dict]:
        if not self.enabled:
            return []

        try:
            response = self.client.table('mpx_sessions').select('*').order('created_at', desc=True).limit(limit).execute()
            return response.data
        except Exception:
            return []

    def save_preset(self, name: str, config: Dict, session_type: str = 'sender') -> bool:
        if not self.enabled:
            return False

        try:
            data = {
                'name': name,
                'session_type': session_type,
                'host': config.get('host', '0.0.0.0'),
                'port': config.get('port', 5000),
                'protocol': config.get('protocol', 'TCP'),
                'sample_rate': config.get('samplerate', 192000),
                'block_size': config.get('blocksize', 1024),
                'device_name': config.get('device', ''),
                'updated_at': datetime.now().isoformat()
            }

            existing = self.client.table('mpx_presets').select('id').eq('name', name).execute()

            if existing.data:
                self.client.table('mpx_presets').update(data).eq('id', existing.data[0]['id']).execute()
            else:
                self.client.table('mpx_presets').insert(data).execute()

            return True
        except Exception as e:
            print(f"Failed to save preset: {e}")
            return False

    def get_presets(self, session_type: str = None) -> List[Dict]:
        if not self.enabled:
            return []

        try:
            query = self.client.table('mpx_presets').select('*')
            if session_type:
                query = query.eq('session_type', session_type)
            response = query.execute()
            return response.data
        except Exception:
            return []

    def delete_preset(self, preset_name: str) -> bool:
        if not self.enabled:
            return False

        try:
            self.client.table('mpx_presets').delete().eq('name', preset_name).execute()
            return True
        except Exception:
            return False

    def log_statistics(self, session_id: str, stats: Dict) -> bool:
        if not self.enabled:
            return False

        try:
            data = {
                'session_id': session_id,
                'latency_ms': stats.get('avg_latency', 0),
                'packet_loss_percent': stats.get('packet_loss_rate', 0),
                'buffer_fill_percent': stats.get('buffer_fill', 0),
                'left_channel_db': stats.get('left_db', -60),
                'right_channel_db': stats.get('right_db', -60),
                'bytes_transferred': stats.get('bytes_sent', 0) + stats.get('bytes_received', 0),
                'jitter_ms': stats.get('jitter', 0),
                'timestamp': datetime.now().isoformat()
            }

            self.client.table('mpx_statistics').insert(data).execute()
            return True
        except Exception:
            return False

    def get_statistics(self, days: int = 7) -> Dict:
        if not self.enabled:
            return {}

        try:
            from datetime import timedelta

            cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()

            sessions = self.client.table('mpx_sessions').select('*').gte('created_at', cutoff_date).execute()

            total_sessions = len(sessions.data)
            total_uptime = sum(
                s.get('duration_seconds', 0) for s in sessions.data
            )

            return {
                'total_sessions': total_sessions,
                'total_uptime_hours': total_uptime / 3600,
                'avg_session_duration': (total_uptime / total_sessions / 60) if total_sessions > 0 else 0
            }
        except Exception:
            return {}
