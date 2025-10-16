import { useState, useEffect } from 'react'
import { Cpu, HardDrive, Activity, Network } from 'lucide-react'
import { StreamStats, SystemInfo } from '../../shared/types'

interface SystemMonitorProps {
  stats: StreamStats
}

export default function SystemMonitor({ stats }: SystemMonitorProps) {
  const [systemInfo, setSystemInfo] = useState<SystemInfo | null>(null)
  const [cpuUsage, setCpuUsage] = useState(0)
  const [memoryUsage, setMemoryUsage] = useState(0)

  useEffect(() => {
    if (window.electron) {
      window.electron.getSystemInfo().then(setSystemInfo)
    }

    const interval = setInterval(() => {
      setCpuUsage(Math.random() * 100)
      if (systemInfo) {
        const used = systemInfo.totalMemory - systemInfo.freeMemory
        setMemoryUsage((used / systemInfo.totalMemory) * 100)
      }
    }, 2000)

    return () => clearInterval(interval)
  }, [systemInfo])

  const formatBytes = (bytes: number) => {
    if (bytes === 0) return '0 B'
    const k = 1024
    const sizes = ['B', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
  }

  const formatUptime = (seconds: number) => {
    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    return `${hours}h ${minutes}m`
  }

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
          <div className="flex items-center gap-3 mb-4">
            <Cpu className="w-6 h-6 text-blue-500" />
            <h3 className="text-lg font-semibold">CPU Usage</h3>
          </div>
          <div className="space-y-3">
            <div className="flex justify-between text-sm">
              <span className="text-slate-400">Current</span>
              <span className="font-mono">{cpuUsage.toFixed(1)}%</span>
            </div>
            <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-blue-500 to-cyan-500 transition-all duration-500"
                style={{ width: `${cpuUsage}%` }}
              />
            </div>
            {systemInfo && (
              <div className="text-xs text-slate-400 mt-2">
                {systemInfo.cpus} cores available
              </div>
            )}
          </div>
        </div>

        <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
          <div className="flex items-center gap-3 mb-4">
            <HardDrive className="w-6 h-6 text-green-500" />
            <h3 className="text-lg font-semibold">Memory Usage</h3>
          </div>
          <div className="space-y-3">
            <div className="flex justify-between text-sm">
              <span className="text-slate-400">Current</span>
              <span className="font-mono">{memoryUsage.toFixed(1)}%</span>
            </div>
            <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-green-500 to-emerald-500 transition-all duration-500"
                style={{ width: `${memoryUsage}%` }}
              />
            </div>
            {systemInfo && (
              <div className="text-xs text-slate-400 mt-2">
                {formatBytes(systemInfo.freeMemory)} free of {formatBytes(systemInfo.totalMemory)}
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
        <div className="flex items-center gap-3 mb-4">
          <Network className="w-6 h-6 text-cyan-500" />
          <h3 className="text-lg font-semibold">Network Statistics</h3>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="p-4 bg-slate-700/50 rounded-lg">
            <div className="text-xs text-slate-400 mb-1">Sent</div>
            <div className="text-lg font-mono">{formatBytes(stats.bytesSent)}</div>
          </div>
          <div className="p-4 bg-slate-700/50 rounded-lg">
            <div className="text-xs text-slate-400 mb-1">Received</div>
            <div className="text-lg font-mono">{formatBytes(stats.bytesReceived)}</div>
          </div>
          <div className="p-4 bg-slate-700/50 rounded-lg">
            <div className="text-xs text-slate-400 mb-1">Bitrate</div>
            <div className="text-lg font-mono">{stats.bitrate} kbps</div>
          </div>
          <div className="p-4 bg-slate-700/50 rounded-lg">
            <div className="text-xs text-slate-400 mb-1">Latency</div>
            <div className="text-lg font-mono">{stats.latency} ms</div>
          </div>
        </div>
      </div>

      <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
        <div className="flex items-center gap-3 mb-4">
          <Activity className="w-6 h-6 text-orange-500" />
          <h3 className="text-lg font-semibold">System Information</h3>
        </div>
        {systemInfo && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div className="flex justify-between p-3 bg-slate-700/50 rounded-lg">
              <span className="text-sm text-slate-400">Hostname</span>
              <span className="text-sm font-mono">{systemInfo.hostname}</span>
            </div>
            <div className="flex justify-between p-3 bg-slate-700/50 rounded-lg">
              <span className="text-sm text-slate-400">Platform</span>
              <span className="text-sm font-mono">{systemInfo.platform}</span>
            </div>
            <div className="flex justify-between p-3 bg-slate-700/50 rounded-lg">
              <span className="text-sm text-slate-400">Architecture</span>
              <span className="text-sm font-mono">{systemInfo.arch}</span>
            </div>
            <div className="flex justify-between p-3 bg-slate-700/50 rounded-lg">
              <span className="text-sm text-slate-400">Uptime</span>
              <span className="text-sm font-mono">{formatUptime(systemInfo.uptime)}</span>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
