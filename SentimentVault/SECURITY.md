# Security Policy

## Reporting Security Vulnerabilities

If you discover a security vulnerability in SentimentVault, **do not open a public GitHub issue**. Instead, please use the GitHub Security Advisory feature to report it responsibly.

### How to Report

1. Go to the Security tab of the repository
2. Click "Report a vulnerability"
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
- Any known mitigations
- Your name and contact information (optional)

### Response Timeline

- **Acknowledgment:** Within 24 hours
- **Initial Assessment:** Within 48 hours
- **Patch Development:** Typically 1-2 weeks
- **Public Disclosure:** After patch release

## Security Best Practices

### For Users

1. **Keep Dependencies Updated**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **Use Environment Variables**
   - Never hardcode API keys or passwords
   - Store sensitive data in `.env` (not in version control)

3. **Secure Redis Connection**
   - Always use authentication in production
   - Enable encryption for remote connections

4. **API Security**
   - Use HTTPS in production
   - Implement rate limiting
   - Add authentication/authorization as needed

### For Contributors

1. **Code Review**
   - All changes reviewed before merge
   - Security-focused code review

2. **Dependency Management**
   - Minimize external dependencies
   - Regularly audit dependencies with `pip-audit`
   ```bash
   pip install pip-audit
   pip-audit
   ```

3. **Sensitive Data**
   - Never commit secrets, keys, or credentials
   - Use `.env` files (with `.gitignore`)
   - Rotate secrets regularly

## Known Security Considerations

### Model Poisoning
- Use only official Hugging Face models
- Verify model checksums
- Keep model files in restricted directories

### Cache Injection
- Input validation on all API endpoints
- MD5 hashing prevents collision attacks
- TTL expiration limits data exposure

### Data Privacy
- Amazon review text is stored temporarily in Redis
- 1-hour TTL ensures data expiration
- No persistent storage of raw predictions

## Security Updates

### Vulnerability Scanning

We use:
- GitHub Security Advisories
- Dependabot for dependency updates
- Regular manual security audits

### Patch Schedule

- **Critical:** Released immediately (< 24 hours)
- **High:** Released within 1 week
- **Medium:** Released within 2 weeks
- **Low:** Included in regular releases

## Production Security Checklist

- [ ] Use HTTPS/TLS for all API connections
- [ ] Enable Redis password authentication
- [ ] Configure firewall rules appropriately
- [ ] Enable API rate limiting
- [ ] Implement request logging
- [ ] Set up monitoring/alerting
- [ ] Regularly update dependencies
- [ ] Rotate secrets periodically
- [ ] Use environment-specific configurations
- [ ] Enable audit logging

## Compliance

SentimentVault is designed with security in mind but does not claim compliance with specific standards (HIPAA, GDPR, etc.). Users deploying in regulated environments should:

1. Conduct their own security assessment
2. Implement additional controls as needed
3. Document compliance measures
4. Perform regular security audits

## Security Headers

The FastAPI application includes:
- CORS restrictions (configurable)
- Request validation with Pydantic
- Error handling that doesn't expose internals
- Rate limiting support (external)

## Encryption

- Transit: Use HTTPS/TLS in production
- At-Rest: Redis persistence can be encrypted
- Tokenizer: No sensitive data in model files

## Reporting Other Issues

For non-security bugs and features:
- Use GitHub Issues
- Follow standard bug reporting guidelines
- Reference [CONTRIBUTING.md](./CONTRIBUTING.md)

## Security Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [PyPI Security](https://pypi.org/security/)
- [Hugging Face Security](https://huggingface.co/security)
- [FastAPI Security](https://fastapi.tiangolo.com/advanced/security/)

## Version Support

| Version | Status | Security Updates |
|---------|--------|------------------|
| 1.0.0+ | Active | Yes |
| < 1.0.0 | EOL | No |

---

**Last Updated:** January 2025
