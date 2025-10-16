# MPX Channel Mode Implementation - Complete Documentation

## 📅 Implementation Date
October 15, 2025

## 🎯 Feature Overview
Added **Channel Mode Selection** to MPX Audio Link system enabling:
- **Stereo (L/R)**: Traditional 2-channel left/right audio transmission
- **MPX Composite**: Single-channel FM multiplex signal transmission

## 🔧 Technical Implementation

### 1. GUI Changes

#### Sender (mpx_sender_pro.py)
- Added Channel Mode radio buttons in Main tab (row 7)
- Options: "Stereo (L/R)" | "MPX Composite"
- Default: "Stereo (L/R)"
- Adjusted all subsequent row numbers (+1)

#### Receiver (mpx_receiver_pro.py)
- Added Channel Mode radio buttons in Main tab (row 7)
- Identical layout to sender for consistency
- Adjusted all subsequent row numbers (+1)

### 2. Audio Stream Configuration

#### Channel Count
```python
# Cache mode at startup to avoid GUI thread deadlock
self.is_mpx_mode = (self.channel_mode_var.get() == "MPX Composite")
channels = 1 if self.is_mpx_mode else 2

sd.InputStream(
    device=device_id,
    channels=channels,  # 1 for MPX, 2 for Stereo
    samplerate=samplerate,
    blocksize=blocksize,
    dtype=np.int16,
    callback=callback
)
```

#### Why Cache the Mode?
**Critical Fix**: Audio callback runs in separate thread. Accessing Tkinter variables (`channel_mode_var.get()`) from audio thread causes **deadlock**. Solution: cache boolean flag `self.is_mpx_mode` at startup in main thread, use cached value in audio callback.

### 3. VU Meter Adaptation

#### MPX Mode Behavior
```python
if self.is_mpx_mode:
    # Both VU meters show same MPX signal level
    self.draw_vu_meter_with_peak(self.vu_left_canvas, left_db, peak_left)
    self.draw_vu_meter_with_peak(self.vu_right_canvas, left_db, peak_left)
    self.vu_left_label.config(text=f"{left_db:.1f} dB")
    self.vu_right_label.config(text="MPX")  # Label instead of dB value
else:
    # Standard stereo display
    # Left and right channels independently
```

### 4. Audio Processing

#### MPX Mode Processing
```python
if self.is_mpx_mode:
    # Convert stereo input to mono if needed
    if len(audio_chunk.shape) == 2 and audio_chunk.shape[1] > 1:
        audio_chunk = audio_chunk[:, 0].reshape(-1, 1)
```

#### Signal Flow
**Stereo Mode:**
```
Input Device → 2 channels (L/R) → Network → 2 channels → Output Device
```

**MPX Mode:**
```
MPX Device → 1 channel (composite) → Network → 1 channel → Output Device
                                                             ↓
                                                    FM Exciter/Transmitter
```

### 5. Database Schema Updates

#### Migration: `add_channel_mode_to_mpx_system`

**Tables Modified:**
1. **mpx_sessions**
   - Added: `channel_mode TEXT NOT NULL DEFAULT 'Stereo (L/R)'`
   - Constraint: `CHECK (channel_mode IN ('Stereo (L/R)', 'MPX Composite'))`
   - Index: `idx_mpx_sessions_channel_mode`

2. **mpx_presets**
   - Added: `channel_mode TEXT NOT NULL DEFAULT 'Stereo (L/R)'`
   - Constraint: `preset_channel_mode_check`
   - Index: `idx_mpx_presets_channel_mode`

3. **mpx_statistics**
   - Added: `channel_mode TEXT DEFAULT 'Stereo (L/R)'`
   - For historical analysis

#### Sample Presets Created
```sql
- "MPX Studio Link" (sender, MPX Composite)
- "Stereo Backup Link" (sender, Stereo L/R)
- "MPX to Transmitter" (receiver, MPX Composite)
```

### 6. Preset System Integration

#### Saving Presets
```python
config = {
    'host': self.host_var.get(),
    'port': int(self.port_var.get()),
    'protocol': self.protocol_var.get(),
    'samplerate': int(self.samplerate_var.get()),
    'blocksize': int(self.blocksize_var.get()),
    'device': self.device_var.get(),
    'channel_mode': self.channel_mode_var.get()  # NEW
}
```

## 📡 MPX Composite Signal Specification

### Frequency Components (192 kHz sample rate)
```
0-15 kHz:    L+R (mono sum) - Main audio channel
19 kHz:      Pilot tone (9-10% modulation)
23-53 kHz:   L-R @ 38 kHz subcarrier (DSB-SC)
57 kHz:      RDS/RBDS data (optional)
```

### Sample Rate Selection
- **192 kHz**: Nyquist at 96 kHz - covers all MPX components including RDS
- **Bandwidth**: Full 0-96 kHz spectrum preserved
- **No filtering**: Composite signal transmitted intact

### Why MPX Mode?

#### Traditional Stereo Issues:
❌ Separates L/R channels
❌ Loses pilot tone
❌ Loses RDS data
❌ Requires stereo encoder at receiver

#### MPX Composite Benefits:
✅ Complete FM signal in one channel
✅ Preserves all components
✅ Direct connection to FM exciter
✅ Perfect for STL (Studio-to-Transmitter Link)
✅ Remote broadcast ready

## 🎛️ Use Cases

### 1. Studio-to-Transmitter Link (STL)
```
Radio Studio → MPX Sender → Internet/WAN → MPX Receiver → FM Exciter → Transmitter
            [Channel Mode: MPX Composite]
```

### 2. Remote Broadcasting
```
Remote Location → MPX Sender → Internet → Studio → MPX Receiver → Broadcast Chain
                [MPX Composite @ 192 kHz]
```

### 3. Backup/Redundant Link
```
Main Studio → Primary MPX Link (fiber)
           ↘
            → Backup MPX Link (IP) → Transmitter Site
```

### 4. Traditional Stereo Audio
```
Audio Source → Sender [Stereo L/R] → Receiver → Recording/Processing
```

## 🐛 Bug Fixes Applied

### Issue: Receiver Deadlock on Start
**Symptom:** Clicking START RECEIVE causes complete GUI freeze, requires force quit

**Root Cause:** Audio callback thread accessing Tkinter variable
```python
# BAD - Causes deadlock
def audio_output_callback(self, outdata, frames, time_info, status):
    if self.channel_mode_var.get() == "MPX Composite":  # ❌ GUI access from audio thread
        # process...
```

**Solution:** Cache mode flag in main thread
```python
# GOOD - No GUI access from audio thread
def start_receiver(self):
    self.is_mpx_mode = (self.channel_mode_var.get() == "MPX Composite")  # ✅ Cache in main thread
    # start audio stream...

def audio_output_callback(self, outdata, frames, time_info, status):
    if self.is_mpx_mode:  # ✅ Use cached boolean
        # process...
```

**Files Fixed:**
- `mpx_sender_pro.py` - Added `self.is_mpx_mode` cache
- `mpx_receiver_pro.py` - Added `self.is_mpx_mode` cache

## 📊 Performance Characteristics

### Bandwidth Comparison
| Mode | Channels | Sample Rate | Bandwidth |
|------|----------|-------------|-----------|
| Stereo L/R | 2 | 192 kHz | ~1.5 MB/s |
| MPX Composite | 1 | 192 kHz | ~750 KB/s |

### Benefits of MPX Mode:
- **50% bandwidth reduction** vs stereo
- Preserves all FM signal components
- No additional encoding/decoding needed
- Lower latency (single channel processing)

## 🔒 Security & Reliability

All existing features work with both modes:
- ✅ AES-256 encryption
- ✅ Forward Error Correction (FEC)
- ✅ TCP reliable transport
- ✅ UDP low-latency transport
- ✅ Buffer management
- ✅ Session monitoring
- ✅ Statistics logging to Supabase

## 📝 Configuration Examples

### Example 1: MPX Link
```python
Sender:
- Protocol: TCP
- Sample Rate: 192000 Hz
- Block Size: 1024
- Channel Mode: MPX Composite
- Device: [MPX Generator Output]

Receiver:
- Protocol: TCP
- Sample Rate: 192000 Hz
- Block Size: 1024
- Channel Mode: MPX Composite
- Device: [FM Exciter Input]
```

### Example 2: Stereo Audio
```python
Sender:
- Protocol: UDP
- Sample Rate: 96000 Hz
- Block Size: 512
- Channel Mode: Stereo (L/R)
- Device: [Stereo Audio Interface]

Receiver:
- Protocol: UDP
- Sample Rate: 96000 Hz
- Block Size: 512
- Channel Mode: Stereo (L/R)
- Device: [Studio Monitors]
```

## 🧪 Testing Performed

### Test 1: Mode Switching
✅ Stereo mode: 2 channels, independent L/R meters
✅ MPX mode: 1 channel, synchronized meters, "MPX" label

### Test 2: Deadlock Fix
✅ Receiver starts without freezing
✅ No GUI hangs during audio streaming
✅ Clean shutdown

### Test 3: Preset Save/Load
✅ Channel mode saved to local config
✅ Channel mode synced to Supabase
✅ Loads correctly from cloud presets

### Test 4: Audio Quality
✅ Stereo mode: Full L/R separation
✅ MPX mode: Complete composite signal preserved
✅ No artifacts or distortion

## 🎓 Technical Notes

### Thread Safety
- GUI variables accessed only in main thread
- Audio callback uses cached boolean flags
- VU meter updates use thread-safe locks

### Sample Rate Requirements
MPX mode requires **minimum 192 kHz** to capture:
- 57 kHz RDS: Requires Nyquist of 114 kHz minimum
- Safety margin: 192 kHz provides 96 kHz Nyquist
- Clean frequency response to 80+ kHz

### Future Enhancements
Possible additions:
- [ ] MPX spectrum analyzer (FFT visualization)
- [ ] Automatic pilot tone detection
- [ ] RDS decoder integration
- [ ] Pre-emphasis/de-emphasis controls
- [ ] MPX power meter (total deviation)

## 📚 References

### FM Multiplex Standards
- ITU-R BS.450: Pilot-tone System for FM Stereo
- FCC §73.322: Stereophonic Transmissions
- EBU R68: Alignment Level in Digital Audio Systems

### File Modifications
```
mpx_sender_pro.py:
- Lines 53-54: Added is_mpx_mode cache
- Lines 134-143: Added Channel Mode GUI
- Lines 441-442: Cache mode at startup
- Lines 520-541: Use cached mode in VU updates
- Lines 547-560: Use cached mode in VU display
- Line 318: Added channel_mode to preset save

mpx_receiver_pro.py:
- Lines 56-57: Added is_mpx_mode cache
- Lines 134-143: Added Channel Mode GUI
- Lines 404-405: Cache mode at startup
- Lines 562-564: Use cached mode in audio callback
- Lines 579-600: Use cached mode in VU updates
- Lines 607-616: Use cached mode in VU display
- Line 318: Added channel_mode to preset save
```

## ✅ Implementation Status

**Status:** ✅ COMPLETE AND TESTED
**Build:** ✅ Successful
**Database:** ✅ Migrated
**Runtime:** ✅ Verified working

---

**Implementation by:** MPX Development Team
**Documentation Version:** 1.0
**Last Updated:** 2025-10-15
