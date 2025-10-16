import { useState, useEffect } from 'react'
import { Mic, Volume2, Play, Square, RefreshCw } from 'lucide-react'

export default function AudioControls() {
  const [mode, setMode] = useState<'sender' | 'receiver'>('sender')
  const [channelMode, setChannelMode] = useState<'mono' | 'stereo' | 'multi'>('stereo')
  const [inputDevice, setInputDevice] = useState('')
  const [outputDevice, setOutputDevice] = useState('')
  const [isStreaming, setIsStreaming] = useState(false)
  const [inputLevel, setInputLevel] = useState(0)
  const [outputLevel, setOutputLevel] = useState(0)

  const startStreaming = async () => {
    if (window.electron) {
      await window.electron.pythonCommand('start_stream', {
        mode,
        channelMode,
        inputDevice,
        outputDevice,
      })
      setIsStreaming(true)
    }
  }

  const stopStreaming = async () => {
    if (window.electron) {
      await window.electron.pythonCommand('stop_stream', {})
      setIsStreaming(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
        <h2 className="text-lg font-semibold mb-4">Operation Mode</h2>
        <div className="grid grid-cols-2 gap-3">
          <button
            onClick={() => setMode('sender')}
            className={`p-4 rounded-lg border-2 transition-all ${
              mode === 'sender'
                ? 'border-blue-500 bg-blue-500/10'
                : 'border-slate-600 hover:border-slate-500'
            }`}
          >
            <Mic className="w-6 h-6 mx-auto mb-2" />
            <div className="text-sm font-medium">Sender</div>
            <div className="text-xs text-slate-400">Transmit Audio</div>
          </button>
          <button
            onClick={() => setMode('receiver')}
            className={`p-4 rounded-lg border-2 transition-all ${
              mode === 'receiver'
                ? 'border-blue-500 bg-blue-500/10'
                : 'border-slate-600 hover:border-slate-500'
            }`}
          >
            <Volume2 className="w-6 h-6 mx-auto mb-2" />
            <div className="text-sm font-medium">Receiver</div>
            <div className="text-xs text-slate-400">Receive Audio</div>
          </button>
        </div>
      </div>

      <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
        <h2 className="text-lg font-semibold mb-4">Channel Mode</h2>
        <div className="grid grid-cols-3 gap-3">
          {(['mono', 'stereo', 'multi'] as const).map((ch) => (
            <button
              key={ch}
              onClick={() => setChannelMode(ch)}
              className={`p-3 rounded-lg border-2 transition-all ${
                channelMode === ch
                  ? 'border-cyan-500 bg-cyan-500/10'
                  : 'border-slate-600 hover:border-slate-500'
              }`}
            >
              <div className="text-sm font-medium capitalize">{ch}</div>
              <div className="text-xs text-slate-400">
                {ch === 'mono' && '1 Channel'}
                {ch === 'stereo' && '2 Channels'}
                {ch === 'multi' && '8+ Channels'}
              </div>
            </button>
          ))}
        </div>
      </div>

      <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold">Audio Devices</h2>
          <button className="p-2 hover:bg-slate-700 rounded-lg transition-colors">
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>

        {mode === 'sender' && (
          <div className="space-y-3">
            <div>
              <label className="text-sm text-slate-400 mb-2 block">Input Device</label>
              <select
                value={inputDevice}
                onChange={(e) => setInputDevice(e.target.value)}
                className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 focus:outline-none focus:border-blue-500"
              >
                <option value="">Select Input Device</option>
                <option value="default">Default Input</option>
              </select>
            </div>

            <div>
              <label className="text-sm text-slate-400 mb-2 block">Input Level</label>
              <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-green-500 to-yellow-500 transition-all duration-100"
                  style={{ width: `${inputLevel}%` }}
                />
              </div>
            </div>
          </div>
        )}

        {mode === 'receiver' && (
          <div className="space-y-3">
            <div>
              <label className="text-sm text-slate-400 mb-2 block">Output Device</label>
              <select
                value={outputDevice}
                onChange={(e) => setOutputDevice(e.target.value)}
                className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 focus:outline-none focus:border-blue-500"
              >
                <option value="">Select Output Device</option>
                <option value="default">Default Output</option>
              </select>
            </div>

            <div>
              <label className="text-sm text-slate-400 mb-2 block">Output Level</label>
              <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-blue-500 to-cyan-500 transition-all duration-100"
                  style={{ width: `${outputLevel}%` }}
                />
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="flex gap-3">
        {!isStreaming ? (
          <button
            onClick={startStreaming}
            className="flex-1 bg-green-600 hover:bg-green-700 text-white py-4 rounded-lg font-semibold flex items-center justify-center gap-2 transition-colors"
          >
            <Play className="w-5 h-5" />
            Start Streaming
          </button>
        ) : (
          <button
            onClick={stopStreaming}
            className="flex-1 bg-red-600 hover:bg-red-700 text-white py-4 rounded-lg font-semibold flex items-center justify-center gap-2 transition-colors"
          >
            <Square className="w-5 h-5" />
            Stop Streaming
          </button>
        )}
      </div>
    </div>
  )
}
