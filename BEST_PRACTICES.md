# CodeM Best Practices

## Documentation Principles

Good project documentation should be:

- clear
- traceable
- concise
- repeatable
- evidence-based
- easy to review on GitHub

## README Best Practice

The README should be a public project landing page.

It should not contain every internal note.

Use README for:

- project brief
- key objective
- parts summary
- documentation links
- current results
- project structure

Use `docs/` for detailed records.

## Folder Structure Best Practice

Recommended CodeM project structure:

```text
project/
├── README.md
├── docs/
│   └── revisions/
├── images/
├── parts/
├── tests/
├── logs/
├── references/
└── exports/
```

## Objective Best Practice

Use this structure:

```text
Purpose:
-

Problem / Need:
-

Target Output:
-

Success Criteria:
-

Scope / Limits:
-

Initial Notes:
-
```

The objective should explain what the project is trying to accomplish, not every technical detail.

## Revision Best Practice

Save a revision when a change is important enough that you may need to prove, compare, or recover it later.

Examples:

- configuration changed
- test completed
- build failed
- build succeeded
- evidence added
- design decision made

## Parts List Best Practice

Each row should represent a specific item, module, material, or tool.

Recommended notes:

- use standard part numbers where possible
- add supplier/source when known
- attach images for visual proof
- avoid vague names like "wire thing" or "motor stuff"

## Image Best Practice

Images should be used as evidence.

Good images include:

- wiring photos
- assembly photos
- test setup
- damaged component
- measurement proof
- result screenshot

Avoid uploading very large images when a compressed version is enough.

## GitHub Commit Best Practice

A commit message should explain the change.

Good format:

```text
Action + object + reason/context
```

Examples:

```text
Add parts images for rover build
Update testing notes after bench test
Fix README project brief formatting
Record ESC calibration results
```

## Security Best Practice

Never commit:

- passwords
- access tokens
- API keys
- private emails
- private addresses
- school internal credentials
- unapproved private documents

## Stable Release Best Practice

Keep a known-good version.

For CodeM:

```text
v1.29.5 = stable baseline
v1.30.x = future refactor branch
```

Do not mix major refactoring with urgent feature fixes.

## Refactor Best Practice

When splitting the application later:

1. Extract helper functions.
2. Extract Git logic.
3. Extract Markdown/README generation.
4. Extract parts/image logic.
5. Extract UI tabs.
6. Keep `main.py` as a small launcher.

Do not refactor everything in one uncontrolled change.
