import { app, BrowserWindow, ipcMain, screen } from 'electron'
import * as path from 'path'
import { spawn, ChildProcess } from 'child_process'
import Store from 'electron-store'

const store = new Store()

let mainWindow: BrowserWindow | null = null
let pythonProcess: ChildProcess | null = null

const isDev = process.env.NODE_ENV === 'development'
const isKioskMode = process.env.KIOSK_MODE === 'true'

function createWindow() {
  const primaryDisplay = screen.getPrimaryDisplay()
  const { width, height } = primaryDisplay.workAreaSize

  mainWindow = new BrowserWindow({
    width: isKioskMode ? width : 1400,
    height: isKioskMode ? height : 900,
    fullscreen: isKioskMode,
    kiosk: isKioskMode,
    frame: !isKioskMode,
    autoHideMenuBar: true,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js'),
    },
  })

  if (isDev) {
    mainWindow.loadURL('http://localhost:5173')
    mainWindow.webContents.openDevTools()
  } else {
    mainWindow.loadFile(path.join(__dirname, '../renderer/index.html'))
  }

  mainWindow.on('closed', () => {
    mainWindow = null
  })

  if (isKioskMode) {
    mainWindow.setMenuBarVisibility(false)
    mainWindow.webContents.on('before-input-event', (event, input) => {
      if (input.key === 'F11' || (input.control && input.key === 'w')) {
        event.preventDefault()
      }
    })
  }
}

function startPythonBackend() {
  const pythonPath = isDev
    ? 'python3'
    : path.join(process.resourcesPath, 'python', 'backend.py')

  const scriptPath = isDev
    ? path.join(__dirname, '../../python/backend.py')
    : pythonPath

  pythonProcess = spawn('python3', [scriptPath])

  pythonProcess.stdout?.on('data', (data) => {
    console.log(`Python: ${data}`)
    if (mainWindow) {
      mainWindow.webContents.send('python-log', data.toString())
    }
  })

  pythonProcess.stderr?.on('data', (data) => {
    console.error(`Python Error: ${data}`)
    if (mainWindow) {
      mainWindow.webContents.send('python-error', data.toString())
    }
  })

  pythonProcess.on('close', (code) => {
    console.log(`Python process exited with code ${code}`)
  })
}

app.whenReady().then(() => {
  createWindow()
  startPythonBackend()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('will-quit', () => {
  if (pythonProcess) {
    pythonProcess.kill()
  }
})

ipcMain.handle('get-config', (_, key: string) => {
  return store.get(key)
})

ipcMain.handle('set-config', (_, key: string, value: any) => {
  store.set(key, value)
  return true
})

ipcMain.handle('get-all-config', () => {
  return store.store
})

ipcMain.handle('get-system-info', async () => {
  const os = require('os')
  return {
    platform: process.platform,
    arch: process.arch,
    cpus: os.cpus().length,
    totalMemory: os.totalmem(),
    freeMemory: os.freemem(),
    uptime: os.uptime(),
    hostname: os.hostname(),
  }
})

ipcMain.handle('python-command', async (_, command: string, args: any) => {
  if (mainWindow) {
    mainWindow.webContents.send('python-command', { command, args })
  }
  return { success: true }
})
