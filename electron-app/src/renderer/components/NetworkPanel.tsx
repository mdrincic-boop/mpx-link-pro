import { useState, useEffect } from 'react'
import { Network, Save, RefreshCw, Wifi, Cable } from 'lucide-react'

interface NetworkConfig {
  method: 'dhcp' | 'static'
  ipAddress: string
  netmask: string
  gateway: string
  dns1: string
  dns2: string
  interface: string
}

export default function NetworkPanel() {
  const [config, setConfig] = useState<NetworkConfig>({
    method: 'dhcp',
    ipAddress: '192.168.1.100',
    netmask: '255.255.255.0',
    gateway: '192.168.1.1',
    dns1: '8.8.8.8',
    dns2: '8.8.4.4',
    interface: 'eth0',
  })

  const [currentConfig, setCurrentConfig] = useState<any>(null)
  const [interfaces, setInterfaces] = useState<string[]>([])
  const [saving, setSaving] = useState(false)
  const [saved, setSaved] = useState(false)

  useEffect(() => {
    loadNetworkInfo()
  }, [])

  const loadNetworkInfo = async () => {
    if (window.electron) {
      try {
        const result = await window.electron.pythonCommand('get_network_info', {})
        if (result.data) {
          setCurrentConfig(result.data.current)
          setInterfaces(result.data.interfaces || ['eth0', 'wlan0'])
        }
      } catch (error) {
        console.error('Failed to load network info:', error)
      }
    }
  }

  const handleSave = async () => {
    setSaving(true)

    if (window.electron) {
      try {
        await window.electron.pythonCommand('configure_network', config)
        setSaved(true)
        setTimeout(() => setSaved(false), 3000)

        // Reload current config
        setTimeout(loadNetworkInfo, 2000)
      } catch (error) {
        console.error('Failed to save network config:', error)
      }
    }

    setSaving(false)
  }

  const handleRefresh = () => {
    loadNetworkInfo()
  }

  return (
    <div className="space-y-6">
      <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <Network className="w-6 h-6 text-blue-500" />
            <div>
              <h2 className="text-lg font-semibold">Network Configuration</h2>
              <p className="text-sm text-slate-400">Configure static IP or use DHCP</p>
            </div>
          </div>
          <button
            onClick={handleRefresh}
            className="p-2 hover:bg-slate-700 rounded-lg transition-colors"
            title="Refresh network info"
          >
            <RefreshCw className="w-5 h-5" />
          </button>
        </div>

        {currentConfig && (
          <div className="mb-6 p-4 bg-slate-700/50 rounded-lg border border-slate-600">
            <div className="flex items-center gap-2 mb-3">
              <Cable className="w-5 h-5 text-green-500" />
              <span className="font-semibold">Current Configuration</span>
            </div>
            <div className="grid grid-cols-2 gap-3 text-sm">
              <div>
                <span className="text-slate-400">IP Address:</span>
                <span className="ml-2 font-mono text-green-400">{currentConfig.ip || 'N/A'}</span>
              </div>
              <div>
                <span className="text-slate-400">Gateway:</span>
                <span className="ml-2 font-mono text-green-400">{currentConfig.gateway || 'N/A'}</span>
              </div>
              <div>
                <span className="text-slate-400">Netmask:</span>
                <span className="ml-2 font-mono text-green-400">{currentConfig.netmask || 'N/A'}</span>
              </div>
              <div>
                <span className="text-slate-400">DNS:</span>
                <span className="ml-2 font-mono text-green-400">{currentConfig.dns || 'N/A'}</span>
              </div>
            </div>
          </div>
        )}

        <div className="space-y-4">
          <div>
            <label className="text-sm text-slate-400 mb-2 block">Network Interface</label>
            <select
              value={config.interface}
              onChange={(e) => setConfig({ ...config, interface: e.target.value })}
              className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 focus:outline-none focus:border-blue-500"
            >
              {interfaces.map((iface) => (
                <option key={iface} value={iface}>
                  {iface}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="text-sm text-slate-400 mb-2 block">Connection Method</label>
            <div className="grid grid-cols-2 gap-3">
              <button
                onClick={() => setConfig({ ...config, method: 'dhcp' })}
                className={`p-4 rounded-lg border-2 transition-all ${
                  config.method === 'dhcp'
                    ? 'border-blue-500 bg-blue-500/10'
                    : 'border-slate-600 hover:border-slate-500'
                }`}
              >
                <Wifi className="w-6 h-6 mx-auto mb-2" />
                <div className="text-sm font-medium">DHCP (Automatic)</div>
                <div className="text-xs text-slate-400">Get IP automatically</div>
              </button>

              <button
                onClick={() => setConfig({ ...config, method: 'static' })}
                className={`p-4 rounded-lg border-2 transition-all ${
                  config.method === 'static'
                    ? 'border-blue-500 bg-blue-500/10'
                    : 'border-slate-600 hover:border-slate-500'
                }`}
              >
                <Cable className="w-6 h-6 mx-auto mb-2" />
                <div className="text-sm font-medium">Static IP</div>
                <div className="text-xs text-slate-400">Manual configuration</div>
              </button>
            </div>
          </div>

          {config.method === 'static' && (
            <>
              <div>
                <label className="text-sm text-slate-400 mb-2 block">IP Address</label>
                <input
                  type="text"
                  value={config.ipAddress}
                  onChange={(e) => setConfig({ ...config, ipAddress: e.target.value })}
                  className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 focus:outline-none focus:border-blue-500 font-mono"
                  placeholder="192.168.1.100"
                />
              </div>

              <div>
                <label className="text-sm text-slate-400 mb-2 block">Subnet Mask</label>
                <input
                  type="text"
                  value={config.netmask}
                  onChange={(e) => setConfig({ ...config, netmask: e.target.value })}
                  className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 focus:outline-none focus:border-blue-500 font-mono"
                  placeholder="255.255.255.0"
                />
              </div>

              <div>
                <label className="text-sm text-slate-400 mb-2 block">Gateway</label>
                <input
                  type="text"
                  value={config.gateway}
                  onChange={(e) => setConfig({ ...config, gateway: e.target.value })}
                  className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 focus:outline-none focus:border-blue-500 font-mono"
                  placeholder="192.168.1.1"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm text-slate-400 mb-2 block">Primary DNS</label>
                  <input
                    type="text"
                    value={config.dns1}
                    onChange={(e) => setConfig({ ...config, dns1: e.target.value })}
                    className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 focus:outline-none focus:border-blue-500 font-mono"
                    placeholder="8.8.8.8"
                  />
                </div>

                <div>
                  <label className="text-sm text-slate-400 mb-2 block">Secondary DNS</label>
                  <input
                    type="text"
                    value={config.dns2}
                    onChange={(e) => setConfig({ ...config, dns2: e.target.value })}
                    className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 focus:outline-none focus:border-blue-500 font-mono"
                    placeholder="8.8.4.4"
                  />
                </div>
              </div>
            </>
          )}
        </div>
      </div>

      <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
        <h3 className="text-sm font-semibold mb-3 text-slate-300">Common DNS Servers</h3>
        <div className="grid grid-cols-2 gap-3 text-sm">
          <div className="p-3 bg-slate-700/50 rounded-lg">
            <div className="font-medium mb-1">Google DNS</div>
            <div className="font-mono text-xs text-slate-400">8.8.8.8 / 8.8.4.4</div>
          </div>
          <div className="p-3 bg-slate-700/50 rounded-lg">
            <div className="font-medium mb-1">Cloudflare DNS</div>
            <div className="font-mono text-xs text-slate-400">1.1.1.1 / 1.0.0.1</div>
          </div>
          <div className="p-3 bg-slate-700/50 rounded-lg">
            <div className="font-medium mb-1">Quad9 DNS</div>
            <div className="font-mono text-xs text-slate-400">9.9.9.9 / 149.112.112.112</div>
          </div>
          <div className="p-3 bg-slate-700/50 rounded-lg">
            <div className="font-medium mb-1">OpenDNS</div>
            <div className="font-mono text-xs text-slate-400">208.67.222.222 / 208.67.220.220</div>
          </div>
        </div>
      </div>

      <button
        onClick={handleSave}
        disabled={saving}
        className={`w-full py-4 rounded-lg font-semibold flex items-center justify-center gap-2 transition-colors ${
          saved
            ? 'bg-green-600 text-white'
            : saving
            ? 'bg-slate-600 text-slate-400 cursor-wait'
            : 'bg-blue-600 hover:bg-blue-700 text-white'
        }`}
      >
        {saved ? (
          <>
            <RefreshCw className="w-5 h-5" />
            Configuration Saved! (Reboot may be required)
          </>
        ) : saving ? (
          <>
            <RefreshCw className="w-5 h-5 animate-spin" />
            Applying Configuration...
          </>
        ) : (
          <>
            <Save className="w-5 h-5" />
            Apply Network Configuration
          </>
        )}
      </button>

      <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-4">
        <p className="text-sm text-yellow-300">
          <strong>Warning:</strong> Changing network settings may temporarily disconnect the device.
          Make sure you have physical access to the machine or a backup connection method.
        </p>
      </div>
    </div>
  )
}
