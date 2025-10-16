import { useState, useEffect } from 'react'
import { Save, RefreshCw, Database, Wifi } from 'lucide-react'

export default function SettingsPanel() {
  const [autoStart, setAutoStart] = useState(true)
  const [kioskMode, setKioskMode] = useState(false)
  const [enableWebInterface, setEnableWebInterface] = useState(true)
  const [webPort, setWebPort] = useState('3000')
  const [supabaseUrl, setSupabaseUrl] = useState('')
  const [supabaseKey, setSupabaseKey] = useState('')
  const [saved, setSaved] = useState(false)

  useEffect(() => {
    if (window.electron) {
      window.electron.getAllConfig().then((config) => {
        setAutoStart(config.autoStart ?? true)
        setKioskMode(config.kioskMode ?? false)
        setEnableWebInterface(config.enableWebInterface ?? true)
        setWebPort(config.webPort ?? '3000')
        setSupabaseUrl(config.supabaseUrl ?? '')
        setSupabaseKey(config.supabaseKey ?? '')
      })
    }
  }, [])

  const handleSave = async () => {
    if (window.electron) {
      await window.electron.setConfig('autoStart', autoStart)
      await window.electron.setConfig('kioskMode', kioskMode)
      await window.electron.setConfig('enableWebInterface', enableWebInterface)
      await window.electron.setConfig('webPort', webPort)
      await window.electron.setConfig('supabaseUrl', supabaseUrl)
      await window.electron.setConfig('supabaseKey', supabaseKey)

      setSaved(true)
      setTimeout(() => setSaved(false), 2000)
    }
  }

  return (
    <div className="space-y-6">
      <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
        <h2 className="text-lg font-semibold mb-4">Application Settings</h2>

        <div className="space-y-4">
          <div className="flex items-center justify-between p-4 bg-slate-700/50 rounded-lg">
            <div>
              <div className="font-medium">Auto Start</div>
              <div className="text-sm text-slate-400">Launch app on system boot</div>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={autoStart}
                onChange={(e) => setAutoStart(e.target.checked)}
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-slate-600 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
            </label>
          </div>

          <div className="flex items-center justify-between p-4 bg-slate-700/50 rounded-lg">
            <div>
              <div className="font-medium">Kiosk Mode</div>
              <div className="text-sm text-slate-400">Fullscreen with no exit (requires restart)</div>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={kioskMode}
                onChange={(e) => setKioskMode(e.target.checked)}
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-slate-600 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
            </label>
          </div>
        </div>
      </div>

      <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
        <div className="flex items-center gap-3 mb-4">
          <Wifi className="w-6 h-6 text-blue-500" />
          <h2 className="text-lg font-semibold">Web Interface</h2>
        </div>

        <div className="space-y-4">
          <div className="flex items-center justify-between p-4 bg-slate-700/50 rounded-lg">
            <div>
              <div className="font-medium">Enable Web Interface</div>
              <div className="text-sm text-slate-400">Remote control via browser</div>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={enableWebInterface}
                onChange={(e) => setEnableWebInterface(e.target.checked)}
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-slate-600 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
            </label>
          </div>

          {enableWebInterface && (
            <div>
              <label className="text-sm text-slate-400 mb-2 block">Web Port</label>
              <input
                type="text"
                value={webPort}
                onChange={(e) => setWebPort(e.target.value)}
                className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 focus:outline-none focus:border-blue-500 font-mono"
                placeholder="3000"
              />
            </div>
          )}
        </div>
      </div>

      <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
        <div className="flex items-center gap-3 mb-4">
          <Database className="w-6 h-6 text-green-500" />
          <h2 className="text-lg font-semibold">Supabase Configuration</h2>
        </div>

        <div className="space-y-4">
          <div>
            <label className="text-sm text-slate-400 mb-2 block">Supabase URL</label>
            <input
              type="text"
              value={supabaseUrl}
              onChange={(e) => setSupabaseUrl(e.target.value)}
              className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 focus:outline-none focus:border-blue-500 font-mono text-sm"
              placeholder="https://your-project.supabase.co"
            />
          </div>

          <div>
            <label className="text-sm text-slate-400 mb-2 block">Supabase Anon Key</label>
            <input
              type="password"
              value={supabaseKey}
              onChange={(e) => setSupabaseKey(e.target.value)}
              className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 focus:outline-none focus:border-blue-500 font-mono text-sm"
              placeholder="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            />
          </div>
        </div>
      </div>

      <button
        onClick={handleSave}
        className={`w-full py-4 rounded-lg font-semibold flex items-center justify-center gap-2 transition-colors ${
          saved
            ? 'bg-green-600 text-white'
            : 'bg-blue-600 hover:bg-blue-700 text-white'
        }`}
      >
        {saved ? (
          <>
            <RefreshCw className="w-5 h-5" />
            Settings Saved!
          </>
        ) : (
          <>
            <Save className="w-5 h-5" />
            Save Settings
          </>
        )}
      </button>
    </div>
  )
}
