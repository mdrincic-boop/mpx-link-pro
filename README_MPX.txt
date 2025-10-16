MPX over IP - Advanced 192 kHz PCM Audio Link
==============================================

DESCRIPTION:
------------
Professional-grade desktop application for real-time stereo MPX signal transmission
over IP networks. Supports 19 kHz pilot tone, 38 kHz subcarrier, and 57 kHz RDS
transmission with advanced features for broadcasting and professional audio.

INSTALLATION:
-------------
1. Install Python dependencies:
   pip install -r requirements.txt

2. Configure environment variables (optional):
   - Copy .env.example to .env
   - Add Supabase credentials for cloud logging/presets

APPLICATIONS:
-------------

Basic Versions (Simple GUI):
1. MPX Sender (Basic):
   python mpx_sender.py

2. MPX Receiver (Basic):
   python mpx_receiver.py

Professional Versions (Full Features):
1. MPX Sender PRO:
   python mpx_sender_pro.py

2. MPX Receiver PRO:
   python mpx_receiver_pro.py

REQUIREMENTS:
-------------
- Python 3.8+
- PortAudio installed on system
- Audio interface supporting 96/192/384 kHz
- Network connection (LAN or WAN)
- Optional: Supabase account for cloud features

CONFIGURATION:
--------------
Audio Settings:
- Sample Rate: 96000, 192000, or 384000 Hz
- Bit Depth: 16-bit PCM
- Channels: Stereo (2)
- Block Size: 512, 1024, or 2048 frames
- Protocols: TCP (reliable) or UDP (low latency)

FEATURES - BASIC VERSION:
-------------------------
- Real-time stereo audio transmission at 192 kHz
- TCP/UDP protocol selection
- VU meters with dBFS display
- Device selection for input/output
- Adjustable block size for latency tuning
- Safe teardown without exceptions

FEATURES - PRO VERSION:
-----------------------

1. MONITORING & STATISTICS:
   - Real-time latency measurement
   - Packet loss tracking and reporting
   - Quality graphs and trends
   - Buffer status indicator
   - Detailed session statistics
   - Export stats to CSV/JSON

2. AUDIO PROCESSING:
   - AGC (Automatic Gain Control)
   - Audio Limiter/Compressor
   - FFT Spectrum Analyzer
   - 19 kHz Pilot Tone Level Monitor
   - 38 kHz Subcarrier Level Monitor
   - Peak Hold VU Meters
   - Real-time signal analysis

3. SECURITY:
   - AES-256 Encryption
   - Password-based authentication
   - Shared secret verification
   - Forward Error Correction (FEC)
   - Packet integrity checking

4. LOGGING & DIAGNOSTICS:
   - Automatic session logging
   - Audio recording (incoming/outgoing)
   - Event logging with timestamps
   - Alert system for connection issues
   - Export logs to multiple formats

5. MULTI-STREAM SUPPORT:
   - Multiple stream handling
   - Audio mixing and routing
   - Per-stream volume control
   - Failover/backup streams

6. USER INTERFACE:
   - Tabbed interface (Main/Processing/Security/Monitor/Presets)
   - Configuration presets (save/load/delete)
   - Light/Dark theme support
   - Real-time statistics display
   - VU meters with peak hold
   - Buffer status visualization

7. ADVANCED FEATURES:
   - Auto-reconnect on disconnect
   - Configurable reconnect interval
   - Bandwidth limiting options
   - Multi-sample rate support (96/192/384 kHz)
   - Adaptive buffer sizing
   - Jitter compensation

8. CLOUD INTEGRATION:
   - Supabase session logging
   - Cloud-based preset storage
   - Cross-device configuration sync
   - Historical statistics
   - Usage analytics

VU METERS:
----------
- Updates every 100ms
- Shows L/R channel levels in dBFS
- Range: -60 dBFS to 0 dBFS
- Color-coded zones:
  * Green: -60 to -18 dBFS (safe)
  * Yellow: -18 to -6 dBFS (caution)
  * Red: -6 to 0 dBFS (peak)
- Peak hold indicators (PRO version)

PROTOCOLS:
----------
TCP Mode:
- Reliable delivery with automatic retransmission
- Connection-oriented with automatic reconnection
- Best for WAN/internet connections
- Higher latency but guaranteed delivery

UDP Mode:
- Low latency, connectionless
- No retransmission (packet loss possible)
- Best for LAN connections
- Lowest possible latency

SECURITY NOTES:
---------------
- Encryption adds ~5-10ms latency
- Use strong passwords (16+ characters)
- FEC adds ~10% bandwidth overhead
- Authentication tokens expire after 5 seconds

TROUBLESHOOTING:
----------------
1. No audio devices found:
   - Check PortAudio installation
   - Verify audio driver compatibility

2. Connection refused:
   - Check firewall settings
   - Verify host/port configuration
   - Ensure sender is listening before receiver connects

3. High packet loss:
   - Reduce block size
   - Switch from UDP to TCP
   - Enable FEC
   - Check network bandwidth

4. Audio dropouts:
   - Increase buffer size
   - Check CPU usage
   - Verify sample rate support on audio interface

5. Encryption errors:
   - Ensure matching passwords on sender/receiver
   - Check for password typos
   - Verify encryption is enabled on both sides

PERFORMANCE TIPS:
-----------------
- Use TCP for internet, UDP for LAN
- Start with 1024 frame block size
- Enable AGC for varying input levels
- Use limiter to prevent clipping
- Monitor buffer fill (keep 30-70%)
- Close unnecessary applications
- Use wired network for best stability

LOGGING:
--------
Logs are stored in:
- Session logs: logs/*.json
- Audio recordings: recordings/*.raw
- Statistics exports: logs/*.csv

DATABASE SCHEMA:
----------------
Supabase Tables:
- mpx_sessions: Session metadata and configuration
- mpx_statistics: Real-time statistics sampling
- mpx_presets: Saved configuration presets

ADVANCED USAGE:
---------------
1. Multi-site Distribution:
   - Run multiple receivers from one sender
   - Use UDP multicast for efficiency
   - Configure unique ports per receiver

2. Backup/Failover:
   - Configure secondary sender/receiver pair
   - Monitor connection quality
   - Automatic failover on connection loss

3. Professional Broadcasting:
   - Use 192 kHz for full MPX spectrum
   - Enable AGC and limiter
   - Monitor pilot tone and subcarrier levels
   - Enable encryption for secure transmission
   - Log all sessions for audit trail

SUPPORT:
--------
For issues or feature requests, check logs directory for diagnostic information.

VERSION:
--------
MPX over IP v2.0 Pro - October 2025
