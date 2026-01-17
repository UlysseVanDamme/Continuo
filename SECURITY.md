# Security and Deployment Guide

This guide covers security best practices and deployment recommendations for Continuo.

---

## Environment Variables Setup

Each component requires specific environment variables. **Never commit `.env` files to git.**

### Quick Start

1. Copy the example files:
   ```bash
   cp backend-api/.env.example backend-api/.env
   cp pi-agent/.env.example pi-agent/.env
   cp worker/.env.example worker/.env
   ```

2. Edit each `.env` file with your actual credentials

3. Verify `.env` is in `.gitignore` (it already is)

---

## AWS Security Best Practices

### Use IAM Roles (Recommended)

For production deployments, use IAM roles instead of access keys:

**For EC2/Fargate:**
- Attach IAM roles to instances/tasks
- Remove `AWS_ACCESS_KEY` and `AWS_SECRET_KEY` from environment
- AWS SDK will automatically use the instance role

**For Local Development:**
- Use `aws configure` to set up credentials
- Or use environment variables for testing

### IAM Permissions Required

**S3 Bucket Policy (Pi Agent & Backend):**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject"
      ],
      "Resource": "arn:aws:s3:::your-bucket-name/*"
    }
  ]
}
```

**SQS Queue Policy (Worker):**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "sqs:ReceiveMessage",
        "sqs:DeleteMessage",
        "sqs:GetQueueAttributes"
      ],
      "Resource": "arn:aws:sqs:region:account-id:queue-name"
    }
  ]
}
```

---

## Database Security

### PostgreSQL Best Practices

1. **Use SSL/TLS connections**
   ```
   DATABASE_URL=postgresql://user:password@host:port/db?sslmode=require
   ```

2. **Create dedicated database users** with minimal permissions:
   ```sql
   CREATE USER continuo_backend WITH PASSWORD 'secure-password';
   CREATE USER continuo_worker WITH PASSWORD 'secure-password';
   
   GRANT SELECT, INSERT ON practice_sessions TO continuo_backend;
   GRANT INSERT, SELECT ON practice_sessions TO continuo_worker;
   ```

3. **Use managed services** (e.g., Neon, AWS RDS) with automated backups

---

## API Security

### INGEST_API_KEY

Generate a strong random key:

```bash
# Using Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Using OpenSSL
openssl rand -base64 32
```

Store this securely and use it for authenticating ingestion requests.

---

## Network Security

### CORS Configuration

The backend restricts CORS to `WEBSITE_LINK`. In production:

```bash
# Production
WEBSITE_LINK=https://your-production-domain.com

# Development
WEBSITE_LINK=http://localhost:3000
```

### Firewall Rules

- **Backend API:** Expose only necessary ports (typically 8000 or 80/443)
- **Database:** Restrict access to backend and worker IPs only
- **SQS/S3:** Use VPC endpoints for private access (optional)

---

## Secrets Management

### Development
- Use `.env` files (already gitignored)
- Never commit credentials

### Production Options

1. **AWS Secrets Manager**
   ```python
   import boto3
   secrets = boto3.client('secretsmanager')
   response = secrets.get_secret_value(SecretId='continuo/db')
   ```

2. **Environment Variables** (ECS/Fargate)
   - Set in task definition
   - Reference from Secrets Manager or Parameter Store

3. **Kubernetes Secrets** (if using K8s)
   ```yaml
   apiVersion: v1
   kind: Secret
   metadata:
     name: continuo-secrets
   type: Opaque
   data:
     database-url: <base64-encoded>
   ```

---

## Pre-Deployment Checklist

- [ ] All `.env` files created and configured
- [ ] `.env` files NOT committed to git
- [ ] Strong random keys generated for API keys
- [ ] Database user permissions configured (least privilege)
- [ ] IAM roles configured (for AWS deployments)
- [ ] CORS properly configured for your domain
- [ ] SSL/TLS enabled for database connections
- [ ] Firewall rules configured
- [ ] Backup strategy in place

---

## Security Monitoring

### Recommended Practices

1. **Rotate credentials regularly** (quarterly for API keys, immediately if compromised)
2. **Monitor CloudWatch logs** for unusual activity
3. **Set up CloudWatch alarms** for failed authentication attempts
4. **Review IAM access** regularly
5. **Keep dependencies updated** (`pip list --outdated`)

---

## Common Pitfalls to Avoid

❌ **Don't** commit `.env` files  
❌ **Don't** use root database credentials  
❌ **Don't** expose the database publicly  
❌ **Don't** hardcode credentials in code  
❌ **Don't** use the same API key across environments  

✅ **Do** use environment variables  
✅ **Do** use IAM roles where possible  
✅ **Do** implement least privilege access  
✅ **Do** enable SSL/TLS connections  
✅ **Do** rotate credentials regularly  

---

## Getting Help

If you discover a security vulnerability:
1. **Do not** open a public issue
2. Contact the repository owner privately
3. Allow time for the issue to be addressed before disclosure

---

## License

(To be added - consider MIT, Apache 2.0, or GPL v3)
