param(
  [string]$RepoName = "rahul_bedrock",
  [ValidateSet("public","private")][string]$Visibility = "public"
)

Write-Host "Checking for Git and GitHub CLI (gh)..."
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  Write-Host "ERROR: Git not found. Install Git from https://git-scm.com/downloads and re-run this script." -ForegroundColor Red
  exit 1
}

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
  Write-Host "GitHub CLI (gh) not found. Please install from https://cli.github.com/ and ensure 'gh' is in PATH." -ForegroundColor Yellow
  Write-Host "You can try: winget install --id GitHub.cli -e --accept-package-agreements (requires admin)."
  exit 1
}

# Ensure README and .gitignore exist
if (-not (Test-Path README.md)) {
  @"
# rahul_bedrock

AWS Bedrock project — contains scripts to check AWS credentials and example Bedrock calls.

How to use:
1. Activate the venv: `.\exercise1\Scripts\Activate.ps1` or run directly using the venv python: `& C:\Users\<you>\Desktop\exercise1\Scripts\python.exe check_credentials.py`
2. Run `python check_credentials.py` to verify credentials.

"@ | Out-File -Encoding utf8 README.md
  git add README.md
}

if (-not (Test-Path .gitignore)) {
  @"
# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
*.log

# Virtual environments
exercise1/
venv/
.env/
.venv/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Archives
*.zip
"@ | Out-File -Encoding utf8 .gitignore
  git add .gitignore
}

Write-Host "Initializing git repository (if not present) and committing files..."
if (-not (Test-Path .git)) {
  git init
  git add .
  git commit -m "Initial commit"
} else {
  git add .
  git commit -m "Add/Update project files" 2>$null
}

Write-Host "Checking GitHub CLI authentication..."
$auth = gh auth status 2>&1
if ($LASTEXITCODE -ne 0) {
  Write-Host "You will be prompted to authenticate with GitHub (browser will open)." -ForegroundColor Green
  gh auth login
} else {
  Write-Host "Authenticated with GitHub." -ForegroundColor Green
}

Write-Host "Creating GitHub repo '$RepoName' (visibility: $Visibility) and pushing..."
# Create repo under authenticated user or org and push
gh repo create $RepoName --$Visibility --source=. --push --confirm

Write-Host "Done. Opening repo in browser..."
gh repo view --web

Write-Host "If the repo already exists remotely, you can add it as a remote and push manually:"
Write-Host "  git remote add origin https://github.com/<your-username>/$RepoName.git"
Write-Host "  git branch -M main"
Write-Host "  git push -u origin main"
