# DVC Tutorial from Scratch

A beginner-friendly, hands-on tutorial showing how **Git versions code and DVC versions data**.

This project creates a small chemistry dataset containing compounds and molecular features, tracks the generated `data/` directory with DVC, and demonstrates three data versions. The example uses a local folder as DVC storage so you can learn the complete workflow without creating a cloud account.

> **Important:** the folder is named `S3` for learning purposes, but it is **not Amazon S3**. It is an ordinary local directory located beside the Git repository.

## What you will learn

- Initialize DVC inside an existing Git repository
- Configure a local DVC remote
- Move an already Git-tracked dataset to DVC
- Create multiple data versions
- Understand the role of `data.dvc`
- Push data objects to DVC storage
- Restore an older code-and-data version
- Restore only an older dataset
- Return safely to the latest version

## Git and DVC responsibilities

| Item | Managed by | Purpose |
| --- | --- | --- |
| `mycode.py` | Git | Generates the chemistry dataset |
| `data.dvc` | Git | Small metadata pointer identifying one data version |
| `.dvc/config` | Git | Stores the DVC remote configuration |
| `.dvcignore` | Git | Defines files DVC should ignore |
| `data/` | DVC | Contains the generated CSV and is ignored by Git |
| `.dvc/cache/` | DVC | Local content-addressed data cache |
| `../S3/` | DVC remote | Local storage used to recover cached data objects |

Git stores the code and the DVC pointer. DVC stores the actual versioned data.

## Project structure

```text
DVC_tutorial_from_scratch/
├── .dvc/
│   └── config
├── .dvcignore
├── .gitignore
├── data.dvc
├── mycode.py
├── requirements.txt
└── README.md

S3/                         # Local DVC remote beside the repository
```

The generated directory is not shown because it is ignored by Git:

```text
data/
└── sample_data.csv
```

## Dataset versions in this repository

The repository history contains three real data versions:

| Version | Git commit | Rows | Change |
| --- | --- | ---: | --- |
| V1 | `91439fe` | 3 | Initial compound dataset |
| V2 | `edb5a06` | 4 | Added Acetone |
| V3 | `3c8d311` | 5 | Added the `GF2` example row |

View the history yourself:

```bash
git log --oneline --all --graph
```

## Prerequisites

- Git
- Python 3.10 or newer
- `pip`

Check that they are available:

```bash
git --version
python --version
python -m pip --version
```

On some macOS and Linux systems, use `python3` instead of `python`.

## Quick start

### 1. Clone the repository

```bash
git clone https://github.com/Tosif-Ahmad/DVC_tutorial_from_scratch.git
cd DVC_tutorial_from_scratch
```

### 2. Create a virtual environment

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install the dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
dvc version
```

### 4. Recreate the local DVC remote

The committed `.dvc/config` points to `../S3`. From inside the repository, create that directory:

macOS/Linux:

```bash
mkdir -p ../S3
dvc remote list
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force ../S3
dvc remote list
```

Expected remote configuration:

```text
myremote    ../S3
```

Creating this directory gives you an **empty** DVC remote. It does not download the original author's local data objects. Follow [Rebuild all historical versions](#rebuild-all-historical-versions-after-a-fresh-clone) to populate it.

### 5. Generate and store the latest dataset

```bash
python mycode.py
dvc add data/
dvc status
dvc push
git status
```

The script creates `data/sample_data.csv`. Because the generated CSV matches V3, `dvc add data/` should not change the committed `data.dvc` file.

## Build the project from scratch

This section explains the workflow used to create the repository.

### Step 1: Create and clone a Git repository

Create an empty repository on GitHub, then run:

```bash
git clone <YOUR-REPOSITORY-URL>
cd <YOUR-REPOSITORY-NAME>
```

### Step 2: Create the Python environment

```bash
python -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

Or activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
python -m pip install "dvc>=3,<4" "pandas>=2,<3"
```

### Step 3: Generate and commit the initial dataset with Git

After creating `mycode.py`, run:

```bash
python mycode.py
git add mycode.py data/
git commit -m "Create initial chemistry dataset"
git push origin main
```

At this point, Git tracks both the Python script and the CSV. This is intentional for the exercise; the next steps transfer responsibility for `data/` to DVC.

### Step 4: Initialize DVC

```bash
dvc init
git add .dvc/ .dvcignore
git commit -m "Initialize DVC"
git push origin main
```

`dvc init` creates DVC's internal configuration and `.dvcignore` file.

### Step 5: Create and configure the local remote

From inside the repository:

```bash
mkdir ../S3
dvc remote add -d myremote ../S3
dvc remote list
git add .dvc/config
git commit -m "Configure local DVC remote"
git push origin main
```

The `-d` option makes `myremote` the default remote. Later commands can therefore use `dvc push` and `dvc pull` without specifying `-r myremote`.

### Step 6: Stop tracking the dataset with Git

Because `data/` was committed earlier, remove it from Git's index while keeping it on disk:

```bash
git rm -r --cached data/
git commit -m "Stop tracking data with Git"
git push origin main
```

`--cached` is important: it tells Git to stop tracking the directory without deleting your local dataset.

### Step 7: Track the dataset with DVC

```bash
dvc add data/
git add data.dvc .gitignore
git commit -m "Track first data version with DVC"
dvc push
git push origin main
```

`dvc add data/` performs three important actions:

1. Stores the dataset content in `.dvc/cache/`.
2. Creates `data.dvc`, containing the dataset hash and path.
3. Adds `/data` to `.gitignore`, preventing Git from tracking the dataset again.

`dvc push` then copies the required cached objects to `../S3/`.

### Is `dvc commit` required here?

No. A normal `dvc add data/` already stores the data in DVC's local cache and updates `data.dvc`. Running `dvc commit` immediately afterward is redundant.

`dvc commit` is useful in special workflows—for example, after `dvc add --no-commit`, which creates the metadata without storing the data in the cache.

## Create a new data version

Modify `mycode.py` so it generates an additional row, then run:

```bash
python mycode.py
dvc status
dvc add data/
git diff -- data.dvc
git add mycode.py data.dvc
git commit -m "Create second data version"
dvc push
git push origin main
```

Repeat the same workflow for V3:

```bash
python mycode.py
dvc status
dvc add data/
git diff -- data.dvc
git add mycode.py data.dvc
git commit -m "Create third data version"
dvc push
git push origin main
```

The reliable order is:

1. Change the code.
2. Run the code to generate changed data.
3. Use `dvc status` to observe the data change.
4. Run `dvc add` to cache the new content and update `data.dvc`.
5. Commit `mycode.py` and `data.dvc` together with Git.
6. Run `dvc push` to store the data object in the DVC remote.
7. Push the Git commit to GitHub.

## Check that everything is synchronized

```bash
git status
dvc status
dvc status -c
```

Typical clean results are:

- `git status`: working tree clean
- `dvc status`: data and pipelines are up to date
- `dvc status -c`: cache and remote are up to date

## Rebuild all historical versions after a fresh clone

A fresh clone has the Git commits and their `data.dvc` pointers, but your newly created `../S3` directory is empty. You can regenerate each dataset using the historical version of `mycode.py` and push it into your local remote.

Ensure the dependencies are installed before starting. Then run:

```bash
git switch --detach 91439fe
python mycode.py
dvc add data/
dvc push

git switch --detach edb5a06
python mycode.py
dvc add data/
dvc push

git switch --detach 3c8d311
python mycode.py
dvc add data/
dvc push

git switch main
dvc checkout
git status
```

At each historical commit, `dvc add data/` should reproduce the `data.dvc` pointer already saved in that commit. Do not create a Git commit while in detached HEAD mode.

## Restore an older code-and-data version

Before switching versions, confirm that you have no uncommitted work:

```bash
git status
```

For example, restore V2:

```bash
git switch --detach edb5a06
dvc pull
```

Git restores the V2 versions of `mycode.py` and `data.dvc`. DVC reads that historical pointer, downloads the matching object from `../S3`, and restores `data/sample_data.csv`.

Inspect the restored dataset:

```bash
git log -1 --oneline
python -c "import pandas as pd; print(pd.read_csv('data/sample_data.csv'))"
```

Return to the latest version:

```bash
git switch main
dvc pull
```

Use `dvc checkout` instead of `dvc pull` when the required object already exists in `.dvc/cache/`. `dvc pull` retrieves missing objects from the remote and checks them out into the workspace.

## Restore only an older dataset

The following example keeps the current `mycode.py` but temporarily restores the V1 dataset:

```bash
git switch main
git checkout 91439fe -- data.dvc
dvc pull
```

Now `data/` contains V1 while your current code remains unchanged. `git status` shows that `data.dvc` differs from the current version.

Return the pointer and dataset to the latest version:

```bash
git restore --source=HEAD --staged --worktree data.dvc
dvc checkout
git status
```

Do not commit the older `data.dvc` unless you intentionally want to make that dataset current.

## Useful commands cheat sheet

| Command | Purpose |
| --- | --- |
| `dvc init` | Initialize DVC in the Git repository |
| `dvc remote add -d myremote ../S3` | Add the local directory as the default remote |
| `dvc remote list` | Display configured remotes |
| `dvc add data/` | Track or update the dataset and its pointer |
| `dvc status` | Compare workspace data with DVC metadata |
| `dvc status -c` | Compare the local cache with remote storage |
| `dvc push` | Copy cached data objects to the remote |
| `dvc pull` | Download required objects and restore workspace data |
| `dvc checkout` | Restore workspace data from the local cache |
| `git diff data.dvc` | Inspect a change to the data pointer |
| `git log --oneline --all --graph` | Display the Git version history |

## Common mistakes and solutions

### `dvc add data/` says the data is already tracked by Git

Stop tracking it in Git without deleting the local directory:

```bash
git rm -r --cached data/
git commit -m "Stop tracking data with Git"
dvc add data/
```

### Git does not show changes inside `data/`

This is expected. DVC added `/data` to `.gitignore`. Git tracks `data.dvc`; DVC tracks the actual data.

### Git does not track the `S3` directory

The configured remote is `../S3`, which is outside the repository. It acts as local DVC storage and should not be committed to Git.

### `dvc pull` reports missing files

The local `../S3` remote is empty or does not contain the selected version. Follow the historical rebuild section to regenerate and push all three versions.

### The data did not change after switching Git commits

Git switches `data.dvc`, but the ignored `data/` directory is restored separately. Run:

```bash
dvc checkout
```

Use `dvc pull` if the required object is not already in the local cache.

### `data.dvc` changed unexpectedly

The generated CSV differs from the data described by the current Git commit. Inspect the differences and your environment before committing:

```bash
dvc status
git diff data.dvc
```

## Limitations of this learning setup

The local `../S3` remote works well for understanding DVC on one computer, but it is not shared with GitHub or other users. In a collaborative or production project, use shared remote storage such as Amazon S3, Azure Blob Storage, Google Cloud Storage, SSH, or another supported service.

## Official documentation

- [DVC Get Started](https://dvc.org/doc/start)
- [dvc add](https://dvc.org/doc/command-reference/add)
- [dvc commit](https://dvc.org/doc/command-reference/commit)
- [dvc remote add](https://dvc.org/doc/command-reference/remote/add)
- [dvc push](https://dvc.org/doc/command-reference/push)
- [dvc pull](https://dvc.org/doc/command-reference/pull)
- [dvc checkout](https://dvc.org/doc/command-reference/checkout)

