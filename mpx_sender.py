import tkinter as tk
from tkinter import ttk, messagebox
import sounddevice as sd
import numpy as np
import socket
import threading
import struct
import time
from audio_utils import get_audio_devices, calculate_db_fs, normalize_db


class MPXSender:
    def __init__(self, root):
        self.root = root
        self.root.title("MPX Sender - 192 kHz PCM Audio Link")
        self.root.geometry("500x550")
        self.root.resizable(False, False)

        self.is_running = False
        self.stream = None
        self.socket_obj = None
        self.client_socket = None
        self.vu_levels = [0.0, 0.0]
        self.vu_lock = threading.Lock()
        self.last_vu_update = time.time()

        self.setup_gui()
        self.update_vu_meters()

    def setup_gui(self):
        style = ttk.Style()
        style.theme_use('clam')

        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(main_frame, text="MPX SENDER", font=('Arial', 16, 'bold')).grid(
            row=0, column=0, columnspan=2, pady=10
        )

        input_devices, _ = get_audio_devices()

        ttk.Label(main_frame, text="Audio Input Device:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.device_var = tk.StringVar(value=input_devices[0] if input_devices else "")
        device_combo = ttk.Combobox(main_frame, textvariable=self.device_var, values=input_devices, width=40)
        device_combo.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(main_frame, text="Host:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.host_var = tk.StringVar(value="0.0.0.0")
        ttk.Entry(main_frame, textvariable=self.host_var, width=42).grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(main_frame, text="Port:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.port_var = tk.StringVar(value="5000")
        ttk.Entry(main_frame, textvariable=self.port_var, width=42).grid(row=3, column=1, pady=5, padx=5)

        ttk.Label(main_frame, text="Protocol:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.protocol_var = tk.StringVar(value="TCP")
        protocol_frame = ttk.Frame(main_frame)
        protocol_frame.grid(row=4, column=1, sticky=tk.W, pady=5, padx=5)
        ttk.Radiobutton(protocol_frame, text="TCP", variable=self.protocol_var, value="TCP").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(protocol_frame, text="UDP", variable=self.protocol_var, value="UDP").pack(side=tk.LEFT, padx=5)

        ttk.Label(main_frame, text="Sample Rate:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.samplerate_var = tk.StringVar(value="192000")
        ttk.Entry(main_frame, textvariable=self.samplerate_var, width=42, state='readonly').grid(row=5, column=1, pady=5, padx=5)

        ttk.Label(main_frame, text="Block Size (frames):").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.blocksize_var = tk.StringVar(value="1024")
        ttk.Combobox(main_frame, textvariable=self.blocksize_var, values=["512", "1024", "2048"], width=40).grid(row=6, column=1, pady=5, padx=5)

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=20)

        self.start_button = ttk.Button(button_frame, text="START", command=self.start_sender, width=15)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = ttk.Button(button_frame, text="STOP", command=self.stop_sender, width=15, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        vu_frame = ttk.LabelFrame(main_frame, text="VU Meters (dBFS)", padding="10")
        vu_frame.grid(row=8, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))

        ttk.Label(vu_frame, text="L:").grid(row=0, column=0, sticky=tk.W)
        self.vu_left_canvas = tk.Canvas(vu_frame, width=300, height=25, bg='#2b2b2b', highlightthickness=0)
        self.vu_left_canvas.grid(row=0, column=1, padx=5, pady=5)
        self.vu_left_label = ttk.Label(vu_frame, text="-60.0 dB", width=10)
        self.vu_left_label.grid(row=0, column=2, padx=5)

        ttk.Label(vu_frame, text="R:").grid(row=1, column=0, sticky=tk.W)
        self.vu_right_canvas = tk.Canvas(vu_frame, width=300, height=25, bg='#2b2b2b', highlightthickness=0)
        self.vu_right_canvas.grid(row=1, column=1, padx=5, pady=5)
        self.vu_right_label = ttk.Label(vu_frame, text="-60.0 dB", width=10)
        self.vu_right_label.grid(row=1, column=2, padx=5)

        self.status_label = ttk.Label(main_frame, text="Status: Idle", foreground="gray")
        self.status_label.grid(row=9, column=0, columnspan=2, pady=10)

    def start_sender(self):
        try:
            device_str = self.device_var.get()
            device_id = int(device_str.split(':')[0])
            port = int(self.port_var.get())
            blocksize = int(self.blocksize_var.get())
            samplerate = int(self.samplerate_var.get())

            self.is_running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)

            protocol = self.protocol_var.get()

            if protocol == "TCP":
                threading.Thread(target=self.tcp_sender_thread, args=(port, device_id, blocksize, samplerate), daemon=True).start()
            else:
                host = self.host_var.get()
                threading.Thread(target=self.udp_sender_thread, args=(host, port, device_id, blocksize, samplerate), daemon=True).start()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to start sender: {str(e)}")
            self.stop_sender()

    def tcp_sender_thread(self, port, device_id, blocksize, samplerate):
        try:
            self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_obj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket_obj.bind(('0.0.0.0', port))
            self.socket_obj.listen(1)
            self.socket_obj.settimeout(1.0)

            self.update_status("Waiting for connection...")

            while self.is_running:
                try:
                    self.client_socket, addr = self.socket_obj.accept()
                    self.update_status(f"Connected: {addr[0]}:{addr[1]}")
                    self.start_audio_stream(device_id, blocksize, samplerate, self.tcp_audio_callback)
                    break
                except socket.timeout:
                    continue
                except Exception as e:
                    if self.is_running:
                        self.update_status(f"Connection error: {str(e)}")
                    break

        except Exception as e:
            if self.is_running:
                self.update_status(f"TCP Error: {str(e)}")
                messagebox.showerror("TCP Error", str(e))

    def udp_sender_thread(self, host, port, device_id, blocksize, samplerate):
        try:
            self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket_obj.connect((host, port))
            self.update_status(f"Sending to {host}:{port} (UDP)")
            self.start_audio_stream(device_id, blocksize, samplerate, self.udp_audio_callback)

        except Exception as e:
            if self.is_running:
                self.update_status(f"UDP Error: {str(e)}")
                messagebox.showerror("UDP Error", str(e))

    def start_audio_stream(self, device_id, blocksize, samplerate, callback):
        try:
            self.stream = sd.InputStream(
                device=device_id,
                channels=2,
                samplerate=samplerate,
                blocksize=blocksize,
                dtype=np.int16,
                callback=callback
            )
            self.stream.start()
        except Exception as e:
            if self.is_running:
                self.update_status(f"Audio Error: {str(e)}")
                messagebox.showerror("Audio Error", str(e))

    def tcp_audio_callback(self, indata, frames, time_info, status):
        if not self.is_running or self.client_socket is None:
            return

        try:
            audio_bytes = indata.tobytes()
            length_header = struct.pack('!I', len(audio_bytes))
            self.client_socket.sendall(length_header + audio_bytes)
            self.update_vu_from_audio(indata)
        except Exception:
            pass

    def udp_audio_callback(self, indata, frames, time_info, status):
        if not self.is_running or self.socket_obj is None:
            return

        try:
            audio_bytes = indata.tobytes()
            self.socket_obj.send(audio_bytes)
            self.update_vu_from_audio(indata)
        except Exception:
            pass

    def update_vu_from_audio(self, audio_data):
        current_time = time.time()
        if current_time - self.last_vu_update >= 0.1:
            left_db, right_db = calculate_db_fs(audio_data.astype(np.float32) / 32768.0)
            with self.vu_lock:
                self.vu_levels = [left_db, right_db]
            self.last_vu_update = current_time

    def update_vu_meters(self):
        if not self.root.winfo_exists():
            return

        with self.vu_lock:
            left_db, right_db = self.vu_levels

        self.draw_vu_meter(self.vu_left_canvas, left_db)
        self.draw_vu_meter(self.vu_right_canvas, right_db)

        self.vu_left_label.config(text=f"{left_db:.1f} dB")
        self.vu_right_label.config(text=f"{right_db:.1f} dB")

        self.root.after(100, self.update_vu_meters)

    def draw_vu_meter(self, canvas, db_value):
        canvas.delete("all")
        normalized = normalize_db(db_value)
        width = int(normalized * 290)

        if db_value > -6:
            color = '#ff0000'
        elif db_value > -18:
            color = '#ffaa00'
        else:
            color = '#00ff00'

        if width > 0:
            canvas.create_rectangle(5, 5, 5 + width, 20, fill=color, outline='')

        canvas.create_rectangle(5, 5, 295, 20, outline='#555555', width=1)

    def update_status(self, message):
        if self.root.winfo_exists():
            self.root.after(0, lambda: self.status_label.config(text=f"Status: {message}"))

    def stop_sender(self):
        self.is_running = False

        if self.stream is not None:
            try:
                self.stream.stop()
                self.stream.close()
            except Exception:
                pass
            self.stream = None

        if self.client_socket is not None:
            try:
                self.client_socket.close()
            except Exception:
                pass
            self.client_socket = None

        if self.socket_obj is not None:
            try:
                self.socket_obj.close()
            except Exception:
                pass
            self.socket_obj = None

        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.update_status("Stopped")


def main():
    root = tk.Tk()
    app = MPXSender(root)
    root.mainloop()


if __name__ == "__main__":
    main()
