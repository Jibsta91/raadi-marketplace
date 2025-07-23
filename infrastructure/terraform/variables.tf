# Variables for Raadi Marketplace Infrastructure

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "raadi-marketplace"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "prod"
  validation {
    condition     = contains(["dev", "test", "prod"], var.environment)
    error_message = "Environment must be one of: dev, test, prod."
  }
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "domain_name" {
  description = "Domain name for the application"
  type        = string
  default     = ""
}

variable "cloudflare_api_token" {
  description = "Cloudflare API token"
  type        = string
  default     = ""
  sensitive   = true
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "Availability zones to use"
  type        = list(string)
  default     = []
}

variable "enable_nat_gateway" {
  description = "Enable NAT Gateway for private subnets"
  type        = bool
  default     = true
}

variable "enable_vpn_gateway" {
  description = "Enable VPN Gateway"
  type        = bool
  default     = false
}

variable "db_allocated_storage" {
  description = "Allocated storage for RDS instance"
  type        = number
  default     = 20
}

variable "db_max_allocated_storage" {
  description = "Maximum allocated storage for RDS instance"
  type        = number
  default     = 100
}

variable "db_backup_retention_period" {
  description = "Backup retention period for RDS"
  type        = number
  default     = 7
}

variable "enable_monitoring" {
  description = "Enable enhanced monitoring"
  type        = bool
  default     = true
}

variable "log_retention_days" {
  description = "CloudWatch log retention in days"
  type        = number
  default     = 30
}

variable "ssl_certificate_arn" {
  description = "ARN of SSL certificate in AWS Certificate Manager"
  type        = string
  default     = ""
}

variable "allowed_cidr_blocks" {
  description = "CIDR blocks allowed to access the application"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "github_repo" {
  description = "GitHub repository for CI/CD"
  type        = string
  default     = "Jibsta91/raadi-marketplace"
}

variable "container_insights_enabled" {
  description = "Enable CloudWatch Container Insights"
  type        = bool
  default     = true
}

variable "backup_enabled" {
  description = "Enable AWS Backup"
  type        = bool
  default     = true
}

variable "enable_waf" {
  description = "Enable AWS WAF"
  type        = bool
  default     = true
}

variable "image_tag" {
  description = "Docker image tag to deploy"
  type        = string
  default     = "latest"
}
