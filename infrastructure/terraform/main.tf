# Terraform configuration for Raadi Marketplace
terraform {
  required_version = ">= 1.5"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 4.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.1"
    }
  }

  # Terraform Cloud configuration
  cloud {
    organization = "raadi"
    
    workspaces {
      name = "raadi"
    }
  }
}

# Configure AWS Provider
provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Project     = "raadi-marketplace"
      Environment = var.environment
      ManagedBy   = "terraform"
      Owner       = "raadi-team"
    }
  }
}

# Configure Cloudflare Provider (for DNS and CDN)
provider "cloudflare" {
  api_token = var.cloudflare_api_token
}

# Data sources
# Random password for database
resource "random_password" "db_password" {
  length  = 32
  special = true
}

# Random password for Redis
resource "random_password" "redis_password" {
  length  = 32
  special = false
}

# Generate JWT secret key
resource "random_password" "jwt_secret" {
  length  = 64
  special = false
}
