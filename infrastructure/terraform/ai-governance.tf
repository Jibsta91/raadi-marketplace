# AI Governance and RBAC Policies for Raadi Marketplace

# AI Governance Tagging Strategy
locals {
  # AI-driven governance tags
  ai_governance_tags = {
    # Core Governance
    "ai:governance:version"     = "v1.0"
    "ai:governance:policy"      = "raadi-enterprise-policy"
    "ai:governance:compliance"  = "gdpr,iso27001,pci-dss"
    "ai:governance:risk-level"  = "medium"
    "ai:governance:criticality" = "high"
    
    # Resource Management
    "ai:resource:auto-scale"    = "enabled"
    "ai:resource:backup"        = "required"
    "ai:resource:monitoring"    = "enhanced"
    "ai:resource:lifecycle"     = "production"
    
    # Security & Access
    "ai:security:encryption"    = "required"
    "ai:security:public-access" = "restricted"
    "ai:security:data-class"    = "confidential"
    "ai:security:network-tier"  = "private"
    
    # Cost & Optimization
    "ai:cost:budget-alert"      = "enabled"
    "ai:cost:optimization"      = "automated"
    "ai:cost:owner"            = "platform-team"
    "ai:cost:center"           = "marketplace"
    
    # Deployment & CI/CD
    "ai:deployment:strategy"    = "blue-green"
    "ai:deployment:approval"    = "required"
    "ai:deployment:rollback"    = "automated"
    "ai:deployment:canary"      = "enabled"
  }
  
  # Standard governance tags
  standard_tags = {
    Project             = var.project_name
    Environment         = var.environment
    ManagedBy          = "terraform"
    GitHubRepo         = var.github_repo
    Owner              = "platform-team"
    BusinessUnit       = "marketplace"
    CostCenter         = "engineering"
    DataClassification = "confidential"
    BackupRequired     = "true"
    MonitoringEnabled  = "true"
    CreatedBy          = "terraform-cloud"
    LastModified       = timestamp()
  }
  
  # Combine all tags
  common_tags = merge(local.ai_governance_tags, local.standard_tags)
}

# AI Governance IAM Policies

# GitHub Actions OIDC Provider for secure authentication
resource "aws_iam_openid_connect_provider" "github_actions" {
  url = "https://token.actions.githubusercontent.com"
  
  client_id_list = [
    "sts.amazonaws.com",
  ]
  
  thumbprint_list = [
    "6938fd4d98bab03faadb97b34396831e3780aea1",
    "1c58a3a8518e8759bf075b76b750d4f2df264fcd"
  ]
  
  tags = merge(local.common_tags, {
    Name = "${var.project_name}-github-oidc"
    "ai:governance:purpose" = "cicd-authentication"
  })
}

# GitHub Actions Role with AI Governance Policies
resource "aws_iam_role" "github_actions" {
  name = "${var.project_name}-github-actions-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Federated = aws_iam_openid_connect_provider.github_actions.arn
        }
        Action = "sts:AssumeRoleWithWebIdentity"
        Condition = {
          StringEquals = {
            "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
          }
          StringLike = {
            "token.actions.githubusercontent.com:sub" = "repo:${var.github_repo}:*"
          }
        }
      }
    ]
  })
  
  tags = merge(local.common_tags, {
    Name = "${var.project_name}-github-actions-role"
    "ai:governance:access-type" = "automated-cicd"
    "ai:security:privileged" = "true"
  })
}

# AI Governance Policy for GitHub Actions
resource "aws_iam_policy" "github_actions_ai_governance" {
  name        = "${var.project_name}-github-actions-ai-governance"
  description = "AI Governance policy for GitHub Actions with least privilege"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AIGovernanceECRAccess"
        Effect = "Allow"
        Action = [
          "ecr:GetAuthorizationToken",
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:PutImage",
          "ecr:InitiateLayerUpload",
          "ecr:UploadLayerPart",
          "ecr:CompleteLayerUpload"
        ]
        Resource = "*"
        Condition = {
          StringEquals = {
            "aws:RequestedRegion" = var.aws_region
          }
        }
      },
      {
        Sid    = "AIGovernanceECSAccess"
        Effect = "Allow"
        Action = [
          "ecs:UpdateService",
          "ecs:DescribeServices",
          "ecs:DescribeClusters",
          "ecs:DescribeTaskDefinition",
          "ecs:RegisterTaskDefinition"
        ]
        Resource = "*"
        Condition = {
          StringLike = {
            "aws:ResourceTag/Project" = var.project_name
          }
        }
      },
      {
        Sid    = "AIGovernanceLogging"
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
          "logs:DescribeLogGroups",
          "logs:DescribeLogStreams"
        ]
        Resource = "arn:aws:logs:${var.aws_region}:*:log-group:/aws/ecs/${var.project_name}*"
      },
      {
        Sid    = "AIGovernanceMonitoring"
        Effect = "Allow"
        Action = [
          "cloudwatch:PutMetricData",
          "cloudwatch:GetMetricStatistics",
          "cloudwatch:ListMetrics"
        ]
        Resource = "*"
        Condition = {
          StringEquals = {
            "cloudwatch:namespace" = "AWS/ECS"
          }
        }
      }
    ]
  })
  
  tags = merge(local.common_tags, {
    Name = "${var.project_name}-github-actions-ai-governance-policy"
    "ai:governance:policy-type" = "least-privilege"
  })
}

# Attach AI Governance Policy to GitHub Actions Role
resource "aws_iam_role_policy_attachment" "github_actions_ai_governance" {
  role       = aws_iam_role.github_actions.name
  policy_arn = aws_iam_policy.github_actions_ai_governance.arn
}

# AI Governance Policy for Resource Tagging Enforcement
resource "aws_iam_policy" "ai_governance_tagging" {
  name        = "${var.project_name}-ai-governance-tagging"
  description = "AI Governance policy for enforcing resource tagging"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "DenyUntaggedResources"
        Effect = "Deny"
        Action = [
          "ec2:RunInstances",
          "ecs:CreateCluster",
          "ecs:CreateService",
          "rds:CreateDBInstance",
          "s3:CreateBucket"
        ]
        Resource = "*"
        Condition = {
          "Null" = {
            "aws:RequestTag/Project" = "true"
          }
        }
      },
      {
        Sid    = "RequireAIGovernanceTags"
        Effect = "Deny"
        Action = [
          "ec2:RunInstances",
          "ecs:CreateCluster",
          "ecs:CreateService"
        ]
        Resource = "*"
        Condition = {
          "Null" = {
            "aws:RequestTag/ai:governance:version" = "true"
          }
        }
      }
    ]
  })
  
  tags = merge(local.common_tags, {
    Name = "${var.project_name}-ai-governance-tagging-policy"
    "ai:governance:enforcement" = "strict"
  })
}

# Developer Role with AI Governance Constraints
resource "aws_iam_role" "developer_role" {
  name = "${var.project_name}-developer-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        Action = "sts:AssumeRole"
        Condition = {
          StringEquals = {
            "sts:ExternalId" = "${var.project_name}-developer"
          }
        }
      }
    ]
  })
  
  tags = merge(local.common_tags, {
    Name = "${var.project_name}-developer-role"
    "ai:governance:access-level" = "developer"
    "ai:security:mfa-required" = "true"
  })
}

# Developer Policy with AI Governance
resource "aws_iam_policy" "developer_ai_governance" {
  name        = "${var.project_name}-developer-ai-governance"
  description = "AI Governance policy for developers with restricted access"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowReadOnlyAccess"
        Effect = "Allow"
        Action = [
          "ecs:Describe*",
          "ecs:List*",
          "ecr:Describe*",
          "ecr:List*",
          "logs:Describe*",
          "logs:Get*",
          "cloudwatch:Get*",
          "cloudwatch:List*",
          "cloudwatch:Describe*"
        ]
        Resource = "*"
        Condition = {
          StringLike = {
            "aws:ResourceTag/Project" = var.project_name
          }
        }
      },
      {
        Sid    = "DenyProductionModification"
        Effect = "Deny"
        Action = [
          "ecs:UpdateService",
          "ecs:DeleteService",
          "ecs:DeleteCluster",
          "ecr:DeleteRepository",
          "logs:DeleteLogGroup"
        ]
        Resource = "*"
        Condition = {
          StringEquals = {
            "aws:ResourceTag/Environment" = "prod"
          }
        }
      }
    ]
  })
  
  tags = merge(local.common_tags, {
    Name = "${var.project_name}-developer-ai-governance-policy"
    "ai:governance:privilege-level" = "read-only"
  })
}

# Attach Developer AI Governance Policy
resource "aws_iam_role_policy_attachment" "developer_ai_governance" {
  role       = aws_iam_role.developer_role.name
  policy_arn = aws_iam_policy.developer_ai_governance.arn
}

# Admin Role with Full AI Governance
resource "aws_iam_role" "admin_role" {
  name = "${var.project_name}-admin-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        Action = "sts:AssumeRole"
        Condition = {
          StringEquals = {
            "sts:ExternalId" = "${var.project_name}-admin"
          }
          Bool = {
            "aws:MultiFactorAuthPresent" = "true"
          }
        }
      }
    ]
  })
  
  tags = merge(local.common_tags, {
    Name = "${var.project_name}-admin-role"
    "ai:governance:access-level" = "admin"
    "ai:security:mfa-required" = "true"
    "ai:security:privileged" = "true"
  })
}

# Admin Policy with AI Governance Oversight
resource "aws_iam_policy" "admin_ai_governance" {
  name        = "${var.project_name}-admin-ai-governance"
  description = "AI Governance policy for administrators with full access"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "FullAccessWithGovernance"
        Effect = "Allow"
        Action = "*"
        Resource = "*"
        Condition = {
          StringLike = {
            "aws:ResourceTag/Project" = var.project_name
          }
        }
      },
      {
        Sid    = "RequireApprovalForCriticalActions"
        Effect = "Deny"
        Action = [
          "ecs:DeleteCluster",
          "ecr:DeleteRepository",
          "rds:DeleteDBInstance",
          "s3:DeleteBucket"
        ]
        Resource = "*"
        Condition = {
          StringEquals = {
            "aws:ResourceTag/ai:governance:criticality" = "high"
          }
          "Null" = {
            "aws:RequestTag/ai:governance:approval" = "true"
          }
        }
      }
    ]
  })
  
  tags = merge(local.common_tags, {
    Name = "${var.project_name}-admin-ai-governance-policy"
    "ai:governance:privilege-level" = "full-access"
  })
}

# Attach Admin AI Governance Policy
resource "aws_iam_role_policy_attachment" "admin_ai_governance" {
  role       = aws_iam_role.admin_role.name
  policy_arn = aws_iam_policy.admin_ai_governance.arn
}

# Data source for current AWS account
data "aws_caller_identity" "current" {}
