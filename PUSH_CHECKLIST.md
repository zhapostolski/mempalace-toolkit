# MemPalace GitHub Release Checklist

## Before Pushing

- [x] Repository initialized at `<repository-path>`
- [x] All source code copied from `/path/to/.mempalace/src`
- [x] `.gitignore` configured (excludes palace data, secrets, venv)
- [x] LICENSE file present (MIT)
- [x] README.md with full documentation
- [x] CONTRIBUTING.md with guidelines
- [x] CHANGELOG.md with version history
- [x] CODEOWNERS configured
- [x] SECURITY.md policy
- [x] CI/CD workflow (GitHub Actions)
- [x] Issue templates (bug report, feature request)
- [x] Pull request template
- [x] Code of Conduct
- [x] Initial commit created

## Manual Steps Required

### 1. Create GitHub Repository

```bash
# Login to GitHub or use CLI
gh auth login

# Create public repository
gh repo create milla-jovovich/mempalace --public --description "The highest-scoring AI memory system ever benchmarked. Local, free, no API required."

# Or manually:
# - Go to https://github.com/new
# - Repository name: mempalace
# - Owner: milla-jovovich
# - Visibility: Public
# - Do NOT initialize with README (we already have one)
```

### 2. Push Repository

```bash
cd <repository-path>

# Add remote (replace with your actual username if different)
git remote add origin https://github.com/milla-jovovich/mempalace.git

# Push main branch
git push -u origin main
```

### 3. Create First Release

```bash
# Create tag and release
git tag v3.0.11
git push origin v3.0.11

# Create GitHub release
gh release create v3.0.11 \
  --title "MemPalace v3.0.11" \
  --notes "See CHANGELOG.md for full changelog" \
  --latest
```

### 4. PyPI Publishing (Optional)

```bash
# Test PyPI first
pip install build
python -m build

pip install twine
twine upload --repository testpypi dist/*

# If successful, publish to real PyPI
twine upload dist/*

# Note: You'll need an account at https://pypi.org and API token
```

### 5. Configure Repository Settings

- [ ] Enable Issues
- [ ] Enable Discussions
- [ ] Enable Discussions (for Q&A)
- [ ] Add topics: `ai`, `memory`, `llm`, `mcp`, `chromadb`, `rag`, `local-ai`
- [ ] Add Discord badge to README
- [ ] Set homepage URL (if applicable)

### 6. Post-Push Tasks

- [ ] Verify CI/CD workflow runs on push
- [ ] Test `pip install mempalace` (after PyPI publish)
- [ ] Update Discord announcement
- [ ] Share on Hacker News / Reddit (optional)

## Verification

After pushing, verify:

```bash
# Clone fresh and test
cd /tmp
git clone https://github.com/milla-jovovich/mempalace.git
cd mempalace
pip install -e ".[dev]"
pytest tests/ -v
```

## Current Repository Status

```bash
# Run these commands to check status
cd <repository-path>
git log --oneline -1
git status
ls -la
```

---

**Ready to push?** Run the `CREATE_RELEASE` script or follow the manual steps above.
