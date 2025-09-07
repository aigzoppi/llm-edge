const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const axios = require('axios');

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1000,
    height: 700,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    },
    icon: path.join(__dirname, 'assets/icon.png') // Optional icon
  });

  mainWindow.loadFile('index.html');
  
  // Open DevTools in development
  if (process.argv.includes('--dev')) {
    mainWindow.webContents.openDevTools();
  }
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

// IPC handlers for REST API calls
ipcMain.handle('api-call', async (event, { method, endpoint, baseUrl, data }) => {
  try {
    const url = `${baseUrl}${endpoint}`;
    console.log(`Making ${method} request to: ${url}`);
    
    const config = {
      method: method.toLowerCase(),
      url: url,
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 10000,
    };
    
    if (data && (method === 'POST' || method === 'PUT')) {
      config.data = data;
    }
    
    const response = await axios(config);
    
    return {
      success: true,
      data: response.data,
      status: response.status,
      statusText: response.statusText
    };
  } catch (error) {
    console.error('API call failed:', error);
    
    return {
      success: false,
      error: error.message,
      status: error.response?.status || 0,
      statusText: error.response?.statusText || 'Network Error'
    };
  }
});
