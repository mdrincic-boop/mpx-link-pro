import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sounddevice as sd
import numpy as np
import socket
import threading
import struct
import time
from datetime import datetime
from collections import deque
from audio_utils import get_audio_devices, calculate_db_fs, normalize_db
from monitoring import StreamMonitor
from audio_processing import AudioProcessor, FFTAnalyzer, PeakHolder
from encryption import AudioEncryption, AuthenticationManager, FECEncoder
from logging_manager import SessionLogger, AudioRecorder, AlertSystem
from config_manager import ConfigManager
from supabase_integration import SupabaseManager
from modern_theme import ModernTheme


class MPXReceiverPro:
    def __init__(self, root):
        self.root = root
        self.root.title("MPX Receiver PRO - Advanced 192 kHz Audio Link")
        self.root.geometry("900x950")

        self.theme = ModernTheme('dark')
        self.theme.apply_to_root(self.root)

        self.is_running = False
        self.reconnect_enabled = False
        self.stream = None
        self.socket_obj = None
        self.audio_buffer = deque(maxlen=100)
        self.buffer_lock = threading.Lock()
        self.vu_levels = [0.0, 0.0]
        self.peak_levels = [0.0, 0.0]
        self.vu_lock = threading.Lock()
        self.last_vu_update = time.time()
        self.expected_sequence = 0

        self.monitor = StreamMonitor()
        self.audio_processor = AudioProcessor()
        self.fft_analyzer = FFTAnalyzer()
        self.peak_holder = PeakHolder()
        self.encryption = AudioEncryption()
        self.auth = AuthenticationManager()
        self.fec = FECEncoder()
        self.logger = SessionLogger()
        self.recorder = AudioRecorder()
        self.alerts = AlertSystem()
        self.config = ConfigManager()
        self.supabase = SupabaseManager()

        self.session_id = None
        self.is_mpx_mode = False

        self.setup_gui()
        self.update_vu_meters()
        self.update_stats_display()
        self.load_config()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_gui(self):
        pass

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        main_tab = ttk.Frame(notebook)
        processing_tab = ttk.Frame(notebook)
        security_tab = ttk.Frame(notebook)
        monitor_tab = ttk.Frame(notebook)
        presets_tab = ttk.Frame(notebook)

        notebook.add(main_tab, text='Main')
        notebook.add(processing_tab, text='Processing')
        notebook.add(security_tab, text='Security')
        notebook.add(monitor_tab, text='Monitor')
        notebook.add(presets_tab, text='Presets')

        self.setup_main_tab(main_tab)
        self.setup_processing_tab(processing_tab)
        self.setup_security_tab(security_tab)
        self.setup_monitor_tab(monitor_tab)
        self.setup_presets_tab(presets_tab)

    def setup_main_tab(self, parent):
        parent.configure(style='TFrame')

        main_frame = ttk.Frame(parent, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = ttk.Label(main_frame, text="MPX RECEIVER PRO", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        _, output_devices = get_audio_devices()

        ttk.Label(main_frame, text="Audio Output Device:", font=self.theme.FONTS['body']).grid(row=1, column=0, sticky=tk.W, pady=8)
        self.device_var = tk.StringVar(value=output_devices[0] if output_devices else "")
        device_combo = ttk.Combobox(main_frame, textvariable=self.device_var, values=output_devices, width=50)
        device_combo.grid(row=1, column=1, pady=8, padx=5, sticky=(tk.W, tk.E))

        ttk.Label(main_frame, text="Host:", font=self.theme.FONTS['body']).grid(row=2, column=0, sticky=tk.W, pady=8)
        self.host_var = tk.StringVar(value="127.0.0.1")
        ttk.Entry(main_frame, textvariable=self.host_var, width=52).grid(row=2, column=1, pady=8, padx=5, sticky=(tk.W, tk.E))

        ttk.Label(main_frame, text="Port:", font=self.theme.FONTS['body']).grid(row=3, column=0, sticky=tk.W, pady=8)
        self.port_var = tk.StringVar(value="5000")
        ttk.Entry(main_frame, textvariable=self.port_var, width=52).grid(row=3, column=1, pady=8, padx=5, sticky=(tk.W, tk.E))

        ttk.Label(main_frame, text="Protocol:", font=self.theme.FONTS['body']).grid(row=4, column=0, sticky=tk.W, pady=8)
        self.protocol_var = tk.StringVar(value="TCP")
        protocol_frame = ttk.Frame(main_frame)
        protocol_frame.grid(row=4, column=1, sticky=tk.W, pady=8, padx=5)
        ttk.Radiobutton(protocol_frame, text="TCP", variable=self.protocol_var, value="TCP").pack(
            side=tk.LEFT, padx=5
        )
        ttk.Radiobutton(protocol_frame, text="UDP", variable=self.protocol_var, value="UDP").pack(
            side=tk.LEFT, padx=5
        )

        ttk.Label(main_frame, text="Sample Rate:", font=self.theme.FONTS['body']).grid(row=5, column=0, sticky=tk.W, pady=8)
        self.samplerate_var = tk.StringVar(value="192000")
        ttk.Combobox(main_frame, textvariable=self.samplerate_var, values=["96000", "192000", "384000"],
                     width=50).grid(row=5, column=1, pady=8, padx=5, sticky=(tk.W, tk.E))

        ttk.Label(main_frame, text="Block Size:", font=self.theme.FONTS['body']).grid(row=6, column=0, sticky=tk.W, pady=8)
        self.blocksize_var = tk.StringVar(value="1024")
        ttk.Combobox(main_frame, textvariable=self.blocksize_var, values=["512", "1024", "2048"], width=50).grid(
            row=6, column=1, pady=8, padx=5, sticky=(tk.W, tk.E)
        )

        ttk.Label(main_frame, text="Channel Mode:", font=self.theme.FONTS['body']).grid(row=7, column=0, sticky=tk.W, pady=8)
        self.channel_mode_var = tk.StringVar(value="Stereo (L/R)")
        mode_frame = ttk.Frame(main_frame)
        mode_frame.grid(row=7, column=1, sticky=tk.W, pady=8, padx=5)
        ttk.Radiobutton(mode_frame, text="Stereo (L/R)", variable=self.channel_mode_var, value="Stereo (L/R)").pack(
            side=tk.LEFT, padx=5
        )
        ttk.Radiobutton(mode_frame, text="MPX Composite", variable=self.channel_mode_var, value="MPX Composite").pack(
            side=tk.LEFT, padx=5
        )

        self.auto_reconnect_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="Auto-reconnect on disconnect", variable=self.auto_reconnect_var).grid(
            row=8, column=0, columnspan=2, pady=5
        )

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=9, column=0, columnspan=2, pady=25)

        self.start_button = ttk.Button(button_frame, text="▶ START RECEIVE", command=self.start_receiver,
                                       width=20, style='Success.TButton')
        self.start_button.pack(side=tk.LEFT, padx=8)

        self.stop_button = ttk.Button(button_frame, text="⬛ STOP", command=self.stop_receiver, width=15,
                                       state=tk.DISABLED, style='Danger.TButton')
        self.stop_button.pack(side=tk.LEFT, padx=8)

        ttk.Button(button_frame, text="⬤ RECORD", command=self.toggle_recording, width=15).pack(side=tk.LEFT, padx=8)

        vu_frame = ttk.LabelFrame(main_frame, text="VU METERS WITH PEAK HOLD", padding="15")
        vu_frame.grid(row=10, column=0, columnspan=2, pady=20, sticky=(tk.W, tk.E))

        ttk.Label(vu_frame, text="L", font=self.theme.FONTS['subheading']).grid(row=0, column=0, sticky=tk.W, padx=(0,10))
        self.vu_left_canvas = tk.Canvas(vu_frame, width=500, height=40, bg=self.theme.colors['vu_bg'],
                                        highlightthickness=1, highlightbackground=self.theme.colors['border'])
        self.vu_left_canvas.grid(row=0, column=1, padx=10, pady=8)
        self.vu_left_label = ttk.Label(vu_frame, text="-60.0 dB", width=12, font=self.theme.FONTS['mono'])
        self.vu_left_label.grid(row=0, column=2, padx=(10,0))

        ttk.Label(vu_frame, text="R", font=self.theme.FONTS['subheading']).grid(row=1, column=0, sticky=tk.W, padx=(0,10))
        self.vu_right_canvas = tk.Canvas(vu_frame, width=500, height=40, bg=self.theme.colors['vu_bg'],
                                         highlightthickness=1, highlightbackground=self.theme.colors['border'])
        self.vu_right_canvas.grid(row=1, column=1, padx=10, pady=8)
        self.vu_right_label = ttk.Label(vu_frame, text="-60.0 dB", width=12, font=self.theme.FONTS['mono'])
        self.vu_right_label.grid(row=1, column=2, padx=(10,0))

        buffer_frame = ttk.LabelFrame(main_frame, text="BUFFER STATUS", padding="15")
        buffer_frame.grid(row=11, column=0, columnspan=2, pady=15, sticky=(tk.W, tk.E))

        self.buffer_canvas = tk.Canvas(buffer_frame, width=500, height=40, bg=self.theme.colors['vu_bg'],
                                       highlightthickness=1, highlightbackground=self.theme.colors['border'])
        self.buffer_canvas.pack(pady=8)

        self.buffer_label = ttk.Label(buffer_frame, text="Buffer: 0%", font=self.theme.FONTS['mono'])
        self.buffer_label.pack(pady=5)

        self.status_label = ttk.Label(main_frame, text="Status: Idle", style='Muted.TLabel',
                                      font=self.theme.FONTS['body'])
        self.status_label.grid(row=12, column=0, columnspan=2, pady=15)

    def setup_processing_tab(self, parent):
        parent.configure(style='TFrame')
        frame = ttk.Frame(parent, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="AUDIO PROCESSING", style='Heading.TLabel').pack(pady=(0,20))

        self.agc_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(frame, text="Enable AGC (Automatic Gain Control)", variable=self.agc_var,
                        command=self.toggle_agc).pack(anchor=tk.W, pady=5)

        self.limiter_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(frame, text="Enable Limiter", variable=self.limiter_var,
                        command=self.toggle_limiter).pack(anchor=tk.W, pady=5)

        ttk.Separator(frame, orient='horizontal').pack(fill=tk.X, pady=20)

        ttk.Label(frame, text="MPX SIGNAL ANALYSIS", style='Heading.TLabel').pack(pady=(0,15))

        self.pilot_label = ttk.Label(frame, text="19 kHz Pilot: -- dB", font=self.theme.FONTS['mono'])
        self.pilot_label.pack(pady=8)

        self.subcarrier_label = ttk.Label(frame, text="38 kHz Subcarrier: -- dB", font=self.theme.FONTS['mono'])
        self.subcarrier_label.pack(pady=8)

    def setup_security_tab(self, parent):
        parent.configure(style='TFrame')
        frame = ttk.Frame(parent, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="SECURITY SETTINGS", style='Heading.TLabel').pack(pady=(0,20))

        self.encrypt_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(frame, text="Enable AES Encryption", variable=self.encrypt_var).pack(anchor=tk.W, pady=5)

        ttk.Label(frame, text="Encryption Password:").pack(anchor=tk.W, pady=5)
        self.password_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.password_var, show="*", width=40).pack(anchor=tk.W, padx=20, pady=5)

        ttk.Separator(frame, orient='horizontal').pack(fill=tk.X, pady=10)

        self.auth_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(frame, text="Enable Authentication", variable=self.auth_var).pack(anchor=tk.W, pady=5)

        ttk.Label(frame, text="Shared Secret:").pack(anchor=tk.W, pady=5)
        self.secret_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.secret_var, show="*", width=40).pack(anchor=tk.W, padx=20, pady=5)

        ttk.Separator(frame, orient='horizontal').pack(fill=tk.X, pady=10)

        self.fec_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(frame, text="Enable Forward Error Correction (FEC)", variable=self.fec_var).pack(
            anchor=tk.W, pady=5
        )

    def setup_monitor_tab(self, parent):
        parent.configure(style='TFrame')
        frame = ttk.Frame(parent, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="STREAM MONITOR", style='Heading.TLabel').pack(pady=(0,20))

        stats_frame = ttk.LabelFrame(frame, text="STATISTICS", padding="15")
        stats_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.stats_text = tk.Text(stats_frame, height=20, width=70,
                                  bg=self.theme.colors['bg_secondary'],
                                  fg=self.theme.colors['text_primary'],
                                  font=self.theme.FONTS['mono'],
                                  borderwidth=0,
                                  insertbackground=self.theme.colors['text_primary'])
        self.stats_text.pack(fill=tk.BOTH, expand=True)

    def setup_presets_tab(self, parent):
        parent.configure(style='TFrame')
        frame = ttk.Frame(parent, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="CONFIGURATION PRESETS", style='Heading.TLabel').pack(pady=(0,20))

        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Save Current Config", command=self.save_preset).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Load Preset", command=self.load_preset).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Preset", command=self.delete_preset).pack(side=tk.LEFT, padx=5)

        self.presets_listbox = tk.Listbox(frame, height=15, width=60,
                                          bg=self.theme.colors['bg_secondary'],
                                          fg=self.theme.colors['text_primary'],
                                          font=self.theme.FONTS['body'],
                                          selectbackground=self.theme.colors['accent_blue'],
                                          selectforeground='white',
                                          borderwidth=0,
                                          highlightthickness=1,
                                          highlightbackground=self.theme.colors['border'])
        self.presets_listbox.pack(pady=10)

        self.refresh_presets_list()

    def toggle_agc(self):
        self.audio_processor.agc_enabled = self.agc_var.get()

    def toggle_limiter(self):
        self.audio_processor.limiter_enabled = self.limiter_var.get()

    def toggle_recording(self):
        if not self.recorder.is_recording:
            self.recorder.start_recording("incoming")
            messagebox.showinfo("Recording", "Audio recording started")
        else:
            self.recorder.stop_recording()
            messagebox.showinfo("Recording", "Audio recording stopped")

    def save_preset(self):
        name = simpledialog.askstring("Save Preset", "Enter preset name:")
        if name:
            config = {
                'host': self.host_var.get(),
                'port': int(self.port_var.get()),
                'protocol': self.protocol_var.get(),
                'samplerate': int(self.samplerate_var.get()),
                'blocksize': int(self.blocksize_var.get()),
                'device': self.device_var.get(),
                'channel_mode': self.channel_mode_var.get()
            }
            self.config.save_preset(name, config)
            self.supabase.save_preset(name, config, 'receiver')
            self.refresh_presets_list()
            messagebox.showinfo("Success", f"Preset '{name}' saved!")

    def load_preset(self):
        selection = self.presets_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a preset to load")
            return

        preset_name = self.presets_listbox.get(selection[0])
        config = self.config.load_preset(preset_name)

        if config:
            self.host_var.set(config.get('host', '127.0.0.1'))
            self.port_var.set(str(config.get('port', 5000)))
            self.protocol_var.set(config.get('protocol', 'TCP'))
            self.samplerate_var.set(str(config.get('samplerate', 192000)))
            self.blocksize_var.set(str(config.get('blocksize', 1024)))
            self.device_var.set(config.get('device', ''))
            messagebox.showinfo("Success", f"Preset '{preset_name}' loaded!")

    def delete_preset(self):
        selection = self.presets_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a preset to delete")
            return

        preset_name = self.presets_listbox.get(selection[0])
        self.config.delete_preset(preset_name)
        self.supabase.delete_preset(preset_name)
        self.refresh_presets_list()
        messagebox.showinfo("Success", f"Preset '{preset_name}' deleted!")

    def refresh_presets_list(self):
        self.presets_listbox.delete(0, tk.END)
        for preset_name in self.config.get_presets():
            self.presets_listbox.insert(tk.END, preset_name)

    def load_config(self):
        self.host_var.set(self.config.get('host', '127.0.0.1'))
        self.port_var.set(str(self.config.get('port', 5000)))

    def start_receiver(self):
        try:
            device_str = self.device_var.get()
            device_id = int(device_str.split(':')[0])
            host = self.host_var.get()
            port = int(self.port_var.get())
            blocksize = int(self.blocksize_var.get())
            samplerate = int(self.samplerate_var.get())

            if self.encrypt_var.get() and self.password_var.get():
                self.encryption.set_password(self.password_var.get())

            if self.auth_var.get() and self.secret_var.get():
                self.auth = AuthenticationManager(self.secret_var.get())

            if self.fec_var.get():
                self.fec = FECEncoder(redundancy=2)

            self.is_running = True
            self.reconnect_enabled = self.auto_reconnect_var.get()
            self.expected_sequence = 0
            self.monitor.start()

            self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.logger.start_session('receiver', {
                'host': host,
                'port': port,
                'protocol': self.protocol_var.get(),
                'samplerate': samplerate,
                'blocksize': blocksize
            })

            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)

            self.audio_processor = AudioProcessor(samplerate)
            self.audio_processor.agc_enabled = self.agc_var.get()
            self.audio_processor.limiter_enabled = self.limiter_var.get()

            self.is_mpx_mode = (self.channel_mode_var.get() == "MPX Composite")
            channels = 1 if self.is_mpx_mode else 2

            self.stream = sd.OutputStream(
                device=device_id,
                channels=channels,
                samplerate=samplerate,
                blocksize=blocksize,
                dtype=np.int16,
                callback=self.audio_output_callback
            )
            self.stream.start()

            protocol = self.protocol_var.get()

            if protocol == "TCP":
                threading.Thread(target=self.tcp_receiver_thread, args=(host, port), daemon=True).start()
            else:
                threading.Thread(target=self.udp_receiver_thread, args=(host, port), daemon=True).start()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to start receiver: {str(e)}")
            self.stop_receiver()

    def tcp_receiver_thread(self, host, port):
        while self.is_running and self.reconnect_enabled:
            try:
                self.update_status(f"Connecting to {host}:{port}...")
                self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket_obj.settimeout(5.0)
                self.socket_obj.connect((host, port))
                self.socket_obj.settimeout(None)
                self.update_status(f"Connected to {host}:{port}")
                self.logger.log_event('connection', {'remote': f"{host}:{port}"})

                while self.is_running:
                    seq_data = self.recv_exact(4)
                    if not seq_data:
                        break

                    sequence = struct.unpack('!I', seq_data)[0]

                    length_data = self.recv_exact(4)
                    if not length_data:
                        break

                    length = struct.unpack('!I', length_data)[0]
                    audio_data = self.recv_exact(length)
                    if not audio_data:
                        break

                    if self.encrypt_var.get():
                        audio_data = self.encryption.decrypt(audio_data)

                    if self.fec_var.get():
                        audio_data, valid = self.fec.decode(audio_data)
                        if not valid:
                            continue

                    audio_array = np.frombuffer(audio_data, dtype=np.int16).reshape(-1, 2)

                    with self.buffer_lock:
                        self.audio_buffer.append(audio_array)

                    self.monitor.record_packet_received(len(audio_data), sequence)
                    self.update_vu_from_audio(audio_array)
                    self.fft_analyzer.add_samples(audio_array)

                    if self.recorder.is_recording:
                        self.recorder.write_audio(audio_data)

            except Exception as e:
                if self.is_running:
                    self.update_status(f"Connection lost: {str(e)}")
                    self.alerts.raise_alert('warning', 'Connection lost', {'error': str(e)})

            finally:
                if self.socket_obj:
                    try:
                        self.socket_obj.close()
                    except Exception:
                        pass
                    self.socket_obj = None

                if self.is_running and self.reconnect_enabled:
                    self.update_status("Reconnecting in 2 seconds...")
                    time.sleep(2)

    def udp_receiver_thread(self, host, port):
        try:
            self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket_obj.bind((host, port))
            self.socket_obj.settimeout(1.0)
            self.update_status(f"Listening on {host}:{port} (UDP)")

            while self.is_running:
                try:
                    data, addr = self.socket_obj.recvfrom(65536)

                    seq_data = data[:4]
                    audio_data = data[4:]

                    sequence = struct.unpack('!I', seq_data)[0]

                    if self.encrypt_var.get():
                        audio_data = self.encryption.decrypt(audio_data)

                    if self.fec_var.get():
                        audio_data, valid = self.fec.decode(audio_data)
                        if not valid:
                            continue

                    audio_array = np.frombuffer(audio_data, dtype=np.int16).reshape(-1, 2)

                    with self.buffer_lock:
                        self.audio_buffer.append(audio_array)

                    self.monitor.record_packet_received(len(audio_data), sequence)
                    self.update_vu_from_audio(audio_array)
                    self.fft_analyzer.add_samples(audio_array)

                    if self.recorder.is_recording:
                        self.recorder.write_audio(audio_data)

                except socket.timeout:
                    continue
                except Exception:
                    if not self.is_running:
                        break

        except Exception as e:
            if self.is_running:
                self.update_status(f"UDP Error: {str(e)}")
                self.alerts.raise_alert('error', 'UDP connection failed', {'error': str(e)})

    def recv_exact(self, n):
        data = bytearray()
        while len(data) < n:
            if not self.is_running:
                return None
            try:
                packet = self.socket_obj.recv(n - len(data))
                if not packet:
                    return None
                data.extend(packet)
            except Exception:
                return None
        return bytes(data)

    def audio_output_callback(self, outdata, frames, time_info, status):
        if not self.is_running:
            outdata.fill(0)
            return

        with self.buffer_lock:
            if len(self.audio_buffer) > 0:
                audio_chunk = self.audio_buffer.popleft()

                if self.is_mpx_mode:
                    if len(audio_chunk.shape) == 2 and audio_chunk.shape[1] > 1:
                        audio_chunk = audio_chunk[:, 0].reshape(-1, 1)

                if len(audio_chunk) >= frames:
                    processed = self.audio_processor.process(audio_chunk[:frames])
                    outdata[:] = processed
                else:
                    processed = self.audio_processor.process(audio_chunk)
                    outdata[:len(processed)] = processed
                    outdata[len(processed):].fill(0)
            else:
                outdata.fill(0)

    def update_vu_from_audio(self, audio_data):
        current_time = time.time()
        if current_time - self.last_vu_update >= 0.1:
            if self.is_mpx_mode:
                if len(audio_data.shape) == 1 or audio_data.shape[1] == 1:
                    mono_data = audio_data.flatten() if len(audio_data.shape) > 1 else audio_data
                    mono_db = calculate_db_fs(np.array([mono_data.astype(np.float32) / 32768.0]).T)[0]
                    peak_mono = self.peak_holder.update(mono_db, mono_db)[0]
                    with self.vu_lock:
                        self.vu_levels = [mono_db, mono_db]
                        self.peak_levels = [peak_mono, peak_mono]
                else:
                    left_db, right_db = calculate_db_fs(audio_data.astype(np.float32) / 32768.0)
                    peak_left, peak_right = self.peak_holder.update(left_db, right_db)
                    with self.vu_lock:
                        self.vu_levels = [left_db, right_db]
                        self.peak_levels = [peak_left, peak_right]
            else:
                left_db, right_db = calculate_db_fs(audio_data.astype(np.float32) / 32768.0)
                peak_left, peak_right = self.peak_holder.update(left_db, right_db)
                with self.vu_lock:
                    self.vu_levels = [left_db, right_db]
                    self.peak_levels = [peak_left, peak_right]

            self.last_vu_update = current_time

    def update_vu_meters(self):
        if not self.root.winfo_exists():
            return

        with self.vu_lock:
            left_db, right_db = self.vu_levels
            peak_left, peak_right = self.peak_levels

        if self.channel_mode_var.get() == "MPX Composite":
            self.draw_vu_meter_with_peak(self.vu_left_canvas, left_db, peak_left)
            self.draw_vu_meter_with_peak(self.vu_right_canvas, left_db, peak_left)
            self.vu_left_label.config(text=f"{left_db:.1f} dB")
            self.vu_right_label.config(text="MPX")
        else:
            self.draw_vu_meter_with_peak(self.vu_left_canvas, left_db, peak_left)
            self.draw_vu_meter_with_peak(self.vu_right_canvas, right_db, peak_right)
            self.vu_left_label.config(text=f"{left_db:.1f} dB")
            self.vu_right_label.config(text=f"{right_db:.1f} dB")

        with self.buffer_lock:
            buffer_fill = len(self.audio_buffer) / self.audio_buffer.maxlen * 100

        self.draw_buffer_meter(buffer_fill)
        self.buffer_label.config(text=f"Buffer: {buffer_fill:.0f}%")

        pilot_level = self.fft_analyzer.get_pilot_tone_level()
        subcarrier_level = self.fft_analyzer.get_subcarrier_level()

        self.pilot_label.config(text=f"19 kHz Pilot: {pilot_level:.1f} dB")
        self.subcarrier_label.config(text=f"38 kHz Subcarrier: {subcarrier_level:.1f} dB")

        self.root.after(100, self.update_vu_meters)

    def draw_vu_meter_with_peak(self, canvas, db_value, peak_db):
        canvas.delete("all")
        normalized = normalize_db(db_value)
        peak_normalized = normalize_db(peak_db)

        canvas_width = 490
        meter_width = int(normalized * canvas_width)
        peak_pos = int(peak_normalized * canvas_width)

        color = self.theme.get_vu_color(db_value)

        if meter_width > 0:
            canvas.create_rectangle(5, 5, 5 + meter_width, 35, fill=color, outline='', width=0)

            glow_color = color
            for i in range(3):
                offset = i * 2
                canvas.create_rectangle(5, 5 + offset, 5 + meter_width, 35 - offset,
                                       outline=glow_color, width=1)

        if peak_pos > 0:
            canvas.create_line(5 + peak_pos, 5, 5 + peak_pos, 35,
                             fill=self.theme.colors['text_primary'], width=3)

        for i in range(0, canvas_width, int(canvas_width / 10)):
            canvas.create_line(5 + i, 5, 5 + i, 35,
                             fill=self.theme.colors['border'], width=1)

    def draw_buffer_meter(self, fill_percent):
        self.buffer_canvas.delete("all")

        canvas_width = 490
        meter_width = int((fill_percent / 100) * canvas_width)

        if fill_percent > 80:
            color = self.theme.colors['danger']
        elif fill_percent > 50:
            color = self.theme.colors['warning']
        else:
            color = self.theme.colors['success']

        if meter_width > 0:
            self.buffer_canvas.create_rectangle(5, 5, 5 + meter_width, 35, fill=color, outline='', width=0)

            for i in range(3):
                offset = i * 2
                self.buffer_canvas.create_rectangle(5, 5 + offset, 5 + meter_width, 35 - offset,
                                                   outline=color, width=1)

        for i in range(0, canvas_width, int(canvas_width / 10)):
            self.buffer_canvas.create_line(5 + i, 5, 5 + i, 35,
                                          fill=self.theme.colors['border'], width=1)

    def update_stats_display(self):
        if not self.root.winfo_exists():
            return

        if self.is_running:
            stats = self.monitor.get_stats()

            with self.buffer_lock:
                buffer_fill = len(self.audio_buffer) / self.audio_buffer.maxlen * 100

            stats_text = f"""
Uptime: {stats['uptime']:.1f} seconds
Packets Received: {stats['packets_received']}
Packets Lost: {stats['packets_lost']}
Packet Loss Rate: {stats['packet_loss_rate']:.2f}%
Bytes Received: {stats['bytes_received']:,}
Bitrate: {stats['bitrate']/1000000:.2f} Mbps
Avg Latency: {stats['avg_latency']:.2f} ms
Max Latency: {stats['max_latency']:.2f} ms
Min Latency: {stats['min_latency']:.2f} ms
Quality: {stats['avg_quality']:.1f}%
Buffer Fill: {buffer_fill:.1f}%
            """

            self.stats_text.delete('1.0', tk.END)
            self.stats_text.insert('1.0', stats_text)

            if self.supabase.enabled:
                stats['buffer_fill'] = buffer_fill
                self.supabase.log_statistics(self.session_id, stats)

        self.root.after(1000, self.update_stats_display)

    def update_status(self, message):
        if self.root.winfo_exists():
            self.root.after(0, lambda: self.status_label.config(text=f"Status: {message}"))

    def stop_receiver(self):
        self.is_running = False
        self.reconnect_enabled = False

        if self.stream is not None:
            try:
                self.stream.stop()
                self.stream.close()
            except Exception:
                pass
            self.stream = None

        if self.socket_obj is not None:
            try:
                self.socket_obj.close()
            except Exception:
                pass
            self.socket_obj = None

        if self.recorder.is_recording:
            self.recorder.stop_recording()

        with self.buffer_lock:
            self.audio_buffer.clear()

        stats = self.monitor.get_stats()
        self.logger.end_session(stats)

        if self.supabase.enabled and self.session_id:
            self.supabase.log_session({
                'session_id': self.session_id,
                'type': 'receiver',
                'start_time': datetime.now().isoformat(),
                'end_time': datetime.now().isoformat(),
                'config': {
                    'host': self.host_var.get(),
                    'port': int(self.port_var.get()),
                    'protocol': self.protocol_var.get(),
                    'samplerate': int(self.samplerate_var.get()),
                    'blocksize': int(self.blocksize_var.get())
                },
                'final_stats': stats
            })

        self.monitor.reset()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.update_status("Stopped")

    def on_closing(self):
        if self.is_running:
            self.stop_receiver()

        self.config.save()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = MPXReceiverPro(root)
    root.mainloop()


if __name__ == "__main__":
    main()
