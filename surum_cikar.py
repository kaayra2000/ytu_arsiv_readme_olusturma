#!/usr/bin/env python3
"""Release helper script for semantic version tagging with a merge flow.

Flow:
1) Merge main into current feature branch.
2) Checkout main and merge feature branch into main.
3) Calculate next semantic version tag (major/minor/patch).
4) Create annotated tag with release note.
5) Push main and tag to remote.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass


SEMVER_RE = re.compile(r"^(?P<prefix>v?)(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)$")


@dataclass(frozen=True)
class SemVer:
    major: int
    minor: int
    patch: int

    def bump(self, kind: str) -> "SemVer":
        if kind == "major":
            return SemVer(self.major + 1, 0, 0)
        if kind == "minor":
            return SemVer(self.major, self.minor + 1, 0)
        if kind == "patch":
            return SemVer(self.major, self.minor, self.patch + 1)
        raise ValueError(f"Unsupported bump kind: {kind}")

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"


def run_git(cmd: list[str], check: bool = True, capture: bool = False, dry_run: bool = False) -> str:
    full_cmd = ["git", *cmd]
    print("$", " ".join(full_cmd))
    if dry_run:
        return ""
    completed = subprocess.run(
        full_cmd,
        check=check,
        text=True,
        capture_output=capture,
    )
    if capture:
        return completed.stdout.strip()
    return ""


def ensure_git_repo(dry_run: bool) -> None:
    try:
        run_git(["rev-parse", "--is-inside-work-tree"], capture=True, dry_run=dry_run)
    except subprocess.CalledProcessError as exc:
        raise RuntimeError("Current directory is not a git repository.") from exc


def get_worktree_status(dry_run: bool) -> str:
    if dry_run:
        return ""
    return run_git(["status", "--porcelain"], capture=True, dry_run=False)


def maybe_create_release_commit(
    source_branch: str,
    auto_commit: bool,
    commit_message: str,
    auto_yes: bool,
    dry_run: bool,
) -> None:
    run_git(["checkout", source_branch], dry_run=dry_run)
    status = get_worktree_status(dry_run=dry_run)

    if dry_run:
        return

    if not status:
        return

    if not auto_commit:
        raise RuntimeError("Worktree is not clean. Use --auto-commit flow or commit/stash manually.")

    print("\nDetected uncommitted changes. A release commit will be created on source branch.")
    print(f"- Source branch  : {source_branch}")
    print(f"- Commit message : {commit_message}")
    if not confirm("Create release commit now?", auto_yes=auto_yes):
        raise RuntimeError("Aborted: release commit was not created.")

    run_git(["add", "-A"], dry_run=False)
    run_git(["commit", "-m", commit_message], dry_run=False)


def current_branch(dry_run: bool) -> str:
    if dry_run:
        return "feature-branch"
    return run_git(["rev-parse", "--abbrev-ref", "HEAD"], capture=True, dry_run=False)


def ask_bump_kind() -> str:
    options = {"major", "minor", "patch"}
    while True:
        val = input("Bump type (major/minor/patch): ").strip().lower()
        if val in options:
            return val
        print("Please enter one of: major, minor, patch")


def ask_release_note() -> str:
    note = input("Release note: ").strip()
    if note:
        return note
    return "Release"


def parse_tag(tag_name: str, expected_prefix: str) -> SemVer | None:
    match = SEMVER_RE.match(tag_name)
    if not match:
        return None
    prefix = match.group("prefix")
    if prefix != expected_prefix:
        return None
    return SemVer(
        major=int(match.group("major")),
        minor=int(match.group("minor")),
        patch=int(match.group("patch")),
    )


def find_latest_semver(prefix: str, dry_run: bool) -> SemVer:
    if dry_run:
        return SemVer(0, 0, 0)

    tags_output = run_git(["tag", "--list", f"{prefix}*", "--sort=-v:refname"], capture=True, dry_run=False)
    if not tags_output:
        return SemVer(0, 0, 0)

    for raw_tag in tags_output.splitlines():
        version = parse_tag(raw_tag.strip(), prefix)
        if version is not None:
            return version
    return SemVer(0, 0, 0)


def confirm(prompt: str, auto_yes: bool) -> bool:
    if auto_yes:
        return True
    value = input(f"{prompt} [y/N]: ").strip().lower()
    return value in {"y", "yes"}


def create_release(
    bump_kind: str,
    release_note: str,
    remote: str,
    base_branch: str,
    source_branch: str,
    tag_prefix: str,
    auto_commit: bool,
    commit_message: str,
    auto_yes: bool,
    dry_run: bool,
) -> None:
    ensure_git_repo(dry_run=dry_run)
    same_branch_release = source_branch == base_branch

    maybe_create_release_commit(
        source_branch=source_branch,
        auto_commit=auto_commit,
        commit_message=commit_message,
        auto_yes=auto_yes,
        dry_run=dry_run,
    )

    # Always fetch latest refs before merging.
    run_git(["fetch", remote], dry_run=dry_run)

    if same_branch_release:
        # Source and base are the same branch: only sync with remote.
        run_git(["checkout", base_branch], dry_run=dry_run)
        run_git(["pull", "--ff-only", remote, base_branch], dry_run=dry_run)
    else:
        # Step 1: merge base into source branch.
        run_git(["merge", "--no-ff", "--no-edit", f"{remote}/{base_branch}"], dry_run=dry_run)

        # Step 2: move to base branch and merge source into base.
        run_git(["checkout", base_branch], dry_run=dry_run)
        run_git(["pull", "--ff-only", remote, base_branch], dry_run=dry_run)
        run_git(["merge", "--no-ff", "--no-edit", source_branch], dry_run=dry_run)

    latest = find_latest_semver(prefix=tag_prefix, dry_run=dry_run)
    next_version = latest.bump(bump_kind)
    tag_name = f"{tag_prefix}{next_version}"

    if not dry_run:
        existing = run_git(["tag", "--list", tag_name], capture=True, dry_run=False)
        if existing:
            raise RuntimeError(f"Tag already exists: {tag_name}")

    print("\nRelease summary")
    print(f"- Source branch : {source_branch}")
    print(f"- Base branch   : {base_branch}")
    print(f"- Release mode  : {'same-branch' if same_branch_release else 'merge-branch'}")
    print(f"- Bump kind     : {bump_kind}")
    print(f"- New tag       : {tag_name}")
    print(f"- Note          : {release_note}")

    if not confirm("Continue with tag creation and push?", auto_yes=auto_yes):
        print("Aborted by user.")
        return

    run_git(["tag", "-a", tag_name, "-m", release_note], dry_run=dry_run)
    run_git(["push", remote, base_branch], dry_run=dry_run)
    run_git(["push", remote, tag_name], dry_run=dry_run)

    print("\nRelease completed successfully.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create release tag after merge flow.")
    parser.add_argument("--bump", choices=["major", "minor", "patch"], help="SemVer bump type")
    parser.add_argument("--note", help="Release note for annotated tag")
    parser.add_argument("--remote", default="origin", help="Git remote name (default: origin)")
    parser.add_argument("--base", default="main", help="Base branch to release from (default: main)")
    parser.add_argument("--source", help="Source branch to merge into base (default: current branch)")
    parser.add_argument("--tag-prefix", default="v", help="Tag prefix (default: v)")
    parser.add_argument(
        "--no-auto-commit",
        action="store_true",
        help="Disable automatic release commit when worktree is dirty",
    )
    parser.add_argument(
        "--commit-message",
        default="chore: release prep",
        help="Commit message for automatic release commit",
    )
    parser.add_argument("--yes", action="store_true", help="Skip confirmation prompts")
    parser.add_argument("--dry-run", action="store_true", help="Print commands without executing")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    bump_kind = args.bump or ask_bump_kind()
    release_note = args.note or ask_release_note()

    try:
        source_branch = args.source or current_branch(dry_run=args.dry_run)
        create_release(
            bump_kind=bump_kind,
            release_note=release_note,
            remote=args.remote,
            base_branch=args.base,
            source_branch=source_branch,
            tag_prefix=args.tag_prefix,
            auto_commit=not args.no_auto_commit,
            commit_message=args.commit_message,
            auto_yes=args.yes,
            dry_run=args.dry_run,
        )
    except subprocess.CalledProcessError as exc:
        print(f"Git command failed with exit code {exc.returncode}.", file=sys.stderr)
        return exc.returncode
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Interrupted.", file=sys.stderr)
        return 130

    return 0


if __name__ == "__main__":
    raise SystemExit(main())