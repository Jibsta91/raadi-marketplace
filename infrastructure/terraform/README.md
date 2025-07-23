# Terraform Cloud Configuration

This project is configured to use Terraform Cloud for state management and execution.

## Configuration

- **Organization**: raadi-marketplace
- **Project ID**: prj-CPNeHfFfgeyMqGGG
- **Workspace ID**: ws-MYEXTVRn8FhGXQjS

## Required GitHub Secrets

Add these secrets to your GitHub repository (Settings → Secrets and variables → Actions):

```
AWS_ACCESS_KEY_ID          # Your AWS access key ID
AWS_SECRET_ACCESS_KEY      # Your AWS secret access key
TF_API_TOKEN              # Your Terraform Cloud API token
```

## Getting Terraform Cloud API Token

1. Go to [Terraform Cloud](https://app.terraform.io/)
2. Click on your profile → User Settings
3. Go to "Tokens" tab
4. Click "Create an API token"
5. Copy the token and add it as `TF_API_TOKEN` secret in GitHub

## Workspace Variables

Configure these variables in your Terraform Cloud workspace:

### Terraform Variables
```
aws_region = "us-east-1"
app_name = "raadi-marketplace"
environment = "prod"
```

### Environment Variables
```
AWS_ACCESS_KEY_ID     # (sensitive)
AWS_SECRET_ACCESS_KEY # (sensitive)
```

## Deployment

The CI/CD pipeline will automatically:
1. Run security scans and tests
2. Build Docker image
3. Deploy infrastructure via Terraform Cloud
4. Update ECS service
5. Perform health checks
