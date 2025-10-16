import sys
import json
import sounddevice as sd
import numpy as np
import socket
import threading
import struct
import time
import subprocess
import re
from collections import deque

class AudioBackend:
    def __init__(self):
        self.is_running = False
        self.stream = None
        self.socket_obj = None
        self.client_socket = None
        self.mode = 'sender'
        self.channel_mode = 'stereo'
        self.audio_buffer = deque(maxlen=100)
        self.buffer_lock = threading.Lock()
        self.sequence_number = 0
        self.expected_sequence = 0

        self.config = {
            'sample_rate': 48000,
            'buffer_size': 512,
            'channels': 2,
            'remote_host': '127.0.0.1',
            'remote_port': 5000,
            'local_port': 5000
        }

    def log(self, message):
        print(json.dumps({'type': 'log', 'message': message}), flush=True)

    def error(self, message):
        print(json.dumps({'type': 'error', 'message': message}), file=sys.stderr, flush=True)

    def send_stats(self, stats):
        print(json.dumps({'type': 'stats', 'data': stats}), flush=True)

    def get_audio_devices(self):
        devices = sd.query_devices()
        device_list = []
        for idx, dev in enumerate(devices):
            device_list.append({
                'id': idx,
                'name': dev['name'],
                'channels': dev['max_input_channels'] if self.mode == 'sender' else dev['max_output_channels'],
                'sample_rate': dev['default_samplerate']
            })
        return device_list

    def get_network_info(self):
        try:
            result = subprocess.run(['ip', 'addr', 'show'], capture_output=True, text=True)
            interfaces = []
            current_ip = None
            current_netmask = None

            for line in result.stdout.split('\n'):
                if re.match(r'^\d+:', line):
                    match = re.search(r'^\d+:\s+(\S+):', line)
                    if match:
                        iface = match.group(1)
                        if iface != 'lo':
                            interfaces.append(iface)

                if 'inet ' in line:
                    match = re.search(r'inet\s+(\S+)', line)
                    if match and not current_ip:
                        ip_cidr = match.group(1)
                        parts = ip_cidr.split('/')
                        current_ip = parts[0]
                        if len(parts) > 1:
                            cidr = int(parts[1])
                            current_netmask = self._cidr_to_netmask(cidr)

            gateway_result = subprocess.run(['ip', 'route', 'show', 'default'], capture_output=True, text=True)
            gateway = None
            if gateway_result.stdout:
                match = re.search(r'default via (\S+)', gateway_result.stdout)
                if match:
                    gateway = match.group(1)

            dns_servers = []
            try:
                with open('/etc/resolv.conf', 'r') as f:
                    for line in f:
                        if line.startswith('nameserver'):
                            dns = line.split()[1]
                            dns_servers.append(dns)
            except:
                pass

            return {
                'interfaces': interfaces,
                'current': {
                    'ip': current_ip,
                    'netmask': current_netmask,
                    'gateway': gateway,
                    'dns': ', '.join(dns_servers[:2]) if dns_servers else 'N/A'
                }
            }
        except Exception as e:
            self.error(f'Failed to get network info: {e}')
            return {
                'interfaces': ['eth0', 'wlan0'],
                'current': {
                    'ip': 'N/A',
                    'netmask': 'N/A',
                    'gateway': 'N/A',
                    'dns': 'N/A'
                }
            }

    def _cidr_to_netmask(self, cidr):
        mask = (0xffffffff >> (32 - cidr)) << (32 - cidr)
        return f"{(mask >> 24) & 0xff}.{(mask >> 16) & 0xff}.{(mask >> 8) & 0xff}.{mask & 0xff}"

    def configure_network(self, config):
        try:
            interface = config.get('interface', 'eth0')
            method = config.get('method', 'dhcp')

            connection_name = f'mpx-{interface}'

            subprocess.run(['nmcli', 'connection', 'delete', connection_name],
                         capture_output=True, stderr=subprocess.DEVNULL)

            if method == 'dhcp':
                cmd = [
                    'nmcli', 'connection', 'add',
                    'type', 'ethernet',
                    'con-name', connection_name,
                    'ifname', interface,
                    'ipv4.method', 'auto'
                ]
            else:
                ip_address = config.get('ipAddress', '192.168.1.100')
                netmask = config.get('netmask', '255.255.255.0')
                gateway = config.get('gateway', '192.168.1.1')
                dns1 = config.get('dns1', '8.8.8.8')
                dns2 = config.get('dns2', '8.8.4.4')

                cidr = self._netmask_to_cidr(netmask)
                ip_with_cidr = f"{ip_address}/{cidr}"

                cmd = [
                    'nmcli', 'connection', 'add',
                    'type', 'ethernet',
                    'con-name', connection_name,
                    'ifname', interface,
                    'ipv4.method', 'manual',
                    'ipv4.addresses', ip_with_cidr,
                    'ipv4.gateway', gateway,
                    'ipv4.dns', f"{dns1},{dns2}"
                ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                subprocess.run(['nmcli', 'connection', 'up', connection_name],
                             capture_output=True)
                self.log(f'Network configured successfully: {connection_name}')
                return {'success': True}
            else:
                self.error(f'Failed to configure network: {result.stderr}')
                return {'success': False, 'error': result.stderr}

        except Exception as e:
            self.error(f'Network configuration error: {e}')
            return {'success': False, 'error': str(e)}

    def _netmask_to_cidr(self, netmask):
        return sum([bin(int(x)).count('1') for x in netmask.split('.')])


    def audio_callback_sender(self, indata, frames, time_info, status):
        if status:
            self.log(f'Audio status: {status}')

        try:
            audio_data = indata.copy()

            if self.channel_mode == 'mono':
                audio_data = np.mean(audio_data, axis=1, keepdims=True)
            elif self.channel_mode == 'stereo' and audio_data.shape[1] > 2:
                audio_data = audio_data[:, :2]

            packet_data = struct.pack('!I', self.sequence_number)
            packet_data += audio_data.tobytes()

            if self.client_socket:
                try:
                    self.client_socket.sendall(packet_data)
                    self.sequence_number += 1
                except Exception as e:
                    self.error(f'Send error: {e}')

        except Exception as e:
            self.error(f'Callback error: {e}')

    def audio_callback_receiver(self, outdata, frames, time_info, status):
        if status:
            self.log(f'Audio status: {status}')

        try:
            with self.buffer_lock:
                if len(self.audio_buffer) > 0:
                    audio_data = self.audio_buffer.popleft()
                    outdata[:] = audio_data[:frames]
                else:
                    outdata.fill(0)
        except Exception as e:
            self.error(f'Callback error: {e}')
            outdata.fill(0)

    def receive_thread(self):
        self.log('Receiver thread started')

        try:
            self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_obj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket_obj.bind(('0.0.0.0', self.config['local_port']))
            self.socket_obj.listen(1)

            self.log(f"Listening on port {self.config['local_port']}")

            conn, addr = self.socket_obj.accept()
            self.log(f'Connected from {addr}')

            expected_size = self.config['buffer_size'] * self.config['channels'] * 4 + 4

            while self.is_running:
                try:
                    packet = conn.recv(expected_size)
                    if not packet:
                        break

                    if len(packet) < 4:
                        continue

                    sequence = struct.unpack('!I', packet[:4])[0]
                    audio_bytes = packet[4:]

                    audio_data = np.frombuffer(audio_bytes, dtype=np.float32)
                    audio_data = audio_data.reshape(-1, self.config['channels'])

                    with self.buffer_lock:
                        self.audio_buffer.append(audio_data)

                except Exception as e:
                    self.error(f'Receive error: {e}')
                    break

            conn.close()

        except Exception as e:
            self.error(f'Socket error: {e}')
        finally:
            if self.socket_obj:
                self.socket_obj.close()

    def start_stream(self, config):
        if self.is_running:
            self.log('Already running')
            return

        self.config.update(config)
        self.mode = config.get('mode', 'sender')
        self.channel_mode = config.get('channelMode', 'stereo')

        if self.channel_mode == 'mono':
            self.config['channels'] = 1
        elif self.channel_mode == 'stereo':
            self.config['channels'] = 2
        else:
            self.config['channels'] = 8

        self.is_running = True

        try:
            if self.mode == 'sender':
                self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket_obj.connect((self.config['remote_host'], self.config['remote_port']))
                self.client_socket = self.socket_obj

                self.stream = sd.InputStream(
                    device=config.get('inputDevice'),
                    channels=self.config['channels'],
                    samplerate=self.config['sample_rate'],
                    blocksize=self.config['buffer_size'],
                    callback=self.audio_callback_sender
                )

                self.stream.start()
                self.log('Sender started')

            else:
                receive_thread = threading.Thread(target=self.receive_thread, daemon=True)
                receive_thread.start()

                self.stream = sd.OutputStream(
                    device=config.get('outputDevice'),
                    channels=self.config['channels'],
                    samplerate=self.config['sample_rate'],
                    blocksize=self.config['buffer_size'],
                    callback=self.audio_callback_receiver
                )

                self.stream.start()
                self.log('Receiver started')

        except Exception as e:
            self.error(f'Start error: {e}')
            self.stop_stream()

    def stop_stream(self):
        self.is_running = False

        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

        if self.client_socket:
            self.client_socket.close()
            self.client_socket = None

        if self.socket_obj:
            self.socket_obj.close()
            self.socket_obj = None

        self.log('Stream stopped')

    def process_command(self, cmd):
        command = cmd.get('command')
        args = cmd.get('args', {})

        if command == 'start_stream':
            self.start_stream(args)
        elif command == 'stop_stream':
            self.stop_stream()
        elif command == 'get_devices':
            devices = self.get_audio_devices()
            print(json.dumps({'type': 'devices', 'data': devices}), flush=True)
        elif command == 'get_network_info':
            network_info = self.get_network_info()
            print(json.dumps({'type': 'network_info', 'data': network_info}), flush=True)
        elif command == 'configure_network':
            result = self.configure_network(args)
            print(json.dumps({'type': 'network_config_result', 'data': result}), flush=True)
        else:
            self.error(f'Unknown command: {command}')

def main():
    backend = AudioBackend()
    backend.log('Audio backend initialized')

    try:
        while True:
            line = sys.stdin.readline()
            if not line:
                break

            try:
                cmd = json.loads(line)
                backend.process_command(cmd)
            except json.JSONDecodeError as e:
                backend.error(f'JSON error: {e}')
            except Exception as e:
                backend.error(f'Command error: {e}')

    except KeyboardInterrupt:
        backend.log('Shutting down')
    finally:
        backend.stop_stream()

if __name__ == '__main__':
    main()
