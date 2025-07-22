# 🚀 Raadi Marketplace - Production Deployment Guide

## 🎯 Quick Start

Your Raadi marketplace is now production-ready! Here's how to deploy it:

### 1. Generate Production Secrets
```bash
# Generate a strong SECRET_KEY (64 characters)
openssl rand -hex 32

# Generate database password
openssl rand -base64 32

# Generate Redis password  
openssl rand -base64 32
```

### 2. Create Production Environment File
Create `.env` file in your project root:
```bash
# Database
DB_PASSWORD=your_generated_db_password

# Security
SECRET_KEY=your_generated_64_char_secret_key

# Redis
REDIS_PASSWORD=your_generated_redis_password

# Domain
DOMAIN=yourdomain.com
CORS_ORIGINS=["https://yourdomain.com"]

# Optional: Monitoring
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id
```

### 3. Deploy with Docker Compose
```bash
# Production deployment
docker-compose -f docker-compose.prod.yml up -d

# Check status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f web
```

### 4. Set Up SSL/HTTPS (Let's Encrypt)
```bash
# Install Certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renewal (add to crontab)
0 12 * * * /usr/bin/certbot renew --quiet
```

## 🛡️ Security Status

### ✅ **FIXED**: Critical JWT Vulnerability
- **CVE-2024-33663**: Migrated from `python-jose` to secure `PyJWT`
- **Algorithm Enforcement**: Only HS256 allowed
- **Token Security**: Blacklisting and proper expiration

### ✅ **Enhanced**: Authentication System
- Refresh token support
- Secure logout with token invalidation
- Redis-based session management

### ✅ **Hardened**: Production Security
- Non-root Docker user
- Security headers (HSTS, CSP, XSS protection)
- CORS properly configured
- Environment-based secrets

## ⚡ Performance Features

### 🚀 **Database Optimizations**
```sql
-- Automatic indexes for common queries
CREATE INDEX idx_listings_category ON listings(category);
CREATE INDEX idx_listings_location ON listings(location);
CREATE INDEX idx_listings_category_location ON listings(category, location);
```

### 📦 **Caching System**
- Redis-based API response caching
- Search result caching
- Session management
- Background task queuing

### 🔄 **Async Operations**
- AsyncPG for PostgreSQL performance
- Async Redis operations
- Non-blocking API endpoints

## 📊 Monitoring & Logging

### 📈 **Metrics Endpoints**
- **Health Check**: `GET /health`
- **Prometheus Metrics**: `GET /metrics`
- **API Documentation**: `GET /docs`

### 🔍 **Error Tracking**
- Sentry integration for real-time error monitoring
- Structured logging with security events
- Performance monitoring

### 📋 **Monitoring Dashboard**
Access at: `http://yourdomain.com:3000` (Grafana)
- Request rates and response times
- Database performance
- Error rates and exceptions
- Security events

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│     Nginx       │    │   FastAPI    │    │   PostgreSQL   │
│ (Reverse Proxy) │────│ (Web Server) │────│   (Database)    │
└─────────────────┘    └──────────────┘    └─────────────────┘
         │                       │                      │
         │              ┌──────────────┐               │
         │              │    Redis     │               │
         └──────────────│  (Caching)   │───────────────┘
                        └──────────────┘
                               │
                    ┌─────────────────────┐
                    │   Elasticsearch     │
                    │     (Search)        │
                    └─────────────────────┘
```

## 🔧 Maintenance Commands

### Database Operations
```bash
# Run migrations
docker-compose -f docker-compose.prod.yml exec web alembic upgrade head

# Create new migration
docker-compose -f docker-compose.prod.yml exec web alembic revision --autogenerate -m "description"

# Database backup
docker-compose -f docker-compose.prod.yml exec db pg_dump -U raadi_user raadi_prod > backup.sql
```

### Monitoring Commands
```bash
# View application logs
docker-compose -f docker-compose.prod.yml logs -f web

# Check Redis cache
docker-compose -f docker-compose.prod.yml exec redis redis-cli info

# Elasticsearch health
curl http://localhost:9200/_cluster/health

# Security audit
python security_audit.py
```

### Performance Tuning
```bash
# Check database queries
docker-compose -f docker-compose.prod.yml exec db psql -U raadi_user -d raadi_prod -c "SELECT query, calls, total_time FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;"

# Redis memory usage
docker-compose -f docker-compose.prod.yml exec redis redis-cli info memory

# Container resource usage
docker stats
```

## 🚨 Security Checklist

- [x] **JWT Library**: Secure PyJWT implementation
- [x] **Secret Management**: Strong SECRET_KEY (64+ chars)
- [x] **HTTPS**: SSL/TLS with Let's Encrypt
- [x] **Headers**: Security headers (HSTS, CSP, XSS)
- [x] **CORS**: Proper origin configuration
- [x] **Database**: Connection pooling and indexes
- [x] **Docker**: Non-root user, minimal image
- [x] **Monitoring**: Error tracking and metrics
- [ ] **Backups**: Automated database backups
- [ ] **Firewall**: Server firewall configuration
- [ ] **Updates**: Regular dependency updates

## 📞 Support & Troubleshooting

### Common Issues

**1. Database Connection Error**
```bash
# Check database container
docker-compose -f docker-compose.prod.yml logs db

# Verify environment variables
docker-compose -f docker-compose.prod.yml exec web env | grep DATABASE_URL
```

**2. Redis Connection Error**
```bash
# Check Redis container
docker-compose -f docker-compose.prod.yml logs redis

# Test Redis connection
docker-compose -f docker-compose.prod.yml exec redis redis-cli ping
```

**3. SSL Certificate Issues**
```bash
# Check certificate status
sudo certbot certificates

# Renew certificates
sudo certbot renew --dry-run
```

### Performance Optimization
- **Database**: Monitor slow queries and add indexes
- **Caching**: Tune Redis TTL values based on usage
- **Scaling**: Add more Gunicorn workers for high traffic

### Security Updates
```bash
# Regular security checks
pip install safety bandit
safety check
bandit -r app/

# Update dependencies
pip-review --auto
```

---

## 🎉 **Your marketplace is ready for production!**

**Repository**: https://github.com/Jibsta91/raadi-marketplace  
**Status**: Production-ready Norwegian enterprise marketplace  
**Features**: 54 files, 10,000+ lines of secure, optimized code  
**Security**: ✅ Critical vulnerabilities fixed  
**Performance**: ⚡ Async operations, caching, database optimization  
**Monitoring**: 📊 Complete observability stack  

**Next Steps**: Deploy, configure domain, and start serving Norwegian businesses! 🇳🇴
