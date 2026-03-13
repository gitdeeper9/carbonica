# Security Policy for CARBONICA

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of CARBONICA seriously. If you believe you have found a security vulnerability, please report it to us as described below.

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to:

**gitdeeper@gmail.com**

You should receive a response within 48 hours. If for some reason you do not, please follow up via email to ensure we received your original message.

Please include the following information in your report:

- Type of issue (e.g., buffer overflow, SQL injection, cross-site scripting, etc.)
- Full paths of source file(s) related to the manifestation of the issue
- The location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it

## Preferred Languages

We prefer all communications to be in English.

## Policy

We follow the principle of [Responsible Disclosure](https://en.wikipedia.org/wiki/Responsible_disclosure).

## Security Considerations for Deployment

When deploying CARBONICA in production, please consider the following security measures:

### 1. Environment Variables
- Never commit `.env` files to version control
- Use strong passwords for database connections
- Rotate API keys regularly
- Use secrets management services in production
- Example `.env` file should be `.env.example` only

### 2. Network Security
- Run services behind a firewall
- Use HTTPS/TLS for all web interfaces
- Restrict database access to localhost when possible
- Use VPN for remote connections
- Implement rate limiting for API endpoints
- Use read-only database users for queries

### 3. Authentication
- Change default passwords immediately
- Use strong password policies
- Enable 2FA for administrative access
- Implement rate limiting for login attempts
- Use JWT with short expiration times

### 4. Data Security
- Encrypt sensitive data at rest
- Use secure backup strategies
- Implement data retention policies
- Anonymize data when sharing publicly
- Verify checksums for downloaded datasets
- Use signed commits and tags

### 5. API Security
- Validate all input data
- Sanitize file paths and names
- Limit file upload sizes
- Use API keys with restricted permissions
- Log all access attempts
- Monitor for unusual patterns

### 6. Container Security
- Use specific image tags (not 'latest')
- Run containers as non-root user
- Scan images for vulnerabilities
- Use read-only root filesystems
- Limit container capabilities

### 7. Data Validation
- Validate all input data against schemas
- Sanitize all file inputs
- Verify checksums for downloaded datasets
- Use parameterized queries for databases
- Escape all output to prevent XSS

### 8. Scientific Integrity
- Verify data provenance
- Document all assumptions
- Use version control for all code and data
- Maintain audit trails for data processing
- Validate against independent observations

## Security Updates

Security updates will be released as soon as possible after a vulnerability is confirmed. Updates will be announced via:

- GitHub releases
- PyPI package updates
- Project website announcements
- Direct email to registered users (optional)

## Responsible Disclosure Timeline

1. **Vulnerability Reported**: Reporter submits details
2. **Acknowledgment**: Within 48 hours, we acknowledge receipt
3. **Investigation**: We investigate and validate the report
4. **Fix Development**: We develop and test a fix
5. **Release**: We release a patched version
6. **Public Disclosure**: After users have time to update

## Acknowledgements

We thank the security researchers and users who report vulnerabilities to us responsibly. Contributors will be acknowledged in release notes (unless they prefer anonymity).

## Contact

- **Email**: gitdeeper@gmail.com
- **PGP Key**: Available on request
- **ORCID**: 0009-0003-8903-0029

## License

This security policy is part of the CARBONICA project and is covered under the MIT License.
