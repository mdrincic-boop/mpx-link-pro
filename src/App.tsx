import { useState } from 'react';
import { Activity, Radio, Shield, Settings, Save, Play, Square, Wifi, WifiOff } from 'lucide-react';

function App() {
  const [activeTab, setActiveTab] = useState('main');
  const [isConnected, setIsConnected] = useState(false);
  const [isStreaming, setIsStreaming] = useState(false);

  const tabs = [
    { id: 'main', label: 'Main', icon: Radio },
    { id: 'processing', label: 'Audio Processing', icon: Activity },
    { id: 'security', label: 'Security', icon: Shield },
    { id: 'monitor', label: 'Monitor', icon: Activity },
    { id: 'presets', label: 'Presets', icon: Save },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
      {/* Header */}
      <header className="border-b border-slate-700 bg-slate-900/50 backdrop-blur-sm">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-lg flex items-center justify-center">
                <Radio className="w-6 h-6" />
              </div>
              <div>
                <h1 className="text-2xl font-bold">MPX over IP Pro</h1>
                <p className="text-sm text-slate-400">192 kHz Professional Audio Link</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className={`flex items-center gap-2 px-4 py-2 rounded-lg ${
                isConnected ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
              }`}>
                {isConnected ? <Wifi className="w-4 h-4" /> : <WifiOff className="w-4 h-4" />}
                <span className="text-sm font-medium">
                  {isConnected ? 'Connected' : 'Disconnected'}
                </span>
              </div>
              <button className="p-2 hover:bg-slate-700 rounded-lg transition-colors">
                <Settings className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Tabs */}
      <div className="border-b border-slate-700 bg-slate-900/30">
        <div className="container mx-auto px-6">
          <div className="flex gap-1">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-2 px-6 py-3 border-b-2 transition-all ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-400 bg-slate-800/50'
                      : 'border-transparent text-slate-400 hover:text-slate-200 hover:bg-slate-800/30'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span className="font-medium">{tab.label}</span>
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-8">
        {activeTab === 'main' && (
          <div className="space-y-6">
            {/* Connection Settings */}
            <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
              <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                <Wifi className="w-5 h-5 text-blue-400" />
                Connection Settings
              </h2>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    Host Address
                  </label>
                  <input
                    type="text"
                    placeholder="192.168.1.100"
                    className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-2 focus:outline-none focus:border-blue-500 transition-colors"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    Port
                  </label>
                  <input
                    type="text"
                    placeholder="9000"
                    className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-2 focus:outline-none focus:border-blue-500 transition-colors"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    Protocol
                  </label>
                  <select className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-2 focus:outline-none focus:border-blue-500 transition-colors">
                    <option>TCP (Reliable)</option>
                    <option>UDP (Low Latency)</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    Sample Rate
                  </label>
                  <select className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-2 focus:outline-none focus:border-blue-500 transition-colors">
                    <option>192000 Hz</option>
                    <option>96000 Hz</option>
                    <option>384000 Hz</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Audio Devices */}
            <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
              <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                <Radio className="w-5 h-5 text-blue-400" />
                Audio Devices
              </h2>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    Input Device
                  </label>
                  <select className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-2 focus:outline-none focus:border-blue-500 transition-colors">
                    <option>Default Audio Device</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    Output Device
                  </label>
                  <select className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-2 focus:outline-none focus:border-blue-500 transition-colors">
                    <option>Default Audio Device</option>
                  </select>
                </div>
              </div>
            </div>

            {/* VU Meters */}
            <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
              <h2 className="text-xl font-bold mb-4">VU Meters</h2>
              <div className="space-y-4">
                {['Left', 'Right'].map((channel) => (
                  <div key={channel}>
                    <div className="flex justify-between text-sm text-slate-400 mb-2">
                      <span>{channel} Channel</span>
                      <span>-12.3 dBFS</span>
                    </div>
                    <div className="h-8 bg-slate-900 rounded-lg overflow-hidden relative">
                      <div
                        className="h-full bg-gradient-to-r from-green-500 via-yellow-500 to-red-500 transition-all duration-150"
                        style={{ width: '65%' }}
                      />
                      <div className="absolute inset-0 flex items-center justify-between px-2 text-xs text-slate-300 font-mono">
                        <span>-60</span>
                        <span>-40</span>
                        <span>-20</span>
                        <span>-6</span>
                        <span>0</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Control Buttons */}
            <div className="flex gap-4">
              <button
                onClick={() => {
                  setIsConnected(!isConnected);
                  if (!isConnected) setIsStreaming(false);
                }}
                className={`flex-1 flex items-center justify-center gap-2 py-4 rounded-xl font-semibold transition-all ${
                  isConnected
                    ? 'bg-red-500 hover:bg-red-600 text-white'
                    : 'bg-blue-500 hover:bg-blue-600 text-white'
                }`}
              >
                {isConnected ? <WifiOff className="w-5 h-5" /> : <Wifi className="w-5 h-5" />}
                {isConnected ? 'Disconnect' : 'Connect'}
              </button>
              <button
                onClick={() => setIsStreaming(!isStreaming)}
                disabled={!isConnected}
                className={`flex-1 flex items-center justify-center gap-2 py-4 rounded-xl font-semibold transition-all ${
                  !isConnected
                    ? 'bg-slate-700 text-slate-500 cursor-not-allowed'
                    : isStreaming
                    ? 'bg-orange-500 hover:bg-orange-600 text-white'
                    : 'bg-green-500 hover:bg-green-600 text-white'
                }`}
              >
                {isStreaming ? <Square className="w-5 h-5" /> : <Play className="w-5 h-5" />}
                {isStreaming ? 'Stop Stream' : 'Start Stream'}
              </button>
            </div>
          </div>
        )}

        {activeTab === 'processing' && (
          <div className="space-y-6">
            <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
              <h2 className="text-xl font-bold mb-4">Audio Processing</h2>
              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 bg-slate-900/50 rounded-lg">
                  <div>
                    <h3 className="font-medium">AGC (Automatic Gain Control)</h3>
                    <p className="text-sm text-slate-400">Maintains consistent audio levels</p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" className="sr-only peer" />
                    <div className="w-11 h-6 bg-slate-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-500"></div>
                  </label>
                </div>
                <div className="flex items-center justify-between p-4 bg-slate-900/50 rounded-lg">
                  <div>
                    <h3 className="font-medium">Audio Limiter</h3>
                    <p className="text-sm text-slate-400">Prevents audio clipping</p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" className="sr-only peer" />
                    <div className="w-11 h-6 bg-slate-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-500"></div>
                  </label>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'security' && (
          <div className="space-y-6">
            <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
              <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                <Shield className="w-5 h-5 text-blue-400" />
                Encryption Settings
              </h2>
              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 bg-slate-900/50 rounded-lg">
                  <div>
                    <h3 className="font-medium">AES-256 Encryption</h3>
                    <p className="text-sm text-slate-400">Secure audio transmission</p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" className="sr-only peer" />
                    <div className="w-11 h-6 bg-slate-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-500"></div>
                  </label>
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    Encryption Password
                  </label>
                  <input
                    type="password"
                    placeholder="Enter strong password"
                    className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-2 focus:outline-none focus:border-blue-500 transition-colors"
                  />
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'monitor' && (
          <div className="space-y-6">
            <div className="grid grid-cols-3 gap-4">
              <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
                <div className="text-sm text-slate-400 mb-1">Latency</div>
                <div className="text-3xl font-bold text-blue-400">12.5 ms</div>
              </div>
              <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
                <div className="text-sm text-slate-400 mb-1">Packet Loss</div>
                <div className="text-3xl font-bold text-green-400">0.02%</div>
              </div>
              <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
                <div className="text-sm text-slate-400 mb-1">Buffer Fill</div>
                <div className="text-3xl font-bold text-yellow-400">45%</div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'presets' && (
          <div className="space-y-6">
            <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold">Configuration Presets</h2>
                <button className="px-4 py-2 bg-blue-500 hover:bg-blue-600 rounded-lg font-medium transition-colors">
                  Save Current
                </button>
              </div>
              <div className="space-y-2">
                {['Default Config', 'Low Latency', 'High Quality', 'Secure Link'].map((preset) => (
                  <div
                    key={preset}
                    className="flex items-center justify-between p-4 bg-slate-900/50 rounded-lg hover:bg-slate-900 transition-colors cursor-pointer"
                  >
                    <span className="font-medium">{preset}</span>
                    <div className="flex gap-2">
                      <button className="px-3 py-1 bg-blue-500 hover:bg-blue-600 rounded text-sm transition-colors">
                        Load
                      </button>
                      <button className="px-3 py-1 bg-red-500 hover:bg-red-600 rounded text-sm transition-colors">
                        Delete
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
