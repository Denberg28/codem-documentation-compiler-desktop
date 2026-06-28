# CodeM Security Policy

## Supported Version

The current stable baseline is:

```text
CodeM v1.29.5
```

Security fixes should be applied first to the stable baseline before experimental branches.

## Security Model

CodeM is a local desktop application.

It is designed to manage local project documentation and publish files to GitHub through Git.

## Credentials

CodeM should not store:

- GitHub passwords
- GitHub personal access tokens
- API keys
- SSH private keys
- system passwords

Git authentication should be handled by Git, SSH agent, or Git Credential Manager.

## Repository URL Safety

Repository URLs should not contain embedded credentials.

Do not use:

```text
https://username:token@github.com/user/repo.git
```

Use:

```text
https://github.com/user/repo.git
```

or SSH:

```text
git@github.com:user/repo.git
```

## Image Upload Safety

Images should be local project evidence.

Recommended restrictions:

- use PNG, JPG, JPEG, GIF, WEBP, or BMP
- avoid oversized files
- avoid private or sensitive screenshots
- avoid images containing credentials or private data

## Documentation Safety

Before publishing to GitHub, review files for:

- passwords
- API keys
- private emails
- private phone numbers
- private addresses
- student records
- internal school documents
- sponsor information not approved for release

## Git Safety

Before publishing:

1. Pull updates.
2. Review README.
3. Confirm no sensitive files are included.
4. Use a clear commit message.
5. Push to GitHub.

## Recovery Safety

Recovery actions should preserve history.

A recovered state should create a new commit instead of silently deleting later work.

## Deletion Safety

Local deletion should move files to Recycle Bin when possible.

Avoid permanent deletion unless manually confirmed outside CodeM.

## Reporting a Security Issue

For personal/local use, record the issue in:

```text
docs/security_notes.md
```

For a public GitHub project, open a private security advisory or contact the repository owner directly.

Do not publish sensitive security details publicly until fixed.
