# Automation provenance

The book and illustrations in this repository are licensed under CC BY 4.0.
The workflows and contribution templates under `.github/` are separately
licensed under the MIT License in this directory.

## pr-readback

The human self-review gate used by `workflows/picture-readback.yml` is the
[`Tiffany-Studios/pr-readback`](https://github.com/Tiffany-Studios/pr-readback)
GitHub Action, pinned to commit
[`1a0d7b05838c3272681dd7afdfc1821732a27140`](https://github.com/Tiffany-Studios/pr-readback/commit/1a0d7b05838c3272681dd7afdfc1821732a27140).

It supplies the bidirectional coupling between an author's self-review
attestation and the pull request's draft state. Sugar-Bear-Shortcut instantiates
that attestation as a responsible-grown-up readback: a child may make the lesson,
but an adult account owns the proposal and reviews what will be published. The
local picture receipt is a child-sized companion: it inventories changed
files, validates the numbered PNG pages, checks their README image references,
and reports evidence without granting authority.

`pr-readback` is distributed under the MIT License. Upstream records its
prior-art lineage—from the Developer Certificate of Origin through earlier
self-attestation implementations—in its README:
https://github.com/Tiffany-Studios/pr-readback#prior-art
