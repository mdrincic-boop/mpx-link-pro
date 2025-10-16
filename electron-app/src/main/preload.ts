import { contextBridge, ipcRenderer } from 'electron'

contextBridge.exposeInMainWorld('electron', {
  getConfig: (key: string) => ipcRenderer.invoke('get-config', key),
  setConfig: (key: string, value: any) => ipcRenderer.invoke('set-config', key, value),
  getAllConfig: () => ipcRenderer.invoke('get-all-config'),
  getSystemInfo: () => ipcRenderer.invoke('get-system-info'),
  pythonCommand: (command: string, args: any) => ipcRenderer.invoke('python-command', command, args),

  onPythonLog: (callback: (data: string) => void) => {
    ipcRenderer.on('python-log', (_, data) => callback(data))
  },

  onPythonError: (callback: (data: string) => void) => {
    ipcRenderer.on('python-error', (_, data) => callback(data))
  },

  onPythonCommand: (callback: (data: any) => void) => {
    ipcRenderer.on('python-command', (_, data) => callback(data))
  },
})
