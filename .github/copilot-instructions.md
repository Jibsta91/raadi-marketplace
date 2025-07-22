# Copilot Instructions for Raadi Enterprise Marketplace

<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

## Project Overview
This is a Norwegian enterprise marketplace webapp called "Raadi" built with Python, FastAPI, and Docker. The application includes AI-powered services for governance, cybersecurity, infrastructure management, and data management.

## Tech Stack
- **Backend**: FastAPI, Python 3.11+
- **Database**: PostgreSQL with SQLAlchemy
- **Cache**: Redis
- **Search**: Elasticsearch
- **Containerization**: Docker & Docker Compose
- **Authentication**: JWT with OAuth2
- **Task Queue**: Celery

## Key Components

### AI Services
- **AI Governance**: Content moderation, fraud detection, bias analysis, compliance monitoring
- **AI Cybersecurity**: Threat detection, vulnerability scanning, security monitoring
- **AI Infrastructure**: Auto-scaling, resource optimization, predictive maintenance
- **AI Data Management**: Data quality assessment, privacy compliance, lifecycle management

### Marketplace Categories
- **Torget**: General marketplace/classified ads
- **Jobb**: Job listings and career opportunities
- **Bil og campingvogn**: Cars and camping vehicles
- **Eiendom**: Real estate
- **Reise**: Travel services
- **Båt**: Boats and marine vehicles
- **MC**: Motorcycles
- **Nyttekjøretøy**: Commercial vehicles and machinery

## Code Guidelines
1. Use Norwegian terms for marketplace categories and user-facing content
2. Follow FastAPI best practices with proper dependency injection
3. Implement proper error handling with custom exceptions
4. Use Pydantic models for request/response validation
5. Follow RESTful API design principles
6. Implement proper authentication and authorization
7. Use type hints throughout the codebase
8. Follow PEP 8 style guidelines
9. Write comprehensive docstrings for all functions and classes
10. Implement proper logging and monitoring

## Environment Variables
The application uses environment variables for configuration. Key variables include:
- DATABASE_URL
- REDIS_URL
- ELASTICSEARCH_URL
- SECRET_KEY
- OPENAI_API_KEY
- AWS credentials for file storage

## Development Notes
- The application is designed to be microservices-ready
- All AI services have placeholder implementations that can be enhanced with real AI models
- The codebase follows enterprise-level patterns and best practices
- Docker containers are optimized for production deployment
