const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  selectFile: () => ipcRenderer.invoke('select-file'),
  selectDirectory: () => ipcRenderer.invoke('select-directory'),
  runAutomation: (data) => ipcRenderer.invoke('run-automation', data),
  syncWebDriver: (data) => ipcRenderer.invoke('sync-webdriver', data),
  pushToDev: () => ipcRenderer.invoke('push-to-dev'),
  onLog: (callback) => ipcRenderer.on('automation-log', (_event, value) => callback(value)),

  removeLogListener: () => ipcRenderer.removeAllListeners('automation-log')
});
