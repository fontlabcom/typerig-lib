---
this_file: UPSTREAM.md
---
# Upstream provenance

TypeRig is authored by Vassil Kateliev / Karandash Type Foundry.
Upstream: https://github.com/kateliev/TypeRig

Packaging baseline: commit `7f92f3a297673e0bd74be7509077006c41c7b9b2`.
The complete `Lib/typerig` tree is shipped with unchanged executable code; four
files carry docstring/header edits only (listed in CHANGELOG.md). Original
copyright notices and the Mozilla Public License 2.0 in LICENSE are retained.
Packaging infrastructure is maintained in https://github.com/fontlabcom/typerig-lib.
GUI scripts remain maintained upstream; the repository retains them for provenance,
but they are excluded from both wheel and source distribution.
