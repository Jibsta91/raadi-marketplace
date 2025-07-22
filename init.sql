-- Create database and user for Raadi
CREATE DATABASE raadi_db;
CREATE USER raadi_user WITH PASSWORD 'raadi_pass';
GRANT ALL PRIVILEGES ON DATABASE raadi_db TO raadi_user;

-- Connect to raadi_db
\c raadi_db;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Grant schema permissions
GRANT ALL ON SCHEMA public TO raadi_user;
