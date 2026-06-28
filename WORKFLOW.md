# CodeM Workflow

## Recommended Project Workflow

Use this workflow when documenting and publishing a project with CodeM.

## 1. Create or Open a Project

Start in the **Projects** tab.

For a new project:

1. Enter the project name.
2. Select the project type.
3. Fill in the objective template.
4. Choose the save location.
5. Click **Project Details** / create action.

For an existing project:

1. Select it from **Open Project**.
2. Confirm the current project label.
3. Continue editing in Docs, Parts, Exports, or Git.

## 2. Define the Project Objective

Use the objective template:

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

Keep the objective concise. This becomes part of the public GitHub project brief.

## 3. Write Documentation

Use the Docs tab for structured records:

- Overview
- Build Notes
- Testing
- Results
- Future Work

Each tab should answer a different question:

```text
Overview     = why the project exists
Build Notes  = what was built and how
Testing      = how it was tested
Results      = what was proven or learned
Future Work  = what happens next
```

Avoid repeating the same content in multiple tabs.

## 4. Add Parts and Images

Use the Parts tab to record hardware, software, tools, and materials.

Recommended fields:

- Code
- Part Number
- Description
- Quantity
- Unit of Measure
- Purpose
- Cost
- Supplier
- Image
- Notes

Use the image `+` button to attach local evidence or part images.

## 5. Save Revisions

Use **Save Revision** when the documentation reaches a meaningful milestone.

Examples:

- first working prototype
- first failed test
- fixed wiring issue
- final configuration
- test result evidence
- sponsor/demo version

Write a short revision comment explaining what changed.

## 6. Compile README

Use **Compile README** before publishing.

The README should act as a clean public landing page, not a full internal notebook.

Recommended README content:

```text
Project Brief
Overview
Hardware / Tools Used
Documentation Links
Build Notes
Testing
Results
Future Work
Project Structure
```

## 7. Publish to GitHub

Use the Git tab.

Recommended sync flow:

1. Validate repository URL.
2. Pull Updates.
3. Enter a clear commit message.
4. Publish to GitHub.

Good commit messages:

```text
Update build notes after motor wiring test
Add parts list and project objective
Record first bench test results
Fix README and attach evidence images
```

Avoid vague commit messages like:

```text
update
final
test
changes
```

## 8. Use Recovery Carefully

Use Recovery History only when you need to inspect or restore a previous commit.

Recovering should create a new commit and preserve history.

Do not rewrite history unless you fully understand the consequence.

## 9. Before Sharing a Project

Check:

- README is clean
- objective is clear
- parts list is saved
- images are included
- no passwords or tokens are in files
- GitHub repository opens correctly
- documentation links work

## 10. Stable Version Rule

Use:

```text
CodeM v1.29.5
```

as the firm baseline.

Future major changes should start from:

```text
v1.30.x
```

and should be tested separately.
