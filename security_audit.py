# Security audit script for Raadi Marketplace
# Run with: python security_audit.py

import subprocess
import sys
import os

def run_safety_check():
    """Run safety check on dependencies."""
    print("🔍 Running safety check on dependencies...")
    try:
        result = subprocess.run(['safety', 'check', '--json'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ No known security vulnerabilities found in dependencies")
        else:
            print("⚠️  Security vulnerabilities found:")
            print(result.stdout)
    except FileNotFoundError:
        print("❌ Safety not installed. Install with: pip install safety")

def check_jwt_implementation():
    """Check JWT implementation for security best practices."""
    print("\n🔍 Checking JWT implementation...")
    
    # Check if python-jose is still in requirements
    with open('requirements.txt', 'r') as f:
        requirements = f.read()
        if 'python-jose' in requirements:
            print("⚠️  WARNING: python-jose found in requirements.txt")
            print("   This library has known vulnerabilities (CVE-2024-33663)")
            print("   Recommendation: Migrate to PyJWT")
        else:
            print("✅ python-jose not found in requirements")

def check_docker_security():
    """Check Docker configuration for security best practices."""
    print("\n🔍 Checking Docker security...")
    
    # Check if .dockerignore exists
    if os.path.exists('.dockerignore'):
        print("✅ .dockerignore file exists")
    else:
        print("⚠️  No .dockerignore file found")
        print("   Recommendation: Create .dockerignore to exclude sensitive files")
    
    # Check Dockerfile for non-root user
    if os.path.exists('Dockerfile'):
        with open('Dockerfile', 'r') as f:
            dockerfile_content = f.read()
            if 'USER' in dockerfile_content and 'root' not in dockerfile_content.split('USER')[1].split('\n')[0]:
                print("✅ Non-root user configured in Dockerfile")
            else:
                print("⚠️  Running as root in Docker container")
                print("   Recommendation: Add non-root user to Dockerfile")

def check_environment_variables():
    """Check for hardcoded secrets."""
    print("\n🔍 Checking for hardcoded secrets...")
    
    sensitive_patterns = [
        'password',
        'secret',
        'key',
        'token',
        'api_key'
    ]
    
    # Check main application files
    files_to_check = []
    for root, dirs, files in os.walk('app'):
        for file in files:
            if file.endswith('.py'):
                files_to_check.append(os.path.join(root, file))
    
    issues_found = False
    for file_path in files_to_check:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                for pattern in sensitive_patterns:
                    if f'{pattern}=' in content and 'env' not in content:
                        print(f"⚠️  Potential hardcoded secret in {file_path}")
                        issues_found = True
        except:
            continue
    
    if not issues_found:
        print("✅ No obvious hardcoded secrets found")

def main():
    print("🛡️  Raadi Marketplace Security Audit")
    print("=" * 40)
    
    run_safety_check()
    check_jwt_implementation()
    check_docker_security()
    check_environment_variables()
    
    print("\n📋 Security Recommendations:")
    print("1. Update PyJWT to latest version (>=2.8.0)")
    print("2. Ensure SECRET_KEY is cryptographically strong (64+ chars)")
    print("3. Enable HTTPS in production with Let's Encrypt")
    print("4. Configure proper CORS settings")
    print("5. Implement rate limiting")
    print("6. Regular dependency updates")
    print("7. Use security headers (CSP, HSTS, etc.)")
    print("8. Regular security audits and penetration testing")

if __name__ == "__main__":
    main()
