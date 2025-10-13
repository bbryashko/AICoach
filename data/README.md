# Data Directory

This directory contains application data including OAuth tokens and other sensitive information.

## 🔒 Security Notice

**IMPORTANT**: This directory contains sensitive authentication data:

- `tokens/` - OAuth access and refresh tokens for Strava API
- These tokens provide access to user accounts and should NEVER be shared
- All token files are automatically excluded from git via `.gitignore`

## 📁 Structure

```
data/
├── .gitignore          # Excludes sensitive files from git
├── README.md          # This file
└── tokens/            # OAuth token storage (git-ignored)
    ├── user1_strava.json
    ├── user2_strava.json
    └── ...
```

## 🚨 What to do if tokens are accidentally committed

If OAuth tokens are accidentally committed to git:

1. **Immediately revoke the tokens**: 
   - Go to https://www.strava.com/settings/apps
   - Revoke access for the AI Coach application
   
2. **Remove from git history**:
   ```bash
   git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch data/tokens/*.json' --prune-empty --tag-name-filter cat -- --all
   ```
   
3. **Re-authenticate users**:
   ```bash
   python main.py --oauth-setup <user_id>
   ```

## 🛡️ Token Management

- Tokens are automatically refreshed when they expire
- Each user has their own token file
- Tokens include both access tokens (short-lived) and refresh tokens (long-lived)
- Failed token refresh will require re-authentication via browser OAuth flow