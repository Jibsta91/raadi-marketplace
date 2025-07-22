import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.redis import RedisIntegration
import structlog
import logging
from prometheus_client import Counter, Histogram, generate_latest
from typing import Optional
from app.core.config import settings


# Prometheus metrics
REQUEST_COUNT = Counter(
    'raadi_requests_total',
    'Total number of requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'raadi_request_duration_seconds',
    'Request duration in seconds',
    ['method', 'endpoint']
)

USER_REGISTRATIONS = Counter(
    'raadi_user_registrations_total',
    'Total number of user registrations'
)

LISTINGS_CREATED = Counter(
    'raadi_listings_created_total',
    'Total number of listings created',
    ['category']
)

SEARCH_QUERIES = Counter(
    'raadi_search_queries_total',
    'Total number of search queries',
    ['category']
)


def setup_sentry(dsn: Optional[str] = None):
    """Initialize Sentry for error tracking"""
    if dsn or settings.SENTRY_DSN:
        sentry_sdk.init(
            dsn=dsn or settings.SENTRY_DSN,
            integrations=[
                FastApiIntegration(auto_enabling_integrations=False),
                SqlalchemyIntegration(),
                RedisIntegration(),
            ],
            traces_sample_rate=0.1,  # 10% of transactions for performance monitoring
            environment=settings.ENVIRONMENT,
            release=getattr(settings, 'VERSION', '1.0.0'),
        )


def setup_logging():
    """Configure structured logging"""
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            min_level=logging.INFO
        ),
        logger_factory=structlog.WriteLoggerFactory(),
        cache_logger_on_first_use=False,
    )


def get_logger(name: str):
    """Get a structured logger instance"""
    return structlog.get_logger(name)


class MetricsMiddleware:
    """Middleware to collect Prometheus metrics"""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        method = scope["method"]
        path = scope["path"]
        
        # Start timer
        start_time = time.time()
        
        # Process request
        status_code = 200
        
        async def send_wrapper(message):
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message["status"]
            await send(message)
        
        try:
            await self.app(scope, receive, send_wrapper)
        except Exception as e:
            status_code = 500
            raise e
        finally:
            # Record metrics
            duration = time.time() - start_time
            REQUEST_COUNT.labels(
                method=method,
                endpoint=path,
                status=str(status_code)
            ).inc()
            REQUEST_DURATION.labels(
                method=method,
                endpoint=path
            ).observe(duration)


class SecurityLogger:
    """Security event logger"""
    
    def __init__(self):
        self.logger = get_logger("security")
    
    def log_failed_login(self, email: str, ip_address: str):
        """Log failed login attempt"""
        self.logger.warning(
            "Failed login attempt",
            email=email,
            ip_address=ip_address,
            event_type="failed_login"
        )
    
    def log_successful_login(self, user_id: int, ip_address: str):
        """Log successful login"""
        self.logger.info(
            "Successful login",
            user_id=user_id,
            ip_address=ip_address,
            event_type="successful_login"
        )
    
    def log_token_refresh(self, user_id: int, ip_address: str):
        """Log token refresh"""
        self.logger.info(
            "Token refreshed",
            user_id=user_id,
            ip_address=ip_address,
            event_type="token_refresh"
        )
    
    def log_logout(self, user_id: int, ip_address: str):
        """Log user logout"""
        self.logger.info(
            "User logout",
            user_id=user_id,
            ip_address=ip_address,
            event_type="logout"
        )
    
    def log_suspicious_activity(self, description: str, user_id: int = None, ip_address: str = None):
        """Log suspicious activity"""
        self.logger.warning(
            "Suspicious activity detected",
            description=description,
            user_id=user_id,
            ip_address=ip_address,
            event_type="suspicious_activity"
        )


# Global instances
security_logger = SecurityLogger()


def get_metrics():
    """Get Prometheus metrics"""
    return generate_latest()


import time  # Import needed for MetricsMiddleware
