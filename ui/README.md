# Edge AI Camera UI - Getting Started (For Non-Developers)

This guide will help you run the Camera UI app, even if you have never used Node.js, Electron, or command-line tools before. Just follow each step carefully.

## 1. Install Node.js (with NVM)

Node.js is required to run this app. The easiest way to install it is with NVM (Node Version Manager).

### a. Open your Terminal
- On Linux, press `Ctrl+Alt+T` or search for "Terminal" in your applications menu.

### b. Install NVM
Copy and paste this command into your terminal, then press Enter:

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
```

After it finishes, activate NVM:

```bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
```

### c. Install Node.js (LTS version)

```bash
nvm install --lts
nvm use --lts
```

## 2. Install App Dependencies

In your terminal, go to the app folder (replace the path if your folder is different):

```bash
cd /home/fenix/projects/llm-edge/ui
```

Install the required packages:

```bash
npm install
```

## 3. Run the App

Start the app with this command:

```bash
npm start
```

The Camera UI will open in a new window. If you see a security prompt, allow camera access.

## 4. Troubleshooting
- If you see errors about Node or npm not found, repeat the NVM and Node.js steps above.
- If the app window does not appear, check your terminal for error messages and share them with your support contact.

---

**You do not need to write any code or change any files. Just follow the steps above!**
