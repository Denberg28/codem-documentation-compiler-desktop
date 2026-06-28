# CodeM FAQ

## What is CodeM?

CodeM is a local desktop application for compiling project documentation, parts lists, images, revisions, and GitHub-ready README files.

It is designed for research, engineering builds, UAV projects, electronics repair, software tools, and academic documentation.

## What is the stable baseline version?

The current firm foundation build is:

```text
CodeM v1.29.5
```

This version should be treated as the stable fallback before major refactoring or modularization.

## What problem does CodeM solve?

CodeM reduces the friction of documenting projects by combining:

- project setup
- documentation editing
- parts tracking
- image attachment
- revision saving
- README generation
- GitHub publishing
- recovery history

into one workflow.

## Does CodeM store my GitHub password or token?

No.

CodeM does not store GitHub passwords or access tokens. Authentication should remain handled by Git or Git Credential Manager.

## Where are project files stored?

Each project is stored as a local folder containing:

```text
project/
├── README.md
├── docs/
├── images/
├── parts/
├── tests/
├── logs/
├── references/
└── exports/
```

## What is the purpose of README.md?

`README.md` is the public-facing project landing page for GitHub.

It should be clean, readable, and focused on project overview, evidence, parts, and documentation links.

## Where should detailed documentation go?

Detailed documentation should stay inside:

```text
docs/
```

The README should link to details instead of becoming a long dump of every note.

## What is Save Revision for?

Save Revision creates a timestamped local record of important documentation changes.

Use it after meaningful updates such as:

- major build changes
- test results
- design decisions
- failures and fixes
- research findings

## Does deleting a recent project delete the GitHub repository?

No.

Deleting a recent local project only affects the local folder or recent-project entry. It does not delete the GitHub repository.

## Can CodeM be split into multiple Python files?

Yes, but the recommended approach is:

```text
v1.29.5 = stable monolithic foundation
v1.30.x = modular refactor branch
```

Do not split the code inside the stable release unless a full regression test is planned.

## What should be tested before building an EXE?

Before packaging CodeM, test:

- project creation
- project loading
- documentation save
- revision save
- parts list save
- image upload
- README compile
- GitHub pull
- GitHub publish
- recovery history
- project delete to recycle bin
