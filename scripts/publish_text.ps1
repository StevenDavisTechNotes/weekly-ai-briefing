# usage: .\scripts\publish_text.ps1

$ErrorActionPreference = "Stop"

function Invoke-CheckedCommand {
    param(
        [scriptblock]$Command,
        [string]$Description
    )

    & $Command
    if ($LASTEXITCODE -ne 0) {
        throw "$Description failed with exit code $LASTEXITCODE."
    }
}

Push-Location (Split-Path -Parent $PSScriptRoot)
try {
    $date = Get-Date -Format "yyyy-MM-dd"

    Invoke-CheckedCommand { uv run python -m weekly_ai_briefing.email_briefing --voice } "Voice generation"
    Invoke-CheckedCommand { uv run python -m weekly_ai_briefing.publish } "Publishing"
    Invoke-CheckedCommand { git add index.html editions/html_format } "git add"
    Invoke-CheckedCommand { git commit -m "Publish $date edition" } "git commit"
    Invoke-CheckedCommand { git push } "git push"

    $pageUrl = Invoke-CheckedCommand {
        uv run python -c "from weekly_ai_briefing.config import MARKDOWN_FOLDER; from weekly_ai_briefing.email_briefing.briefing import edition_page_url, find_latest_briefing; briefing, _ = find_latest_briefing(MARKDOWN_FOLDER); print(edition_page_url(briefing.stem))"
    } "Getting the edition page URL"

    Write-Host "Waiting for GitHub Pages to publish $pageUrl (up to 10 minutes)..."
    $deadline = (Get-Date).AddMinutes(2)
    $pageIsLive = $false
    while ((Get-Date) -lt $deadline) {
        try {
            $response = Invoke-WebRequest -Uri $pageUrl -Method Head -TimeoutSec 15
            if ($response.StatusCode -eq 200) {
                $pageIsLive = $true
                break
            }
        }
        catch {
            Write-Host "The page is not live yet; checking again in 15 seconds."
        }

        Start-Sleep -Seconds 15
    }

    if (-not $pageIsLive) {
        throw "Timed out waiting for $pageUrl. Once GitHub Pages is live, send the email with: uv run python -m weekly_ai_briefing.email_briefing --email"
    }

    Invoke-CheckedCommand { uv run python -m weekly_ai_briefing.email_briefing --email } "Email delivery"
}
finally {
    Pop-Location
}
