# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability, please **do NOT open a public issue**.

Instead, email us at [security@mempalace.dev](mailto:security@mempalace.dev) with:

- Description of the vulnerability
- Steps to reproduce
- Impact assessment
- Suggested fix (if any)

We will respond within 48 hours.

## Security Best Practices

### API Keys

- Never commit API keys to the repository
- Use environment variables or `.env` files
- Add keys to `.gitignore`

### Local Data

MemPalace stores all data locally. Protect your machine:

- Use strong passwords
- Keep your OS updated
- Back up your palace regularly

## Dependencies

We regularly audit dependencies:

```bash
pip install pip-audit
pip-audit
```

Report vulnerabilities via the process above.

---

**Last updated**: 2026-05-01
