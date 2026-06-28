# CodeM

**Research-to-GitHub Compiler — Materialize projects into proof.**

CodeM is a lightweight desktop application for organizing project documentation, parts lists, images, revisions, exports, and GitHub publishing in one workflow.

It is designed for research, engineering builds, UAV projects, electronics repair, academic work, and documentation-heavy prototypes.

---

## Stable Release

```text
CodeM Desktop v1.29.5
```

This is the firm desktop baseline for Windows EXE packaging.

Recommended version strategy:

```text
v1.29.5 = stable desktop EXE baseline
v1.30.x = future desktop modular refactor
v2.0.x  = future Streamlit web version
```

---

## Main Purpose

CodeM helps convert project work into organized proof:

```text
project idea → documentation → parts list → evidence images → README → GitHub
```

Instead of scattering notes across folders, screenshots, CSV files, and Git commands, CodeM provides a single workflow for building a clean project record.

---

## Features

- Project creation and loading
- Structured project objective template
- Documentation editor
- Save Revision system
- Parts list / bill of materials editor
- Image attachment support
- GitHub-ready README compiler
- Export support
- GitHub sync tools
- Git recovery tools
- Commit message sanitization
- Image upload size protection
- Responsive documentation toolbar
- Minimal local desktop workflow

---

## Recommended Project Structure

CodeM creates and manages project folders using a structure similar to:

```text
project/
├── README.md
├── project.json
├── docs/
│   ├── overview.md
│   ├── build_notes.md
│   ├── testing.md
│   ├── results.md
│   ├── future_work.md
│   └── revisions/
├── images/
├── parts/
│   └── parts.csv
├── tests/
├── logs/
├── references/
└── exports/
```

---

## Documentation Philosophy

CodeM follows this documentation rule:

```text
README.md = clean public landing page
docs/     = detailed working documentation
parts/    = structured bill of materials
images/   = evidence and visual references
```

The README should be easy to read on GitHub. Detailed notes should stay inside the `docs/` folder.

---

## Desktop Version

The current stable desktop version is:

```text
codem_v1_29_5_main.py
```

This version is intended to be packaged as:

```text
CodeM_v1_29_5.exe
```

---

## EXE Packaging

Use the included packaging documents and scripts:

```text
build_codem_v1_29_5_exe.bat
build_codem_v1_29_5_exe.ps1
EXE_PACKAGING_GUIDE.md
RELEASE_CHECKLIST.md
GITHUB_RELEASE_GUIDE.md
TROUBLESHOOTING.md
```

Basic build command:

```bat
build_codem_v1_29_5_exe.bat
```

Expected output:

```text
dist\CodeM_v1_29_5.exe
```

Recommended PyInstaller command:

```bat
pyinstaller ^
  --noconfirm ^
  --clean ^
  --onefile ^
  --windowed ^
  --icon codem_icon.ico ^
  --name CodeM_v1_29_5 ^
  codem_v1_29_5_main.py
```

---

## Installation for Development

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bat
.venv\Scripts\activate
```

Install packaging dependency:

```bash
pip install pyinstaller
```

Run the source file:

```bash
python codem_v1_29_5_main.py
```

---

## GitHub Release Practice

Use the GitHub repository for:

- source code
- documentation
- packaging guide
- changelog
- security notes

Use **GitHub Releases** for:

- compiled `.exe`
- source ZIP
- release notes
- checksum

Avoid committing these directly to the main repository:

```text
.venv/
build/
dist/
*.spec
```

---

## Recommended Git Commands

Initial upload:

```bash
git init
git branch -M main
git add .
git commit -m "Initial CodeM v1.29.5 release"
git remote add origin https://github.com/YOUR_USERNAME/codem.git
git push -u origin main
```

Create release tag:

```bash
git tag v1.29.5
git push origin v1.29.5
```

---

## Security Notes

CodeM should not store:

- GitHub passwords
- GitHub personal access tokens
- API keys
- SSH private keys
- private student records
- internal credentials

Git authentication should be handled by:

- Git Credential Manager
- SSH key
- GitHub CLI
- system Git configuration

Before pushing a project, review all files for sensitive information.

---

## Storage Guidance

GitHub is good for:

- README files
- documentation
- source code
- CSV parts lists
- compressed images
- small logs
- configuration notes

Avoid using GitHub as a dump drive for:

- raw drone videos
- large datasets
- large ZIP backups
- uncompressed photo collections
- private records

Recommended project repository target size:

```text
Ideal: below 500 MB
Soft limit: below 1 GB
Avoid: above 5 GB
```

---

## Future Direction

The desktop version remains stable at:

```text
CodeM Desktop v1.29.5
```

Planned future direction:

```text
CodeM Web v2.0.x
```

The web version is intended to use:

```text
Streamlit UI
GitHub as central project storage
local temporary clone
Git pull / commit / push workflow
```

---

## Included Documentation

Recommended repository documentation:

```text
README.md
FAQ.md
WORKFLOW.md
BEST_PRACTICES.md
SECURITY.md
CHANGELOG.md
EXE_PACKAGING_GUIDE.md
RELEASE_CHECKLIST.md
GITHUB_RELEASE_GUIDE.md
TROUBLESHOOTING.md
```

---

## Release Notes

### v1.29.5

Firm desktop baseline release.

Highlights:

- project workflow
- documentation editor
- parts list with image upload
- README generation
- GitHub sync/recovery
- revision saving
- responsive Docs toolbar
- commit message sanitization
- image upload size protection

---

## License

Choose a license before public release.

Recommended:

```text
MIT License
```

MIT is simple, permissive, and common for open-source desktop tools.

---

## Status

```text
Stable desktop baseline: v1.29.5
Next major branch: v2.0.0 Streamlit web prototype
```
