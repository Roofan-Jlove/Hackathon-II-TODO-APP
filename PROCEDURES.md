# 📋 Project Procedures - CLI Todo Manager

> Comprehensive guide for all project workflows, releases, and maintenance procedures.

**Last Updated:** 2025-12-29
**Current Version:** v1.0.0
**Project Status:** Hackathon Phase 1 Complete

---

## 📑 Table of Contents

1. [Installation & Setup](#installation--setup)
2. [Development Workflow](#development-workflow)
3. [Testing Procedures](#testing-procedures)
4. [Release Procedures](#release-procedures)
5. [GitHub Release Creation](#github-release-creation)
6. [Deployment](#deployment)
7. [Maintenance](#maintenance)
8. [Troubleshooting](#troubleshooting)

---

## 🚀 Installation & Setup

### Prerequisites Installation

#### 1. Install Python 3.13+

**Windows:**
```powershell
# Download from python.org or use winget
winget install Python.Python.3.13
```

**macOS:**
```bash
# Using Homebrew
brew install python@3.13
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.13 python3.13-venv

# Fedora
sudo dnf install python3.13
```

**Verify:**
```bash
python --version
# Should output: Python 3.13.x
```

---

#### 2. Install UV Package Manager

**Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Verify:**
```bash
uv --version
# Should output: uv x.x.x
```

---

### Project Setup

#### Clone Repository

```bash
# Clone from GitHub
git clone https://github.com/Roofan-Jlove/Hackathon-II-TODO-APP.git
cd Hackathon-II-TODO-APP

# Checkout development branch
git checkout console-app
```

#### Install Dependencies

```bash
# Create virtual environment and install dependencies
uv sync

# Verify installation
uv run python -c "import colorama; import dateutil; print('Dependencies OK')"
```

---

## 💻 Development Workflow

### Branch Strategy

**Main Branches:**
- `main` - Production-ready code (reserved for future)
- `console-app` - Main development branch (current)
- `feature/*` - Feature branches (create as needed)

### Creating a Feature Branch

```bash
# Create and checkout feature branch
git checkout -b feature/my-new-feature

# Make changes, commit regularly
git add .
git commit -m "feat: Add my new feature"

# Push to remote
git push origin feature/my-new-feature

# Create pull request on GitHub
```

### Commit Message Convention

Follow conventional commits format:

```bash
# Feature
git commit -m "feat: Add recurring task feature"

# Bug fix
git commit -m "fix: Correct ID validation error"

# Documentation
git commit -m "docs: Update README with new features"

# Tests
git commit -m "test: Add unit tests for priority validation"

# Refactor
git commit -m "refactor: Simplify tag normalization logic"

# Chore
git commit -m "chore: Update dependencies"
```

### Code Changes Workflow

```bash
# 1. Pull latest changes
git pull origin console-app

# 2. Make changes to code
# Edit files in src/

# 3. Run tests (MUST pass before commit)
uv run python -m unittest discover -s tests -p "test_*.py" -v

# 4. Stage changes
git add src/models.py src/storage.py

# 5. Commit with descriptive message
git commit -m "feat: Add new validation function"

# 6. Push to remote
git push origin console-app
```

---

## 🧪 Testing Procedures

### Run All Tests

```bash
# Run all 56 unit tests
uv run python -m unittest discover -s tests -p "test_*.py" -v

# Expected output:
# Ran 56 tests in 0.005s
# OK
```

### Run Specific Test Suites

```bash
# Test models only
uv run python -m unittest tests.unit.test_models -v

# Test specific class
uv run python -m unittest tests.unit.test_models.TestValidateRecurrencePattern -v

# Test specific method
uv run python -m unittest tests.unit.test_models.TestValidateRecurrencePattern.test_valid_pattern_daily -v
```

### Test-Driven Development (TDD) Workflow

```bash
# 1. Write failing test
# Edit: tests/unit/test_models.py
# Add new test method

# 2. Run test (should FAIL)
uv run python -m unittest tests.unit.test_models.TestNewFeature -v

# 3. Implement feature
# Edit: src/models.py
# Add minimal code to pass test

# 4. Run test (should PASS)
uv run python -m unittest tests.unit.test_models.TestNewFeature -v

# 5. Run all tests (ensure no regressions)
uv run python -m unittest discover -s tests -p "test_*.py" -v

# 6. Refactor if needed
# Clean up code while keeping tests green

# 7. Commit
git add tests/unit/test_models.py src/models.py
git commit -m "feat: Add new feature with tests"
```

### Test Coverage Verification

```bash
# Verify all tests pass
uv run python -m unittest discover -s tests -p "test_*.py" -v

# Check test count (should be 56)
uv run python -m unittest discover -s tests -p "test_*.py" -v 2>&1 | grep "Ran"
# Output: Ran 56 tests in 0.005s
```

---

## 📦 Release Procedures

### Pre-Release Checklist

Before creating a release, ensure:

- [ ] All tests pass (56/56)
- [ ] Documentation updated (README.md, CLAUDE.md)
- [ ] CHANGELOG.md updated (if exists)
- [ ] Version numbers updated
- [ ] All features tested manually
- [ ] No debug code or TODOs in main code
- [ ] Git status clean (no uncommitted changes)

### Creating a Release Tag

#### Step 1: Determine Version Number

Follow [Semantic Versioning](https://semver.org/):
- **MAJOR.MINOR.PATCH** (e.g., 1.0.0)
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

Examples:
- `v1.0.0` - Initial release (Hackathon Phase 1)
- `v1.1.0` - Add file persistence (new feature)
- `v1.0.1` - Fix bug in tag validation (patch)
- `v2.0.0` - Complete redesign (breaking change)

#### Step 2: Create Annotated Tag

```bash
# Create annotated tag with release notes
git tag -a v1.0.0 -m "$(cat <<'EOF'
Release v1.0.0 - Hackathon Phase 1 Complete

🎉 CLI Todo Manager - Hackathon Phase 1 Release

## Features
✅ User Stories 1-9 complete
✅ 100% test coverage (56/56 tests)
✅ Production-ready code

## Highlights
- Colorful CLI with emojis
- Recurring tasks with auto-recreation
- Priorities, tags, search, filter, sort
- Functional programming architecture

## Installation
git clone https://github.com/Roofan-Jlove/Hackathon-II-TODO-APP.git
cd Hackathon-II-TODO-APP
git checkout v1.0.0
uv sync
uv run python src/main.py

Built with ❤️ using Python, UV, and Claude Code
EOF
)"
```

#### Step 3: Verify Tag

```bash
# List tags
git tag -l

# View tag details
git show v1.0.0

# View tag message
git tag -l -n9 v1.0.0
```

#### Step 4: Push Tag to Remote

```bash
# Push specific tag
git push origin v1.0.0

# Or push all tags
git push origin --tags
```

#### Step 5: Verify on GitHub

```bash
# Check tags on GitHub
https://github.com/Roofan-Jlove/Hackathon-II-TODO-APP/tags
```

---

## 🚀 GitHub Release Creation

### Method 1: Manual (Web Interface) - RECOMMENDED

#### Step 1: Navigate to Releases

Go to: https://github.com/Roofan-Jlove/Hackathon-II-TODO-APP/releases/new

Or click:
1. Go to repository main page
2. Click "Releases" in right sidebar
3. Click "Draft a new release"

#### Step 2: Fill Release Form

**Choose a tag:** Select `v1.0.0` from dropdown

**Release title:** `v1.0.0 - Hackathon Phase 1 Complete`

**Description:** Use the comprehensive release notes template (see Release Notes Template section below)

**Options:**
- ☑️ **Set as the latest release** (check this)
- ☐ **Set as a pre-release** (leave unchecked)
- ☐ **Create a discussion** (optional)

#### Step 3: Publish

Click **"Publish release"** button

#### Step 4: Verify

Visit: https://github.com/Roofan-Jlove/Hackathon-II-TODO-APP/releases

Verify:
- ✅ Release appears in list
- ✅ Tag is correct (v1.0.0)
- ✅ Download links work (ZIP, tar.gz)
- ✅ Release notes display correctly

---

### Method 2: Using GitHub CLI (Advanced)

#### Prerequisites

```bash
# Install GitHub CLI
# Windows
winget install GitHub.cli

# macOS
brew install gh

# Linux
sudo apt install gh  # Debian/Ubuntu
sudo dnf install gh  # Fedora

# Verify
gh --version
```

#### Authenticate

```bash
# Login to GitHub
gh auth login

# Follow prompts:
# - Select "GitHub.com"
# - Select "HTTPS"
# - Authenticate via web browser
```

#### Create Release

```bash
# Create release from tag
gh release create v1.0.0 \
  --title "v1.0.0 - Hackathon Phase 1 Complete" \
  --notes-file RELEASE_NOTES.md \
  --latest

# Or with inline notes
gh release create v1.0.0 \
  --title "v1.0.0 - Hackathon Phase 1 Complete" \
  --notes "🎉 CLI Todo Manager - Hackathon Phase 1 Release

Features:
✅ All 9 user stories complete
✅ 100% test coverage
✅ Production ready

See full release notes at:
https://github.com/Roofan-Jlove/Hackathon-II-TODO-APP/releases/tag/v1.0.0"
```

#### Verify Release

```bash
# List releases
gh release list

# View specific release
gh release view v1.0.0
```

---

### Release Notes Template

Use this template for GitHub releases:

```markdown
# 🎉 CLI Todo Manager - v[VERSION] Release

> Brief description of this release

[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue)](https://www.python.org/)
[![Test Coverage](https://img.shields.io/badge/test%20coverage-100%25-brightgreen)](./tests)

---

## 🚀 What's New in v[VERSION]

[Brief summary of major changes]

### New Features
✅ Feature 1
✅ Feature 2
✅ Feature 3

### Bug Fixes
🐛 Fix 1
🐛 Fix 2

### Improvements
⚡ Improvement 1
⚡ Improvement 2

---

## 📊 Statistics

- **Features Completed**: X/Y
- **Test Coverage**: XX/XX tests (100%)
- **Code Quality**: Production Ready

---

## 📦 Installation

```bash
git clone https://github.com/Roofan-Jlove/Hackathon-II-TODO-APP.git
cd Hackathon-II-TODO-APP
git checkout v[VERSION]
uv sync
uv run python src/main.py
```

---

## 📖 Documentation

- [README.md](./README.md) - User guide
- [CLAUDE.md](./CLAUDE.md) - Developer guide
- [PROCEDURES.md](./PROCEDURES.md) - Procedures

---

## 🐛 Known Issues

- Issue 1 (if any)
- Issue 2 (if any)

---

## 🙏 Contributors

- [@Roofan-Jlove](https://github.com/Roofan-Jlove)

---

**Full Changelog**: https://github.com/Roofan-Jlove/Hackathon-II-TODO-APP/compare/v[PREVIOUS]...v[VERSION]
```

---

## 🏗️ Deployment

### Running the Application

#### Development Mode

```bash
# Standard run
uv run python src/main.py

# With verbose output (if implemented)
uv run python src/main.py --verbose

# With specific Python version
uv run --python 3.13 python src/main.py
```

#### Production Mode

```bash
# Ensure clean environment
uv sync --frozen

# Run application
uv run python src/main.py
```

### Platform-Specific Notes

#### Windows

```powershell
# Ensure UTF-8 console support
chcp 65001

# Run application
uv run python src/main.py
```

#### macOS/Linux

```bash
# Ensure terminal supports UTF-8 and emojis
export LANG=en_US.UTF-8

# Run application
uv run python src/main.py
```

---

## 🔧 Maintenance

### Updating Dependencies

```bash
# Check for outdated packages
uv pip list --outdated

# Update specific package
uv add colorama@latest

# Update all packages
uv sync --upgrade

# Verify tests still pass
uv run python -m unittest discover -s tests -p "test_*.py" -v
```

### Code Quality Checks

```bash
# Check code style (if using ruff or black)
# Note: Not currently installed, but recommended for future

# Manual checks:
# 1. No hardcoded values
# 2. Proper error handling
# 3. Clear function names
# 4. Comprehensive docstrings
# 5. No unused imports
```

### Regular Maintenance Tasks

**Weekly:**
- [ ] Pull latest changes from remote
- [ ] Run all tests
- [ ] Check for security updates

**Monthly:**
- [ ] Review and update dependencies
- [ ] Review and close stale issues
- [ ] Update documentation if needed

**Per Release:**
- [ ] Update version numbers
- [ ] Update CHANGELOG.md
- [ ] Tag release
- [ ] Create GitHub release
- [ ] Test installation from scratch

---

## 🐛 Troubleshooting

### Common Issues

#### Issue 1: Tests Fail After Update

```bash
# Solution: Reinstall dependencies
uv sync --reinstall

# Verify
uv run python -m unittest discover -s tests -p "test_*.py" -v
```

#### Issue 2: UV Not Found

```bash
# Solution: Ensure UV is in PATH
# Windows: Add to PATH environment variable
# macOS/Linux: Add to ~/.bashrc or ~/.zshrc
export PATH="$HOME/.cargo/bin:$PATH"
```

#### Issue 3: Unicode/Emoji Not Displaying

```bash
# Windows Solution:
chcp 65001

# Or in PowerShell:
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# macOS/Linux Solution:
export LANG=en_US.UTF-8
```

#### Issue 4: Permission Denied on Scripts

```bash
# macOS/Linux Solution:
chmod +x .specify/scripts/bash/*.sh

# Verify
ls -la .specify/scripts/bash/
```

#### Issue 5: Git Tag Already Exists

```bash
# Delete local tag
git tag -d v1.0.0

# Delete remote tag
git push origin :refs/tags/v1.0.0

# Recreate tag
git tag -a v1.0.0 -m "Release notes..."
git push origin v1.0.0
```

---

## 📞 Support & Resources

### Documentation
- **User Guide**: [README.md](./README.md)
- **Developer Guide**: [CLAUDE.md](./CLAUDE.md)
- **This File**: [PROCEDURES.md](./PROCEDURES.md)

### External Resources
- **Python Docs**: https://docs.python.org/3.13/
- **UV Docs**: https://docs.astral.sh/uv/
- **Colorama Docs**: https://pypi.org/project/colorama/
- **python-dateutil Docs**: https://dateutil.readthedocs.io/

### Getting Help
- **GitHub Issues**: https://github.com/Roofan-Jlove/Hackathon-II-TODO-APP/issues
- **GitHub Discussions**: https://github.com/Roofan-Jlove/Hackathon-II-TODO-APP/discussions

---

## 📝 Quick Reference

### Essential Commands

```bash
# Setup
uv sync                          # Install dependencies
uv run python src/main.py        # Run application

# Testing
uv run python -m unittest discover -s tests -p "test_*.py" -v  # All tests

# Git
git status                       # Check status
git pull origin console-app      # Pull latest
git push origin console-app      # Push changes

# Release
git tag -a v1.0.0 -m "..."      # Create tag
git push origin v1.0.0          # Push tag
```

### File Structure

```
Project Root/
├── src/              # Source code
├── tests/            # Test files
├── specs/            # Specifications
├── .specify/         # Project config
├── README.md         # User guide
├── CLAUDE.md         # Developer guide
├── PROCEDURES.md     # This file
└── pyproject.toml    # UV configuration
```

---

<div align="center">

**Last Updated:** 2025-12-29
**Version:** 1.0.0
**Maintained by:** [@Roofan-Jlove](https://github.com/Roofan-Jlove)

[⬆ Back to Top](#-project-procedures---cli-todo-manager)

</div>
