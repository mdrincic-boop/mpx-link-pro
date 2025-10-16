import { useState, useEffect } from 'react'
import { Radio, Activity, Settings, Monitor, Wifi, WifiOff, Network } from 'lucide-react'
import SystemMonitor from './components/SystemMonitor'
import AudioControls from './components/AudioControls'
import ConnectionPanel from './components/ConnectionPanel'
import NetworkPanel from './components/NetworkPanel'
import SettingsPanel from './components/SettingsPanel'
import StatusBar from './components/StatusBar'
import { StreamStats } from '../shared/types'

type View = 'audio' | 'connection' | 'network' | 'monitor' | 'settings'

export default function App() {
  const [currentView, setCurrentView] = useState<View>('audio')
  const [isConnected, setIsConnected] = useState(false)
  const [streamStats, setStreamStats] = useState<StreamStats>({
    status: 'idle',
    bytesSent: 0,
    bytesReceived: 0,
    packetsLost: 0,
    latency: 0,
    bitrate: 0,
    uptime: 0,
  })

  useEffect(() => {
    if (window.electron) {
      window.electron.onPythonLog((data) => {
        console.log('[Python]', data)
      })

      window.electron.onPythonError((data) => {
        console.error('[Python Error]', data)
      })
    }
  }, [])

  const navigation = [
    { id: 'audio' as View, label: 'Audio', icon: Radio },
    { id: 'connection' as View, label: 'Connection', icon: isConnected ? Wifi : WifiOff },
    { id: 'network' as View, label: 'Network', icon: Network },
    { id: 'monitor' as View, label: 'Monitor', icon: Activity },
    { id: 'settings' as View, label: 'Settings', icon: Settings },
  ]

  return (
    <div className="h-screen flex flex-col bg-slate-900 text-slate-100">
      <header className="bg-slate-800 border-b border-slate-700 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-lg flex items-center justify-center">
              <Monitor className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold">MPX Link PRO</h1>
              <p className="text-xs text-slate-400">Professional Audio Streaming</p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`} />
            <span className="text-sm text-slate-400">
              {isConnected ? 'Connected' : 'Disconnected'}
            </span>
          </div>
        </div>
      </header>

      <div className="flex flex-1 overflow-hidden">
        <nav className="w-20 bg-slate-800 border-r border-slate-700 flex flex-col items-center py-6 gap-4">
          {navigation.map((item) => (
            <button
              key={item.id}
              onClick={() => setCurrentView(item.id)}
              className={`w-12 h-12 rounded-lg flex items-center justify-center transition-all ${
                currentView === item.id
                  ? 'bg-blue-600 text-white'
                  : 'text-slate-400 hover:bg-slate-700 hover:text-slate-200'
              }`}
              title={item.label}
            >
              <item.icon className="w-5 h-5" />
            </button>
          ))}
        </nav>

        <main className="flex-1 overflow-auto p-6">
          {currentView === 'audio' && <AudioControls />}
          {currentView === 'connection' && (
            <ConnectionPanel
              isConnected={isConnected}
              onConnect={() => setIsConnected(true)}
              onDisconnect={() => setIsConnected(false)}
            />
          )}
          {currentView === 'network' && <NetworkPanel />}
          {currentView === 'monitor' && <SystemMonitor stats={streamStats} />}
          {currentView === 'settings' && <SettingsPanel />}
        </main>
      </div>

      <StatusBar stats={streamStats} />
    </div>
  )
}
