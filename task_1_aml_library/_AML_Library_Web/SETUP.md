# Setup Instructions

## Quick Start

### 1. Install Dependencies
```bash
cd AML_Library_Web
npm install
```

### 2. Copy Markdown Files
Copy all markdown files from the **parent directory** (task_1_aml_library, i.e. the folder that contains this AML_Library_Web folder) to `public/AML_Library/` (excluding `TASK_RELATIONSHIPS.md`):

**Files to copy:**
- README.md
- 00_COMPREHENSIVE_RED_FLAGS_MASTER.md
- 01_Professional_Money_Laundering_Trade_MSB.md
- 02_Bulk_Cash_Smuggling_Mexico_TCOs.md
- 03_Oil_Smuggling_Mexico_Cartels.md
- 04_Chinese_ML_Networks_Mexico_TCOs.md
- 05_Synthetic_Opioids_Proceeds.md
- 06_Underground_Banking_Schemes.md
- 07_Human_Trafficking_Proceeds.md
- 08_General_ML_TF_Indicators.md
- Red_Flag_to_Feature_Mapping.md
- SOURCES.md

**PowerShell command (run from AML_Library_Web):**
```powershell
Copy-Item "..\*.md" -Destination "public\AML_Library\" -Exclude "TASK_RELATIONSHIPS.md"
```

### 3. Run Development Server
```bash
npm run dev
```

The app will be available at `http://localhost:5173`

## Project Status

✅ Project structure created
✅ All React components created
✅ Routing configured
✅ Tailwind CSS configured
✅ Package.json with all dependencies

⏳ **Remaining:**
- Install dependencies (`npm install`)
- Copy markdown files to `public/AML_Library/`
- Test the application

## Build for Production

```bash
npm run build
```

Output will be in the `dist/` directory.

## Deploy to GitHub Pages

1. Install gh-pages:
```bash
npm install --save-dev gh-pages
```

2. Add to package.json scripts:
```json
"deploy": "npm run build && gh-pages -d dist"
```

3. Deploy:
```bash
npm run deploy
```
