const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  runAutomation: (config) => ipcRenderer.invoke('run-automation', config),
  selectFile: () => ipcRenderer.invoke('select-file'),
  selectDirectory: () => ipcRenderer.invoke('select-directory'),
  onLog: (callback) => ipcRenderer.on('automation-log', (event, message) => callback(message)),
  removeLogListener: () => ipcRenderer.removeAllListeners('automation-log')
});
