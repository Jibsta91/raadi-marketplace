#!/bin/bash

# Raadi Marketplace Release v19 Creation Script
# This script creates a GitHub release for version v19

REPO_OWNER="Jibsta91"
REPO_NAME="raadi-marketplace"
TAG_NAME="v19"
RELEASE_NAME="Release v19"
COMMIT_SHA="5a00d8604d0c6576db140f6b7ec65ee0d9068d2a"

# Release body with comprehensive details
RELEASE_BODY=$(cat << 'EOF'
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
```
675080425974.dkr.ecr.us-east-1.amazonaws.com/raadi-marketplace:main
675080425974.dkr.ecr.us-east-1.amazonaws.com/raadi-marketplace:latest
675080425974.dkr.ecr.us-east-1.amazonaws.com/raadi-marketplace:main-5a00d86
```

### 📋 Technical Details
- **Commit:** 5a00d8604d0c6576db140f6b7ec65ee0d9068d2a
- **AWS Region:** us-east-1
- **ECS Cluster:** raadi-marketplace-cluster
- **ECS Service:** raadi-marketplace-service
- **Python Version:** 3.11

### 🏗️ Infrastructure
- Complete AWS ECS Fargate deployment
- Terraform-managed infrastructure
- Docker containerized application
- CI/CD pipeline with GitHub Actions

### 🔧 Services
- FastAPI web application
- PostgreSQL database
- Redis cache
- Elasticsearch search
- AI services (governance, cybersecurity, infrastructure, data management)
- Nginx reverse proxy

### 🌟 DevOps Enhancements
- **Automated Releases:** GitHub Actions workflow for seamless releases
- **Permission Management:** Proper workflow permissions configuration
- **Docker Integration:** Automated ECR push and ECS deployment
- **Release Automation:** Support for both manual and tag-triggered releases
- **Enhanced Documentation:** Comprehensive release notes with technical details

**Full Changelog:** https://github.com/Jibsta91/raadi-marketplace/compare/v18...v19
EOF
)

echo "Creating GitHub Release v19 for Raadi Marketplace..."
echo "Repository: $REPO_OWNER/$REPO_NAME"
echo "Tag: $TAG_NAME"
echo "Commit: $COMMIT_SHA"
echo ""

# If GitHub CLI is available, use it
if command -v gh &> /dev/null; then
    echo "Using GitHub CLI to create release..."
    gh release create "$TAG_NAME" \
        --title "$RELEASE_NAME" \
        --notes "$RELEASE_BODY" \
        --target main \
        --repo "$REPO_OWNER/$REPO_NAME"
    
    if [ $? -eq 0 ]; then
        echo "✅ Release created successfully!"
        echo "🔗 View release: https://github.com/$REPO_OWNER/$REPO_NAME/releases/tag/$TAG_NAME"
    else
        echo "❌ Failed to create release with GitHub CLI"
    fi
else
    echo "GitHub CLI not found."
    echo ""
    echo "To create the release manually:"
    echo "1. Go to: https://github.com/$REPO_OWNER/$REPO_NAME/releases/new"
    echo "2. Choose tag: $TAG_NAME"
    echo "3. Release title: $RELEASE_NAME"
    echo "4. Copy and paste the release notes from this script"
    echo ""
    echo "Or install GitHub CLI: https://cli.github.com/"
fi

echo ""
echo "Release Information:"
echo "==================="
echo "Tag: $TAG_NAME"
echo "Title: $RELEASE_NAME"
echo "Commit: $COMMIT_SHA"
echo "Docker Images:"
echo "  - 675080425974.dkr.ecr.us-east-1.amazonaws.com/raadi-marketplace:main"
echo "  - 675080425974.dkr.ecr.us-east-1.amazonaws.com/raadi-marketplace:latest"
echo "  - 675080425974.dkr.ecr.us-east-1.amazonaws.com/raadi-marketplace:main-5a00d86"
