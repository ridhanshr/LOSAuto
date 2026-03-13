const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  runAutomation: (config) => ipcRenderer.invoke('run-automation', config),
  selectFile: () => ipcRenderer.invoke('select-file'),
  selectDirectory: () => ipcRenderer.invoke('select-directory'),
  runAutomation: (data) => ipcRenderer.invoke('run-automation', data),
  syncWebDriver: (data) => ipcRenderer.invoke('sync-webdriver', data),
  onLog: (callback) => ipcRenderer.on('automation-log', (_event, value) => callback(value)),

  removeLogListener: () => ipcRenderer.removeAllListeners('automation-log')
});
