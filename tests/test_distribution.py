# this_file: tests/test_distribution.py
"""Verify the public standalone imports and distribution boundary."""
import os
from pathlib import Path
import tarfile
import zipfile

from typerig.core.objects.point import Point
from typerig.core.func.math import normalize2max


def test_point_arithmetic_and_zero_origin():
    result = Point(-2, 5) + Point(2, -5)
    assert (result.x, result.y) == (0, 0), "Point arithmetic changed"
    assert (Point().x, Point().y) == (0, 0), "Default origin changed"
    assert normalize2max([2, 4]) == [0.5, 1.0], "Normalization changed"


def test_artifacts_retain_complete_library_without_gui_scripts():
    artifact_dir = os.environ.get("TYPERIG_ARTIFACT_DIR")
    if not artifact_dir:
        import pytest
        pytest.skip("Build artifacts first and set TYPERIG_ARTIFACT_DIR")
    root = Path(__file__).resolve().parents[1]
    sources = {str(p.relative_to(root / "Lib")): p.read_bytes()
               for p in (root / "Lib/typerig").rglob("*")
               if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"
               and not any(part.startswith(".") for part in p.relative_to(root).parts)}
    wheel, = Path(artifact_dir).glob("*.whl")
    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()
        for name, data in sources.items():
            assert archive.read(name) == data, f"Missing or altered library file: {name}"
        assert all(n.startswith("typerig/") or ".dist-info/" in n for n in names)
        assert not any("/.claude/" in n or "__pycache__" in n for n in names)
        assert any(n.endswith("/licenses/LICENSE") for n in names), "MPL license missing"
    sdist, = Path(artifact_dir).glob("*.tar.gz")
    with tarfile.open(sdist) as archive:
        members = {m.name.split("/", 1)[1]: m for m in archive.getmembers() if "/" in m.name}
        for name, data in sources.items():
            assert archive.extractfile(members["Lib/" + name]).read() == data
        assert not any(n.startswith(("Scripts/", "Docs/")) for n in members), "GUI assets shipped"


def test_distribution_privacy_and_published_docs():
    artifact_dir = os.environ.get("TYPERIG_ARTIFACT_DIR")
    if not artifact_dir:
        import pytest
        pytest.skip("Build artifacts first and set TYPERIG_ARTIFACT_DIR")
    forbidden_names = {"." + n for n in ("claude", "omc", "codegraph", "git")}
    forbidden_paths = ["/" + name + "/" for name in ("Users", "home", "tmp", "private")]
    wheel, = Path(artifact_dir).glob("*.whl")
    sdist, = Path(artifact_dir).glob("*.tar.gz")
    with zipfile.ZipFile(wheel) as archive:
        entries = [(n, archive.read(n)) for n in archive.namelist()]
    with tarfile.open(sdist) as archive:
        entries += [(m.name, archive.extractfile(m).read())
                    for m in archive.getmembers() if m.isfile()]
    for name, data in entries:
        assert not forbidden_names.intersection(Path(name).parts), f"Tool state: {name}"
        assert Path(name).name != "WORK.md", "Private verification log shipped"
        text = data.decode("utf-8", errors="ignore")
        for forbidden in forbidden_paths:
            assert forbidden not in text, f"Local filesystem path in {name}"
