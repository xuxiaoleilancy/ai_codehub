#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Git Version Management Script
This script provides a set of utilities for managing Git repositories with best practices.
"""

import os
import sys
import subprocess
import argparse
from datetime import datetime
from typing import List, Optional, Tuple

class GitManager:
    def __init__(self, repo_path: str = "."):
        """Initialize GitManager with repository path."""
        self.repo_path = os.path.abspath(repo_path)
        if not self._is_git_repo():
            raise ValueError(f"{self.repo_path} is not a Git repository")

    def _is_git_repo(self) -> bool:
        """Check if the current directory is a Git repository."""
        try:
            self._run_git_command(["rev-parse", "--git-dir"])
            return True
        except subprocess.CalledProcessError:
            return False

    def _run_git_command(self, command: List[str]) -> Tuple[str, str]:
        """Run a Git command and return stdout and stderr."""
        try:
            result = subprocess.run(
                ["git"] + command,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip(), result.stderr.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error running Git command: {e.stderr}")
            raise

    def get_current_branch(self) -> str:
        """Get the current branch name."""
        stdout, _ = self._run_git_command(["branch", "--show-current"])
        return stdout

    def get_status(self) -> str:
        """Get the current repository status."""
        stdout, _ = self._run_git_command(["status"])
        return stdout

    def create_branch(self, branch_name: str, base_branch: str = "main") -> None:
        """Create a new branch from the specified base branch."""
        # First, ensure we're on the base branch
        self._run_git_command(["checkout", base_branch])
        # Pull latest changes
        self._run_git_command(["pull"])
        # Create and switch to new branch
        self._run_git_command(["checkout", "-b", branch_name])
        print(f"Created and switched to branch: {branch_name}")

    def commit_changes(self, message: str, add_all: bool = True) -> None:
        """Commit changes with the given message."""
        if add_all:
            self._run_git_command(["add", "."])
        self._run_git_command(["commit", "-m", message])
        print(f"Committed changes with message: {message}")

    def push_changes(self, branch: Optional[str] = None) -> None:
        """Push changes to remote repository."""
        if branch is None:
            branch = self.get_current_branch()
        self._run_git_command(["push", "origin", branch])
        print(f"Pushed changes to branch: {branch}")

    def pull_changes(self) -> None:
        """Pull latest changes from remote repository."""
        self._run_git_command(["pull"])
        print("Pulled latest changes")

    def merge_branch(self, source_branch: str, target_branch: str = "main") -> None:
        """Merge source branch into target branch."""
        # Switch to target branch
        self._run_git_command(["checkout", target_branch])
        # Pull latest changes
        self._run_git_command(["pull"])
        # Merge source branch
        self._run_git_command(["merge", source_branch])
        print(f"Merged {source_branch} into {target_branch}")

    def delete_branch(self, branch_name: str, force: bool = False) -> None:
        """Delete a branch."""
        if force:
            self._run_git_command(["branch", "-D", branch_name])
        else:
            self._run_git_command(["branch", "-d", branch_name])
        print(f"Deleted branch: {branch_name}")

    def create_tag(self, tag_name: str, message: str) -> None:
        """Create a new tag with the given name and message."""
        self._run_git_command(["tag", "-a", tag_name, "-m", message])
        print(f"Created tag: {tag_name}")

    def push_tag(self, tag_name: str) -> None:
        """Push a tag to remote repository."""
        self._run_git_command(["push", "origin", tag_name])
        print(f"Pushed tag: {tag_name}")

def main():
    parser = argparse.ArgumentParser(description="Git Version Management Tool")
    parser.add_argument("--repo", default=".", help="Path to Git repository")
    subparsers = parser.add_subparsers(dest="command", help="Git command to execute")

    # Create branch command
    create_branch_parser = subparsers.add_parser("create-branch", help="Create a new branch")
    create_branch_parser.add_argument("branch_name", help="Name of the new branch")
    create_branch_parser.add_argument("--base", default="main", help="Base branch to create from")

    # Commit command
    commit_parser = subparsers.add_parser("commit", help="Commit changes")
    commit_parser.add_argument("message", help="Commit message")
    commit_parser.add_argument("--no-add", action="store_true", help="Don't add all changes")

    # Push command
    push_parser = subparsers.add_parser("push", help="Push changes")
    push_parser.add_argument("--branch", help="Branch to push")

    # Pull command
    subparsers.add_parser("pull", help="Pull latest changes")

    # Merge command
    merge_parser = subparsers.add_parser("merge", help="Merge branches")
    merge_parser.add_argument("source", help="Source branch to merge")
    merge_parser.add_argument("--target", default="main", help="Target branch to merge into")

    # Delete branch command
    delete_parser = subparsers.add_parser("delete-branch", help="Delete a branch")
    delete_parser.add_argument("branch_name", help="Name of the branch to delete")
    delete_parser.add_argument("--force", action="store_true", help="Force delete")

    # Tag command
    tag_parser = subparsers.add_parser("tag", help="Create and push a tag")
    tag_parser.add_argument("tag_name", help="Name of the tag")
    tag_parser.add_argument("message", help="Tag message")

    args = parser.parse_args()

    try:
        git_manager = GitManager(args.repo)

        if args.command == "create-branch":
            git_manager.create_branch(args.branch_name, args.base)
        elif args.command == "commit":
            git_manager.commit_changes(args.message, not args.no_add)
        elif args.command == "push":
            git_manager.push_changes(args.branch)
        elif args.command == "pull":
            git_manager.pull_changes()
        elif args.command == "merge":
            git_manager.merge_branch(args.source, args.target)
        elif args.command == "delete-branch":
            git_manager.delete_branch(args.branch_name, args.force)
        elif args.command == "tag":
            git_manager.create_tag(args.tag_name, args.message)
            git_manager.push_tag(args.tag_name)
        else:
            parser.print_help()

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 