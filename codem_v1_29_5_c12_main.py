"""
CodeM v1.29.5-c12-c2
Research-to-GitHub Compiler

Purpose:
    Create clean GitHub-ready project documentation and manage a safer,
    minimal Git workflow for solo and team documentation projects.

Design Principles:
    - Minimal workflow
    - No credential storage
    - Git identity is for commit attribution only
    - Recovery creates new history events instead of deleting history
    - Git tab split into Sync, History, and Repair pages
    - Recovery history is always visible in its own page
    - Fix Stuck Sync handles clean unfinished rebase states
    - Scrollable Sync page so all controls remain accessible on smaller screens
    - Markdown editor toolbar for headings, bullets, checklists, and code blocks
    - Auto-bullet continuation and Tab indentation
    - Conflict marker detection before saving
    - Normalize Markdown for cleaner GitHub rendering
    - GitHub pushes selected project folder as a folder, not loose root files
    - Existing project-name popup with open-existing option
    - Safer project-folder publishing workflow
    - Automatically protects old nested .git folders before staging
    - Pulls remote root first, then commits selected project folder
    - Simplified publish workflow: save, commit message, pull, push
    - Create Project button is disabled after a project is loaded to prevent accidental duplicate creation
    - Cleaner README compilation with placeholder filtering
    - Markdown normalization no longer creates nested checklist/bullet artifacts
    - Added README preview note to reduce confusion between docs tabs and compiled README
    - Markdown toolbar now replaces existing line style instead of stacking markdown
    - Removed Normalize Current button
    - Added editor-standard Undo, Redo, and Clean Selection actions
    - New projects are created at workspace level, not inside the currently loaded project
    - Current project name is visible in Docs, Parts, and Exports tabs
    - Improved editor undo/redo reliability with edit separators
    - Recent Projects right-click menu: open, rename, remove entry, delete local folder
    - Cleaner Parts table using Treeview editor
    - Current project badge shown in Docs, Parts, Exports, and Git tabs
    - Recent project delete now moves local folder to Recycle Bin when possible
    - Current project badge uses colored regular text instead of bold
    - Parts tab uses direct in-window spreadsheet-style entry
    - Parts list starts with 5 editable rows
    - Parts list uses fixed non-editable row numbering
    - Parts list columns updated to Code, Part Number, Description, Qty, UOM, Purpose, Cost, Supplier, Notes
    - Parts entry area stretches cleanly across the full tab width
    - Parts list now fits smaller screens using proportional columns
    - Parts cells use standard single-line entry fields
    - Parts rows use fixed clean row height for a spreadsheet-like layout
    - Parts cells are fixed-height wrap-capable text fields
    - Legacy parts CSV headers are migrated instead of appearing as row data
    - Parts table headers use regular weight text
    - Parts Add Row button adds one row at a time
    - Parts table header uses retained font size with bold weight
    - Parts grid supports arrow-key cell navigation
    - Documentation tabs use industry-style default templates
    - Restore Template button added for empty or reset documentation tabs
    - Build Notes, Testing, and Results can be saved as local revisioned records
    - Revisioned records use dedicated folders with automatic timestamped filenames
    - Revision save opens a comment popup and stores the comment inside the revision file
    - Save Revision is available for all documentation tabs
    - Save Revision button moved beside Save Docs for clearer workflow
    - Documentation toolbar simplified into essential grouped actions
    - Toolbar wraps into multiple rows on window resize
    - Documentation toolbar uses uniform button sizes and symmetrical grouped layout
    - Save/Revision and Undo/Redo controls grouped uniformly on the right
    - Docs action buttons align with Format/Edit toolbar rows
    - Toolbar tip moved to the far right of the current-project row
    - Fixed Pylance Callable type hint warning
    - Fixed Git tab layout to remove center blank scroll area
    - Git Sync page now uses compact left controls and full right Git Output
    - Kept v1.28.2 padding
    - Bottom action bar remains visible during window resize
    - Documentation templates updated to a non-redundant industry flow
    - Documentation editor supports image upload and file-path drop/paste
    - Uploaded images are copied into the project images folder
    - Inserted images use GitHub-compatible HTML image markup with width control
    - Fixed Pylance PhotoImage.subsample argument warning
    - Uses single-argument PhotoImage.subsample for type-checker compatibility
    - Removed unsupported Tkinter <Drop> binding to prevent startup crash
    - Parts tab includes Image column before Notes
    - Parts tab supports uploading an image from a plus button inside each Image cell
    - Removed Parts top Upload Image button
    - Prevents old parts header/template text from loading into row 1
    - Fixes old pre-image-column header rows causing false image checkmarks
    - Parts image cells now support right-click image actions
    - Opened projects can edit and save main project details
    - Project details edit mode keeps Project Name and Project Type read-only
    - Only Objective is editable for safer project metadata updates
    - Create tab buttons use uniform size and aligned layout
    - Create tab includes a standard objective template for new projects
    - Create tab action buttons are left-aligned
    - README output changed to a clean GitHub landing-page format
    - Objective template is converted into a compact Project Brief table
    - Empty documentation template sections are hidden from README
    - README uses direct document-tab content without redundant Summary wrapper headings
    - Promoted stable project-documentation workflow to v1.29.0
    - Project Brief table is left-aligned in GitHub README
    - Project Brief includes Current Revision row
    - Docs toolbar redesigned for half-window responsive use
    - Docs action buttons no longer disappear off-screen on narrow window sizes
    - Create tab labels renamed to clearer industry-standard project workflow labels
    - Documentation toolbar button height refined to a moderately compact standard
    - Security hardening: commit message sanitization
    - Security hardening: image upload size limit
    - Stability hardening: safer external image/path handling
    - c1: Create Project button label restored for clearer new-project action
    - c1: Windows subprocess calls hide black console windows for smoother EXE operation
    - c2: Create Project button label corrected in Projects tab
    - c2: Runtime window icon loading added for packaged EXE
    - c3: Popup centering and smoother UI operation handling
    - c3: Notebook tab switching focus polish
    - c4: smoother launch by hiding main window until UI is fully built
    - c4: recommended build changed to --onedir for faster, less jerky startup
    - c5: Save Docs and Save All preserve Markdown indentation
    - c6: Hidden text button added to Docs Format row
    - c7: Hidden text button uses explicit active Docs editor lookup for Pylance compatibility
    - c8: Hidden text feature supports all documentation editor tabs reliably
    - c9: Hidden text active editor fallback uses direct focus_get for Pylance compatibility
    - c10: Save Docs preserves GitHub hidden details blocks without auto-bullets
    - c11: Documentation templates and format heading button updated from H2 to H1
    - c12: GitHub documentation templates use H1 title and H2 section headers for readable size
"""

from __future__ import annotations

import csv
import json
import os
import re
import subprocess
import sys
import shutil
import hashlib
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox
from urllib.parse import urlparse
from collections.abc import Callable
import tkinter as tk
from tkinter import ttk


APP_NAME = "CodeM"
APP_SUBTITLE = "Research-to-GitHub Compiler"
APP_VERSION = "1.29.5-c12"

PROJECT_TYPES = [
    "UAV Build",
    "VTOL Research",
    "Drone Course",
    "Electronics Repair",
    "Software Tool",
    "Research Proposal",
    "General Project",
]

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"}

MAX_COMMIT_MESSAGE_LENGTH = 120
MAX_IMAGE_UPLOAD_BYTES = 20 * 1024 * 1024  # 20 MB



def resource_path(relative_path: str) -> Path:
    """
    Resolve files correctly in both source mode and PyInstaller onefile mode.
    Used for the application icon bundled with --add-data.
    """
    base_path = getattr(sys, "_MEIPASS", None)
    if base_path:
        return Path(base_path) / relative_path
    return Path(__file__).resolve().parent / relative_path


def windows_no_console_creationflags() -> int:
    """
    Prevent black console windows from flashing behind the Tkinter EXE on Windows.

    PyInstaller --windowed hides the main console, but subprocess calls such as Git,
    Explorer, or shell helpers can still briefly create console windows unless this
    creation flag is supplied.
    """
    if sys.platform.startswith("win"):
        return getattr(subprocess, "CREATE_NO_WINDOW", 0)
    return 0


DEFAULT_OBJECTIVE_TEMPLATE = """Purpose:
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
"""


OBJECTIVE_FIELDS = [
    "Purpose",
    "Problem / Need",
    "Target Output",
    "Success Criteria",
    "Scope / Limits",
    "Initial Notes",
]


def parse_objective_fields(text: str) -> dict[str, str]:
    """
    Convert the Create-tab objective template into clean key-value fields
    for README display.
    """
    fields: dict[str, list[str]] = {field: [] for field in OBJECTIVE_FIELDS}
    current_field: str | None = None

    for raw_line in text.splitlines():
        line = raw_line.strip()

        if not line:
            continue

        possible_field = line.rstrip(":")
        if possible_field in fields:
            current_field = possible_field
            continue

        if current_field is None:
            continue

        cleaned = line
        cleaned = re.sub(r"^[-*+]\s*", "", cleaned).strip()

        if cleaned:
            fields[current_field].append(cleaned)

    return {
        field: " ".join(values).strip()
        for field, values in fields.items()
    }


def get_current_revision_label(project_dir: Path) -> str:
    """
    Return the latest saved documentation revision filename across docs/revisions.
    If no revision exists yet, return a clear default.
    """
    revisions_dir = project_dir / "docs" / "revisions"
    if not revisions_dir.exists():
        return "No saved revision yet"

    revision_files = sorted(
        [path for path in revisions_dir.rglob("*.md") if path.is_file()],
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )

    if not revision_files:
        return "No saved revision yet"

    return revision_files[0].name


def objective_to_project_brief_markdown(objective: str, project_type: str, project_dir: Path | None = None) -> str:
    fields = parse_objective_fields(objective)
    current_revision = get_current_revision_label(project_dir) if project_dir is not None else "No saved revision yet"

    rows = [
        ("Project Type", project_type),
        ("Current Revision", current_revision),
        ("Purpose", fields.get("Purpose", "")),
        ("Problem / Need", fields.get("Problem / Need", "")),
        ("Target Output", fields.get("Target Output", "")),
        ("Success Criteria", fields.get("Success Criteria", "")),
        ("Scope / Limits", fields.get("Scope / Limits", "")),
    ]

    visible_rows = [(label, value) for label, value in rows if value.strip()]

    table = ["| Field | Details |", "|:---|:---|"]
    for label, value in visible_rows:
        table.append(f"| {safe_md_cell(label)} | {safe_md_cell(value)} |")

    return "\n".join(table)




def is_template_placeholder_line(line: str) -> bool:
    stripped = line.strip()
    return stripped in {"-", "- ", "- [ ]", "1.", "2.", "3."}


def compact_doc_summary(markdown: str, max_sections: int = 3) -> str:
    """
    Extract only meaningful non-template lines for README summary.
    This prevents README from becoming a dump of blank documentation templates.
    """
    text = cleaned_doc_body(markdown)
    lines = text.splitlines()

    output: list[str] = []
    section_count = 0
    skip_empty_section = False

    for raw_line in lines:
        line = raw_line.rstrip()
        stripped = line.strip()

        if not stripped:
            continue

        if is_template_placeholder_line(stripped):
            continue

        if stripped.startswith("# "):
            continue

        if stripped.startswith("## "):
            section_count += 1
            if section_count > max_sections:
                break
            output.append(stripped)
            skip_empty_section = True
            continue

        # Remove template instructional lines that are meant as prompts.
        lowered = stripped.lower()
        if lowered.startswith(("state ", "briefly ", "explain ", "list ", "document ")):
            continue

        output.append(stripped)
        skip_empty_section = False

    return "\n".join(output).strip()


def doc_tab_content_for_readme(markdown: str) -> str:
    """
    Use the document tab content directly inside README.

    This removes the tab's top-level # Title so README does not repeat:
        ## Results Summary
        # Results
        ## Result Summary

    It keeps the user's actual section headings and content.
    """
    text = cleaned_doc_body(markdown).strip()
    if not text:
        return ""

    lines = text.splitlines()

    # Remove the first H1 only. README already provides the outer section title.
    if lines and lines[0].strip().startswith("# "):
        lines = lines[1:]

    cleaned_lines: list[str] = []
    for line in lines:
        stripped = line.strip()

        # Skip empty placeholder-only lines, but keep normal blank spacing.
        if is_template_placeholder_line(stripped):
            continue

        cleaned_lines.append(line.rstrip())

    return "\n".join(cleaned_lines).strip()


DOC_TABS = {
    "Overview": Path("docs") / "overview.md",
    "Build Notes": Path("docs") / "build_notes.md",
    "Testing": Path("docs") / "testing.md",
    "Results": Path("docs") / "results.md",
    "Future Work": Path("docs") / "future_work.md",
}

REVISIONABLE_DOCS = {
    "Overview": "overview",
    "Build Notes": "build_notes",
    "Testing": "testing",
    "Results": "results",
    "Future Work": "future_work",
}

# Backward-compatible alias for older helper calls.
VERSIONABLE_DOCS = REVISIONABLE_DOCS

PARTS_HEADERS = ["Code", "Part Number", "Description", "Qty", "UOM", "Purpose", "Cost", "Supplier", "Image", "Notes"]
LEGACY_PARTS_HEADERS = ["Item", "Model", "Quantity", "Purpose", "Cost", "Supplier", "Notes"]
PRE_IMAGE_PARTS_HEADERS = ["Code", "Part Number", "Description", "Qty", "UOM", "Purpose", "Cost", "Supplier", "Notes"]

DEFAULT_BASE_DIR = Path.home() / "Documents" / "CodeMProjects"
APP_CONFIG_DIR = Path.home() / ".codem"
APP_CONFIG_FILE = APP_CONFIG_DIR / "config.json"


# =============================================================================
# General helpers
# =============================================================================

def now_string() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def slugify_project_name(name: str) -> str:
    cleaned = name.strip()
    cleaned = re.sub(r"[^\w\s-]", "", cleaned)
    cleaned = re.sub(r"[\s-]+", "_", cleaned)
    return cleaned.strip("_") or "Untitled_Project"


def load_config() -> dict:
    APP_CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    default_config = {
        "base_dir": str(DEFAULT_BASE_DIR),
        "recent_projects": [],
    }

    if not APP_CONFIG_FILE.exists():
        save_config(default_config)
        return default_config

    try:
        data = json.loads(APP_CONFIG_FILE.read_text(encoding="utf-8"))
        return {**default_config, **data}
    except (OSError, json.JSONDecodeError):
        save_config(default_config)
        return default_config


def save_config(config: dict) -> None:
    APP_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    APP_CONFIG_FILE.write_text(json.dumps(config, indent=2), encoding="utf-8")


def write_text_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def read_text_file(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def is_image_file(path: Path) -> bool:
    return path.suffix.lower() in IMAGE_EXTENSIONS and path.exists() and path.is_file()


def sanitize_commit_message(message: str) -> str:
    """
    Keep Git commit messages safe and readable for logs.

    This is not for shell injection prevention because CodeM uses subprocess
    argument lists. It prevents confusing multiline/control-character output.
    """
    cleaned = re.sub(r"[\r\n\t]+", " ", message)
    cleaned = re.sub(r"[\x00-\x1f\x7f]", "", cleaned)
    cleaned = re.sub(r"\s{2,}", " ", cleaned).strip()

    if len(cleaned) > MAX_COMMIT_MESSAGE_LENGTH:
        cleaned = cleaned[:MAX_COMMIT_MESSAGE_LENGTH].rstrip()

    return cleaned or "Update CodeM project documentation"


def validate_image_upload_size(path: Path) -> None:
    size = path.stat().st_size
    if size > MAX_IMAGE_UPLOAD_BYTES:
        size_mb = size / (1024 * 1024)
        limit_mb = MAX_IMAGE_UPLOAD_BYTES / (1024 * 1024)
        raise ValueError(
            f"Image file is too large ({size_mb:.1f} MB). "
            f"Maximum allowed size is {limit_mb:.0f} MB."
        )


def safe_image_filename(source_path: Path) -> str:
    stem = slugify_project_name(source_path.stem)
    digest = hashlib.sha1(str(source_path).encode("utf-8")).hexdigest()[:8]
    return f"{stem}_{digest}{source_path.suffix.lower()}"


def copy_image_to_project(project_dir: Path, source_path: Path) -> Path:
    if not is_image_file(source_path):
        raise ValueError("Selected file is not a supported image.")

    validate_image_upload_size(source_path)

    images_dir = project_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    destination = images_dir / safe_image_filename(source_path)
    if not destination.exists():
        shutil.copy2(source_path, destination)

    return destination


def timestamp_for_filename() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def get_doc_revision_folder(project_dir: Path, doc_label: str) -> Path:
    safe_doc_name = REVISIONABLE_DOCS[doc_label]
    return project_dir / "docs" / "revisions" / safe_doc_name


def save_doc_revision(project_dir: Path, doc_label: str, content: str, comment: str = "") -> Path:
    if doc_label not in REVISIONABLE_DOCS:
        raise ValueError(f"{doc_label} does not support revisioned saving.")

    safe_doc_name = REVISIONABLE_DOCS[doc_label]
    revision_folder = get_doc_revision_folder(project_dir, doc_label)
    revision_folder.mkdir(parents=True, exist_ok=True)

    timestamp = timestamp_for_filename()
    readable_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output_path = revision_folder / f"{safe_doc_name}_{timestamp}.md"

    revision_header = (
        f"# {doc_label} Revision Record\n\n"
        f"**Saved At:** {readable_timestamp}\n\n"
        f"**Revision File:** `{output_path.name}`\n\n"
        f"**Comment:** {comment.strip() or 'No comment provided.'}\n\n"
        "---\n\n"
    )

    output_path.write_text(revision_header + content.rstrip() + "\n", encoding="utf-8")
    return output_path


    safe_doc_name = REVISIONABLE_DOCS[doc_label]
    revision_folder = get_doc_revision_folder(project_dir, doc_label)
    revision_folder.mkdir(parents=True, exist_ok=True)

    output_path = revision_folder / f"{safe_doc_name}_{timestamp_for_filename()}.md"
    output_path.write_text(content.rstrip() + "\n", encoding="utf-8")
    return output_path


def open_folder(path: Path) -> None:
    try:
        if sys.platform.startswith("win"):
            os.startfile(path)  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.run(["open", str(path)], check=False)
        else:
            subprocess.run(["xdg-open", str(path)], check=False)
    except OSError as error:
        messagebox.showerror("Open Folder Failed", str(error))


def get_project_git_root(project_dir: Path) -> Path:
    """
    GitHub repository root for CodeM.

    Intentional industry behavior:
    - The Git repository is initialized in the parent folder.
    - Only the selected project folder is staged and committed.
    - GitHub receives: Project_Folder/README.md, Project_Folder/docs/...
    - This avoids conflicts with GitHub-created root README/license files.
    """
    return project_dir.parent


def get_project_repo_path(project_dir: Path) -> str:
    return project_dir.name


def move_path_to_recycle_bin(path: Path) -> tuple[bool, str]:
    """
    Move a file/folder to the system recycle bin when possible.

    Safety priority:
    1. Use send2trash if available.
    2. Use Windows SHFileOperation with recycle-bin support.
    3. On Linux/macOS fallback, move to a CodeM trash folder in the user's home.
    """
    if not path.exists():
        return True, "Path does not exist."

    try:
        from send2trash import send2trash  # type: ignore
        send2trash(str(path))
        return True, "Moved to Recycle Bin."
    except Exception:
        pass

    if sys.platform.startswith("win"):
        try:
            import ctypes
            from ctypes import wintypes

            FO_DELETE = 3
            FOF_ALLOWUNDO = 0x0040
            FOF_NOCONFIRMATION = 0x0010
            FOF_SILENT = 0x0004

            class SHFILEOPSTRUCTW(ctypes.Structure):
                _fields_ = [
                    ("hwnd", wintypes.HWND),
                    ("wFunc", wintypes.UINT),
                    ("pFrom", wintypes.LPCWSTR),
                    ("pTo", wintypes.LPCWSTR),
                    ("fFlags", ctypes.c_uint16),
                    ("fAnyOperationsAborted", wintypes.BOOL),
                    ("hNameMappings", wintypes.LPVOID),
                    ("lpszProgressTitle", wintypes.LPCWSTR),
                ]

            operation = SHFILEOPSTRUCTW()
            operation.hwnd = None
            operation.wFunc = FO_DELETE
            operation.pFrom = str(path) + "\0\0"
            operation.pTo = None
            operation.fFlags = FOF_ALLOWUNDO | FOF_NOCONFIRMATION | FOF_SILENT

            result = ctypes.windll.shell32.SHFileOperationW(ctypes.byref(operation))
            if result == 0:
                return True, "Moved to Recycle Bin."
            return False, f"Windows recycle operation failed with code {result}."
        except Exception as error:
            return False, f"Recycle Bin operation failed: {error}"

    try:
        trash_dir = Path.home() / ".codem_trash"
        trash_dir.mkdir(parents=True, exist_ok=True)

        destination = trash_dir / path.name
        if destination.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            destination = trash_dir / f"{path.name}_{timestamp}"

        shutil.move(str(path), str(destination))
        return True, f"Moved to CodeM trash: {destination}"
    except OSError as error:
        return False, f"Could not move to trash: {error}"


def protect_nested_git_folder(project_dir: Path) -> tuple[bool, str]:
    """
    Prevent nested Git repositories from breaking parent-repo staging.

    Older CodeM revisions initialized .git inside the project folder.
    CodeM v1.29.5-c12-c2 publishes the project folder from its parent repo, so a nested
    project/.git must be moved aside before `git add Project_Folder`.

    This does NOT delete history. It renames:
        Project/.git
    to:
        Project/.git_codem_nested_backup_YYYYMMDD_HHMMSS
    """
    nested_git = project_dir / ".git"

    if not nested_git.exists():
        return True, "No nested .git folder found."

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = project_dir / f".git_codem_nested_backup_{timestamp}"

    try:
        nested_git.rename(backup)
        return True, f"Nested .git protected: {backup.name}"
    except OSError as error:
        return False, f"Failed to protect nested .git: {error}"


def git_has_commits(path: Path) -> bool:
    success, _output = run_git_command(path, ["rev-parse", "--verify", "HEAD"])
    return success


def git_remote_has_main(path: Path) -> bool:
    success, _output = run_git_command(path, ["ls-remote", "--exit-code", "--heads", "origin", "main"])
    return success


# =============================================================================
# Markdown helpers
# =============================================================================

CONFLICT_MARKERS = ("<<<<<<<", "=======", ">>>>>>>")


def has_conflict_markers(text: str) -> bool:
    return any(line.lstrip().startswith(CONFLICT_MARKERS) for line in text.splitlines())


def strip_conflict_marker_lines(text: str) -> str:
    """
    Remove visible Git conflict marker lines while preserving user content.

    This does not decide which side is correct. It simply removes:
    <<<<<<< ...
    =======
    >>>>>>> ...
    """
    cleaned_lines = [
        line for line in text.splitlines()
        if not line.lstrip().startswith(CONFLICT_MARKERS)
    ]
    return "\n".join(cleaned_lines).rstrip() + "\n"


def is_placeholder_line(stripped: str) -> bool:
    placeholders = {
        "-",
        "- ",
        "- -",
        "- [ ]",
        "- [ ] -",
        "- [ ]  -",
        "o",
        "○",
        "◦",
    }
    return stripped.strip() in placeholders


def normalize_markdown_lists(text: str) -> str:
    """
    GitHub-friendly Markdown normalization without destroying indentation or HTML blocks.

    Critical behavior:
    - Preserve Markdown indentation.
    - Preserve GitHub hidden blocks:
      <details>
      <summary>...</summary>
      </details>
    - Do not auto-add bullets inside <details> blocks.
    - Repair older broken hidden blocks that were saved as '- <details>'.
    """
    list_sections = {
        "notes",
        "evidence",
        "results",
        "conclusion",
        "future work",
        "issues",
        "issues encountered",
        "testing",
        "observations",
        "references",
    }

    output: list[str] = []
    current_section = ""
    in_code_block = False
    in_details_block = False

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if stripped.startswith("```"):
            in_code_block = not in_code_block
            output.append(line)
            continue

        if in_code_block:
            output.append(line)
            continue

        if not stripped:
            output.append("")
            continue

        if is_placeholder_line(stripped):
            continue

        leading = line[: len(line) - len(line.lstrip(" \t"))]
        body = line[len(leading):]
        body_stripped = body.strip()

        # Repair hidden blocks accidentally converted into bullets by older saves.
        body_stripped = re.sub(r"^[-*+]\s+(</?details\b[^>]*>)\s*$", r"\1", body_stripped, flags=re.IGNORECASE)
        body_stripped = re.sub(r"^[-*+]\s+(<summary\b[^>]*>.*?</summary>)\s*$", r"\1", body_stripped, flags=re.IGNORECASE)

        # Fix common toolbar/normalizer artifacts while preserving indent.
        body_stripped = re.sub(r"^-\s+\[\s*\]\s+-\s+", "- [ ] ", body_stripped)
        body_stripped = re.sub(r"^-\s+-\s+", "- ", body_stripped)

        lower_body = body_stripped.lower()

        # Preserve GitHub collapsible details blocks exactly.
        if re.match(r"^<details\b[^>]*>$", body_stripped, flags=re.IGNORECASE):
            in_details_block = True
            output.append(f"{leading}{body_stripped}")
            continue

        if re.match(r"^<summary\b[^>]*>.*</summary>$", body_stripped, flags=re.IGNORECASE):
            output.append(f"{leading}{body_stripped}")
            continue

        if re.match(r"^</details>$", body_stripped, flags=re.IGNORECASE):
            output.append(f"{leading}{body_stripped}")
            in_details_block = False
            continue

        # Preserve all content inside hidden details blocks. Do not auto-bullet it.
        if in_details_block:
            output.append(line)
            continue

        heading_match = re.match(r"^(#{1,6})\s+(.+)$", body_stripped)
        if heading_match and not leading:
            current_section = heading_match.group(2).strip().lower()
            output.append(body_stripped)
            continue

        # Preserve common Markdown and HTML structures.
        already_structured = (
            body_stripped.startswith(("- ", "* ", "+ ", "> ", "|", "![", "[", "<"))
            or bool(re.match(r"^\d+\.\s+", body_stripped))
            or bool(re.match(r"^-\s+\[[ xX]\]\s+", body_stripped))
            or body_stripped.startswith("---")
        )

        if already_structured:
            output.append(f"{leading}{body_stripped}")
            continue

        # Only auto-bullet unindented plain lines under specific list-style sections.
        # Indented lines are user-authored structure and must be preserved.
        if current_section in list_sections and not leading:
            output.append(f"- {body_stripped}")
        else:
            output.append(f"{leading}{body_stripped}")

    normalized = "\n".join(output).strip() + "\n"
    normalized = re.sub(r"\n{3,}", "\n\n", normalized)
    return normalized




def cleaned_doc_body(markdown: str) -> str:
    """
    Prepare a doc body for README compilation.

    This strips the first heading, removes conflict markers, normalizes Markdown,
    and removes empty template-only sub-sections.
    """
    text = strip_conflict_marker_lines(markdown) if has_conflict_markers(markdown) else markdown
    text = extract_body(text)
    text = normalize_markdown_lists(text)

    lines = text.splitlines()
    cleaned: list[str] = []

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Drop empty template subsections:
        # ## Notes
        # ## Evidence
        # ## Conclusion
        if stripped.startswith("## "):
            section_lines: list[str] = []
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith("## "):
                if lines[j].strip():
                    section_lines.append(lines[j].strip())
                j += 1

            meaningful = [entry for entry in section_lines if not is_placeholder_line(entry)]
            if not meaningful:
                i = j
                continue

        cleaned.append(line)
        i += 1

    return "\n".join(cleaned).strip()




# =============================================================================
# Project generation
# =============================================================================

def generate_doc(title: str, instruction: str) -> str:
    return generate_industry_doc_template(title, instruction)


def generate_industry_doc_template(title: str, instruction: str) -> str:
    """
    Generate concise documentation templates with a non-redundant project flow.

    Intended flow:
    - Overview: why, scope, and success criteria
    - Build Notes: what was built and how
    - Testing: how it was tested
    - Results: what the evidence proves
    - Future Work: what happens next
    """
    normalized_title = title.strip().lower()

    if normalized_title == "overview":
        return """# Overview

## Purpose
State what this project is intended to accomplish.

## Problem / Need
Explain the problem, requirement, or opportunity that led to this project.

## Scope
- Included:
- Not included:

## Objectives
- 

## Success Criteria
- 
"""

    if normalized_title == "build notes":
        return """# Build Notes

## Build Summary
Briefly describe what was built, assembled, configured, or changed.

## Materials / Tools Used
- 

## Implementation Steps
1. 
2. 
3. 

## Configuration / Settings
- 

## Design Decisions
- Decision:
  - Reason:

## Issues and Fixes
- Issue:
  - Cause:
  - Fix:
"""

    if normalized_title == "testing":
        return """# Testing

## Test Objective
State what the test is intended to verify.

## Test Setup
- Date:
- Location:
- Equipment:
- Configuration:

## Test Procedure
1. 
2. 
3. 

## Observations
- 

## Test Outcome
- Pass / Fail:
- Notes:
"""

    if normalized_title == "results":
        return """# Results

## Result Summary
Briefly state the final or current outcome.

## Key Findings
- 

## Evidence
- Photos:
- Logs:
- Measurements:
- References:

## Interpretation
Explain what the evidence means and why it matters.

## Lessons Learned
- 

## Conclusion
- 
"""

    if normalized_title == "future work":
        return """# Future Work

## Next Actions
- 

## Improvements
- 

## Pending Tests
- 

## Parts / Resources Needed
- 

## Risks / Limitations
- 

## Long-Term Opportunities
- 
"""

    return f"""# {title}

{instruction}

## Notes
- 
"""




def create_parts_csv(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(PARTS_HEADERS)


def load_parts_csv(path: Path) -> list[list[str]]:
    if not path.exists():
        return []

    with path.open("r", newline="", encoding="utf-8") as file:
        rows = list(csv.reader(file))

    if not rows:
        return []

    header = rows[0]
    data_rows = rows

    # New format: skip header directly.
    if header == PARTS_HEADERS:
        data_rows = rows[1:]

    # Old format from early CodeM revisions:
    # Item, Model, Quantity, Purpose, Cost, Supplier, Notes
    # Convert to:
    # Code, Part Number, Description, Qty, UOM, Purpose, Cost, Supplier, Notes
    elif header == LEGACY_PARTS_HEADERS:
        converted: list[list[str]] = []
        for old_row in rows[1:]:
            padded_old = old_row[: len(LEGACY_PARTS_HEADERS)] + [""] * (len(LEGACY_PARTS_HEADERS) - len(old_row))
            item, model, quantity, purpose, cost, supplier, notes = padded_old
            converted.append([
                item,       # Code
                model,      # Part Number
                "",         # Description
                quantity,   # Qty
                "",         # UOM
                purpose,    # Purpose
                cost,       # Cost
                supplier,   # Supplier
                "",         # Image
                notes,      # Notes
            ])
        data_rows = converted

    normalized: list[list[str]] = []

    for row in data_rows:
        # Prevent old/new header text from becoming row data if a CSV was previously mismatched.
        compact_row = [cell.strip() for cell in row if cell.strip()]
        compact_legacy = [cell.strip() for cell in LEGACY_PARTS_HEADERS]
        compact_current = [cell.strip() for cell in PARTS_HEADERS]
        compact_pre_image = [cell.strip() for cell in PRE_IMAGE_PARTS_HEADERS]

        if compact_row in (compact_legacy, compact_current, compact_pre_image):
            continue

        padded = row[: len(PARTS_HEADERS)] + [""] * (len(PARTS_HEADERS) - len(row))

        # Also skip header-like data from older builds, including rows saved
        # before the Image column existed where Notes shifted into Image.
        lowered = [cell.strip().lower() for cell in padded]
        current_lower = [cell.strip().lower() for cell in PARTS_HEADERS]
        pre_image_lower = [cell.strip().lower() for cell in PRE_IMAGE_PARTS_HEADERS]

        if lowered[: len(current_lower)] == current_lower:
            continue

        if lowered[: len(pre_image_lower)] == pre_image_lower:
            continue

        if (
            lowered[0:8] == [cell.lower() for cell in PRE_IMAGE_PARTS_HEADERS[:8]]
            and lowered[8] == "notes"
        ):
            continue

        if any(cell.strip() for cell in padded):
            normalized.append(padded)

    return normalized


def save_parts_csv(path: Path, rows: list[list[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(PARTS_HEADERS)

        for row in rows:
            padded = row[: len(PARTS_HEADERS)] + [""] * (len(PARTS_HEADERS) - len(row))
            if any(cell.strip() for cell in padded):
                writer.writerow(padded)


def extract_body(markdown: str) -> str:
    lines = markdown.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    return "\n".join(lines).strip()


def safe_md_cell(value: str) -> str:
    return value.replace("|", "\\|").strip()


def generate_parts_markdown(rows: list[list[str]]) -> str:
    if not rows:
        return (
            "| No. | Code | Part Number | Description | Qty | UOM | Purpose | Cost | Supplier | Image | Notes |\n"
            "|---|---|---|---|---|---|---|---|---|---|---|\n"
            "| 1 |  |  |  |  |  |  |  |  |  |  |"
        )

    table = [
        "| No. | Code | Part Number | Description | Qty | UOM | Purpose | Cost | Supplier | Image | Notes |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]

    for index, row in enumerate(rows, start=1):
        padded = row[: len(PARTS_HEADERS)] + [""] * (len(PARTS_HEADERS) - len(row))
        image_value = padded[8].strip()
        image_cell = f'<img src="{safe_md_cell(image_value)}" width="120">' if image_value else ""
        cells = [
            str(index),
            safe_md_cell(padded[0]),
            safe_md_cell(padded[1]),
            safe_md_cell(padded[2]),
            safe_md_cell(padded[3]),
            safe_md_cell(padded[4]),
            safe_md_cell(padded[5]),
            safe_md_cell(padded[6]),
            safe_md_cell(padded[7]),
            image_cell,
            safe_md_cell(padded[9]),
        ]
        table.append("| " + " | ".join(cells) + " |")

    return "\n".join(table)


def generate_readme(project_name: str, project_type: str, objective: str) -> str:
    title = project_name.strip() or "Untitled Project"
    objective = objective.strip() or "State the main objective of the project."

    return f"""# {title}

## Objective
{objective}

## Project Type
{project_type}

## Overview
Briefly describe the project, the problem it solves, and why it matters.

## Hardware / Tools Used
| Item | Model | Purpose | Notes |
|---|---|---|---|
|  |  |  |  |

## Build Notes
Document the build process, wiring, configuration, and important decisions.

## Testing
Record test methods, observations, and evidence.

## Results
Summarize what worked, what failed, and what was learned.

## Issues Encountered
List problems, probable causes, and fixes.

## Future Work
List improvements, next steps, and research continuation.

## Repository Structure
```text
.
├── README.md
├── project.json
├── docs/
│   └── revisions/
├── images/
├── parts/
├── tests/
├── logs/
├── references/
└── exports/
```

## Generated By
CodeM — Research-to-GitHub Compiler

## License
MIT License
"""


def create_project_structure(base_dir: Path, project_name: str, project_type: str, objective: str) -> Path:
    safe_name = slugify_project_name(project_name)
    project_dir = base_dir / safe_name

    if project_dir.exists():
        raise FileExistsError(f"Project folder already exists:\n{project_dir}")

    for folder_name in ["docs", "images", "parts", "tests", "logs", "references", "exports"]:
        (project_dir / folder_name).mkdir(parents=True, exist_ok=True)

    for revision_folder in REVISIONABLE_DOCS.values():
        (project_dir / "docs" / "revisions" / revision_folder).mkdir(parents=True, exist_ok=True)

    metadata = {
        "project_name": project_name.strip(),
        "folder_name": safe_name,
        "project_type": project_type,
        "objective": objective.strip(),
        "created_at": now_string(),
        "updated_at": now_string(),
        "app": APP_NAME,
        "app_revision": APP_VERSION,
    }

    write_text_file(project_dir / "project.json", json.dumps(metadata, indent=2))
    write_text_file(project_dir / "README.md", generate_readme(project_name, project_type, objective))

    starter_docs = {
        "overview.md": generate_doc("Overview", "Explain the project background and why it matters."),
        "build_notes.md": generate_doc("Build Notes", "Document assembly, wiring, configuration, and important decisions."),
        "testing.md": generate_doc("Testing", "Record test methods, setup, observations, and evidence."),
        "results.md": generate_doc("Results", "Summarize what worked, what failed, and what was learned."),
        "future_work.md": generate_doc("Future Work", "List improvements, next steps, and research continuation."),
    }

    for filename, content in starter_docs.items():
        write_text_file(project_dir / "docs" / filename, content)

    create_parts_csv(project_dir / "parts" / "parts_list.csv")

    write_text_file(
        project_dir / "tests" / "test_log.md",
        generate_doc("Test Log", "Add dated test entries, results, problems, fixes, and conclusions."),
    )

    write_text_file(
        project_dir / "logs" / "change_log.md",
        "# Change Log\n\n"
        f"## {now_string()}\n"
        "- Project created using CodeM.\n",
    )

    return project_dir


def read_project_metadata(project_dir: Path) -> dict:
    metadata_path = project_dir / "project.json"
    if not metadata_path.exists():
        return {}

    try:
        return json.loads(metadata_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def summarize_markdown_section(text: str, fallback: str) -> str:
    body = extract_body(text)
    lines = [line.strip() for line in body.splitlines() if line.strip() and not line.strip().startswith("#")]
    clean_lines = [line for line in lines if line not in {"-", "- "}]

    if not clean_lines:
        return fallback

    summary = " ".join(clean_lines)
    return summary[:900].rstrip() + ("..." if len(summary) > 900 else "")


def generate_readme_from_project(project_dir: Path) -> str:
    metadata = read_project_metadata(project_dir)
    if metadata is None:
        raise FileNotFoundError("Missing project.json")

    project_name = metadata.get("project_name", project_dir.name)
    project_type = metadata.get("project_type", "General Project")
    objective = metadata.get("objective", "")

    parts_rows = load_parts_csv(project_dir / "parts" / "parts_list.csv")
    parts_table = generate_parts_markdown(parts_rows)

    overview = doc_tab_content_for_readme(read_text_file(project_dir / DOC_TABS["Overview"]))
    build_notes = doc_tab_content_for_readme(read_text_file(project_dir / DOC_TABS["Build Notes"]))
    testing = doc_tab_content_for_readme(read_text_file(project_dir / DOC_TABS["Testing"]))
    results = doc_tab_content_for_readme(read_text_file(project_dir / DOC_TABS["Results"]))
    future_work = doc_tab_content_for_readme(read_text_file(project_dir / DOC_TABS["Future Work"]))

    project_brief = objective_to_project_brief_markdown(objective, project_type, project_dir)

    doc_links = "\n".join(
        f"- [{label}]({relative_path.as_posix()})"
        for label, relative_path in DOC_TABS.items()
    )

    sections: list[str] = [
        f"# {project_name}",
        "",
        "## Project Brief",
        project_brief,
        "",
        "## Overview",
        overview or "This project is currently being documented.",
        "",
        "## Hardware / Tools Used",
        parts_table,
        "",
        "## Documentation",
        doc_links,
    ]

    if build_notes:
        sections.extend(["", "## Build Notes", build_notes])

    if testing:
        sections.extend(["", "## Testing", testing])

    if results:
        sections.extend(["", "## Results", results])

    if future_work:
        sections.extend(["", "## Future Work", future_work])

    sections.extend(
        [
            "",
            "## Project Structure",
            "```text",
            f"{project_dir.name}/",
            "├── README.md",
            "├── docs/",
            "│   └── revisions/",
            "├── images/",
            "├── parts/",
            "├── tests/",
            "├── logs/",
            "├── references/",
            "└── exports/",
            "```",
            "",
            "---",
            "Generated with CodeM.",
            "",
        ]
    )

    return "\n".join(sections)




def generate_showcase_brief(project_dir: Path) -> str:
    metadata = read_project_metadata(project_dir)

    project_name = metadata.get("project_name", project_dir.name)
    project_type = metadata.get("project_type", "General Project")
    objective = metadata.get("objective", "State the main objective of the project.")

    overview = summarize_markdown_section(
        read_text_file(project_dir / DOC_TABS["Overview"]),
        "Briefly explain the project and why it matters.",
    )
    results = summarize_markdown_section(
        read_text_file(project_dir / DOC_TABS["Results"]),
        "Summarize the current result, output, or proof of progress.",
    )
    future_work = summarize_markdown_section(
        read_text_file(project_dir / DOC_TABS["Future Work"]),
        "List the next practical steps for improvement or continuation.",
    )

    parts_rows = load_parts_csv(project_dir / "parts" / "parts_list.csv")
    parts_summary = "\n".join(
        f"- {row[0]} {f'({row[1]})' if row[1] else ''}".strip()
        for row in parts_rows[:8]
        if row and row[0].strip()
    ) or "- Add key parts, tools, or resources used."

    return f"""# {project_name}

## One-Page Project Showcase

**Project Type:** {project_type}  
**Status:** In Development  
**Generated:** {now_string()}

## Objective
{objective}

## Problem / Opportunity
{overview}

## Solution / Work Completed
{results}

## Key Parts / Tools
{parts_summary}

## Research / Practical Value
This project creates documented proof of technical work that can support learning, research continuation, school presentation, collaboration, and future funding.

## Next Step
{future_work}

## Generated By
CodeM — Research-to-GitHub Compiler
"""


# =============================================================================
# Git helpers
# =============================================================================

def run_git_command(path: Path, args: list[str]) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=path,
            capture_output=True,
            text=True,
            check=False,
            creationflags=windows_no_console_creationflags(),
        )
        output = (result.stdout.strip() + "\n" + result.stderr.strip()).strip()
        return result.returncode == 0, output or "Command completed."
    except FileNotFoundError:
        return False, "Git is not installed or not available in PATH."
    except OSError as error:
        return False, str(error)


def get_git_dir(path: Path) -> Path | None:
    success, output = run_git_command(path, ["rev-parse", "--git-dir"])
    if not success:
        return None

    git_dir = Path(output.strip())
    if not git_dir.is_absolute():
        git_dir = path / git_dir
    return git_dir


def git_operation_state(path: Path) -> str:
    git_dir = get_git_dir(path)
    if git_dir is None:
        return "not initialized"

    if (git_dir / "rebase-merge").exists() or (git_dir / "rebase-apply").exists():
        return "rebase in progress"
    if (git_dir / "MERGE_HEAD").exists():
        return "merge in progress"
    if (git_dir / "CHERRY_PICK_HEAD").exists():
        return "cherry-pick in progress"

    return "clean"


def git_init(path: Path) -> tuple[bool, str]:
    return run_git_command(path, ["init"])


def git_status_short(path: Path) -> tuple[bool, str]:
    return run_git_command(path, ["status", "--short"])


def git_status_full(path: Path) -> tuple[bool, str]:
    return run_git_command(path, ["status"])


def git_add_all(path: Path) -> tuple[bool, str]:
    return run_git_command(path, ["add", "."])


def git_add_project_folder(git_root: Path, project_dir: Path) -> tuple[bool, str]:
    return run_git_command(git_root, ["add", get_project_repo_path(project_dir)])


def git_commit(path: Path, message: str) -> tuple[bool, str]:
    return run_git_command(path, ["commit", "-m", message])


def git_branch_main(path: Path) -> tuple[bool, str]:
    return run_git_command(path, ["branch", "-M", "main"])


def git_add_or_set_remote(path: Path, remote_url: str) -> tuple[bool, str]:
    success, output = run_git_command(path, ["remote", "add", "origin", remote_url])
    if not success and "remote origin already exists" in output.lower():
        return run_git_command(path, ["remote", "set-url", "origin", remote_url])
    return success, output


def git_pull_rebase_autostash(path: Path) -> tuple[bool, str]:
    return run_git_command(path, ["pull", "--rebase", "--autostash", "origin", "main"])


def git_fetch_origin(path: Path) -> tuple[bool, str]:
    return run_git_command(path, ["fetch", "origin"])


def git_pull_merge_allow_unrelated(path: Path) -> tuple[bool, str]:
    return run_git_command(path, ["pull", "--allow-unrelated-histories", "--no-edit", "origin", "main"])


def git_push_main(path: Path) -> tuple[bool, str]:
    return run_git_command(path, ["push", "-u", "origin", "main"])


def git_get_user(path: Path) -> tuple[bool, str]:
    return run_git_command(path, ["config", "--get", "user.name"])


def git_get_email(path: Path) -> tuple[bool, str]:
    return run_git_command(path, ["config", "--get", "user.email"])


def git_set_identity(path: Path, username: str, email: str) -> tuple[bool, str]:
    ok_name, out_name = run_git_command(path, ["config", "user.name", username])
    ok_email, out_email = run_git_command(path, ["config", "user.email", email])
    return ok_name and ok_email, "\n".join([out_name, out_email]).strip()


def git_log_history(path: Path, max_count: int = 75) -> tuple[bool, str]:
    return run_git_command(
        path,
        [
            "log",
            f"--max-count={max_count}",
            "--date=iso",
            "--pretty=format:%h%x1f%an%x1f%ad%x1f%s",
        ],
    )


def git_show_commit(path: Path, commit_hash: str) -> tuple[bool, str]:
    return run_git_command(
        path,
        ["show", "--stat", "--summary", "--date=iso", "--format=fuller", commit_hash],
    )


def git_create_branch(path: Path, branch_name: str) -> tuple[bool, str]:
    return run_git_command(path, ["branch", branch_name])


def git_restore_worktree_from_commit(path: Path, commit_hash: str) -> tuple[bool, str]:
    return run_git_command(path, ["restore", "--source", commit_hash, "--", "."])


def git_commit_recovery(path: Path, source_commit: str, source_message: str) -> tuple[bool, str]:
    return run_git_command(
        path,
        [
            "commit",
            "-m",
            f"Recover project state from {source_commit}",
            "-m",
            f"Recovered snapshot source: {source_message}",
        ],
    )


def git_rebase_abort(path: Path) -> tuple[bool, str]:
    return run_git_command(path, ["rebase", "--abort"])


def git_rebase_continue(path: Path) -> tuple[bool, str]:
    return run_git_command(path, ["rebase", "--continue"])


def git_rebase_continue_no_edit(path: Path) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            ["git", "-c", "core.editor=true", "rebase", "--continue"],
            cwd=path,
            capture_output=True,
            text=True,
            check=False,
            creationflags=windows_no_console_creationflags(),
        )
        output = (result.stdout.strip() + "\n" + result.stderr.strip()).strip()
        return result.returncode == 0, output or "Command completed."
    except FileNotFoundError:
        return False, "Git is not installed or not available in PATH."
    except OSError as error:
        return False, str(error)


def git_merge_abort(path: Path) -> tuple[bool, str]:
    return run_git_command(path, ["merge", "--abort"])


def sanitize_github_remote_url(raw_url: str) -> tuple[bool, str, str]:
    url = raw_url.strip()

    if not url:
        return False, "", "Remote URL is empty."

    unsafe_markers = ["token=", "password=", "ghp_", "github_pat_", "oauth"]
    if any(marker in url.lower() for marker in unsafe_markers):
        return False, "", "Remote URL appears to contain a token or credential. Remove secrets before saving."

    if url.startswith("git@github.com:"):
        return True, url, "SSH remote URL accepted."

    parsed = urlparse(url)

    if parsed.scheme != "https":
        return False, "", "Use a GitHub HTTPS URL or SSH URL."

    if parsed.username or parsed.password:
        return False, "", "Do not include username, password, or token inside the remote URL."

    if parsed.netloc.lower() != "github.com":
        return False, "", "Only github.com repository URLs are accepted."

    path = parsed.path.strip("/")
    if not path or len(path.split("/")) < 2:
        return False, "", "URL must look like https://github.com/owner/repository.git"

    if not path.endswith(".git"):
        path += ".git"

    return True, f"https://github.com/{path}", "HTTPS remote URL accepted."


def mask_remote_url_for_display(remote_url: str) -> str:
    parsed = urlparse(remote_url)
    if parsed.username or parsed.password:
        return f"{parsed.scheme}://***@{parsed.hostname}{parsed.path}"
    return remote_url


# =============================================================================
# Main UI
# =============================================================================

class CodeMApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.withdraw()  # c4 smooth startup: hide until UI is ready

        self.config_data: dict = load_config()
        self.base_dir: Path = Path(self.config_data["base_dir"])
        self.current_project: Path | None = None

        self.project_name_var = tk.StringVar()
        self.project_type_var = tk.StringVar(value=PROJECT_TYPES[0])
        self.base_dir_var = tk.StringVar(value=str(self.base_dir))
        self.git_name_var = tk.StringVar()
        self.git_email_var = tk.StringVar()
        self.commit_message_var = tk.StringVar(value="Update CodeM project documentation")
        self.status_var = tk.StringVar(value="Ready.")
        self.current_project_label_var = tk.StringVar(value="Current Project: None")

        self.objective_text: tk.Text
        self.recent_list: tk.Listbox
        self.notebook: ttk.Notebook
        self.editor_widgets: dict[str, tk.Text] = {}
        self.editor_image_refs: list[tk.PhotoImage] = []
        self.image_width_var = tk.StringVar(value="600")
        self.parts_entries: list[list[ttk.Entry]] = []
        self.parts_grid_entries: list[list[tk.Widget]] = []
        self.current_parts_cell: tk.Widget | None = None
        self.current_part_image_row: int | None = None
        self.current_part_image_button: ttk.Button | None = None
        self.parts_tree: ttk.Treeview
        self.parts_grid_entries: list[list[tk.Widget]]
        self.remote_url_text: tk.Text
        self.history_tree: ttk.Treeview
        self.git_output: tk.Text
        self.create_project_button: ttk.Button
        self.clear_project_button: ttk.Button
        self.edit_project_details_button: ttk.Button
        self.save_project_details_button: ttk.Button
        self.project_name_entry: ttk.Entry
        self.project_type_combo: ttk.Combobox
        self.base_dir_entry: ttk.Entry
        self.browse_button: ttk.Button
        self.docs_project_label: ttk.Label
        self.parts_project_label: ttk.Label
        self.exports_project_label: ttk.Label
        self.git_project_label: ttk.Label

        self.title(f"{APP_NAME} v{APP_VERSION}")
        self._set_application_icon()
        self.geometry("1180x760")
        self.minsize(900, 560)

        self._set_theme()
        self._center_window()
        self._build_ui()
        self._refresh_recent_projects()

    # ---------------------------------------------------------------------
    # Window and theme
    # ---------------------------------------------------------------------
        self._show_when_ready()

    def _set_theme(self) -> None:
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"))
        style.configure("Subtitle.TLabel", font=("Segoe UI", 10))
        style.configure("Section.TLabel", font=("Segoe UI", 11, "bold"))
        style.configure("TButton", padding=(10, 6))
        style.configure("Primary.TButton", padding=(12, 7))
        style.configure("Treeview", rowheight=24)
        style.configure("ProjectBadge.TLabel", font=("Segoe UI", 10), foreground="#0B5CAD")
        style.configure("PartsHeader.TLabel", font=("Segoe UI", 9, "bold"))
        style.configure("Toolbar.TButton", padding=(6, 3))

    def _center_window(self) -> None:
        self.update_idletasks()
        width = 1180
        height = 760
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")


    def _set_application_icon(self) -> None:
        """
        Set the Tkinter title-bar/window icon in source and packaged EXE mode.

        PyInstaller --icon changes the EXE file icon, but Tkinter also needs
        iconbitmap/iconphoto at runtime for the window title bar.
        """
        ico_path = resource_path("codem_icon.ico")
        png_path = resource_path("codem_icon.png")

        try:
            if ico_path.exists():
                self.iconbitmap(str(ico_path))
                return
        except tk.TclError:
            pass

        try:
            if png_path.exists():
                self._app_icon_photo = tk.PhotoImage(file=str(png_path))
                self.iconphoto(True, self._app_icon_photo)
        except tk.TclError:
            pass



    def _show_when_ready(self) -> None:
        """
        Reveal the main window only after the UI has been constructed.

        This reduces the ugly blank/black/partially-painted startup feeling when
        the app is launched as a packaged Windows EXE.
        """
        try:
            self.update_idletasks()
            self.deiconify()
            self.lift()
            self.after(80, self.focus_force)
        except tk.TclError:
            pass

    def _center_child_window(self, window: tk.Toplevel, width: int | None = None, height: int | None = None) -> None:
        """
        Center a popup relative to the main app window.

        Tkinter popups feel jerky when they appear at random/default positions.
        This helper makes dialogs feel intentional and stable.
        """
        try:
            self.update_idletasks()
            window.update_idletasks()

            if width is None:
                width = max(window.winfo_reqwidth(), window.winfo_width(), 360)
            if height is None:
                height = max(window.winfo_reqheight(), window.winfo_height(), 180)

            parent_x = self.winfo_rootx()
            parent_y = self.winfo_rooty()
            parent_w = max(self.winfo_width(), 1)
            parent_h = max(self.winfo_height(), 1)

            x = parent_x + (parent_w - width) // 2
            y = parent_y + (parent_h - height) // 2

            window.geometry(f"{width}x{height}+{max(x, 0)}+{max(y, 0)}")
            window.transient(self)
            window.lift()
            window.focus_force()
        except tk.TclError:
            pass

    def _prepare_operation(self, message: str | None = None) -> None:
        """
        Flush pending UI drawing before heavier operations.

        This does not make long Git operations asynchronous, but it prevents the
        app from feeling frozen before status labels/buttons visually update.
        """
        if message:
            self.status_var.set(message)
        try:
            self.update_idletasks()
        except tk.TclError:
            pass

    def _after_operation(self, message: str | None = None) -> None:
        if message:
            self.status_var.set(message)
        try:
            self.update_idletasks()
        except tk.TclError:
            pass

    def _on_main_tab_changed(self, event: tk.Event | None = None) -> None:
        """
        Keep tab transitions visually calm.

        The app does not animate tabs because Tkinter ttk.Notebook has no native
        animation, but this avoids focus jumps and ensures the new tab is drawn
        immediately.
        """
        try:
            self.update_idletasks()
            self.focus_set()
        except tk.TclError:
            pass


    def _build_ui(self) -> None:
        root = ttk.Frame(self, padding=18)
        root.pack(fill="both", expand=True)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)

        header = ttk.Frame(root)
        header.grid(row=0, column=0, sticky="ew")

        ttk.Label(header, text=APP_NAME, style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text=f"{APP_SUBTITLE} — Materialize projects into proof.",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(2, 12))

        self.notebook = ttk.Notebook(root)
        self.notebook.grid(row=1, column=0, sticky="nsew")
        self.notebook.bind("<<NotebookTabChanged>>", self._on_main_tab_changed)

        self.create_tab = ttk.Frame(self.notebook, padding=14)
        self.docs_tab = ttk.Frame(self.notebook, padding=12)
        self.parts_tab = ttk.Frame(self.notebook, padding=12)
        self.exports_tab = ttk.Frame(self.notebook, padding=12)
        self.git_tab = ttk.Frame(self.notebook, padding=12)

        self.notebook.add(self.create_tab, text="Projects")
        self.notebook.add(self.docs_tab, text="Docs")
        self.notebook.add(self.parts_tab, text="Parts")
        self.notebook.add(self.exports_tab, text="Exports")
        self.notebook.add(self.git_tab, text="Git")

        self._build_create_tab()
        self.edit_project_details_button.configure(state="disabled")
        self.save_project_details_button.configure(state="disabled")
        self._build_docs_tab()
        self._build_parts_tab()
        self._build_exports_tab()
        self._build_git_tab()
        self._build_action_bar(root)

    def _build_action_bar(self, parent: ttk.Frame) -> None:
        bar = ttk.Frame(parent)
        bar.grid(row=2, column=0, sticky="ew", pady=(14, 0))
        bar.columnconfigure(10, weight=1)

        ttk.Button(bar, text="Open Folder", command=self._open_current_project).grid(row=0, column=0, sticky="w")
        ttk.Button(bar, text="Compile README", command=self._compile_readme).grid(row=0, column=1, sticky="w", padx=(8, 0))
        ttk.Button(bar, text="Export Showcase", command=self._export_showcase_brief).grid(row=0, column=2, sticky="w", padx=(8, 0))
        ttk.Button(bar, text="Save All", command=self._save_all).grid(row=0, column=3, sticky="w", padx=(8, 0))

        ttk.Label(bar, textvariable=self.status_var).grid(row=0, column=10, sticky="e")

    # ---------------------------------------------------------------------
    # Create tab
    # ---------------------------------------------------------------------

    def _build_create_tab(self) -> None:
        paned = ttk.PanedWindow(self.create_tab, orient="horizontal")
        paned.pack(fill="both", expand=True)

        left = ttk.Frame(paned, padding=(0, 0, 16, 0))
        right = ttk.Frame(paned, padding=(16, 0, 0, 0))
        paned.add(left, weight=3)
        paned.add(right, weight=2)

        ttk.Label(left, text="Project Details", style="Section.TLabel").pack(anchor="w", pady=(0, 8))

        ttk.Label(left, text="Project Name").pack(anchor="w")
        self.project_name_entry = ttk.Entry(left, textvariable=self.project_name_var)
        self.project_name_entry.pack(fill="x", pady=(3, 12))

        ttk.Label(left, text="Project Type").pack(anchor="w")
        self.project_type_combo = ttk.Combobox(
            left,
            textvariable=self.project_type_var,
            values=PROJECT_TYPES,
            state="readonly",
        )
        self.project_type_combo.pack(fill="x", pady=(3, 12))

        ttk.Label(left, text="Objective").pack(anchor="w")
        self.objective_text = tk.Text(left, height=8, wrap="word", font=("Segoe UI", 10))
        self.objective_text.insert("1.0", DEFAULT_OBJECTIVE_TEMPLATE)
        self.objective_text.pack(fill="both", expand=True, pady=(3, 12))

        ttk.Label(left, text="Project Save Location").pack(anchor="w")
        location_row = ttk.Frame(left)
        location_row.pack(fill="x", pady=(3, 12))

        self.base_dir_entry = ttk.Entry(location_row, textvariable=self.base_dir_var)
        self.base_dir_entry.pack(side="left", fill="x", expand=True)
        self.browse_button = ttk.Button(location_row, text="Browse", command=self._browse_base_dir)
        self.browse_button.pack(side="left", padx=(8, 0))

        create_buttons = ttk.Frame(left)
        create_buttons.pack(anchor="w", pady=(8, 0))

        button_width = 20

        self.clear_project_button = ttk.Button(
            create_buttons,
            text="New Project",
            width=button_width,
            command=self._clear_project_form,
        )
        self.clear_project_button.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        self.edit_project_details_button = ttk.Button(
            create_buttons,
            text="Edit Details",
            width=button_width,
            command=self._enable_project_details_editing,
        )
        self.edit_project_details_button.grid(row=0, column=1, sticky="ew", padx=(0, 8))

        self.save_project_details_button = ttk.Button(
            create_buttons,
            text="Save Details",
            width=button_width,
            command=self._save_project_details,
        )
        self.save_project_details_button.grid(row=0, column=2, sticky="ew", padx=(0, 8))

        self.create_project_button = ttk.Button(
            create_buttons,
            text="Create Project",
            width=button_width,
            style="Primary.TButton",
            command=self._create_project,
        )
        self.create_project_button.grid(row=0, column=3, sticky="ew")

        for column in range(4):
            create_buttons.columnconfigure(column, weight=1)

        ttk.Label(right, text="Open Project", style="Section.TLabel").pack(anchor="w", pady=(0, 8))

        self.recent_list = tk.Listbox(right, height=14, font=("Segoe UI", 10), activestyle="dotbox")
        self.recent_list.pack(fill="both", expand=True)
        self.recent_list.bind("<<ListboxSelect>>", self._on_recent_select)
        self.recent_list.bind("<Double-Button-1>", self._open_selected_recent)
        self.recent_list.bind("<Button-3>", self._show_recent_context_menu)
        self.recent_menu = tk.Menu(self, tearoff=0)
        self.recent_menu.add_command(label="Open", command=self._open_recent_from_menu)
        self.recent_menu.add_command(label="Rename", command=self._rename_recent_from_menu)
        self.recent_menu.add_separator()
        self.recent_menu.add_command(label="Remove Entry Only", command=self._remove_recent_entry_from_menu)
        self.recent_menu.add_command(label="Delete Local Folder + Remove Entry", command=self._delete_recent_folder_from_menu)

        ttk.Label(
            right,
            text="Select a project to open, edit, sync, or export.",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(8, 0))

    def _add_toolbar_button(
        self,
        parent: ttk.Frame,
        text: str,
        command: Callable[[], object],
        row: int,
        column: int,
        width: int = 14,
    ) -> ttk.Button:
        button = ttk.Button(parent, text=text, command=command, width=width, style="Toolbar.TButton")
        button.grid(row=row, column=column, sticky="ew", padx=3, pady=2)
        return button

    def _add_toolbar_group_label(self, parent: ttk.Frame, text: str, row: int) -> None:
        label = ttk.Label(parent, text=text, style="Subtitle.TLabel")
        label.grid(row=row, column=0, sticky="w", padx=(0, 8), pady=3)

    # ---------------------------------------------------------------------
    # Docs tab
    # ---------------------------------------------------------------------

    def _build_docs_tab(self) -> None:
        top = ttk.Frame(self.docs_tab)
        top.pack(fill="x", pady=(0, 8))

        ttk.Label(top, text="Documentation Editor", style="Section.TLabel").pack(side="left")
        self.docs_project_label = ttk.Label(top, textvariable=self.current_project_label_var, style="ProjectBadge.TLabel")
        self.docs_project_label.pack(side="left", padx=(16, 0))

        ttk.Label(
            top,
            text="Tip: use Image to upload, or copy an image file path then press Ctrl+Alt+V.",
            style="Subtitle.TLabel",
        ).pack(side="right", padx=(16, 0))

        toolbar = ttk.Frame(self.docs_tab)
        toolbar.pack(fill="x", pady=(0, 6))
        toolbar.columnconfigure(0, weight=1)
        toolbar.columnconfigure(1, weight=0)

        tool_panel = ttk.Frame(toolbar)
        tool_panel.grid(row=0, column=0, sticky="w")

        action_panel = ttk.Frame(toolbar)
        action_panel.grid(row=0, column=1, sticky="ne", padx=(12, 0))

        # Compact two-row tool layout. This keeps the buttons visible on half-window sizes.
        ttk.Label(tool_panel, text="Format").grid(row=0, column=0, sticky="w", padx=(0, 6), pady=2)
        self._add_toolbar_button(tool_panel, "H2", lambda: self._apply_line_style("heading2"), 0, 1, width=10)
        self._add_toolbar_button(tool_panel, "Bullet", lambda: self._apply_line_style("bullet"), 0, 2, width=10)
        self._add_toolbar_button(tool_panel, "Checklist", lambda: self._apply_line_style("checklist"), 0, 3, width=10)
        self._add_toolbar_button(tool_panel, "Plain", lambda: self._apply_line_style("plain"), 0, 4, width=10)
        self._add_toolbar_button(tool_panel, "Hidden", self._insert_hidden_text_block, 0, 5, width=10)

        ttk.Label(tool_panel, text="Insert").grid(row=1, column=0, sticky="w", padx=(0, 6), pady=2)
        self._add_toolbar_button(tool_panel, "Code", self._insert_code_block, 1, 1, width=10)
        self._add_toolbar_button(tool_panel, "Image", self._insert_image_from_dialog, 1, 2, width=10)

        ttk.Label(tool_panel, text="Edit").grid(row=2, column=0, sticky="w", padx=(0, 6), pady=2)
        self._add_toolbar_button(tool_panel, "Clean", self._clean_selection_markdown, 2, 1, width=10)
        self._add_toolbar_button(tool_panel, "Template", self._restore_current_doc_template, 2, 2, width=10)
        self._add_toolbar_button(tool_panel, "Conflicts", self._clean_current_conflict_markers, 2, 3, width=10)

        # Right-side action panel, always visible.
        ttk.Button(action_panel, text="Save Revision", width=14, style="Toolbar.TButton", command=self._save_current_doc_revision).grid(
            row=0, column=0, sticky="ew", padx=2, pady=1
        )
        ttk.Button(action_panel, text="Save Docs", width=14, style="Toolbar.TButton", command=self._save_docs).grid(
            row=0, column=1, sticky="ew", padx=2, pady=1
        )
        ttk.Button(action_panel, text="Undo", width=14, style="Toolbar.TButton", command=self._editor_undo).grid(
            row=1, column=0, sticky="ew", padx=2, pady=1
        )
        ttk.Button(action_panel, text="Redo", width=14, style="Toolbar.TButton", command=self._editor_redo).grid(
            row=1, column=1, sticky="ew", padx=2, pady=1
        )

        ttk.Label(
            action_panel,
            text="Tip: use Image, or Ctrl+Alt+V for image paths.",
            style="Subtitle.TLabel",
        ).grid(row=2, column=0, columnspan=2, sticky="e", padx=2, pady=(4, 0))

        self.docs_notebook = ttk.Notebook(self.docs_tab)
        self.docs_notebook.pack(fill="both", expand=True)
        self.docs_notebook.bind("<<NotebookTabChanged>>", self._on_main_tab_changed)

        for label in DOC_TABS:
            frame = ttk.Frame(self.docs_notebook, padding=8)
            text = tk.Text(frame, wrap="word", font=("Consolas", 10), undo=True, autoseparators=True, maxundo=-1)
            scroll = ttk.Scrollbar(frame, command=text.yview)
            text.configure(yscrollcommand=scroll.set)

            text.bind("<Return>", self._handle_markdown_return)
            text.bind("<Tab>", self._handle_markdown_tab)
            text.bind("<Control-b>", lambda event: self._apply_line_style("bullet"))
            text.bind("<Control-2>", lambda event: self._apply_line_style("heading2"))
            text.bind("<Control-Alt-v>", self._handle_doc_drop_or_paste_path)

            text.pack(side="left", fill="both", expand=True)
            scroll.pack(side="right", fill="y")

            self.docs_notebook.add(frame, text=label)
            self.editor_widgets[label] = text

    # ---------------------------------------------------------------------
    # Parts tab
    # ---------------------------------------------------------------------

    def _build_parts_tab(self) -> None:
        top = ttk.Frame(self.parts_tab)
        top.pack(fill="x", pady=(0, 8))

        ttk.Label(top, text="Parts List", style="Section.TLabel").pack(side="left")
        self.parts_project_label = ttk.Label(top, textvariable=self.current_project_label_var, style="ProjectBadge.TLabel")
        self.parts_project_label.pack(side="left", padx=(16, 0))

        ttk.Button(top, text="Save Parts", command=self._save_parts).pack(side="right")
        ttk.Button(top, text="Add Row", command=lambda: self._add_parts_grid_rows(1)).pack(side="right", padx=(0, 8))
        ttk.Button(top, text="Clear Empty Rows", command=self._clear_empty_part_rows).pack(side="right", padx=(0, 8))

        help_text = (
            "Type directly in the table. Row numbers are fixed. "
            "Cells wrap text internally but keep a standard row height. Click + in the Image column to attach a part image."
        )
        ttk.Label(self.parts_tab, text=help_text, style="Subtitle.TLabel").pack(anchor="w", pady=(0, 8))

        grid_shell = ttk.Frame(self.parts_tab)
        grid_shell.pack(fill="both", expand=True)

        canvas = tk.Canvas(grid_shell, highlightthickness=0)
        scroll_y = ttk.Scrollbar(grid_shell, orient="vertical", command=canvas.yview)

        self.parts_grid_frame = ttk.Frame(canvas)
        self.parts_grid_window = canvas.create_window((0, 0), window=self.parts_grid_frame, anchor="nw")

        def _sync_scrollregion(_event: tk.Event | None = None) -> None:
            canvas.configure(scrollregion=canvas.bbox("all"))

        def _stretch_grid(event: tk.Event) -> None:
            # Fit table to visible width. No forced horizontal overflow.
            canvas.itemconfigure(self.parts_grid_window, width=event.width)

        self.parts_grid_frame.bind("<Configure>", _sync_scrollregion)
        canvas.bind("<Configure>", _stretch_grid)
        canvas.configure(yscrollcommand=scroll_y.set)

        canvas.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")

        grid_shell.columnconfigure(0, weight=1)
        grid_shell.rowconfigure(0, weight=1)

        self.part_image_menu = tk.Menu(self, tearoff=0)
        self.part_image_menu.add_command(label="Upload / Replace Image", command=self._part_image_menu_upload)
        self.part_image_menu.add_command(label="Open Image", command=self._part_image_menu_open)
        self.part_image_menu.add_command(label="Copy Image Path", command=self._part_image_menu_copy_path)
        self.part_image_menu.add_separator()
        self.part_image_menu.add_command(label="Remove Image", command=self._part_image_menu_remove)

        self._render_parts_grid_headers()
        self._add_parts_grid_rows(5)

    # ---------------------------------------------------------------------
    # Exports tab
    # ---------------------------------------------------------------------

    def _build_exports_tab(self) -> None:
        exports_top = ttk.Frame(self.exports_tab)
        exports_top.pack(fill="x", pady=(0, 8))

        ttk.Label(exports_top, text="Export Center", style="Section.TLabel").pack(side="left")
        self.exports_project_label = ttk.Label(exports_top, textvariable=self.current_project_label_var, style="ProjectBadge.TLabel")
        self.exports_project_label.pack(side="left", padx=(16, 0))

        description = (
            "Create polished Markdown outputs for GitHub, project archiving, sponsor review, "
            "school presentation, or research documentation. README.md is a compiled project page "
            "built from Docs + Parts, so it will not look identical to a single Docs tab."
        )
        ttk.Label(self.exports_tab, text=description, style="Subtitle.TLabel", wraplength=900).pack(anchor="w", pady=(0, 16))

        readme = ttk.LabelFrame(self.exports_tab, text="README Compiler", padding=14)
        readme.pack(fill="x", pady=(0, 12))
        ttk.Label(readme, text="Compile README.md from the latest Docs and Parts content.").pack(anchor="w", pady=(0, 8))
        ttk.Button(readme, text="Compile README", command=self._compile_readme).pack(anchor="e")

        showcase = ttk.LabelFrame(self.exports_tab, text="Showcase Brief", padding=14)
        showcase.pack(fill="x", pady=(0, 12))
        ttk.Label(
            showcase,
            text="Generate a one-page public-facing project summary.",
        ).pack(anchor="w", pady=(0, 8))
        ttk.Button(showcase, text="Export Showcase Brief", command=self._export_showcase_brief).pack(anchor="e")

    # ---------------------------------------------------------------------
    # Git tab
    # ---------------------------------------------------------------------

    def _build_git_tab(self) -> None:
        git_header = ttk.Frame(self.git_tab)
        git_header.pack(fill="x", pady=(0, 8))

        ttk.Label(git_header, text="GitHub Workflow", style="Section.TLabel").pack(side="left")
        self.git_project_label = ttk.Label(git_header, textvariable=self.current_project_label_var, style="ProjectBadge.TLabel")
        self.git_project_label.pack(side="left", padx=(16, 0))

        ttk.Label(
            self.git_tab,
            text="Use Sync for daily work, History for recovery, and Repair only when Git is stuck.",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(0, 10))

        git_pages = ttk.Notebook(self.git_tab)
        git_pages.pack(fill="both", expand=True)
        git_pages.bind("<<NotebookTabChanged>>", self._on_main_tab_changed)

        sync_page = ttk.Frame(git_pages, padding=12)
        history_page = ttk.Frame(git_pages, padding=12)
        repair_page = ttk.Frame(git_pages, padding=12)

        git_pages.add(sync_page, text="Sync")
        git_pages.add(history_page, text="History")
        git_pages.add(repair_page, text="Repair")

        self._build_git_sync_page(sync_page)
        self._build_git_history_page(history_page)
        self._build_git_repair_page(repair_page)

    def _build_git_sync_page(self, parent: ttk.Frame) -> None:
        paned = ttk.PanedWindow(parent, orient="horizontal")
        paned.pack(fill="both", expand=True)

        left_shell = ttk.Frame(paned, padding=(0, 0, 10, 0))
        right = ttk.Frame(paned, padding=(10, 0, 0, 0))

        # Keep the workflow compact and give Git Output the wider working area.
        paned.add(left_shell, weight=1)
        paned.add(right, weight=3)

        # Left workflow area: scroll only when the window becomes short.
        workflow_canvas = tk.Canvas(left_shell, highlightthickness=0)
        workflow_scroll = ttk.Scrollbar(left_shell, orient="vertical", command=workflow_canvas.yview)
        workflow = ttk.Frame(workflow_canvas)

        workflow_window = workflow_canvas.create_window((0, 0), window=workflow, anchor="nw")

        def _sync_workflow_scroll(_event: tk.Event | None = None) -> None:
            workflow_canvas.configure(scrollregion=workflow_canvas.bbox("all"))

        def _fit_workflow_width(event: tk.Event) -> None:
            workflow_canvas.itemconfigure(workflow_window, width=event.width)

        workflow.bind("<Configure>", _sync_workflow_scroll)
        workflow_canvas.bind("<Configure>", _fit_workflow_width)
        workflow_canvas.configure(yscrollcommand=workflow_scroll.set)

        workflow_canvas.grid(row=0, column=0, sticky="nsew")
        workflow_scroll.grid(row=0, column=1, sticky="ns")

        left_shell.columnconfigure(0, weight=1)
        left_shell.rowconfigure(0, weight=1)

        ttk.Label(workflow, text="Daily GitHub Sync", style="Section.TLabel").pack(anchor="w", pady=(0, 6))
        ttk.Label(
            workflow,
            text="Flow: validate URL → pull updates → commit message → publish.",
            style="Subtitle.TLabel",
            wraplength=430,
        ).pack(anchor="w", pady=(0, 10))

        identity = ttk.LabelFrame(workflow, text="Commit Author Identity", padding=10)
        identity.pack(fill="x", pady=(0, 8))

        ttk.Label(
            identity,
            text="Used for team commit attribution. Not your GitHub password or token.",
            style="Subtitle.TLabel",
            wraplength=430,
        ).pack(anchor="w", pady=(0, 6))

        identity_grid = ttk.Frame(identity)
        identity_grid.pack(fill="x")

        ttk.Label(identity_grid, text="Git Name").grid(row=0, column=0, sticky="w", padx=(0, 8), pady=2)
        ttk.Entry(identity_grid, textvariable=self.git_name_var).grid(row=0, column=1, sticky="ew", pady=2)

        ttk.Label(identity_grid, text="Git Email").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=2)
        ttk.Entry(identity_grid, textvariable=self.git_email_var).grid(row=1, column=1, sticky="ew", pady=2)

        identity_grid.columnconfigure(1, weight=1)

        identity_buttons = ttk.Frame(identity)
        identity_buttons.pack(fill="x", pady=(6, 0))
        ttk.Button(identity_buttons, text="Load Identity", command=self._git_load_identity).pack(side="left")
        ttk.Button(identity_buttons, text="Save Identity", command=self._git_save_identity).pack(side="left", padx=(8, 0))

        repo = ttk.LabelFrame(workflow, text="Repository", padding=10)
        repo.pack(fill="x", pady=(0, 8))

        ttk.Label(repo, text="Repository URL").pack(anchor="w")
        self.remote_url_text = tk.Text(repo, height=2, wrap="word", font=("Consolas", 10))
        self.remote_url_text.pack(fill="x", pady=(3, 6))

        ttk.Label(
            repo,
            text="CodeM blocks tokens, passwords, and embedded credentials.",
            style="Subtitle.TLabel",
            wraplength=430,
        ).pack(anchor="w", pady=(0, 6))

        repo_buttons = ttk.Frame(repo)
        repo_buttons.pack(fill="x")
        ttk.Button(repo_buttons, text="Validate URL", command=self._validate_remote_url).pack(side="left")
        ttk.Button(repo_buttons, text="Pull Updates", command=self._git_pull).pack(side="left", padx=(8, 0))
        ttk.Button(repo_buttons, text="Fix Stuck Sync", command=self._git_fix_stuck_sync).pack(side="left", padx=(8, 0))

        commit = ttk.LabelFrame(workflow, text="Commit and Publish", padding=10)
        commit.pack(fill="x", pady=(0, 8))

        ttk.Label(commit, text="Commit Message").pack(anchor="w")
        ttk.Entry(commit, textvariable=self.commit_message_var).pack(fill="x", pady=(3, 6))

        commit_buttons = ttk.Frame(commit)
        commit_buttons.pack(fill="x")
        ttk.Button(commit_buttons, text="Publish to GitHub", command=self._git_push).pack(side="left")
        ttk.Button(commit_buttons, text="Git Status", command=self._git_status).pack(side="left", padx=(8, 0))

        ttk.Label(
            commit,
            text="Publish saves docs, stages the current project folder, records the commit message, pulls updates, and pushes.",
            style="Subtitle.TLabel",
            wraplength=430,
        ).pack(anchor="w", pady=(8, 0))

        quick = ttk.LabelFrame(workflow, text="Quick Repair", padding=10)
        quick.pack(fill="x", pady=(0, 8))

        ttk.Label(
            quick,
            text="Use only for 'rebase in progress' or stuck pull/push states.",
            style="Subtitle.TLabel",
            wraplength=430,
        ).pack(anchor="w", pady=(0, 6))

        quick_buttons = ttk.Frame(quick)
        quick_buttons.pack(fill="x")
        ttk.Button(quick_buttons, text="Check State", command=self._git_check_state).pack(side="left")
        ttk.Button(quick_buttons, text="Abort Rebase", command=self._git_abort_rebase).pack(side="left", padx=(8, 0))
        ttk.Button(quick_buttons, text="Abort Merge", command=self._git_abort_merge).pack(side="left", padx=(8, 0))

        # Right output area: no extra center spacer, no duplicate scrollbar.
        ttk.Label(right, text="Git Output", style="Section.TLabel").pack(anchor="w", pady=(0, 8))

        output_frame = ttk.Frame(right)
        output_frame.pack(fill="both", expand=True)

        self.git_output = tk.Text(output_frame, wrap="word", font=("Consolas", 10))
        output_scroll = ttk.Scrollbar(output_frame, orient="vertical", command=self.git_output.yview)
        self.git_output.configure(yscrollcommand=output_scroll.set)

        self.git_output.grid(row=0, column=0, sticky="nsew")
        output_scroll.grid(row=0, column=1, sticky="ns")

        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)

    def _build_git_history_page(self, parent: ttk.Frame) -> None:
        ttk.Label(parent, text="Recovery History", style="Section.TLabel").pack(anchor="w", pady=(0, 8))
        ttk.Label(
            parent,
            text="Recovering a selected event creates a new recovery commit. It does not erase later history.",
            style="Subtitle.TLabel",
            wraplength=900,
        ).pack(anchor="w", pady=(0, 10))

        history_buttons = ttk.Frame(parent)
        history_buttons.pack(fill="x", pady=(0, 8))
        ttk.Button(history_buttons, text="Load History", command=self._git_load_history).pack(side="left")
        ttk.Button(history_buttons, text="Preview Selected", command=self._git_preview_selected_commit).pack(side="left", padx=(8, 0))
        ttk.Button(history_buttons, text="Recover Selected", command=self._git_recover_selected_commit).pack(side="left", padx=(8, 0))

        history_container = ttk.Frame(parent)
        history_container.pack(fill="both", expand=True)

        self.history_tree = ttk.Treeview(
            history_container,
            columns=("hash", "author", "date", "message"),
            show="headings",
            height=14,
            selectmode="browse",
        )

        for col, title, width, stretch in [
            ("hash", "Commit", 100, False),
            ("author", "Who", 180, False),
            ("date", "Date / Time", 230, False),
            ("message", "Commit Message", 560, True),
        ]:
            self.history_tree.heading(col, text=title)
            self.history_tree.column(col, width=width, stretch=stretch)

        history_y = ttk.Scrollbar(history_container, orient="vertical", command=self.history_tree.yview)
        history_x = ttk.Scrollbar(history_container, orient="horizontal", command=self.history_tree.xview)
        self.history_tree.configure(yscrollcommand=history_y.set, xscrollcommand=history_x.set)

        self.history_tree.grid(row=0, column=0, sticky="nsew")
        history_y.grid(row=0, column=1, sticky="ns")
        history_x.grid(row=1, column=0, sticky="ew")
        history_container.columnconfigure(0, weight=1)
        history_container.rowconfigure(0, weight=1)

    def _build_git_repair_page(self, parent: ttk.Frame) -> None:
        ttk.Label(parent, text="Sync Repair", style="Section.TLabel").pack(anchor="w", pady=(0, 8))
        ttk.Label(
            parent,
            text="Use this page when Git says a rebase or merge is already in progress.",
            style="Subtitle.TLabel",
            wraplength=900,
        ).pack(anchor="w", pady=(0, 12))

        repair = ttk.LabelFrame(parent, text="Repair Actions", padding=12)
        repair.pack(fill="x", pady=(0, 12))

        repair_buttons = ttk.Frame(repair)
        repair_buttons.pack(fill="x")
        ttk.Button(repair_buttons, text="Check State", command=self._git_check_state).pack(side="left")
        ttk.Button(repair_buttons, text="Fix Stuck Sync", command=self._git_fix_stuck_sync).pack(side="left", padx=(8, 0))
        ttk.Button(repair_buttons, text="Abort Rebase", command=self._git_abort_rebase).pack(side="left", padx=(8, 0))
        ttk.Button(repair_buttons, text="Abort Merge", command=self._git_abort_merge).pack(side="left", padx=(8, 0))
        ttk.Button(repair_buttons, text="Continue Rebase", command=self._git_continue_rebase).pack(side="left", padx=(8, 0))

        explanation = (
            "Recommended order for your current error:\n"
            "1. Click Check State.\n"
            "2. If it says rebase in progress with working tree clean, click Fix Stuck Sync.\n"
            "3. If that fails, click Abort Rebase.\n"
            "4. Return to Sync and click Pull Updates, then Push to GitHub."
        )

        info = tk.Text(parent, height=8, wrap="word", font=("Segoe UI", 10))
        info.pack(fill="x", pady=(0, 12))
        info.insert("1.0", explanation)
        info.configure(state="disabled")

    # ---------------------------------------------------------------------
    # Project UI state
    # ---------------------------------------------------------------------

    def _set_project_loaded_state(self, loaded: bool) -> None:
        """
        Prevent accidental duplicate project creation while still allowing
        controlled editing of project metadata.
        """
        create_state = "disabled" if loaded else "normal"
        detail_state = "disabled" if loaded else "normal"
        combo_state = "disabled" if loaded else "readonly"

        self.create_project_button.configure(state=create_state)
        self.project_name_entry.configure(state=detail_state)
        self.project_type_combo.configure(state=combo_state)
        self.objective_text.configure(state=detail_state)
        self.base_dir_entry.configure(state=create_state)
        self.browse_button.configure(state=create_state)

        self.edit_project_details_button.configure(state="normal" if loaded else "disabled")
        self.save_project_details_button.configure(state="disabled")

        if loaded and self.current_project:
            self.current_project_label_var.set(f"Current Project: {self.current_project.name}")
        elif not loaded:
            self.current_project_label_var.set("Current Project: None")

    def _enable_project_details_editing(self) -> None:
        if self.current_project is None:
            messagebox.showwarning("No Project Loaded", "Open or create a project first.")
            return

        metadata = read_project_metadata(self.current_project) or {}
        self.project_name_var.set(metadata.get("project_name", self.current_project.name))
        self.project_type_var.set(metadata.get("project_type", PROJECT_TYPES[0]))

        self.objective_text.configure(state="normal")
        self.objective_text.delete("1.0", "end")
        self.objective_text.insert("1.0", metadata.get("objective", "") or DEFAULT_OBJECTIVE_TEMPLATE)

        # Safer industry behavior:
        # Project identity is read-only after creation. Objective is the editable project detail.
        self.project_name_entry.configure(state="disabled")
        self.project_type_combo.configure(state="disabled")
        self.base_dir_entry.configure(state="disabled")
        self.browse_button.configure(state="disabled")

        self.save_project_details_button.configure(state="normal")
        self.edit_project_details_button.configure(state="disabled")
        self.status_var.set("Objective editing enabled. Project name/type are read-only.")

    def _save_project_details(self) -> None:
        project_dir = self._require_project()
        if project_dir is None:
            return

        objective = self.objective_text.get("1.0", "end").strip()

        metadata_path = project_dir / "project.json"
        metadata = read_project_metadata(project_dir) or {}

        project_name = metadata.get("project_name", project_dir.name)
        project_type = metadata.get("project_type", self.project_type_var.get().strip() or PROJECT_TYPES[0])

        metadata["project_name"] = project_name
        metadata["project_type"] = project_type
        metadata["objective"] = objective
        metadata["folder_name"] = project_dir.name
        metadata["updated_at"] = now_string()

        try:
            metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
        except OSError as error:
            messagebox.showerror("Save Project Details Failed", str(error))
            return

        # Refresh README so objective changes are reflected in local documentation.
        self._compile_readme(show_message=False)

        self.project_name_var.set(project_name)
        self.project_type_var.set(project_type)

        self.project_name_entry.configure(state="disabled")
        self.project_type_combo.configure(state="disabled")
        self.objective_text.configure(state="disabled")
        self.save_project_details_button.configure(state="disabled")
        self.edit_project_details_button.configure(state="normal")

        self.current_project_label_var.set(f"Current Project: {project_dir.name}")
        self.status_var.set("Project objective saved.")
        messagebox.showinfo(
            "Project Details Saved",
            "Project objective updated safely.\n\n"
            "Project Name and Project Type remain read-only to protect the folder/repository identity.",
        )

    def _clear_project_form(self) -> None:
        previous_project = self.current_project
        self.current_project = None

        # Keep new projects at the workspace level beside the previous project,
        # never inside the previous project folder.
        if previous_project is not None:
            self.base_dir = previous_project.parent
            self.base_dir_var.set(str(previous_project.parent))

        self.project_name_var.set("")
        self.project_type_var.set(PROJECT_TYPES[0])
        self.objective_text.configure(state="normal")
        self.objective_text.delete("1.0", "end")
        self.objective_text.insert("1.0", DEFAULT_OBJECTIVE_TEMPLATE)
        self._set_project_loaded_state(False)
        self.edit_project_details_button.configure(state="disabled")
        self.save_project_details_button.configure(state="disabled")
        self.status_var.set("Ready to create a new project.")

    # ---------------------------------------------------------------------
    # Project actions
    # ---------------------------------------------------------------------

    def _browse_base_dir(self) -> None:
        selected = filedialog.askdirectory(initialdir=str(self.base_dir))
        if not selected:
            return

        self.base_dir = Path(selected)
        self.base_dir_var.set(str(self.base_dir))
        self.config_data["base_dir"] = str(self.base_dir)
        save_config(self.config_data)

    def _create_project(self) -> None:
        self._prepare_operation("Creating project...")
        project_name = self.project_name_var.get().strip()
        project_type = self.project_type_var.get().strip()
        objective = self.objective_text.get("1.0", "end").strip()
        base_dir = Path(self.base_dir_var.get()).expanduser()

        # Safety: if user accidentally selects an existing CodeM project folder
        # as the save location, create the new project beside it instead.
        if (base_dir / "project.json").exists():
            use_parent = messagebox.askyesno(
                "Project Folder Selected",
                "The selected save location appears to be an existing CodeM project folder.\n\n"
                f"{base_dir}\n\n"
                "Create the new project beside this project instead?",
            )
            if not use_parent:
                return
            base_dir = base_dir.parent
            self.base_dir_var.set(str(base_dir))

        if not project_name:
            messagebox.showwarning("Missing Project Name", "Enter a project name.")
            return

        if not objective:
            messagebox.showwarning("Missing Objective", "Enter a short project objective.")
            return

        try:
            base_dir.mkdir(parents=True, exist_ok=True)
            project_dir = create_project_structure(base_dir, project_name, project_type, objective)
        except FileExistsError:
            existing_dir = base_dir / slugify_project_name(project_name)
            open_existing = messagebox.askyesno(
                "Project Already Exists",
                "A project with the same folder name already exists.\n\n"
                f"{existing_dir}\n\n"
                "Open the existing project instead?",
            )
            if open_existing and existing_dir.exists():
                self.current_project = existing_dir
                self._add_recent_project(existing_dir)
                self._refresh_recent_projects()
                self._load_project(existing_dir)
                self._set_project_loaded_state(True)
                self.notebook.select(self.docs_tab)
                self.status_var.set(f"Opened existing: {existing_dir.name}")
            return
        except OSError as error:
            messagebox.showerror("Create Project Failed", str(error))
            return

        self.current_project = project_dir
        self._add_recent_project(project_dir)
        self._refresh_recent_projects()
        self._load_project(project_dir)
        self._set_project_loaded_state(True)
        self.notebook.select(self.docs_tab)
        self.status_var.set(f"Created: {project_dir.name}")
        messagebox.showinfo("Project Created", f"Project created successfully:\n\n{project_dir}")

    def _add_recent_project(self, project_dir: Path) -> None:
        recent = self.config_data.get("recent_projects", [])
        project_path = str(project_dir)

        if project_path in recent:
            recent.remove(project_path)

        recent.insert(0, project_path)
        self.config_data["recent_projects"] = recent[:10]
        self.config_data["base_dir"] = self.base_dir_var.get()
        save_config(self.config_data)

    def _refresh_recent_projects(self) -> None:
        self.recent_list.delete(0, tk.END)

        for project in self.config_data.get("recent_projects", []):
            path = Path(project)
            label = path.name if path.exists() else f"{path.name} (missing)"
            self.recent_list.insert(tk.END, label)

    def _get_selected_recent_path(self) -> Path | None:
        selection = self.recent_list.curselection()
        if not selection:
            return None

        recent = self.config_data.get("recent_projects", [])
        index = selection[0]

        if index >= len(recent):
            return None

        return Path(recent[index])

    def _show_recent_context_menu(self, event: tk.Event) -> None:
        index = self.recent_list.nearest(event.y)
        if index < 0:
            return

        self.recent_list.selection_clear(0, tk.END)
        self.recent_list.selection_set(index)
        self.recent_list.activate(index)

        try:
            self.recent_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.recent_menu.grab_release()

    def _open_recent_from_menu(self) -> None:
        path = self._get_selected_recent_path()
        if path is None:
            return

        if not path.exists():
            messagebox.showerror("Missing Project", f"Folder not found:\n{path}")
            return

        self.current_project = path
        self._load_project(path)
        self._set_project_loaded_state(True)
        self.notebook.select(self.docs_tab)
        self.status_var.set(f"Loaded: {path.name}")

    def _rename_recent_from_menu(self) -> None:
        path = self._get_selected_recent_path()
        if path is None:
            return

        if not path.exists():
            messagebox.showerror("Missing Project", f"Folder not found:\n{path}")
            return

        dialog = tk.Toplevel(self)
        dialog.title("Rename Project")
        dialog.transient(self)
        dialog.grab_set()
        dialog.resizable(False, False)

        ttk.Label(dialog, text="New project folder name").pack(anchor="w", padx=16, pady=(16, 4))
        name_var = tk.StringVar(value=path.name)
        entry = ttk.Entry(dialog, textvariable=name_var, width=42)
        entry.pack(fill="x", padx=16, pady=(0, 12))
        entry.focus_set()
        self._center_child_window(dialog, width=420, height=170)

        def apply_rename() -> None:
            new_name = slugify_project_name(name_var.get())
            if not new_name:
                messagebox.showwarning("Invalid Name", "Enter a valid project name.")
                return

            new_path = path.parent / new_name
            if new_path.exists() and new_path != path:
                messagebox.showerror("Folder Exists", f"Another folder already exists:\n{new_path}")
                return

            try:
                path.rename(new_path)
                metadata_path = new_path / "project.json"
                if metadata_path.exists():
                    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
                    metadata["project_name"] = new_name
                    metadata["folder_name"] = new_name
                    metadata["updated_at"] = now_string()
                    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
            except (OSError, json.JSONDecodeError) as error:
                messagebox.showerror("Rename Failed", str(error))
                return

            recent = self.config_data.get("recent_projects", [])
            old_value = str(path)
            if old_value in recent:
                recent[recent.index(old_value)] = str(new_path)
                self.config_data["recent_projects"] = recent
                save_config(self.config_data)

            if self.current_project == path:
                self.current_project = new_path
                self._load_project(new_path)
                self._set_project_loaded_state(True)

            self._refresh_recent_projects()
            self.status_var.set(f"Renamed project to {new_name}")
            dialog.destroy()

        buttons = ttk.Frame(dialog)
        buttons.pack(fill="x", padx=16, pady=(0, 16))
        ttk.Button(buttons, text="Cancel", command=dialog.destroy).pack(side="right")
        ttk.Button(buttons, text="Rename", command=apply_rename).pack(side="right", padx=(0, 8))

        self.wait_window(dialog)

    def _remove_recent_entry_from_menu(self) -> None:
        path = self._get_selected_recent_path()
        if path is None:
            return

        recent = self.config_data.get("recent_projects", [])
        value = str(path)
        if value in recent:
            recent.remove(value)
            self.config_data["recent_projects"] = recent
            save_config(self.config_data)

        if self.current_project == path:
            self.current_project = None
            self._set_project_loaded_state(False)

        self._refresh_recent_projects()
        self.status_var.set("Recent project entry removed.")

    def _delete_recent_folder_from_menu(self) -> None:
        path = self._get_selected_recent_path()
        if path is None:
            return

        confirm = messagebox.askyesno(
            "Move Local Project Folder to Recycle Bin",
            "This will move the local project folder to the Recycle Bin and remove the recent entry.\n\n"
            f"{path}\n\n"
            "This does not delete the GitHub repository. Continue?",
        )
        if not confirm:
            return

        success, message = move_path_to_recycle_bin(path)
        if not success:
            messagebox.showerror("Move to Recycle Bin Failed", message)
            return

        recent = self.config_data.get("recent_projects", [])
        value = str(path)
        if value in recent:
            recent.remove(value)
            self.config_data["recent_projects"] = recent
            save_config(self.config_data)

        if self.current_project == path:
            self.current_project = None
            self._set_project_loaded_state(False)

        self._refresh_recent_projects()
        self.status_var.set(message + " Recent entry removed.")


    def _on_recent_select(self, _event: tk.Event) -> None:
        path = self._get_selected_recent_path()
        if path and path.exists():
            self.current_project = path
            self._load_project(path)
            self._set_project_loaded_state(True)
            self.status_var.set(f"Loaded: {path.name}")

    def _open_selected_recent(self, _event: tk.Event) -> None:
        path = self._get_selected_recent_path()
        if not path:
            return

        if not path.exists():
            messagebox.showerror("Missing Project", f"Folder not found:\n{path}")
            return

        self.current_project = path
        self._load_project(path)
        self._set_project_loaded_state(True)
        open_folder(path)

    def _load_project(self, project_dir: Path) -> None:
        self.base_dir = project_dir.parent
        self.base_dir_var.set(str(project_dir.parent))
        self.current_project_label_var.set(f"Current Project: {project_dir.name}")

        metadata = read_project_metadata(project_dir)
        if metadata:
            self.project_name_var.set(metadata.get("project_name", project_dir.name))
            self.project_type_var.set(metadata.get("project_type", PROJECT_TYPES[0]))
            self.objective_text.configure(state="normal")
            self.objective_text.delete("1.0", "end")
            self.objective_text.insert("1.0", metadata.get("objective", "") or DEFAULT_OBJECTIVE_TEMPLATE)

        default_instructions = {
            "Overview": "Explain the purpose, problem, scope, objectives, and success criteria.",
            "Build Notes": "Document what was built, how it was implemented, and key decisions.",
            "Testing": "Document test objective, setup, procedure, observations, and outcome.",
            "Results": "Summarize findings, evidence, interpretation, lessons learned, and conclusion.",
            "Future Work": "List next actions, improvements, pending tests, resources, and risks.",
        }

        for label, relative_path in DOC_TABS.items():
            text_widget = self.editor_widgets[label]
            text_widget.delete("1.0", "end")
            content = read_text_file(project_dir / relative_path).strip()
            if not content:
                content = generate_industry_doc_template(
                    label,
                    default_instructions.get(label, "Document this section."),
                )
            text_widget.insert("1.0", content)

        self._load_parts(project_dir / "parts" / "parts_list.csv")
        self._load_git_identity_if_available(project_dir)
        self._git_load_history(silent=True)

    def _open_current_project(self) -> None:
        project_dir = self._require_project()
        if project_dir is None:
            return
        open_folder(project_dir)

    def _require_project(self) -> Path | None:
        if not self.current_project:
            messagebox.showwarning("No Project Selected", "Create or select a project first.")
            return None

        if not self.current_project.exists():
            messagebox.showerror("Missing Project", f"Folder not found:\n{self.current_project}")
            return None

        return self.current_project

    # ---------------------------------------------------------------------
    # Markdown editor helpers
    # ---------------------------------------------------------------------

    def _get_current_doc_widget(self) -> tk.Text | None:
        selected_tab = self.docs_notebook.select()
        if not selected_tab:
            return None

        tab_text = self.docs_notebook.tab(selected_tab, "text")
        widget = self.editor_widgets.get(tab_text)
        return widget

    def _strip_line_markdown_prefix(self, line: str) -> str:
        """
        Remove common Markdown line prefixes before applying a new style.

        This prevents stacked output such as:
            - [ ] - [ ] text
            - - text
            - ## text
        """
        text = line.rstrip()

        # Preserve indentation but normalize marker after indentation.
        indent_match = re.match(r"^(\s*)(.*)$", text)
        indent = indent_match.group(1) if indent_match else ""
        body = indent_match.group(2) if indent_match else text

        patterns = [
            r"^#{1,6}\s+",
            r"^[-*+]\s+\[[ xX]\]\s+",
            r"^[-*+]\s+",
            r"^\d+\.\s+",
            r"^>\s+",
        ]

        changed = True
        while changed:
            changed = False
            for pattern in patterns:
                new_body = re.sub(pattern, "", body)
                if new_body != body:
                    body = new_body.lstrip()
                    changed = True

        return indent + body

    def _style_line(self, raw_line: str, style: str) -> str:
        clean = self._strip_line_markdown_prefix(raw_line).strip()

        if style == "plain":
            return clean
        if style == "heading1":
            return f"# {clean}" if clean else "# "
        if style == "heading2":
            return f"## {clean}" if clean else "## "
        if style == "bullet":
            return f"- {clean}" if clean else "- "
        if style == "checklist":
            return f"- [ ] {clean}" if clean else "- [ ] "

        return clean

    def _selected_line_range(self, widget: tk.Text) -> tuple[str, str]:
        try:
            start = widget.index("sel.first linestart")
            end = widget.index("sel.last lineend")
            return start, end
        except tk.TclError:
            start = widget.index("insert linestart")
            end = widget.index("insert lineend")
            return start, end

    def _apply_line_style(self, style: str) -> str:
        widget = self._get_current_doc_widget()
        if widget is None:
            return "break"

        start, end = self._selected_line_range(widget)
        original = widget.get(start, end)
        lines = original.splitlines()

        if not lines:
            lines = [""]

        styled_lines = [self._style_line(line, style) for line in lines]
        replacement = "\n".join(styled_lines)

        try:
            widget.edit_separator()
        except tk.TclError:
            pass

        widget.delete(start, end)
        widget.insert(start, replacement)

        try:
            widget.edit_separator()
        except tk.TclError:
            pass

        widget.focus_set()
        self.status_var.set(f"Applied {style} style.")
        return "break"

    def _clean_selection_markdown(self) -> None:
        widget = self._get_current_doc_widget()
        if widget is None:
            return

        start, end = self._selected_line_range(widget)
        original = widget.get(start, end)
        cleaned_lines = [self._strip_line_markdown_prefix(line).strip() for line in original.splitlines()]
        replacement = "\n".join(cleaned_lines)

        try:
            widget.edit_separator()
        except tk.TclError:
            pass

        widget.delete(start, end)
        widget.insert(start, replacement)

        try:
            widget.edit_separator()
        except tk.TclError:
            pass

        widget.focus_set()
        self.status_var.set("Selection cleaned to plain text.")

    def _editor_undo(self) -> None:
        widget = self._get_current_doc_widget()
        if widget is None:
            return
        widget.focus_set()
        try:
            widget.edit_undo()
            self.status_var.set("Undo.")
        except tk.TclError:
            self.status_var.set("Nothing to undo.")

    def _editor_redo(self) -> None:
        widget = self._get_current_doc_widget()
        if widget is None:
            return
        widget.focus_set()
        try:
            widget.edit_redo()
            self.status_var.set("Redo.")
        except tk.TclError:
            self.status_var.set("Nothing to redo.")



    def _active_docs_editor(self) -> tk.Text | None:
        """
        Return the Text editor for the currently selected documentation tab.

        This supports all documentation editor tabs:
        - Overview
        - Build Notes
        - Testing
        - Results
        - Future Work
        """
        try:
            selected_tab_id = self.docs_notebook.select()
            selected_label = str(self.docs_notebook.tab(selected_tab_id, "text")).strip()
        except tk.TclError:
            return None

        # Primary lookup: tab label matches DOC_TABS/editor_widgets keys.
        editor = self.editor_widgets.get(selected_label)
        if isinstance(editor, tk.Text):
            return editor

        # Fallback lookup: compare normalized labels in case spacing changes.
        normalized_selected = selected_label.lower().replace("&", "and").strip()
        for label, candidate in self.editor_widgets.items():
            normalized_label = str(label).lower().replace("&", "and").strip()
            if normalized_label == normalized_selected and isinstance(candidate, tk.Text):
                return candidate

        # Last fallback: use focus widget when focus is already inside a documentation editor.
        focused = self.focus_get()
        if isinstance(focused, tk.Text):
            for candidate in self.editor_widgets.values():
                if focused == candidate:
                    return focused

        return None


    def _insert_hidden_text_block(self) -> None:
        """
        Insert a GitHub-compatible collapsible Markdown block into the active documentation tab.

        If text is selected, the selection becomes the hidden content.
        The block works on GitHub using HTML <details>/<summary>.
        """
        editor = self._active_docs_editor()
        if editor is None:
            messagebox.showwarning(
                "No Documentation Editor",
                "Select a documentation tab first, then click Hidden.",
            )
            return

        default_summary = "Click to expand"

        try:
            selected = editor.get("sel.first", "sel.last").strip()
            editor.delete("sel.first", "sel.last")
        except tk.TclError:
            selected = ""

        hidden_content = selected or "Hidden details here."
        block = (
            f"\n<details>\n"
            f"<summary>{default_summary}</summary>\n\n"
            f"{hidden_content}\n\n"
            f"</details>\n"
        )

        try:
            insert_index = editor.index("insert")
            line_start = editor.get(f"{insert_index} linestart", insert_index)
            if line_start.strip():
                block = "\n" + block

            editor.insert("insert", block)
            editor.see("insert")
            editor.focus_set()
            self.status_var.set("Hidden text block inserted in current documentation tab.")
        except tk.TclError:
            messagebox.showerror("Insert Failed", "Could not insert hidden text block.")


    def _insert_code_block(self) -> None:
        widget = self._get_current_doc_widget()
        if widget is None:
            return

        try:
            selection = widget.get("sel.first", "sel.last")
            widget.delete("sel.first", "sel.last")
            widget.insert("insert", f"```text\n{selection}\n```\n")
        except tk.TclError:
            widget.insert("insert", "```text\n\n```\n")
            widget.mark_set("insert", "insert -2 lines")

        widget.focus_set()

    def _handle_markdown_tab(self, event: tk.Event) -> str:
        widget = event.widget
        if isinstance(widget, tk.Text):
            widget.insert("insert", "    ")
        return "break"

    def _handle_markdown_return(self, event: tk.Event) -> str | None:
        widget = event.widget
        if not isinstance(widget, tk.Text):
            return None

        line_start = widget.index("insert linestart")
        line_end = widget.index("insert lineend")
        line = widget.get(line_start, line_end)

        bullet_match = re.match(r"^(\s*)([-*+])\s+(.*)$", line)
        checklist_match = re.match(r"^(\s*)-\s+\[[ xX]\]\s+(.*)$", line)
        numbered_match = re.match(r"^(\s*)(\d+)\.\s+(.*)$", line)

        if checklist_match:
            indent, content = checklist_match.groups()
            if not content.strip():
                widget.delete(line_start, line_end)
                return "break"
            widget.insert("insert", f"\n{indent}- [ ] ")
            return "break"

        if bullet_match:
            indent, bullet, content = bullet_match.groups()
            if not content.strip():
                widget.delete(line_start, line_end)
                return "break"
            widget.insert("insert", f"\n{indent}{bullet} ")
            return "break"

        if numbered_match:
            indent, number, content = numbered_match.groups()
            if not content.strip():
                widget.delete(line_start, line_end)
                return "break"
            widget.insert("insert", f"\n{indent}{int(number) + 1}. ")
            return "break"

        return None

    def _ask_revision_comment(self, doc_label: str) -> str | None:
        dialog = tk.Toplevel(self)
        dialog.title(f"Save {doc_label} Revision")
        dialog.transient(self)
        dialog.grab_set()
        dialog.resizable(False, False)

        frame = ttk.Frame(dialog, padding=16)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text=f"Add a comment for this {doc_label} revision").pack(anchor="w", pady=(0, 6))

        comment_text = tk.Text(frame, width=56, height=6, wrap="word", font=("Segoe UI", 10))
        comment_text.pack(fill="both", expand=True)

        hint = (
            "Example: Updated wiring notes after bench test, corrected ESC setup, "
            "or recorded results from test run 01."
        )
        ttk.Label(frame, text=hint, style="Subtitle.TLabel", wraplength=420).pack(anchor="w", pady=(8, 0))

        result: dict[str, str | None] = {"comment": None}

        def save_comment() -> None:
            result["comment"] = comment_text.get("1.0", "end").strip()
            dialog.destroy()

        def cancel() -> None:
            result["comment"] = None
            dialog.destroy()

        buttons = ttk.Frame(frame)
        buttons.pack(fill="x", pady=(12, 0))

        ttk.Button(buttons, text="Cancel", command=cancel).pack(side="right")
        ttk.Button(buttons, text="Save Revision", command=save_comment).pack(side="right", padx=(0, 8))

        comment_text.focus_set()
        self._center_child_window(dialog, width=520, height=300)
        self.wait_window(dialog)
        return result["comment"]

    def _save_current_doc_revision(self) -> None:
        project_dir = self._require_project()
        if project_dir is None:
            return

        widget = self._get_current_doc_widget()
        if widget is None:
            return

        selected_tab = self.docs_notebook.select()
        doc_label = self.docs_notebook.tab(selected_tab, "text") if selected_tab else ""

        content = widget.get("1.0", "end").rstrip()
        if not content:
            messagebox.showwarning("Empty Document", f"{doc_label} is empty. Nothing was revisioned.")
            return

        comment = self._ask_revision_comment(doc_label)
        if comment is None:
            self.status_var.set("Revision save cancelled.")
            return

        try:
            # Save the active document first, then write the revision copy.
            write_text_file(project_dir / DOC_TABS[doc_label], content + "\n")
            revision_path = save_doc_revision(project_dir, doc_label, content, comment)
        except (OSError, ValueError) as error:
            messagebox.showerror("Save Revision Failed", str(error))
            return

        self._touch_project()
        self.status_var.set(f"{doc_label} revision saved: {revision_path.name}")
        messagebox.showinfo(
            "Revision Saved",
            f"{doc_label} was saved as a local revision with your comment:\n\n{revision_path}",
        )

    def _insert_image_from_dialog(self) -> None:
        project_dir = self._require_project()
        if project_dir is None:
            return

        file_path = filedialog.askopenfilename(
            title="Insert Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.webp *.bmp"),
                ("All files", "*.*"),
            ],
        )
        if not file_path:
            return

        self._insert_image_file(Path(file_path))

    def _insert_image_file(self, source_path: Path) -> None:
        project_dir = self._require_project()
        if project_dir is None:
            return

        widget = self._get_current_doc_widget()
        if widget is None:
            return

        if not is_image_file(source_path):
            messagebox.showerror("Unsupported Image", "Use PNG, JPG, JPEG, GIF, WEBP, or BMP image files.")
            return

        try:
            copied_path = copy_image_to_project(project_dir, source_path)
        except (OSError, ValueError) as error:
            messagebox.showerror("Image Insert Failed", str(error))
            return

        width_text = self.image_width_var.get().strip()
        if not width_text.isdigit():
            width_text = "600"
            self.image_width_var.set(width_text)

        relative_path = copied_path.relative_to(project_dir).as_posix()
        image_markup = f'<img src="{relative_path}" width="{width_text}" alt="{copied_path.stem}">'

        widget.insert("insert", f"\n\n{image_markup}\n\n")
        self._insert_image_preview(widget, copied_path, image_markup)
        widget.focus_set()
        self.status_var.set(f"Image inserted: {copied_path.name}")

    def _insert_image_preview(self, widget: tk.Text, image_path: Path, image_markup: str) -> None:
        """
        Tkinter Text cannot provide true MS Word-style drag handles safely.
        This preview gives a bordered in-editor image control with resize buttons
        while keeping the saved Markdown GitHub-compatible.
        """
        try:
            image = tk.PhotoImage(file=str(image_path))
        except tk.TclError:
            # Tk PhotoImage may not support every image type on every platform.
            return

        max_preview_width = 360
        if image.width() > max_preview_width:
            sample = max(1, image.width() // max_preview_width)
            image = image.subsample(sample)

        self.editor_image_refs.append(image)

        frame = ttk.Frame(widget, padding=4, relief="solid", borderwidth=1)
        ttk.Label(frame, image=image).pack()
        ttk.Label(frame, text=image_path.name, style="Subtitle.TLabel").pack(anchor="center", pady=(3, 0))

        controls = ttk.Frame(frame)
        controls.pack(anchor="center", pady=(4, 0))

        ttk.Label(controls, text="Width").pack(side="left", padx=(0, 4))
        width_entry = ttk.Entry(controls, textvariable=self.image_width_var, width=6)
        width_entry.pack(side="left")

        def apply_width() -> None:
            width = self.image_width_var.get().strip()
            if not width.isdigit():
                messagebox.showwarning("Invalid Width", "Width must be a number, e.g. 600.")
                return

            current_line_start = widget.index("insert linestart")
            current_line_end = widget.index("insert lineend")
            # Insert updated markup at cursor as the reliable GitHub output.
            relative = image_path.relative_to(self.current_project).as_posix() if self.current_project else image_path.name
            widget.insert("insert", f'\n<img src="{relative}" width="{width}" alt="{image_path.stem}">\n')
            self.status_var.set(f"Inserted resized image markup: width {width}")

        ttk.Button(controls, text="Insert Resized Markup", command=apply_width).pack(side="left", padx=(6, 0))

        widget.window_create("insert", window=frame)
        widget.insert("insert", "\n")

    def _handle_doc_drop_or_paste_path(self, event: tk.Event) -> str | None:
        """
        Lightweight drag/drop support without external dependencies:
        if a file path is pasted or dropped as text into the editor, CodeM
        detects image paths and inserts them as project images.
        """
        widget = event.widget
        if not isinstance(widget, tk.Text):
            return None

        try:
            raw = self.clipboard_get().strip()
        except tk.TclError:
            return None

        candidate = raw.strip().strip('"').strip("'")
        if candidate.startswith("{") and candidate.endswith("}"):
            candidate = candidate[1:-1]

        path = Path(candidate)
        if path.exists() and is_image_file(path):
            self._insert_image_file(path)
            return "break"

        return None

    def _restore_current_doc_template(self) -> None:
        widget = self._get_current_doc_widget()
        if widget is None:
            return

        selected_tab = self.docs_notebook.select()
        tab_text = self.docs_notebook.tab(selected_tab, "text") if selected_tab else ""

        default_instructions = {
            "Overview": "Explain the purpose, problem, scope, objectives, and success criteria.",
            "Build Notes": "Document what was built, how it was implemented, and key decisions.",
            "Testing": "Document test objective, setup, procedure, observations, and outcome.",
            "Results": "Summarize findings, evidence, interpretation, lessons learned, and conclusion.",
            "Future Work": "List next actions, improvements, pending tests, resources, and risks.",
        }

        current_text = widget.get("1.0", "end").strip()
        if current_text:
            confirm = messagebox.askyesno(
                "Restore Template",
                f"Replace the current {tab_text} content with the default template?\n\n"
                "This will overwrite the visible text in this tab. Continue?",
            )
            if not confirm:
                return

        try:
            widget.edit_separator()
        except tk.TclError:
            pass

        widget.delete("1.0", "end")
        widget.insert(
            "1.0",
            generate_industry_doc_template(
                tab_text,
                default_instructions.get(tab_text, "Document this section."),
            ),
        )

        try:
            widget.edit_separator()
        except tk.TclError:
            pass

        widget.focus_set()
        self.status_var.set(f"{tab_text} template restored.")

    def _clean_current_conflict_markers(self) -> None:
        widget = self._get_current_doc_widget()
        if widget is None:
            return

        text = widget.get("1.0", "end")
        if not has_conflict_markers(text):
            messagebox.showinfo("No Conflict Markers", "No Git conflict markers were found in the current document.")
            return

        confirm = messagebox.askyesno(
            "Clean Conflict Markers",
            "This removes visible Git conflict marker lines only:\n"
            "<<<<<<<, =======, >>>>>>>\n\n"
            "It keeps the surrounding content so you can review it manually. Continue?",
        )
        if not confirm:
            return

        cleaned = strip_conflict_marker_lines(text)
        widget.delete("1.0", "end")
        widget.insert("1.0", cleaned)
        self.status_var.set("Conflict marker lines removed from current document.")

    # ---------------------------------------------------------------------
    # Docs and parts
    # ---------------------------------------------------------------------

    def _save_docs(self) -> bool:
        project_dir = self._require_project()
        if project_dir is None:
            return False

        try:
            conflict_docs: list[str] = []
            for label in DOC_TABS:
                content = self.editor_widgets[label].get("1.0", "end")
                if has_conflict_markers(content):
                    conflict_docs.append(label)

            if conflict_docs:
                proceed = messagebox.askyesno(
                    "Git Conflict Markers Found",
                    "These documents contain visible Git conflict markers:\n\n"
                    + "\n".join(f"- {name}" for name in conflict_docs)
                    + "\n\nSave after automatically removing marker lines and normalizing Markdown?",
                )
                if not proceed:
                    self.status_var.set("Save cancelled due to conflict markers.")
                    return False

            for label, relative_path in DOC_TABS.items():
                content = self.editor_widgets[label].get("1.0", "end").rstrip() + "\n"
                if has_conflict_markers(content):
                    content = strip_conflict_marker_lines(content)
                    self.editor_widgets[label].delete("1.0", "end")
                    self.editor_widgets[label].insert("1.0", content)

                content = normalize_markdown_lists(content)
                self.editor_widgets[label].delete("1.0", "end")
                self.editor_widgets[label].insert("1.0", content)
                write_text_file(project_dir / relative_path, content)
        except OSError as error:
            messagebox.showerror("Save Docs Failed", str(error))
            return False

        self._touch_project()
        self.status_var.set("Docs saved.")
        return True

    def _render_parts_grid_headers(self) -> None:
        # Fixed No. column + proportional data columns that fit the visible area.
        headers = ["No.", *PARTS_HEADERS]
        weights = {
            "No.": 0,
            "Code": 1,
            "Part Number": 2,
            "Description": 4,
            "Qty": 1,
            "UOM": 1,
            "Purpose": 3,
            "Cost": 1,
            "Supplier": 2,
            "Image": 2,
            "Notes": 4,
        }
        min_widths = {
            "No.": 36,
            "Code": 60,
            "Part Number": 95,
            "Description": 150,
            "Qty": 50,
            "UOM": 50,
            "Purpose": 120,
            "Cost": 60,
            "Supplier": 90,
            "Image": 70,
            "Notes": 150,
        }

        for col, header in enumerate(headers):
            label = ttk.Label(self.parts_grid_frame, text=header, style="PartsHeader.TLabel", anchor="w")
            label.grid(row=0, column=col, sticky="nsew", padx=2, pady=(0, 5))
            self.parts_grid_frame.columnconfigure(
                col,
                weight=weights.get(header, 1),
                minsize=min_widths.get(header, 80),
            )

    def _refresh_part_row_numbers(self) -> None:
        for index, row_widgets in enumerate(self.parts_grid_entries, start=1):
            number_label = row_widgets[0]
            if isinstance(number_label, ttk.Label):
                number_label.configure(text=str(index))

    def _find_parts_cell_position(self, widget: tk.Widget) -> tuple[int, int] | None:
        for row_index, row_widgets in enumerate(self.parts_grid_entries):
            for col_index, cell in enumerate(row_widgets[1:]):
                if cell == widget:
                    return row_index, col_index
        return None

    def _focus_parts_cell(self, row_index: int, col_index: int) -> None:
        if row_index < 0:
            row_index = 0
        if col_index < 0:
            col_index = 0

        if row_index >= len(self.parts_grid_entries):
            self._add_parts_grid_rows(row_index - len(self.parts_grid_entries) + 1)

        max_col = len(PARTS_HEADERS) - 1
        if col_index > max_col:
            col_index = max_col

        target = self.parts_grid_entries[row_index][col_index + 1]
        target.focus_set()

        if isinstance(target, ttk.Entry):
            target.icursor("end")
        elif isinstance(target, tk.Text):
            target.mark_set("insert", "end-1c")

    def _remember_parts_cell(self, widget: tk.Widget) -> None:
        self.current_parts_cell = widget

    def _get_current_parts_row_index(self) -> int | None:
        widget = getattr(self, "current_parts_cell", None)
        if widget is None:
            return None

        position = self._find_parts_cell_position(widget)
        if position is None:
            return None

        row_index, _col_index = position
        return row_index

    def _upload_part_image(self, row_index: int | None = None) -> None:
        project_dir = self._require_project()
        if project_dir is None:
            return

        if row_index is None:
            row_index = self._get_current_parts_row_index()

        if row_index is None:
            messagebox.showwarning("No Row Selected", "Click the + button in the target Image cell.")
            return

        file_path = filedialog.askopenfilename(
            title="Upload Part Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.webp *.bmp"),
                ("All files", "*.*"),
            ],
        )
        if not file_path:
            return

        source_path = Path(file_path)
        if not is_image_file(source_path):
            messagebox.showerror("Unsupported Image", "Use PNG, JPG, JPEG, GIF, WEBP, or BMP image files.")
            return

        try:
            copied_path = copy_image_to_project(project_dir, source_path)
            relative_path = copied_path.relative_to(project_dir).as_posix()
        except (OSError, ValueError) as error:
            messagebox.showerror("Image Upload Failed", str(error))
            return

        image_col_index = PARTS_HEADERS.index("Image")
        image_widget = self.parts_grid_entries[row_index][image_col_index + 1]

        if isinstance(image_widget, ttk.Button):
            setattr(image_widget, "codem_image_path", relative_path)
            image_widget.configure(text="✓")
        elif isinstance(image_widget, tk.Text):
            image_widget.delete("1.0", "end")
            image_widget.insert("1.0", relative_path)
        elif isinstance(image_widget, ttk.Entry):
            image_widget.delete(0, "end")
            image_widget.insert(0, relative_path)

        self.status_var.set(f"Part image uploaded: {copied_path.name}")


    def _show_part_image_menu(self, event: tk.Event, row_index: int, button: ttk.Button) -> str:
        self.current_part_image_row = row_index
        self.current_part_image_button = button

        try:
            self.part_image_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.part_image_menu.grab_release()

        return "break"

    def _part_image_menu_upload(self) -> None:
        self._upload_part_image(self.current_part_image_row)

    def _part_image_menu_remove(self) -> None:
        button = self.current_part_image_button
        if button is None:
            return

        image_path = str(getattr(button, "codem_image_path", "")).strip()
        if not image_path:
            self.status_var.set("No image attached to remove.")
            return

        confirm = messagebox.askyesno(
            "Remove Part Image",
            "Remove the image reference from this parts row?\n\n"
            "This does not delete the image file from the project images folder.",
        )
        if not confirm:
            return

        setattr(button, "codem_image_path", "")
        button.configure(text="+")
        self.status_var.set("Part image reference removed.")

    def _part_image_menu_copy_path(self) -> None:
        button = self.current_part_image_button
        if button is None:
            return

        image_path = str(getattr(button, "codem_image_path", "")).strip()
        if not image_path:
            self.status_var.set("No image path to copy.")
            return

        self.clipboard_clear()
        self.clipboard_append(image_path)
        self.status_var.set("Image path copied.")

    def _part_image_menu_open(self) -> None:
        button = self.current_part_image_button
        project_dir = self.current_project
        if button is None or project_dir is None:
            return

        image_path = str(getattr(button, "codem_image_path", "")).strip()
        if not image_path:
            messagebox.showinfo("No Image", "No image is attached to this row.")
            return

        full_path = project_dir / image_path
        if not full_path.exists():
            messagebox.showerror("Image Not Found", f"Image file not found:\n{full_path}")
            return

        open_folder(full_path.parent)

    def _focus_next_parts_cell(self, widget: tk.Widget) -> str:
        position = self._find_parts_cell_position(widget)
        if position is None:
            return "break"

        row_index, col_index = position
        col_index += 1

        if col_index >= len(PARTS_HEADERS):
            row_index += 1
            col_index = 0

        self._focus_parts_cell(row_index, col_index)
        return "break"

    def _navigate_parts_cell(self, widget: tk.Widget, direction: str) -> str:
        position = self._find_parts_cell_position(widget)
        if position is None:
            return "break"

        row_index, col_index = position

        if direction == "left":
            col_index -= 1
        elif direction == "right":
            col_index += 1
        elif direction == "up":
            row_index -= 1
        elif direction == "down":
            row_index += 1

        if col_index < 0:
            if row_index > 0:
                row_index -= 1
                col_index = len(PARTS_HEADERS) - 1
            else:
                col_index = 0

        if col_index >= len(PARTS_HEADERS):
            row_index += 1
            col_index = 0

        self._focus_parts_cell(row_index, col_index)
        return "break"

    def _create_part_cell(self, parent: ttk.Frame, value: str) -> tk.Text:
        cell = tk.Text(
            parent,
            height=1,
            wrap="word",
            font=("Segoe UI", 9),
            padx=4,
            pady=2,
            relief="solid",
            borderwidth=1,
            undo=True,
            autoseparators=True,
        )
        cell.insert("1.0", value)
        cell.bind("<FocusIn>", lambda _event, w=cell: self._remember_parts_cell(w))
        cell.bind("<Tab>", lambda _event, w=cell: self._focus_next_parts_cell(w))
        cell.bind("<Right>", lambda _event, w=cell: self._navigate_parts_cell(w, "right"))
        cell.bind("<Left>", lambda _event, w=cell: self._navigate_parts_cell(w, "left"))
        cell.bind("<Up>", lambda _event, w=cell: self._navigate_parts_cell(w, "up"))
        cell.bind("<Down>", lambda _event, w=cell: self._navigate_parts_cell(w, "down"))
        cell.bind("<Return>", lambda _event: "break")
        return cell

    def _add_parts_grid_rows(self, count: int = 5, rows: list[list[str]] | None = None) -> None:
        rows_to_add = rows if rows is not None else [[""] * len(PARTS_HEADERS) for _ in range(count)]

        for row_values in rows_to_add:
            row_index = len(self.parts_grid_entries) + 1
            padded = row_values[: len(PARTS_HEADERS)] + [""] * (len(PARTS_HEADERS) - len(row_values))
            row_widgets: list[tk.Widget] = []

            number_label = ttk.Label(self.parts_grid_frame, text=str(row_index), anchor="center")
            number_label.grid(row=row_index, column=0, sticky="nsew", padx=2, pady=2)
            row_widgets.append(number_label)

            image_col_number = PARTS_HEADERS.index("Image") + 1

            for col, value in enumerate(padded, start=1):
                if col == image_col_number:
                    stored_image_value = "" if value.strip().lower() == "notes" else value.strip()
                    button_text = "✓" if stored_image_value else "+"
                    cell = ttk.Button(
                        self.parts_grid_frame,
                        text=button_text,
                        width=4,
                        command=lambda r=row_index - 1: self._upload_part_image(r),
                    )
                    setattr(cell, "codem_image_path", stored_image_value)
                    cell.bind(
                        "<Button-3>",
                        lambda event, r=row_index - 1, b=cell: self._show_part_image_menu(event, r, b),
                    )
                else:
                    cell = self._create_part_cell(self.parts_grid_frame, value)

                cell.grid(row=row_index, column=col, sticky="nsew", padx=2, pady=2)
                row_widgets.append(cell)

            self.parts_grid_frame.rowconfigure(row_index, weight=0, minsize=30)
            self.parts_grid_entries.append(row_widgets)

        self._refresh_part_row_numbers()

    def _clear_parts_grid(self) -> None:
        for row_widgets in self.parts_grid_entries:
            for widget in row_widgets:
                widget.destroy()
        self.parts_grid_entries.clear()

    def _clear_empty_part_rows(self) -> None:
        rows = self._collect_parts_rows()
        self._clear_parts_grid()
        if rows:
            self._add_parts_grid_rows(rows=rows)
        minimum_blank_rows = max(0, 5 - len(rows))
        if minimum_blank_rows:
            self._add_parts_grid_rows(minimum_blank_rows)
        self.status_var.set("Empty part rows cleared.")

    def _add_parts_row(self, values: list[str] | None = None) -> None:
        # Compatibility method for older call sites.
        self._add_parts_grid_rows(1, rows=[values or [""] * len(PARTS_HEADERS)])

    def _load_parts(self, path: Path) -> None:
        self._clear_parts_grid()
        rows = load_parts_csv(path)
        if rows:
            self._add_parts_grid_rows(rows=rows)

        blank_rows_needed = max(5 - len(rows), 0)
        if blank_rows_needed:
            self._add_parts_grid_rows(blank_rows_needed)

    def _collect_parts_rows(self) -> list[list[str]]:
        rows: list[list[str]] = []
        for row_widgets in self.parts_grid_entries:
            # First widget is the fixed row number label, so skip it.
            values: list[str] = []
            for widget in row_widgets[1:]:
                if isinstance(widget, ttk.Entry):
                    values.append(widget.get().strip())
                elif isinstance(widget, tk.Text):
                    value = " ".join(widget.get("1.0", "end").split())
                    values.append(value)
                elif isinstance(widget, ttk.Button):
                    values.append(str(getattr(widget, "codem_image_path", "")).strip())
            if any(values):
                rows.append(values)
        return rows

    def _save_parts(self) -> bool:
        project_dir = self._require_project()
        if project_dir is None:
            return False

        try:
            save_parts_csv(project_dir / "parts" / "parts_list.csv", self._collect_parts_rows())
        except OSError as error:
            messagebox.showerror("Save Parts Failed", str(error))
            return False

        self._touch_project()
        self.status_var.set("Parts saved.")
        return True

    def _save_all(self) -> None:
        self._prepare_operation("Saving project files...")
        if not self._save_docs():
            return
        if not self._save_parts():
            return
        self._compile_readme(show_message=False)
        self.status_var.set("All saved and README compiled.")

    def _touch_project(self) -> None:
        project_dir = self.current_project
        if project_dir is None:
            return

        metadata_path = project_dir / "project.json"
        if not metadata_path.exists():
            return

        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            metadata["updated_at"] = now_string()
            metadata["app_revision"] = APP_VERSION
            metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
        except (OSError, json.JSONDecodeError):
            return

    # ---------------------------------------------------------------------
    # Export actions
    # ---------------------------------------------------------------------

    def _compile_readme(self, show_message: bool = True) -> None:
        project_dir = self._require_project()
        if project_dir is None:
            return

        if not self._save_docs():
            return
        if not self._save_parts():
            return

        try:
            readme = generate_readme_from_project(project_dir)
            write_text_file(project_dir / "README.md", readme)
        except OSError as error:
            messagebox.showerror("README Failed", str(error))
            return

        self._touch_project()
        self.status_var.set("README compiled.")
        if show_message:
            messagebox.showinfo("README", "README.md compiled successfully.")

    def _export_showcase_brief(self) -> None:
        project_dir = self._require_project()
        if project_dir is None:
            return

        if not self._save_docs():
            return
        if not self._save_parts():
            return

        try:
            output_path = project_dir / "exports" / "showcase_brief.md"
            write_text_file(output_path, generate_showcase_brief(project_dir))
        except OSError as error:
            messagebox.showerror("Export Failed", str(error))
            return

        self._touch_project()
        self.status_var.set("Showcase brief exported.")
        messagebox.showinfo("Export Complete", f"Showcase brief exported:\n\n{output_path}")

    # ---------------------------------------------------------------------
    # Git core UI helpers
    # ---------------------------------------------------------------------

    def _append_git_output(self, text: str) -> None:
        self.git_output.insert("end", text.rstrip() + "\n\n")
        self.git_output.see("end")

    def _require_git_project(self) -> Path | None:
        return self._require_project()

    def _load_git_identity_if_available(self, project_dir: Path) -> None:
        git_root = get_project_git_root(project_dir)
        success_name, name = git_get_user(git_root)
        success_email, email = git_get_email(git_root)

        if success_name:
            self.git_name_var.set(name.strip())
        if success_email:
            self.git_email_var.set(email.strip())

    def _git_load_identity(self) -> None:
        project_dir = self._require_git_project()
        if project_dir is None:
            return

        self._load_git_identity_if_available(project_dir)
        self._append_git_output("Loaded Git author identity.")
        self.status_var.set("Git author identity loaded.")

    def _git_save_identity(self) -> bool:
        project_dir = self._require_git_project()
        if project_dir is None:
            return False

        username = self.git_name_var.get().strip()
        email = self.git_email_var.get().strip()

        if not username or not email:
            messagebox.showwarning("Missing Identity", "Enter both Git Name and Git Email.")
            return False

        combined = f"{username} {email}".lower()
        unsafe_markers = ["ghp_", "github_pat_", "token", "password"]
        if any(marker in combined for marker in unsafe_markers):
            messagebox.showerror("Unsafe Input", "Git identity must not contain tokens, passwords, or credentials.")
            return False

        success, output = git_set_identity(get_project_git_root(project_dir), username, email)
        self._append_git_output(f"$ git config user.name/user.email\n{output}")
        self.status_var.set("Git author identity saved." if success else "Git identity failed.")
        return success

    def _validate_remote_url(self) -> None:
        raw_url = self.remote_url_text.get("1.0", "end").strip()
        is_valid, clean_url, message = sanitize_github_remote_url(raw_url)

        if not is_valid:
            messagebox.showerror("Unsafe or Invalid Repository URL", message)
            self._append_git_output(f"Repository URL rejected: {message}")
            self.status_var.set("Repository URL rejected.")
            return

        self.remote_url_text.delete("1.0", "end")
        self.remote_url_text.insert("1.0", clean_url)
        self._append_git_output(f"Repository URL validated: {mask_remote_url_for_display(clean_url)}")
        self.status_var.set("Repository URL validated.")

    def _configure_remote(self, project_dir: Path) -> bool:
        raw_url = self.remote_url_text.get("1.0", "end").strip()
        is_valid, clean_url, message = sanitize_github_remote_url(raw_url)

        if not is_valid:
            messagebox.showerror("Unsafe or Invalid Repository URL", message)
            self._append_git_output(f"Repository URL rejected: {message}")
            return False

        self.remote_url_text.delete("1.0", "end")
        self.remote_url_text.insert("1.0", clean_url)

        git_root = get_project_git_root(project_dir)
        success, output = git_init(git_root)
        self._append_git_output(f"$ git init  # root: {git_root}\n{output}")
        if not success:
            return False

        git_branch_main(git_root)

        success, output = git_add_or_set_remote(git_root, clean_url)
        self._append_git_output(f"$ git remote add/set origin {mask_remote_url_for_display(clean_url)}\n{output}")

        return success

    def _prepare_project_folder_for_git(self, project_dir: Path) -> bool:
        success, message = protect_nested_git_folder(project_dir)
        self._append_git_output(message)

        if not success:
            messagebox.showerror(
                "Nested Git Repository Found",
                "CodeM found an old .git repository inside the project folder and could not move it safely.\n\n"
                "Close editors/terminals using this folder and try again.",
            )
            return False

        return True

    def _pull_remote_before_project_stage(self, git_root: Path) -> bool:
        """
        Pull remote repository root before staging the selected project folder.

        This avoids the common conflict where GitHub already has root files
        such as LICENSE or README.md from repository creation.
        """
        if not git_remote_has_main(git_root):
            self._append_git_output("Remote main branch not found yet. Skipping pre-stage pull.")
            return True

        success, output = git_pull_rebase_autostash(git_root)
        self._append_git_output(f"$ git pull --rebase --autostash origin main  # pre-stage root sync\n{output}")

        if success:
            return True

        if "refusing to merge unrelated histories" in output.lower():
            success, output = git_pull_merge_allow_unrelated(git_root)
            self._append_git_output(f"$ git pull --allow-unrelated-histories --no-edit origin main\n{output}")
            return success

        return False

    def _git_status(self) -> None:
        self._prepare_operation("Checking Git status...")
        project_dir = self._require_git_project()
        if project_dir is None:
            return

        git_root = get_project_git_root(project_dir)
        success, output = git_status_full(git_root)
        self._append_git_output(f"$ git status  # root: {git_root}\n{output}")
        self.status_var.set("Git status checked." if success else "Git status failed.")

    def _git_check_state(self) -> None:
        project_dir = self._require_git_project()
        if project_dir is None:
            return

        git_root = get_project_git_root(project_dir)
        state = git_operation_state(git_root)
        success, status = git_status_full(git_root)
        self._append_git_output(f"Git operation state: {state}\n\n$ git status  # root: {git_root}\n{status}")
        self.status_var.set(f"Git state: {state}" if success else "Git state check failed.")

    def _git_fix_stuck_sync(self) -> None:
        project_dir = self._require_git_project()
        if project_dir is None:
            return

        git_root = get_project_git_root(project_dir)
        state = git_operation_state(git_root)
        success_status, status = git_status_full(git_root)
        self._append_git_output(f"Git operation state before repair: {state}\n\n$ git status\n{status}")

        if state == "clean" or state == "not initialized":
            messagebox.showinfo("No Repair Needed", "Git is not stuck in a rebase or merge operation.")
            self.status_var.set("No repair needed.")
            return

        if state == "rebase in progress":
            # First try to finish the rebase without opening an editor.
            success, output = git_rebase_continue_no_edit(git_root)
            self._append_git_output(f"$ git -c core.editor=true rebase --continue\n{output}")

            if success:
                self.status_var.set("Stuck rebase fixed.")
                messagebox.showinfo("Repair Complete", "Rebase was completed. You can now Pull Updates or Push to GitHub.")
                self._git_load_history(silent=True)
                return

            # If there is nothing to continue, user can abort safely.
            ask_abort = messagebox.askyesno(
                "Continue Failed",
                "CodeM could not finish the rebase automatically.\n\n"
                "Do you want CodeM to abort the unfinished rebase state?",
            )
            if ask_abort:
                success_abort, output_abort = git_rebase_abort(git_root)
                self._append_git_output(f"$ git rebase --abort\n{output_abort}")
                self.status_var.set("Rebase aborted." if success_abort else "Abort rebase failed.")
            return

        if state == "merge in progress":
            ask_abort = messagebox.askyesno(
                "Merge In Progress",
                "A merge is in progress. Do you want CodeM to abort the merge?",
            )
            if ask_abort:
                success_abort, output_abort = git_merge_abort(git_root)
                self._append_git_output(f"$ git merge --abort\n{output_abort}")
                self.status_var.set("Merge aborted." if success_abort else "Abort merge failed.")
            return

        messagebox.showwarning("Manual Repair Needed", f"Git state needs manual review: {state}")
        self.status_var.set(f"Manual repair needed: {state}")

    def _git_abort_rebase(self) -> None:
        project_dir = self._require_git_project()
        if project_dir is None:
            return

        confirm = messagebox.askyesno(
            "Abort Rebase",
            "This will abort the current rebase operation and return the repository to its pre-rebase state.\n\nContinue?",
        )
        if not confirm:
            return

        success, output = git_rebase_abort(get_project_git_root(project_dir))
        self._append_git_output(f"$ git rebase --abort\n{output}")
        self.status_var.set("Rebase aborted." if success else "Abort rebase failed.")

    def _git_continue_rebase(self) -> None:
        project_dir = self._require_git_project()
        if project_dir is None:
            return

        success, output = git_rebase_continue(get_project_git_root(project_dir))
        self._append_git_output(f"$ git rebase --continue\n{output}")
        self.status_var.set("Rebase continued." if success else "Continue rebase failed.")

    def _git_abort_merge(self) -> None:
        project_dir = self._require_git_project()
        if project_dir is None:
            return

        confirm = messagebox.askyesno(
            "Abort Merge",
            "This will abort the current merge operation.\n\nContinue?",
        )
        if not confirm:
            return

        success, output = git_merge_abort(get_project_git_root(project_dir))
        self._append_git_output(f"$ git merge --abort\n{output}")
        self.status_var.set("Merge aborted." if success else "Abort merge failed.")

    # ---------------------------------------------------------------------
    # Git workflow
    # ---------------------------------------------------------------------

    def _ensure_identity_if_entered(self, project_dir: Path) -> bool:
        username = self.git_name_var.get().strip()
        email = self.git_email_var.get().strip()

        if not username and not email:
            return True

        if not username or not email:
            messagebox.showwarning(
                "Incomplete Identity",
                "Enter both Git Name and Git Email, or leave both blank to use existing Git config.",
            )
            return False

        unsafe_markers = ["ghp_", "github_pat_", "token", "password"]
        if any(marker in f"{username} {email}".lower() for marker in unsafe_markers):
            messagebox.showerror("Unsafe Input", "Git identity must not contain tokens, passwords, or credentials.")
            return False

        success, output = git_set_identity(get_project_git_root(project_dir), username, email)
        self._append_git_output(f"$ git config user.name/user.email\n{output}")
        return success

    def _git_pull(self) -> None:
        project_dir = self._require_git_project()
        if project_dir is None:
            return

        git_root = get_project_git_root(project_dir)
        state = git_operation_state(git_root)
        if state != "clean" and state != "not initialized":
            repair = messagebox.askyesno(
                "Git Operation In Progress",
                f"Git state: {state}\n\nDo you want CodeM to try Fix Stuck Sync now?",
            )
            if repair:
                self._git_fix_stuck_sync()
            return

        if not self._configure_remote(project_dir):
            self.status_var.set("Remote setup failed.")
            return

        success, output = git_pull_rebase_autostash(git_root)
        self._append_git_output(f"$ git pull --rebase --autostash origin main  # root: {git_root}\n{output}")

        if not success and "refusing to merge unrelated histories" in output.lower():
            success, output = git_pull_merge_allow_unrelated(git_root)
            self._append_git_output(f"$ git pull --allow-unrelated-histories --no-edit origin main  # root: {git_root}\n{output}")

        if success:
            self._load_project(project_dir)
            self._git_load_history(silent=True)
            self.status_var.set("Pulled latest GitHub updates.")
            messagebox.showinfo("Pull Complete", "Latest GitHub updates were pulled into the project.")
        else:
            self.status_var.set("Git pull failed.")
            messagebox.showwarning(
                "Pull Failed",
                "Git could not pull updates automatically.\n\n"
                "Check Git Output. If it says a rebase is in progress, use Sync Repair → Abort Rebase.",
            )

    def _git_commit_only(self) -> None:
        project_dir = self._require_git_project()
        if project_dir is None:
            return

        raw_message = self.commit_message_var.get()
        message = sanitize_commit_message(raw_message)
        self.commit_message_var.set(message)
        if not message:
            messagebox.showwarning("Missing Commit Message", "Enter a commit message first.")
            return

        if not self._save_docs() or not self._save_parts():
            return
        self._compile_readme(show_message=False)

        git_root = get_project_git_root(project_dir)

        success, output = git_init(git_root)
        self._append_git_output(f"$ git init  # root: {git_root}\n{output}")
        if not success:
            return

        if not self._ensure_identity_if_entered(project_dir):
            self.status_var.set("Git identity incomplete.")
            return

        if not self._prepare_project_folder_for_git(project_dir):
            self.status_var.set("Project folder Git prep failed.")
            return

        success, output = git_add_project_folder(git_root, project_dir)
        self._append_git_output(f"$ git add {get_project_repo_path(project_dir)}\n{output}")
        if not success:
            self.status_var.set("Git add failed.")
            messagebox.showerror(
                "Git Add Failed",
                "CodeM could not stage the project folder.\n\n"
                "Check Git Output. This usually means a nested repository or locked file still exists.",
            )
            return

        success, output = git_commit(git_root, message)
        self._append_git_output(f"$ git commit -m \"{message}\"\n{output}")

        if success:
            self._git_load_history(silent=True)
            self.status_var.set("Project folder committed.")
            messagebox.showinfo("Commit Complete", "Selected project folder was committed.")
        else:
            self.status_var.set("No commit created or commit failed.")
            messagebox.showinfo(
                "Commit Not Created",
                "Git did not create a commit. This usually means there were no file changes to commit.",
            )

    def _git_push(self) -> None:
        project_dir = self._require_git_project()
        if project_dir is None:
            return

        git_root = get_project_git_root(project_dir)
        state = git_operation_state(git_root)
        if state != "clean" and state != "not initialized":
            repair = messagebox.askyesno(
                "Git Operation In Progress",
                f"Git state: {state}\n\nDo you want CodeM to try Fix Stuck Sync now?",
            )
            if repair:
                self._git_fix_stuck_sync()
            return

        if not self._configure_remote(project_dir):
            self.status_var.set("Remote setup failed.")
            return

        raw_message = self.commit_message_var.get()
        message = sanitize_commit_message(raw_message)
        self.commit_message_var.set(message)
        if not message:
            messagebox.showwarning("Missing Commit Message", "Enter a commit message before publishing.")
            return

        if not self._save_docs() or not self._save_parts():
            return
        self._compile_readme(show_message=False)

        if not self._ensure_identity_if_entered(project_dir):
            self.status_var.set("Git identity incomplete.")
            return

        if not self._prepare_project_folder_for_git(project_dir):
            self.status_var.set("Project folder Git prep failed.")
            return

        # Pull remote root files first, before staging project folder.
        if not self._pull_remote_before_project_stage(git_root):
            self.status_var.set("Pre-stage pull failed.")
            messagebox.showwarning(
                "Pull Failed",
                "CodeM could not integrate the existing GitHub repository before staging this project.\n\n"
                "Check Git Output, then use Repair if Git reports rebase/merge in progress.",
            )
            return

        success_add, output_add = git_add_project_folder(git_root, project_dir)
        self._append_git_output(f"$ git add {get_project_repo_path(project_dir)}\n{output_add}")

        if not success_add:
            self.status_var.set("Git add failed.")
            messagebox.showerror(
                "Git Add Failed",
                "CodeM could not stage the selected project folder.\n\n"
                "If this project was created using an older CodeM revision, a nested .git folder may still be locked.\n"
                "Close VS Code/terminals using that folder and try again.",
            )
            return

        success_commit, output_commit = git_commit(git_root, message)
        self._append_git_output(f"$ git commit -m \"{message}\"\n{output_commit}")

        if not success_commit:
            self._append_git_output("No new commit may have been created. Continuing to push existing committed changes.")

        # Final pull after commit for team safety.
        success_pull, output_pull = git_pull_rebase_autostash(git_root)
        self._append_git_output(f"$ git pull --rebase --autostash origin main  # final team sync\n{output_pull}")

        if not success_pull and "refusing to merge unrelated histories" in output_pull.lower():
            success_pull, output_pull = git_pull_merge_allow_unrelated(git_root)
            self._append_git_output(f"$ git pull --allow-unrelated-histories --no-edit origin main\n{output_pull}")

        if not success_pull:
            self.status_var.set("Final pull before push failed.")
            messagebox.showwarning(
                "Push Stopped",
                "CodeM stopped before pushing because GitHub updates could not be integrated safely.\n\n"
                "Check Git Output. Use Repair if Git reports rebase/merge in progress.",
            )
            return

        success_push, output_push = git_push_main(git_root)
        self._append_git_output(f"$ git push -u origin main\n{output_push}")

        if success_push:
            self._load_project(project_dir)
            self._git_load_history(silent=True)
            self.status_var.set("Project folder pushed to GitHub.")
            messagebox.showinfo(
                "Push Complete",
                "Selected project folder was safely pushed to GitHub.\n\n"
                f"Published folder: {get_project_repo_path(project_dir)}",
            )
        else:
            self.status_var.set("Git push failed.")
            messagebox.showwarning(
                "Push Failed",
                "Push failed after safe sync.\n\n"
                "Check Git Output for authentication, conflict, or branch protection details.",
            )

    # ---------------------------------------------------------------------
    # Recovery history
    # ---------------------------------------------------------------------

    def _git_load_history(self, silent: bool = False) -> None:
        project_dir = self._require_git_project()
        if project_dir is None:
            return

        success, output = git_log_history(get_project_git_root(project_dir))

        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        if not success:
            if not silent:
                self._append_git_output(f"$ git log\n{output}")
                self.status_var.set("History load failed.")
            return

        rows = [line for line in output.splitlines() if line.strip()]
        for line in rows:
            parts = line.split("\x1f")
            if len(parts) != 4:
                continue

            commit_hash, author, date_time, message = parts
            self.history_tree.insert(
                "",
                "end",
                iid=commit_hash,
                values=(commit_hash, author, date_time, message),
            )

        if not silent:
            self._append_git_output(f"Loaded {len(rows)} commit history event(s).")
            self.status_var.set(f"Loaded {len(rows)} history event(s).")

    def _get_selected_history_commit(self) -> str | None:
        selection = self.history_tree.selection()
        if not selection:
            messagebox.showwarning("No Commit Selected", "Select a recovery event from the history log first.")
            return None
        return selection[0]

    def _git_preview_selected_commit(self) -> None:
        project_dir = self._require_git_project()
        if project_dir is None:
            return

        commit_hash = self._get_selected_history_commit()
        if commit_hash is None:
            return

        success, output = git_show_commit(get_project_git_root(project_dir), commit_hash)
        self._append_git_output(f"$ git show --stat --summary {commit_hash}\n{output}")
        self.status_var.set("Commit preview loaded." if success else "Commit preview failed.")

    def _git_recover_selected_commit(self) -> None:
        project_dir = self._require_git_project()
        if project_dir is None:
            return

        commit_hash = self._get_selected_history_commit()
        if commit_hash is None:
            return

        selected_values = self.history_tree.item(commit_hash, "values")
        selected_author = selected_values[1] if len(selected_values) >= 2 else "Unknown"
        selected_date = selected_values[2] if len(selected_values) >= 3 else "Unknown date"
        selected_message = selected_values[3] if len(selected_values) >= 4 else commit_hash

        confirm = messagebox.askyesno(
            "Recover Selected Commit",
            "CodeM will restore the selected snapshot and create a NEW recovery commit.\n\n"
            "This preserves full project history instead of deleting later history.\n\n"
            f"Selected commit: {commit_hash}\n"
            f"Who: {selected_author}\n"
            f"Date/time: {selected_date}\n"
            f"Message: {selected_message}\n\n"
            "Uncommitted local changes may be overwritten by the restored snapshot. Continue?",
        )
        if not confirm:
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_branch = f"codem-safety-backup-before-restore-{timestamp}"

        git_root = get_project_git_root(project_dir)
        success_backup, output_backup = git_create_branch(git_root, backup_branch)
        self._append_git_output(f"$ git branch {backup_branch}\n{output_backup}")

        if not success_backup:
            self.status_var.set("Backup branch failed. Recovery stopped.")
            messagebox.showerror(
                "Backup Failed",
                "CodeM stopped recovery because it could not create a safety backup branch.",
            )
            return

        success_restore, output_restore = run_git_command(git_root, ["restore", "--source", commit_hash, "--", get_project_repo_path(project_dir)])
        self._append_git_output(f"$ git restore --source {commit_hash} -- {get_project_repo_path(project_dir)}\n{output_restore}")

        if not success_restore:
            self.status_var.set("Restore failed.")
            return

        success_add, output_add = git_add_project_folder(git_root, project_dir)
        self._append_git_output(f"$ git add {get_project_repo_path(project_dir)}\n{output_add}")

        if not success_add:
            self.status_var.set("Git add failed after restore.")
            return

        recovery_source = f"{commit_hash} | {selected_author} | {selected_date} | {selected_message}"
        success_commit, output_commit = git_commit_recovery(git_root, commit_hash, recovery_source)
        self._append_git_output(f"$ git commit recovery\n{output_commit}")

        if success_commit:
            self._load_project(project_dir)
            self._git_load_history(silent=True)
            self.status_var.set("Recovery committed as new history event.")
            messagebox.showinfo(
                "Recovery Complete",
                "Recovered snapshot was saved as a NEW commit.\n\n"
                "The previous timeline was preserved.\n\n"
                f"Safety backup branch created:\n{backup_branch}",
            )
        else:
            self.status_var.set("No recovery commit created.")
            messagebox.showinfo(
                "No Recovery Commit Created",
                "Git did not create a recovery commit. This may mean the selected snapshot matches the current project state.",
            )


def main() -> None:
    app = CodeMApp()
    app.mainloop()


if __name__ == "__main__":
    main()
