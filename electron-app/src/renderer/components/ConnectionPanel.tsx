import { useState } from 'react'
import { Wifi, WifiOff, Server } from 'lucide-react'

interface ConnectionPanelProps {
  isConnected: boolean
  onConnect: () => void
  onDisconnect: () => void
}

export default function ConnectionPanel({ isConnected, onConnect, onDisconnect }: ConnectionPanelProps) {
  const [remoteHost, setRemoteHost] = useState('192.168.1.100')
  const [remotePort, setRemotePort] = useState('5000')
  const [localPort, setLocalPort] = useState('5000')

  return (
    <div className="space-y-6">
      <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
        <div className="flex items-center gap-3 mb-6">
          <div className={`p-3 rounded-lg ${isConnected ? 'bg-green-500/10' : 'bg-slate-700'}`}>
            {isConnected ? (
              <Wifi className="w-6 h-6 text-green-500" />
            ) : (
              <WifiOff className="w-6 h-6 text-slate-400" />
            )}
          </div>
          <div>
            <h2 className="text-lg font-semibold">Connection Status</h2>
            <p className="text-sm text-slate-400">
              {isConnected ? 'Active connection established' : 'No active connection'}
            </p>
          </div>
        </div>

        {isConnected && (
          <div className="space-y-3 mb-6">
            <div className="flex justify-between items-center p-3 bg-slate-700/50 rounded-lg">
              <span className="text-sm text-slate-400">Remote Host</span>
              <span className="text-sm font-mono">{remoteHost}</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-slate-700/50 rounded-lg">
              <span className="text-sm text-slate-400">Remote Port</span>
              <span className="text-sm font-mono">{remotePort}</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-slate-700/50 rounded-lg">
              <span className="text-sm text-slate-400">Local Port</span>
              <span className="text-sm font-mono">{localPort}</span>
            </div>
          </div>
        )}
      </div>

      <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
        <div className="flex items-center gap-3 mb-6">
          <Server className="w-6 h-6 text-blue-500" />
          <h2 className="text-lg font-semibold">Connection Settings</h2>
        </div>

        <div className="space-y-4">
          <div>
            <label className="text-sm text-slate-400 mb-2 block">Remote Host</label>
            <input
              type="text"
              value={remoteHost}
              onChange={(e) => setRemoteHost(e.target.value)}
              disabled={isConnected}
              className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 focus:outline-none focus:border-blue-500 disabled:opacity-50 font-mono text-sm"
              placeholder="192.168.1.100"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-sm text-slate-400 mb-2 block">Remote Port</label>
              <input
                type="text"
                value={remotePort}
                onChange={(e) => setRemotePort(e.target.value)}
                disabled={isConnected}
                className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 focus:outline-none focus:border-blue-500 disabled:opacity-50 font-mono text-sm"
                placeholder="5000"
              />
            </div>

            <div>
              <label className="text-sm text-slate-400 mb-2 block">Local Port</label>
              <input
                type="text"
                value={localPort}
                onChange={(e) => setLocalPort(e.target.value)}
                disabled={isConnected}
                className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 focus:outline-none focus:border-blue-500 disabled:opacity-50 font-mono text-sm"
                placeholder="5000"
              />
            </div>
          </div>
        </div>
      </div>

      <button
        onClick={isConnected ? onDisconnect : onConnect}
        className={`w-full py-4 rounded-lg font-semibold flex items-center justify-center gap-2 transition-colors ${
          isConnected
            ? 'bg-red-600 hover:bg-red-700 text-white'
            : 'bg-blue-600 hover:bg-blue-700 text-white'
        }`}
      >
        {isConnected ? (
          <>
            <WifiOff className="w-5 h-5" />
            Disconnect
          </>
        ) : (
          <>
            <Wifi className="w-5 h-5" />
            Connect
          </>
        )}
      </button>
    </div>
  )
}
