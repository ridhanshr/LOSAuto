const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const { spawn, execSync } = require('child_process');
const fs = require('fs');

let mainWindow;

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

// Helper: Push current changes to dev branch
function pushToDevBranch(projectRoot, logCallback) {
  try {
    const execOpts = { cwd: projectRoot, encoding: 'utf-8', stdio: 'pipe' };
    logCallback('[GIT] Checking for dev branch...');

    // Check if dev branch exists locally
    let branches;
    try {
      branches = execSync('git branch --list dev', execOpts).trim();
    } catch (e) {
      logCallback('[GIT ERROR] Not a git repository or git not installed.');
      return false;
    }

    // Stash current branch name
    const currentBranch = execSync('git rev-parse --abbrev-ref HEAD', execOpts).trim();

    if (!branches) {
      logCallback('[GIT] Branch dev not found, creating...');
      execSync('git checkout -b dev', execOpts);
      logCallback('[GIT] Branch dev created.');
    } else if (currentBranch !== 'dev') {
      logCallback('[GIT] Switching to dev branch...');
      execSync('git checkout dev', execOpts);
    }

    // Merge latest from current working branch if we were on a different branch
    if (currentBranch !== 'dev' && branches) {
      try {
        logCallback(`[GIT] Merging changes from ${currentBranch}...`);
        execSync(`git merge ${currentBranch} --no-edit`, execOpts);
      } catch (e) {
        logCallback('[GIT WARNING] Merge conflict detected, using current state.');
      }
    }

    // Stage all, commit, and push
    execSync('git add -A', execOpts);
    try {
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      execSync(`git commit -m "fast-mode: auto-commit ${timestamp}"`, execOpts);
      logCallback('[GIT] Changes committed.');
    } catch (e) {
      logCallback('[GIT] No new changes to commit.');
    }

    logCallback('[GIT] Pushing to origin/dev...');
    execSync('git push -u origin dev', execOpts);
    logCallback('[GIT] Push to dev branch successful!');

    // Switch back to original branch
    if (currentBranch !== 'dev') {
      execSync(`git checkout ${currentBranch}`, execOpts);
      logCallback(`[GIT] Switched back to ${currentBranch}.`);
    }

    return true;
  } catch (err) {
    logCallback(`[GIT ERROR] ${err.message}`);
    return false;
  }
}

// IPC Handler to push to dev branch
ipcMain.handle('push-to-dev', async (event) => {
  const projectRoot = path.resolve(__dirname, '..');
  const logCallback = (msg) => event.sender.send('automation-log', msg);
  const success = pushToDevBranch(projectRoot, logCallback);
  return { success };
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

    
    // Construct arguments including speed if relevant (implementation in python scripts may vary)
    const args = ['-m', scriptName, '--browser', browserType.toLowerCase(), '--data-file', targetDataFile];
    const isFastMode = speed === 'Fast (Experimental)';
    if (isFastMode) args.push('--fast');

    // In fast mode, push to dev branch first
    if (isFastMode) {
      event.sender.send('automation-log', '=== FAST MODE: Pushing to dev branch before automation ===');
      pushToDevBranch(projectRoot, (msg) => event.sender.send('automation-log', msg));
      event.sender.send('automation-log', '=== Starting headless automation ===');
    }
    
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

