export interface SystemInfo {
  platform: string
  arch: string
  cpus: number
  totalMemory: number
  freeMemory: number
  uptime: number
  hostname: string
}

export interface AudioDevice {
  id: string
  name: string
  type: 'input' | 'output'
  channels: number
  sampleRate: number
  isDefault: boolean
}

export interface StreamConfig {
  mode: 'sender' | 'receiver'
  channelMode: 'mono' | 'stereo' | 'multi'
  inputDevice?: string
  outputDevice?: string
  sampleRate: number
  bufferSize: number
  remoteHost?: string
  remotePort?: number
  localPort?: number
  codec: 'pcm' | 'opus'
  bitrate?: number
}

export interface StreamStats {
  status: 'idle' | 'connecting' | 'connected' | 'error'
  bytesSent: number
  bytesReceived: number
  packetsLost: number
  latency: number
  bitrate: number
  uptime: number
}

export interface MonitoringData {
  cpu: number
  memory: number
  network: {
    sent: number
    received: number
  }
  audio: {
    inputLevel: number
    outputLevel: number
    dropouts: number
  }
  timestamp: number
}

export interface ElectronAPI {
  getConfig: (key: string) => Promise<any>
  setConfig: (key: string, value: any) => Promise<boolean>
  getAllConfig: () => Promise<Record<string, any>>
  getSystemInfo: () => Promise<SystemInfo>
  pythonCommand: (command: string, args: any) => Promise<{ success: boolean }>
  onPythonLog: (callback: (data: string) => void) => void
  onPythonError: (callback: (data: string) => void) => void
  onPythonCommand: (callback: (data: any) => void) => void
}

declare global {
  interface Window {
    electron: ElectronAPI
  }
}
