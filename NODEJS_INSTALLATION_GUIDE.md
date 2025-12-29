# Node.js Installation Guide for IMIS Frontend

## Why You Need Node.js

Your IMIS frontend is built with SvelteKit, which requires Node.js to build the production files. Without Node.js, you can't create the optimized build files needed for deployment.

## Quick Installation (Recommended)

### Option 1: Download from Official Website
1. Go to https://nodejs.org/
2. Download the **LTS version** (Long Term Support)
3. Run the installer with default settings
4. Restart your command prompt/terminal

### Option 2: Using Chocolatey (Windows Package Manager)
```cmd
# Install Chocolatey first (if not installed)
# Run as Administrator
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install Node.js
choco install nodejs
```

### Option 3: Using Winget (Windows 11)
```cmd
winget install OpenJS.NodeJS
```

## Verify Installation

After installation, open a new command prompt and run:
```cmd
node --version
npm --version
```

You should see version numbers for both commands.

## Build Your Frontend

Once Node.js is installed:

1. Navigate to your frontend folder:
   ```cmd
   cd f:\IMIS\frontend
   ```

2. Install dependencies:
   ```cmd
   npm install
   ```

3. Build for production:
   ```cmd
   npm run build
   ```

4. Run the deployment script again:
   ```cmd
   cd ..
   DEPLOY_TO_CPANEL_FIXED.bat
   ```

## Alternative: Use Pre-built Version

If you can't install Node.js right now, you can:

1. Use the source files (already copied by the script)
2. Deploy to Cloudflare Pages (which will build for you)
3. Ask someone with Node.js to build it for you

## Cloudflare Pages Deployment (No Node.js Required Locally)

1. Push your code to GitHub
2. Connect GitHub to Cloudflare Pages
3. Set build settings:
   - Build command: `npm run build`
   - Output directory: `build`
   - Root directory: `frontend`
4. Deploy automatically

## Next Steps

After installing Node.js:
1. Run `DEPLOY_TO_CPANEL_FIXED.bat`
2. Upload the generated files to cPanel
3. Follow the deployment instructions

## Troubleshooting

**"npm is not recognized"**: 
- Restart your command prompt
- Check if Node.js was installed correctly
- Add Node.js to your PATH manually if needed

**Build errors**:
- Delete `node_modules` folder
- Run `npm install` again
- Check for any missing dependencies