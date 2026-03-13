const { app, BrowserWindow, ipcMain, dialog, protocol, net } = require('electron');
const path = require('path');
const { spawn, execSync } = require('child_process');
const fs = require('fs');

let mainWindow;
let currentProcess = null;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    titleBarStyle: 'hidden',
    backgroundColor: '#0f172a',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
    },
  });

  const isDev = process.env.NODE_ENV === 'development';
  if (isDev) {
    mainWindow.loadURL('http://localhost:5173');
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadFile(path.join(__dirname, 'dist/index.html'));
  }
}

app.whenReady().then(() => {
  // Register custom protocol for images
  protocol.handle('atom-img', (request) => {
    const url = decodeURIComponent(request.url.replace('atom-img://', ''));
    const isDev = process.env.NODE_ENV === 'development';
    const projectRoot = isDev ? path.resolve(__dirname, '..') : process.resourcesPath;
    const filePath = path.join(projectRoot, url);
    return net.fetch('file://' + filePath);
  });

  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// IPC Handler to select a file
ipcMain.handle('select-file', async () => {
  console.log('Select file dialog requested');
  const { canceled, filePaths } = await dialog.showOpenDialog(mainWindow, {
    properties: ['openFile'],
    filters: [{ name: 'Excel Files', extensions: ['xlsx', 'xls'] }, { name: 'All Files', extensions: ['*'] }]
  });
  if (!canceled) {
    console.log('File selected:', filePaths[0]);
    return filePaths[0];
  }
  return null;
});

// IPC Handler to select a directory
ipcMain.handle('select-directory', async () => {
  const { canceled, filePaths } = await dialog.showOpenDialog(mainWindow, {
    properties: ['openDirectory'],
  });
  if (!canceled) {
    return filePaths[0];
  }
  return null;
});


// IPC Handler to run Python scripts
ipcMain.handle('run-automation', async (event, { scriptName, browserType, dataFile, speed }) => {
  return new Promise((resolve, reject) => {
    console.log(`Starting automation: ${scriptName} with ${browserType} and speed ${speed}`);
    
    const pythonExe = process.platform === 'win32' ? 'python' : 'python3';
    
    // In production, resources are in process.resourcesPath
    // In dev, they are in the parent directory
    const isDev = process.env.NODE_ENV === 'development';
    const projectRoot = isDev 
      ? path.resolve(__dirname, '..') 
      : process.resourcesPath;
    
    // Use the provided dataFile or fallback to default
    const targetDataFile = dataFile || path.join(projectRoot, 'Data/LOSData.xlsx');

    // Construct arguments including speed if relevant
    const args = ['-m', scriptName, '--browser', browserType.toLowerCase(), '--data-file', targetDataFile];
    const isFastMode = speed === 'Fast (Experimental)';
    if (isFastMode) args.push('--fast');

    console.log(`Executing: ${pythonExe} ${args.join(' ')}`);

    const child = spawn(pythonExe, args, {
      cwd: projectRoot,
      env: { ...process.env, PYTHONUNBUFFERED: '1' },
      shell: true
    });

    currentProcess = child;

    // Watch for new screenshots
    const screenshotDir = path.join(projectRoot, 'Data', 'screenshoot');
    if (!fs.existsSync(screenshotDir)) fs.mkdirSync(screenshotDir, { recursive: true });

    const watcher = fs.watch(screenshotDir, (eventType, filename) => {
      if (filename && filename.endsWith('.png')) {
        event.sender.send('new-screenshot', filename);
      }
    });

    child.stdout.on('data', (data) => {
      event.sender.send('automation-log', data.toString());
    });

    child.stderr.on('data', (data) => {
      event.sender.send('automation-log', `[ERROR] ${data.toString()}`);
    });

    child.on('close', (code) => {
      watcher.close();
      currentProcess = null;
      event.sender.send('automation-log', `--- Process finished with code ${code} ---`);
      resolve({ code });
    });

    child.on('error', (err) => {
      event.sender.send('automation-log', `[SYSTEM ERROR] ${err.message}`);
      reject(err);
    });
  });
});

// IPC Handler to sync WebDrivers
ipcMain.handle('sync-webdriver', async (event, { browserType }) => {
  return new Promise((resolve, reject) => {
    console.log(`Starting WebDriver sync for: ${browserType}`);
    
    const pythonExe = process.platform === 'win32' ? 'python' : 'python3';
    const projectRoot = path.resolve(__dirname, '..');
    
    const args = ['-m', 'src.scripts.sync_webdriver', '--browser', browserType.toLowerCase()];
    
    console.log(`Executing: ${pythonExe} ${args.join(' ')}`);

    const child = spawn(pythonExe, args, {
      cwd: projectRoot,
      env: { ...process.env, PYTHONUNBUFFERED: '1' },
      shell: true
    });

    child.stdout.on('data', (data) => {
      event.sender.send('automation-log', data.toString());
    });

    child.stderr.on('data', (data) => {
      event.sender.send('automation-log', `[ERROR] ${data.toString()}`);
    });

    child.on('close', (code) => {
      const msg = code === 0 ? "Sync completed successfully." : `Sync failed with code ${code}.`;
      event.sender.send('automation-log', `--- ${msg} ---`);
      resolve({ code, success: code === 0 });
    });

    child.on('error', (err) => {
      event.sender.send('automation-log', `[SYSTEM ERROR] ${err.message}`);
      reject(err);
    });
  });
});

// IPC Handler to stop automation
ipcMain.handle('stop-automation', async () => {
  if (currentProcess) {
    console.log('Stopping current automation process...');
    // On Windows, taskkill is more reliable for tree killing
    if (process.platform === 'win32') {
      try {
        execSync(`taskkill /pid ${currentProcess.pid} /f /t`);
      } catch (err) {
        console.error('Error stopping process:', err);
      }
    } else {
      currentProcess.kill('SIGKILL');
    }
    return { success: true };
  }
  return { success: false };
});
