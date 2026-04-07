# GitHub Pages Deployment Guide

This guide explains how to deploy the AML Library Web application to GitHub Pages.

## Prerequisites

- A GitHub repository
- GitHub Actions enabled (enabled by default)
- Push access to the repository

## Deployment Options

### Option 1: Automatic Deployment (Recommended)

The repository includes a GitHub Actions workflow (`.github/workflows/deploy.yml`) that automatically builds and deploys your site when you push changes to the `main` branch.

#### Steps:

1. **Enable GitHub Pages in your repository:**
   - Go to your repository on GitHub
   - Click **Settings** → **Pages**
   - Under **Source**, select **GitHub Actions**
   - Save the changes

2. **Configure the base path:**
   - Open `AML_Library_Web/vite.config.js`
   - Update the `base` path based on your repository name:
     - If your repo is `username/repo-name`, the base should be `/repo-name/`
     - If deploying to a custom domain, use `/`
   - Example: If your repo is `myusername/aml-library`, change base to `/aml-library/`

3. **Push your code:**
   ```bash
   git add .
   git commit -m "Setup GitHub Pages deployment"
   git push origin main
   ```

4. **Monitor deployment:**
   - Go to **Actions** tab in your GitHub repository
   - Watch the workflow run
   - Once complete, your site will be available at:
     `https://username.github.io/repo-name/`

### Option 2: Manual Deployment

If you prefer to deploy manually:

1. **Build the project:**
   ```bash
   cd AML_Library_Web
   npm install
   npm run build
   ```

2. **Update base path in vite.config.js:**
   - Set `base: '/your-repo-name/'` (replace with your actual repo name)

3. **Rebuild:**
   ```bash
   npm run build
   ```

4. **Deploy the `dist` folder:**
   - Use GitHub Desktop, or
   - Use the `gh-pages` package (see below)

#### Using gh-pages package:

1. **Install gh-pages:**
   ```bash
   cd AML_Library_Web
   npm install --save-dev gh-pages
   ```

2. **Add deploy script to package.json:**
   ```json
   "scripts": {
     "deploy": "npm run build && gh-pages -d dist"
   }
   ```

3. **Deploy:**
   ```bash
   npm run deploy
   ```

## Configuring Base Path

The base path depends on your GitHub Pages URL structure:

- **Repository Pages** (username.github.io/repo-name): Use `/repo-name/`
- **User/Organization Pages** (username.github.io): Use `/`
- **Custom Domain**: Use `/`

Update `vite.config.js`:
```javascript
base: '/your-repo-name/',  // Replace with your actual repo name
```

## Troubleshooting

### 404 Errors on Routes

If you see 404 errors when navigating to routes:
- Ensure the `base` path in `vite.config.js` matches your repository name
- Check that React Router is configured correctly

### Assets Not Loading

- Verify the `base` path is correct
- Clear browser cache
- Check browser console for 404 errors on specific assets

### Build Fails

- Check GitHub Actions logs in the **Actions** tab
- Ensure all dependencies are listed in `package.json`
- Verify Node.js version compatibility

## Custom Domain

To use a custom domain:

1. Add a `CNAME` file to `AML_Library_Web/public/` with your domain:
   ```
   yourdomain.com
   ```

2. Update DNS settings as per GitHub Pages documentation

3. Set `base: '/'` in `vite.config.js`

## Local Testing

Test the production build locally:

```bash
cd AML_Library_Web
npm run build
npm run preview
```

This will serve the built files locally so you can verify everything works before deploying.
