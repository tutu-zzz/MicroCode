# MicroCode repository instructions

## Architecture documentation

`doc/infrastructure.md` is generated from the current project tree and Python module docstrings.

After every source, test, configuration, documentation, or file-tree change:

1. Run `python scripts/update_infrastructure.py` from the repository root.
2. Run `python scripts/update_infrastructure.py --check` before handing off the change.
3. Include the updated `doc/infrastructure.md` in the same change.

Do not hand-edit `doc/infrastructure.md`. Update a Python module docstring or the role mappings and
static architecture text in `scripts/update_infrastructure.py`, then regenerate the document.

When Git is initialized, run `python scripts/install_git_hooks.py` once to enable the committed
pre-commit hook that performs this update automatically.

