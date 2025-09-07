// preload.js - Secure bridge between main and renderer
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  makeApiCall: (method, endpoint, baseUrl, data) => 
    ipcRenderer.invoke('api-call', { method, endpoint, baseUrl, data }),
  saveImage: (dataUrl) => ipcRenderer.invoke('save-image', dataUrl)
});