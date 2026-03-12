import React, { useState, useEffect, useRef } from 'react';
import { 
  Play, 
  Terminal, 
  Settings, 
  LayoutDashboard, 
  FileText, 
  PlusSquare, 
  UserPlus, 
  CreditCard, 
  RotateCcw,
  LogOut,
  ChevronRight,
  Monitor,
  FileSearch,
  CheckCircle2,
  AlertCircle,
  Clock
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';
import briLogo from './assets/bri-logo.png';


function cn(...inputs) {
  return twMerge(clsx(inputs));
}

const SidebarItem = ({ icon: Icon, label, active, onClick }) => (
  <button
    onClick={onClick}
    className={cn(
      "w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-all duration-200 group",
      active 
        ? "bg-primary/20 text-primary-light border-r-4 border-primary" 
        : "text-slate-400 hover:bg-slate-800/50 hover:text-slate-200"
    )}
  >
    <Icon className={cn("w-5 h-5", active ? "text-primary-light" : "group-hover:text-slate-200")} />
    <span className="font-medium">{label}</span>
    {active && <motion.div layoutId="active-indicator" className="ml-auto"><ChevronRight className="w-4 h-4" /></motion.div>}
  </button>
);

const Card = ({ title, value, icon: Icon, color }) => (
  <div className="bg-slate-800/40 backdrop-blur-md border border-slate-700/50 rounded-xl p-5 hover:border-slate-600 transition-all duration-300 group">
    <div className="flex justify-between items-start">
      <div>
        <p className="text-slate-400 text-sm font-medium">{title}</p>
        <h3 className="text-2xl font-bold mt-1 text-slate-100">{value}</h3>
      </div>
      <div className={cn("p-2 rounded-lg bg-opacity-10", color)}>
        <Icon className={cn("w-6 h-6", color.replace('bg-', 'text-'))} />
      </div>
    </div>
    <div className="mt-4 flex items-center text-xs text-slate-500">
      <Clock className="w-3 h-3 mr-1" />
      <span>Updated just now</span>
    </div>
  </div>
);

const SettingsView = ({ settings, setSettings, onSave }) => {
  const handleSelectDir = async (target) => {
    if (window.electronAPI && window.electronAPI.selectDirectory) {
      const dir = await window.electronAPI.selectDirectory();
      if (dir) setSettings({...settings, [target]: dir});
    } else {
      alert('Selection API not available. Please restart the app.');
    }
  };


  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div className="bg-slate-800/40 border border-slate-700/50 rounded-2xl p-8">
        <h3 className="text-2xl font-bold mb-6">Application Settings</h3>
        
        <div className="space-y-8">
          <section className="space-y-4">
            <h4 className="text-sm font-bold text-primary-light uppercase tracking-wider">Environment</h4>
            <div className="grid grid-cols-2 gap-6">
              <div className="space-y-2">
                <label className="text-sm text-slate-400">Python Executable Path</label>
                <input 
                  type="text" 
                  value={settings.pythonPath} 
                  onChange={(e) => setSettings({...settings, pythonPath: e.target.value})}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-sm outline-none focus:border-primary" 
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm text-slate-400">Default Browser</label>
                <select 
                  value={settings.defaultBrowser}
                  onChange={(e) => setSettings({...settings, defaultBrowser: e.target.value})}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-sm outline-none focus:border-primary"
                >
                  <option>Microsoft Edge</option>
                  <option>Google Chrome</option>
                </select>
              </div>
            </div>
          </section>

          <section className="space-y-4 pt-6 border-t border-slate-800">
            <h4 className="text-sm font-bold text-secondary-light uppercase tracking-wider">Storage</h4>
            <div className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm text-slate-400">Screenshot Directory</label>
                <div className="flex space-x-2">
                  <input 
                    type="text" 
                    readOnly 
                    value={settings.screenshotDir} 
                    className="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-sm text-slate-500" 
                  />
                  <button 
                  onClick={() => handleSelectDir('screenshotDir')}
                  className="bg-slate-700 hover:bg-slate-600 px-4 py-2 rounded-lg text-xs font-medium transition-colors"
                >
                  Change
                </button>
              </div>
            </div>
            <div className="space-y-2">
              <label className="text-sm text-slate-400">Data Output Directory</label>
              <div className="flex space-x-2">
                <input 
                  type="text" 
                  readOnly 
                  value={settings.dataDir} 
                  className="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-sm text-slate-500" 
                />
                <button 
                  onClick={() => handleSelectDir('dataDir')}
                  className="bg-slate-700 hover:bg-slate-600 px-4 py-2 rounded-lg text-xs font-medium transition-colors"
                >
                  Change
                </button>
              </div>
            </div>

              <div className="space-y-2">
                <label className="text-sm text-slate-400">Log Retention (Days)</label>
                <input 
                  type="number" 
                  value={settings.logRetention} 
                  onChange={(e) => setSettings({...settings, logRetention: e.target.value})}
                  className="w-32 bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-sm outline-none focus:border-primary" 
                />
              </div>
            </div>
          </section>

          <div className="pt-6 border-t border-slate-800 flex justify-end">
            <button 
              onClick={onSave}
              className="bg-primary hover:bg-primary-dark text-white px-8 py-2.5 rounded-xl font-bold transition-all shadow-lg shadow-primary/20"
            >
              Save Changes
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

const App = () => {

  const [activeTab, setActiveTab] = useState('dashboard');
  const [logs, setLogs] = useState([]);
  const [isRunning, setIsRunning] = useState(false);
  const logEndRef = useRef(null);

  // Real States
  const [dataFile, setDataFile] = useState(localStorage.getItem('dataFile') || 'Data/LOSData.xlsx');
  const [browser, setBrowser] = useState(localStorage.getItem('browser') || 'Microsoft Edge');
  const [speed, setSpeed] = useState(localStorage.getItem('speed') || 'Standard (Stable)');
  const [stats, setStats] = useState(() => {
    const savedStats = localStorage.getItem('stats');
    return savedStats ? JSON.parse(savedStats) : { totalRuns: 0, successCount: 0, activeModules: 6 };
  });

  const [settings, setSettings] = useState(() => {
    const saved = localStorage.getItem('appSettings');
    return saved ? JSON.parse(saved) : {
      pythonPath: 'python',
      defaultBrowser: 'Microsoft Edge',
      screenshotDir: 'Data/screenshoot',
      dataDir: 'Data/Output',
      logRetention: 30
    }
  });

  useEffect(() => {
    if (window.electronAPI) {
      window.electronAPI.onLog((message) => {
        setLogs(prev => [...prev, { id: Date.now(), msg: message, type: message.includes('ERROR') ? 'error' : 'info' }]);
      });
    }
    return () => {
      if (window.electronAPI) window.electronAPI.removeLogListener();
    };
  }, []);

  useEffect(() => {
    logEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  useEffect(() => {
    localStorage.setItem('dataFile', dataFile);
    localStorage.setItem('browser', browser);
    localStorage.setItem('speed', speed);
    localStorage.setItem('stats', JSON.stringify(stats));
  }, [dataFile, browser, speed, stats]);

  const handleSelectFile = async () => {
    console.log('Browse file clicked');
    if (window.electronAPI && window.electronAPI.selectFile) {
      try {
        const file = await window.electronAPI.selectFile();
        console.log('File selection result:', file);
        if (file) setDataFile(file);
      } catch (err) {
        console.error('File selection error:', err);
        alert('Error opening file dialog: ' + err.message);
      }
    } else {
      console.error('Electron API not found');
      alert('System API not detected. Please make sure the app is running in Electron and try restarting it.');
    }
  };


  const handleSaveSettings = () => {
    localStorage.setItem('appSettings', JSON.stringify(settings));
    alert('Settings saved successfully!');
  };

  const runAutomation = async (script) => {
    if (isRunning) return;
    
    setIsRunning(true);
    setLogs([]);
    setLogs(prev => [...prev, { id: Date.now(), msg: `>>> Starting session: ${script} at ${new Date().toLocaleTimeString()}`, type: 'system' }]);
    
    try {
      const result = await window.electronAPI.runAutomation({ 
        scriptName: script, 
        browserType: browser, 
        dataFile: dataFile,
        speed: speed
      });
      
      setStats(prev => ({
        ...prev,
        totalRuns: prev.totalRuns + 1,
        successCount: result.code === 0 ? prev.successCount + 1 : prev.successCount
      }));

    } catch (err) {
      setLogs(prev => [...prev, { id: Date.now(), msg: `[SYSTEM ERROR] ${err.message}`, type: 'error' }]);
    } finally {
      setIsRunning(false);
    }
  };

  const tabs = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'main-los', label: 'Main LOS', icon: Play, script: 'src.scripts.main_los' },
    { id: 'supplement', label: 'Supplement', icon: PlusSquare, script: 'src.scripts.supplement_los' },
    { id: 'addon', label: 'Add-On', icon: UserPlus, script: 'src.scripts.addon_los' },
    { id: 'cobrand', label: 'Cobrand', icon: CreditCard, script: 'src.scripts.los_cobrand' },
    { id: 'recontest', label: 'Recontest', icon: RotateCcw, script: 'src.scripts.los_recontest' },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  const successRate = stats.totalRuns > 0 ? ((stats.successCount / stats.totalRuns) * 100).toFixed(1) : "0";

  return (
    <div className="flex h-full bg-background text-slate-100 overflow-hidden">
      {/* Sidebar */}
      <aside className="w-64 border-r border-slate-800/80 bg-slate-900/50 backdrop-blur-xl flex flex-col p-4">
        <div className="flex items-center space-x-3 px-2 py-6">
          <div className="w-10 h-10 flex items-center justify-center">
            <img src={briLogo} alt="BRI Logo" className="w-full h-auto object-contain" />
          </div>
          <h1 className="text-lg font-bold tracking-tight bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">
            LOS Auto Suite
          </h1>
        </div>


        <nav className="flex-1 space-y-1 mt-4">
          {tabs.map(tab => (
            <SidebarItem 
              key={tab.id} 
              icon={tab.icon} 
              label={tab.label} 
              active={activeTab === tab.id}
              onClick={() => setActiveTab(tab.id)}
            />
          ))}
        </nav>

        <div className="mt-auto p-2 border-t border-slate-800/50 pt-4 flex justify-center text-xs text-slate-600 font-mono tracking-widest">
          VERSION 1.0.0
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col relative overflow-hidden">
        {/* Header */}
        <header className="h-16 border-b border-slate-800/50 flex items-center justify-between px-8 bg-slate-900/30 backdrop-blur-sm z-10 drag">
          <motion.h2 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            key={activeTab}
            className="text-xl font-semibold capitalize"
          >
            {activeTab.replace('-', ' ')}
          </motion.h2>
          <div className="flex items-center space-x-4 no-drag">

            <div className="flex items-center bg-slate-800/50 rounded-full px-3 py-1 border border-slate-700/50">
              <div className={cn("w-2 h-2 rounded-full mr-2", isRunning ? "bg-amber-500 animate-pulse" : "bg-emerald-500")} />
              <span className="text-xs font-medium">{isRunning ? "Process Running" : "System Ready"}</span>
            </div>
            <button className="p-2 hover:bg-slate-800 rounded-lg text-slate-400"><Monitor className="w-5 h-5" /></button>
          </div>
        </header>

        {/* Scrollable Area */}
        <div className="flex-1 overflow-y-auto p-8 space-y-8 no-drag">
          <AnimatePresence mode="wait">
            {activeTab === 'dashboard' ? (
              <motion.div 
                key="dashboard"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.3 }}
                className="grid grid-cols-3 gap-6"
              >
                <Card title="Total Runs" value={stats.totalRuns} icon={Play} color="bg-primary" />
                <Card title="Success Rate" value={`${successRate}%`} icon={CheckCircle2} color="bg-emerald-500" />
                <Card title="Active Modules" value={stats.activeModules} icon={FileSearch} color="bg-secondary" />
                
                <motion.div 
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.2 }}
                  className="col-span-3 bg-slate-800/20 border border-slate-800 rounded-2xl p-6"
                >

                <h4 className="text-lg font-semibold mb-4">Quick Start</h4>
                <div className="grid grid-cols-2 gap-4">
                  <button onClick={() => runAutomation('src.scripts.main_los')} className="flex items-center justify-between p-4 bg-primary/10 hover:bg-primary/20 border border-primary/20 rounded-xl transition-all group">
                    <div className="flex items-center space-x-4">
                      <div className="p-3 bg-primary/20 rounded-lg text-primary-light group-hover:scale-110 transition-transform">
                        <Play className="w-5 h-5" />
                      </div>
                      <div className="text-left">
                        <p className="font-semibold">Execute Main LOS</p>
                        <p className="text-xs text-slate-400">Run full origination automation</p>
                      </div>
                    </div>
                    <ChevronRight className="w-5 h-5 text-slate-500 group-hover:translate-x-1 transition-transform" />
                  </button>
                  <button onClick={() => setActiveTab('recontest')} className="flex items-center justify-between p-4 bg-secondary/10 hover:bg-secondary/20 border border-secondary/20 rounded-xl transition-all group">
                    <div className="flex items-center space-x-4">
                      <div className="p-3 bg-secondary/20 rounded-lg text-secondary-light group-hover:scale-110 transition-transform">
                        <RotateCcw className="w-5 h-5" />
                      </div>
                      <div className="text-left">
                        <p className="font-semibold">Recontest View</p>
                        <p className="text-xs text-slate-400">Handle recent recontest tasks</p>
                      </div>
                    </div>
                    <ChevronRight className="w-5 h-5 text-slate-500 group-hover:translate-x-1 transition-transform" />
                  </button>
                </div>
              </motion.div>
            </motion.div>
          ) : activeTab === 'settings' ? (
            <motion.div
              key="settings"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
            >
              <SettingsView 
                settings={settings} 
                setSettings={setSettings} 
                onSave={handleSaveSettings} 
              />
            </motion.div>
          ) : (
            <motion.div 
              key="automation-config"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
              className="max-w-4xl mx-auto space-y-6"
            >

              <div className="bg-slate-800/40 border border-slate-700/50 rounded-2xl p-8">
                <div className="flex items-start justify-between mb-8">
                  <div>
                    <h3 className="text-2xl font-bold">Configure Automation</h3>
                    <p className="text-slate-400 mt-1">Set up parameters for {activeTab.replace('-', ' ')} execution.</p>
                  </div>
                  <div className="p-3 bg-slate-700/50 rounded-xl">
                    {React.createElement(tabs.find(t => t.id === activeTab)?.icon || FileText, { className: "w-8 h-8 text-primary-light" })}
                  </div>
                </div>

                <div className="space-y-6">
                  <div className="grid grid-cols-2 gap-6">
                    <div className="space-y-2">
                      <label className="text-sm font-medium text-slate-300">Browser Environment</label>
                      <select 
                        value={browser}
                        onChange={(e) => setBrowser(e.target.value)}
                        className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2.5 outline-none focus:border-primary transition-colors"
                      >
                        <option>Microsoft Edge</option>
                        <option>Google Chrome</option>
                      </select>
                    </div>
                    <div className="space-y-2">
                      <label className="text-sm font-medium text-slate-300">Execution Speed</label>
                      <select 
                        value={speed}
                        onChange={(e) => setSpeed(e.target.value)}
                        className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2.5 outline-none focus:border-primary transition-colors"
                      >
                        <option>Standard (Stable)</option>
                        <option>Fast (Experimental)</option>
                      </select>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <label className="text-sm font-medium text-slate-300">Data Source (Excel)</label>
                    <div className="flex space-x-2">
                      <input 
                        type="text" 
                        readOnly 
                        value={dataFile}
                        className="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-4 py-2.5 text-slate-400 text-sm outline-none"
                      />
                      <button 
                        onClick={handleSelectFile}
                        className="bg-slate-700 hover:bg-slate-600 px-4 rounded-lg text-sm font-medium transition-colors"
                      >
                        Browse
                      </button>
                    </div>
                  </div>

                  <div className="pt-6 border-t border-slate-800 flex items-center justify-between">
                    <div className="flex items-center text-slate-400 text-sm italic">
                      <AlertCircle className="w-4 h-4 mr-2" />
                      Ensure Excel file is not locked by another process
                    </div>
                    <button 
                      onClick={() => tabs.find(t => t.id === activeTab)?.script && runAutomation(tabs.find(t => t.id === activeTab).script)}
                      disabled={isRunning}
                      className={cn(
                        "flex items-center px-8 py-3 rounded-xl font-bold transition-all shadow-lg",
                        isRunning 
                          ? "bg-slate-700 text-slate-500 cursor-not-allowed" 
                          : "bg-gradient-to-r from-primary to-primary-dark text-white hover:shadow-primary/20 hover:-translate-y-0.5 active:translate-y-0"
                      )}
                    >
                      {isRunning ? "Running..." : "Start Automation"}
                      {!isRunning && <Play className="w-4 h-4 ml-2 fill-current" />}
                    </button>
                  </div>
                </div>
              </div>
            </motion.div>
          )}
          </AnimatePresence>
        </div>


        {/* Terminal Area */}
        <div className="h-48 border-t border-slate-800 bg-slate-950/80 backdrop-blur-md flex flex-col">
          <div className="flex items-center justify-between px-4 py-2 bg-slate-900/50 border-b border-slate-800/50">
            <div className="flex items-center text-xs font-mono text-slate-400 uppercase tracking-widest">
              <Terminal className="w-3 h-3 mr-2" />
              Live Process Console
            </div>
            <button onClick={() => setLogs([])} className="text-xs text-slate-500 hover:text-slate-300 transition-colors">Clear</button>
          </div>
          <div className="flex-1 p-4 font-mono text-sm overflow-y-auto scrollbar-thin">
            {logs.length === 0 ? (
              <p className="text-slate-600 italic">No process logs to display. Start an automation to see output.</p>
            ) : (
              logs.map((log) => (
                <div key={log.id} className={cn(
                  "mb-1 leading-relaxed break-all",
                  log.type === 'error' ? "text-rose-400" : 
                  log.type === 'system' ? "text-primary-light font-bold" : 
                  "text-slate-300"
                )}>
                  <span className="text-slate-600 mr-2">[{new Date(log.id).toLocaleTimeString()}]</span>
                  {log.msg}
                </div>
              ))
            )}
            <div ref={logEndRef} />
          </div>
        </div>
      </main>

      {/* Decorative Gradients */}
      <div className="fixed top-0 left-1/4 w-96 h-96 bg-primary/10 rounded-full blur-[120px] -z-10 pointer-events-none" />
      <div className="fixed bottom-0 right-1/4 w-96 h-96 bg-secondary/10 rounded-full blur-[120px] -z-10 pointer-events-none" />
    </div>
  );
};

export default App;
