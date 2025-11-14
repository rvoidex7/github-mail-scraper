# Set PYTHONPATH to include the 'src' directory
$env:PYTHONPATH = "D:\projects\Ru1vly\github-mail-scraper\src"

# Check if .env file exists
if (Test-Path ".env") {
  # Read the entire content of .env file as GITHUB_TOKEN
  $GITHUB_TOKEN = Get-Content -Raw -Path ".env"
} else {
  Write-Host "Error: .env file not found."
  Write-Host "Please create a .env file and add your GitHub token as its sole content."
  exit 1
}

# Check if GITHUB_TOKEN is set (it should be if .env exists and has content)
if ([string]::IsNullOrEmpty($GITHUB_TOKEN)) {
  Write-Host "Error: GITHUB_TOKEN is empty. Please ensure your .env file contains your GitHub token."
  exit 1
}

Write-Host "Starting continuous scraping..."

while ($true) {
  # Execute the Python scraper directly
  # Assuming python is in PATH and the scraper.cli module is accessible
  python -m scraper.cli auto-fetch --count 100 --token "$GITHUB_TOKEN"
  Write-Host "Sleeping for 10 seconds before next run..."
  Start-Sleep -Seconds 10
}
