# Raadi Marketplace Release v19 Creation Script (PowerShell)
# This script creates a GitHub release for version v19

$REPO_OWNER = "Jibsta91"
$REPO_NAME = "raadi-marketplace" 
$TAG_NAME = "v19"
$RELEASE_NAME = "Release v19"
$COMMIT_SHA = "5a00d8604d0c6576db140f6b7ec65ee0d9068d2a"

Write-Host "Creating GitHub Release v19 for Raadi Marketplace..." -ForegroundColor Green
Write-Host "Repository: $REPO_OWNER/$REPO_NAME" -ForegroundColor Cyan
Write-Host "Tag: $TAG_NAME" -ForegroundColor Cyan  
Write-Host "Commit: $COMMIT_SHA" -ForegroundColor Cyan
Write-Host ""

# Check if GitHub CLI is available
try {
    $ghPath = Get-Command gh -ErrorAction Stop
    Write-Host "GitHub CLI found! Attempting to create release..." -ForegroundColor Yellow
    
    $releaseBody = @"
## Raadi Marketplace Release v19

**Changes in this release:**
Add release workflow for automated GitHub releases

### 🚀 New Features & Improvements
- Added comprehensive release workflow with proper permissions
- Includes automated Docker build and ECR push
- Supports both tag-triggered and manual releases
- Integrated with AWS ECS deployment
- Enhanced release notes with technical details

### 🐳 Docker Images
- 675080425974.dkr.ecr.us-east-1.amazonaws.com/raadi-marketplace:main
- 675080425974.dkr.ecr.us-east-1.amazonaws.com/raadi-marketplace:latest
- 675080425974.dkr.ecr.us-east-1.amazonaws.com/raadi-marketplace:main-5a00d86

### 📋 Technical Details
- **Commit:** 5a00d8604d0c6576db140f6b7ec65ee0d9068d2a
- **AWS Region:** us-east-1
- **ECS Cluster:** raadi-marketplace-cluster
- **ECS Service:** raadi-marketplace-service
- **Python Version:** 3.11

### 🌟 DevOps Enhancements
- **Automated Releases:** GitHub Actions workflow for seamless releases
- **Permission Management:** Proper workflow permissions configuration
- **Docker Integration:** Automated ECR push and ECS deployment
- **Release Automation:** Support for both manual and tag-triggered releases

**Full Changelog:** https://github.com/$REPO_OWNER/$REPO_NAME/compare/v18...v19
"@

    # Create the release using GitHub CLI
    $repoFullName = "$REPO_OWNER/$REPO_NAME"
    & gh release create $TAG_NAME --title $RELEASE_NAME --notes $releaseBody --target main --repo $repoFullName
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Release created successfully!" -ForegroundColor Green
        Write-Host "🔗 View release: https://github.com/$REPO_OWNER/$REPO_NAME/releases/tag/$TAG_NAME" -ForegroundColor Blue
    } else {
        Write-Host "❌ Failed to create release with GitHub CLI" -ForegroundColor Red
    }
}
catch {
    Write-Host "GitHub CLI not found or error occurred." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To create the release manually:" -ForegroundColor Cyan
    Write-Host "1. Go to: https://github.com/$REPO_OWNER/$REPO_NAME/releases/new" -ForegroundColor White
    Write-Host "2. Choose tag: $TAG_NAME" -ForegroundColor White  
    Write-Host "3. Release title: $RELEASE_NAME" -ForegroundColor White
    Write-Host "4. Copy the release notes and Docker image info below" -ForegroundColor White
    Write-Host ""
    Write-Host "Or install GitHub CLI: https://cli.github.com/" -ForegroundColor Blue
}

Write-Host ""
Write-Host "Release Information:" -ForegroundColor Green
Write-Host "===================" -ForegroundColor Green
Write-Host "Tag: $TAG_NAME" -ForegroundColor White
Write-Host "Title: $RELEASE_NAME" -ForegroundColor White
Write-Host "Commit: $COMMIT_SHA" -ForegroundColor White
Write-Host ""
Write-Host "Docker Images:" -ForegroundColor White
Write-Host "- 675080425974.dkr.ecr.us-east-1.amazonaws.com/raadi-marketplace:main" -ForegroundColor Gray
Write-Host "- 675080425974.dkr.ecr.us-east-1.amazonaws.com/raadi-marketplace:latest" -ForegroundColor Gray  
Write-Host "- 675080425974.dkr.ecr.us-east-1.amazonaws.com/raadi-marketplace:main-5a00d86" -ForegroundColor Gray
Write-Host ""
Write-Host "Manual Options:" -ForegroundColor Green
Write-Host "1. GitHub Web: https://github.com/$REPO_OWNER/$REPO_NAME/releases/new" -ForegroundColor Blue
Write-Host "2. GitHub Actions: https://github.com/$REPO_OWNER/$REPO_NAME/actions/workflows/release.yml" -ForegroundColor Blue
