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
    organization = "raadi-marketplace"
    
    workspaces {
      name = "ws-MYEXTVRn8FhGXQjS"
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
data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_caller_identity" "current" {}

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

# Local variables
locals {
  name_prefix = "${var.project_name}-${var.environment}"
  
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
  }
  
  # Environment-specific configurations
  env_config = {
    dev = {
      instance_type     = "t3.micro"
      min_capacity      = 1
      max_capacity      = 2
      desired_capacity  = 1
      db_instance_class = "db.t3.micro"
      redis_node_type   = "cache.t3.micro"
    }
    test = {
      instance_type     = "t3.small"
      min_capacity      = 1
      max_capacity      = 3
      desired_capacity  = 2
      db_instance_class = "db.t3.small"
      redis_node_type   = "cache.t3.small"
    }
    prod = {
      instance_type     = "t3.medium"
      min_capacity      = 2
      max_capacity      = 10
      desired_capacity  = 3
      db_instance_class = "db.t3.medium"
      redis_node_type   = "cache.t3.medium"
    }
  }
  
  current_env = local.env_config[var.environment]
}
