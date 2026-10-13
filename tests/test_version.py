# this_file: tests/test_version.py
"""Exercise actual Hatch VCS versions in isolated Git histories."""
from pathlib import Path
import subprocess
import sys

import pytest


def git(root, *args):
    return subprocess.run(["git", "-C", str(root), *args], check=True,
                          capture_output=True, text=True).stdout.strip()


def version(root):
    return subprocess.run([sys.executable, "-c",
        "from hatchling.builders.wheel import WheelBuilder; "
        "from pathlib import Path; print(WheelBuilder(str(Path.cwd())).metadata.version)"],
        cwd=root, check=True, capture_output=True, text=True).stdout.strip()


@pytest.fixture
def repository(tmp_path):
    config = Path(__file__).resolve().parents[1] / "pyproject.toml"
    (tmp_path / "pyproject.toml").write_bytes(config.read_bytes())
    (tmp_path / "README.md").write_text("Fixture")
    (tmp_path / "LICENSE").write_text("MPL-2.0")
    git(tmp_path, "init")
    git(tmp_path, "config", "user.name", "Test")
    git(tmp_path, "config", "user.email", "test@example.invalid")
    git(tmp_path, "add", ".")
    git(tmp_path, "commit", "-m", "Baseline")
    git(tmp_path, "tag", "v1.2.3")
    return tmp_path


def test_clean_release_and_development_distance(repository):
    assert version(repository) == "1.2.3", "Release tag ignored"
    git(repository, "commit", "--allow-empty", "-m", "Next")
    assert version(repository).startswith("1.2.4.dev1+g"), "Distance incorrect"


@pytest.mark.parametrize("tag", ["v2.0.5-Py3.10", "v1.5.0-py27",
    "v1.2.4-beta", "v1.2.4-host", "v1.2.4.5", "v1v2.3.4"])
def test_incompatible_nearest_tag_does_not_hide_clean_release(repository, tag):
    git(repository, "commit", "--allow-empty", "-m", "Next")
    git(repository, "tag", tag)
    assert version(repository).startswith("1.2.4.dev1+g"), f"Invalid tag selected: {tag}"
