# Raadi Enterprise Marketplace

A comprehensive Norwegian enterprise marketplace webapp with AI-powered governance, cybersecurity, infrastructure, and data management capabilities.

## 🚀 Features

### Core Marketplace
- **Torget** - General marketplace/classified ads
- **Jobb** - Job listings and career opportunities  
- **Bil og campingvogn** - Cars and camping vehicles
- **Eiendom** - Real estate
- **Reise** - Travel services
- **Båt** - Boats and marine vehicles
- **MC** - Motorcycles
- **Nyttekjøretøy** - Commercial vehicles and machinery

### AI-Powered Services
- **AI Governance** - Content moderation, fraud detection, bias analysis
- **AI Cybersecurity** - Threat detection, vulnerability scanning, security monitoring
- **AI Infrastructure** - Auto-scaling, resource optimization, predictive maintenance
- **AI Data Management** - Data quality assessment, privacy compliance, lifecycle management

### User Features
- User registration and authentication
- Personal messaging system
- Notifications system
- Favorites/wishlist functionality
- Advanced search with filters
- Business customer portal
- Mobile-responsive design

## 🛠 Tech Stack

- **Backend**: FastAPI, Python 3.11+
- **Database**: PostgreSQL with SQLAlchemy
- **Cache**: Redis
- **Search**: Elasticsearch
- **Authentication**: JWT with OAuth2
- **Task Queue**: Celery
- **Containerization**: Docker & Docker Compose
- **Monitoring**: Structured logging, Sentry integration

## 🐳 Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd raadi
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start the application**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Main API: http://localhost:8000
   - AI Governance: http://localhost:8001
   - AI Cybersecurity: http://localhost:8002
   - AI Infrastructure: http://localhost:8003
   - AI Data Management: http://localhost:8004
   - API Documentation: http://localhost:8000/docs

## 🏗 Development Setup

1. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up database**
   ```bash
   # Start PostgreSQL, Redis, and Elasticsearch
   docker-compose up -d db redis elasticsearch
   
   # Run database migrations
   alembic upgrade head
   ```

3. **Start the development server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## 📁 Project Structure

```
raadi/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── api/
│   │   └── v1/
│   │       ├── api.py          # API router
│   │       └── endpoints/      # API endpoint modules
│   ├── core/
│   │   ├── config.py          # Application configuration
│   │   ├── database.py        # Database setup
│   │   ├── security.py        # Authentication & security
│   │   └── exceptions.py      # Custom exceptions
│   ├── models/                # SQLAlchemy models
│   ├── schemas/               # Pydantic schemas
│   └── crud/                  # Database operations
├── docker-compose.yml         # Docker services configuration
├── Dockerfile                 # Main application Docker image
├── requirements.txt           # Python dependencies
└── README.md
```

## 🔧 Configuration

The application uses environment variables for configuration. Key variables:

- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string  
- `ELASTICSEARCH_URL` - Elasticsearch connection string
- `SECRET_KEY` - JWT secret key
- `OPENAI_API_KEY` - OpenAI API key for AI services

## 🔐 Authentication

The API uses JWT tokens for authentication. To access protected endpoints:

1. Register or login to get an access token
2. Include the token in the Authorization header: `Bearer <token>`

## 📖 API Documentation

Interactive API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🧪 Testing

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=app tests/
```

## 🚀 Deployment

### Production Docker Deployment

1. **Build production images**
   ```bash
   docker-compose -f docker-compose.prod.yml build
   ```

2. **Deploy to production**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

### Environment Variables for Production

Ensure these environment variables are set in production:
- Set strong `SECRET_KEY`
- Configure proper database credentials
- Set up monitoring with `SENTRY_DSN`
- Configure email settings for notifications

## 🔍 Monitoring & Logging

- Structured logging with JSON format
- Health check endpoints for all services
- Integration with Sentry for error tracking
- Metrics collection for monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

---

**Built with ❤️ for the Norwegian marketplace community**
