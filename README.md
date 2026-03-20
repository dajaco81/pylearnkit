# Monkey Programming

This repository is structured so a learner can pull the latest tasks and `pylearnkit`, then do their work locally without committing generator files or notebook work.

## Repo layout

- `tasks/`: tracked task data files that arrive via `git pull`
- `pylearnkit/`: tracked package code
- `working/`: ignored learner workspace for notebooks such as `tasks1.ipynb`
- `gen/`: ignored generator workspace for building task files locally

## One-time setup

From the repository root:

```bash
python -m pip install -e .
```

That makes `pylearnkit` importable from notebooks inside `working/`.

## Learner workflow

1. Run `git pull` in the repository root.
2. Open or create a notebook in `working/`, for example `working/tasks1.ipynb`.
3. In the notebook:

```python
import pylearnkit
pylearnkit.init()
```

That prints the starter structure, including the correct path for loading tasks from `tasks/`.

## Generator workflow

Keep any task generators in `gen/`. They are ignored by git.

When generating task files from a notebook in `gen/`, write outputs into `../tasks/`.
