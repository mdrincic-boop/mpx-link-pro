/*
  # Add Channel Mode Support to MPX System

  1. Changes
    - Add `channel_mode` column to `mpx_sessions` table
      - Stores either 'Stereo (L/R)' or 'MPX Composite'
      - Default: 'Stereo (L/R)'
    
    - Add `channel_mode` column to `mpx_presets` table
      - Allows saving channel mode in presets
      - Default: 'Stereo (L/R)'
    
    - Add `channel_mode` column to `mpx_statistics` table
      - Tracks which mode was used during session
      - For historical analysis

  2. Purpose
    - Enable MPX Composite signal transmission (1 channel mono)
    - Support traditional Stereo transmission (2 channels L/R)
    - Store configuration in presets and session history
    
  3. Technical Details
    - MPX Composite: Single channel containing full FM multiplex signal
      - 0-15 kHz: L+R (mono sum)
      - 19 kHz: Pilot tone
      - 23-53 kHz: L-R (stereo difference) @ 38 kHz subcarrier
      - 57 kHz: RDS data
    - Stereo (L/R): Traditional two-channel left/right audio
*/

-- Add channel_mode to mpx_sessions
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'mpx_sessions' AND column_name = 'channel_mode'
  ) THEN
    ALTER TABLE mpx_sessions ADD COLUMN channel_mode text DEFAULT 'Stereo (L/R)' NOT NULL;
    ALTER TABLE mpx_sessions ADD CONSTRAINT channel_mode_check 
      CHECK (channel_mode IN ('Stereo (L/R)', 'MPX Composite'));
  END IF;
END $$;

-- Add channel_mode to mpx_presets
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'mpx_presets' AND column_name = 'channel_mode'
  ) THEN
    ALTER TABLE mpx_presets ADD COLUMN channel_mode text DEFAULT 'Stereo (L/R)' NOT NULL;
    ALTER TABLE mpx_presets ADD CONSTRAINT preset_channel_mode_check 
      CHECK (channel_mode IN ('Stereo (L/R)', 'MPX Composite'));
  END IF;
END $$;

-- Add channel_mode to mpx_statistics
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'mpx_statistics' AND column_name = 'channel_mode'
  ) THEN
    ALTER TABLE mpx_statistics ADD COLUMN channel_mode text DEFAULT 'Stereo (L/R)';
  END IF;
END $$;

-- Create index for faster queries by channel_mode
CREATE INDEX IF NOT EXISTS idx_mpx_sessions_channel_mode ON mpx_sessions(channel_mode);
CREATE INDEX IF NOT EXISTS idx_mpx_presets_channel_mode ON mpx_presets(channel_mode);

-- Add comment explaining the feature
COMMENT ON COLUMN mpx_sessions.channel_mode IS 'Audio channel mode: Stereo (L/R) for traditional 2-channel audio, or MPX Composite for single-channel FM multiplex signal including pilot tone, L+R, L-R subcarrier, and RDS data';
COMMENT ON COLUMN mpx_presets.channel_mode IS 'Saved channel mode preference for this preset configuration';
COMMENT ON COLUMN mpx_statistics.channel_mode IS 'Channel mode used during this statistics snapshot';