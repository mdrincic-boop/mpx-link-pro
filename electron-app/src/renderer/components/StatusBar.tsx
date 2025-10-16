import { StreamStats } from '../../shared/types'

interface StatusBarProps {
  stats: StreamStats
}

export default function StatusBar({ stats }: StatusBarProps) {
  const statusColors = {
    idle: 'text-slate-400',
    connecting: 'text-yellow-500',
    connected: 'text-green-500',
    error: 'text-red-500',
  }

  const formatBytes = (bytes: number) => {
    if (bytes === 0) return '0 B'
    const k = 1024
    const sizes = ['B', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
  }

  return (
    <footer className="bg-slate-800 border-t border-slate-700 px-6 py-3">
      <div className="flex items-center justify-between text-sm">
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-2">
            <span className="text-slate-400">Status:</span>
            <span className={`font-medium ${statusColors[stats.status]}`}>
              {stats.status.toUpperCase()}
            </span>
          </div>

          {stats.status === 'connected' && (
            <>
              <div className="flex items-center gap-2">
                <span className="text-slate-400">Latency:</span>
                <span className="font-mono text-slate-200">{stats.latency}ms</span>
              </div>

              <div className="flex items-center gap-2">
                <span className="text-slate-400">Bitrate:</span>
                <span className="font-mono text-slate-200">{stats.bitrate} kbps</span>
              </div>
            </>
          )}
        </div>

        <div className="flex items-center gap-6">
          <div className="flex items-center gap-2">
            <span className="text-slate-400">TX:</span>
            <span className="font-mono text-green-400">{formatBytes(stats.bytesSent)}</span>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-slate-400">RX:</span>
            <span className="font-mono text-blue-400">{formatBytes(stats.bytesReceived)}</span>
          </div>

          {stats.packetsLost > 0 && (
            <div className="flex items-center gap-2">
              <span className="text-slate-400">Lost:</span>
              <span className="font-mono text-red-400">{stats.packetsLost}</span>
            </div>
          )}
        </div>
      </div>
    </footer>
  )
}
