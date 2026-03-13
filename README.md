# LOS Auto Suite (StatementGuard) 🛡️

A modern, high-performance automation suite for Statement & LOS processing. Reimagined with a premium desktop experience using **Electron**, **React**, and **Tailwind CSS**.

## ✨ Features

- **Modern UI/UX**: Dark-themed, glassmorphism-based design with smooth animations.
- **Real-time Console**: Stream logs directly from Python automation scripts.
- **Local Persistence**: Each user has their own statistics and configuration saved locally.
- **Automated Workflows**:
  - Main LOS Automation
  - Supplement & Add-On Processing
  - Cobrand & Recontest Modules
- **Flexible Storage**: Separate directories for screenshots and data outputs.
- **Premium Branding**: Custom BRI assets and localized styling.

## 🚀 One-Line Installation

Open PowerShell as Administrator and run:

```powershell
irm https://raw.githubusercontent.com/ridhanshr/StatementGuard/main/install.ps1 | iex
```

## 🛠️ Tech Stack

- **Frontend**: React 19, Vite, Tailwind CSS, Framer Motion, Lucide Icons.
- **Backend**: Electron (Desktop Wrapper), Node.js.
- **Automation Logic**: Python 3 (Integrated via IPC Bridge).
- **Packaging**: Electron Builder (NSIS Installer).

## 📂 Project Structure

- `gui_modern/`: React frontend and Electron main configuration.
- `src/`: Core Python automation logic and utilities.
- `Data/`: Default storage for Excel logs, screenshots, and configurations (configurable in-app).
- `old_version/`: Legacy Tkinter version and build assets.

## ⚙️ Development

If you want to contribute or build from source:

1. Clone the repository.
2. Install Python dependencies: `pip install -r requirements.txt`.
3. Navigate to `gui_modern/`.
4. Install Node dependencies: `npm install`.
5. Run in dev mode: `npm run dev`.
6. Build installer: `npm run dist`.

## 📄 License

Proprietary - Bank Rakyat Indonesia (BRI) Automation Tooling.
