---
this_file: WORK.md
---
# Work log

Read upstream README and regression suites; consulted official Hatch build selection and hatch-vcs documentation. No previous project planning or packaging documents existed.

Baseline: action suite passed all 58 checks; object suite reached font file tests then failed because system Python lacked fontTools. Packaging declares that upstream dependency.

Verification (Python 3.12.12):
- `uv build --out-dir /tmp/typerig-final-artifacts` built sdist then wheel from sdist in isolated build environments.
- `TYPERIG_ARTIFACT_DIR=/tmp/typerig-final-artifacts ... python -m pytest -q -o pythonpath= tests`: 2 passed, using installed imports.
- Upstream object regression: ALL PASS (185 checks).
- Upstream action regression: ALL PASS (58 checks).
- Wheel installed in an isolated venv; external working directory import resolved to site-packages, Point addition returned (12.0, 23.0), UFO imports succeeded.
- Sdist installed in a second isolated venv; metadata version and Point import succeeded.
- `uvx twine check /tmp/typerig-final-artifacts/*`: both PASSED.
- Artifact tests compare every visible library file byte-for-byte in both distributions; all 153 upstream tracked library files retained. Only library plus dist-info appears in wheel; no Scripts/Docs GUI assets in sdist. Ignored local Claude configuration is explicitly excluded.

Wait, but: source fidelity does not imply host-runtime verification. FontLab/Glyphs proxies remain unchanged and need host APIs; no GUI host execution was performed. A clean release tag and publication remain controller work. Development artifact version: 0.1.1.dev1423+g7f92f3a29.d20261013.

Official build configuration: https://hatch.pypa.io/latest/config/build/
Official version plugin: https://github.com/ofek/hatch-vcs

