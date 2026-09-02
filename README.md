# DVC Tutorial from Scratch

A beginner-friendly, hands-on tutorial showing how **Git versions code and DVC versions data**.

> **Level:** Beginner · **Tools:** Git, Python, pandas, DVC · **Example:** Chemistry dataset · **Data versions:** 3

This project creates a small chemistry dataset containing compounds and molecular features, tracks the generated `data/` directory with DVC, and demonstrates three data versions. The example uses a local folder as DVC storage so you can learn the complete workflow without creating a cloud account.

> **Important:** the folder is named `S3` for learning purposes, but it is **not Amazon S3**. It is an ordinary local directory located beside the Git repository.

## Quick navigation

- [Why DVC?](#why-do-we-need-dvc)
- [Git and DVC responsibilities](#git-and-dvc-responsibilities)
- [Project structure](#project-structure)
- [Quick start](#quick-start)
- [Build the project from scratch](#build-the-project-from-scratch)
- [Create a new data version](#create-a-new-data-version)
- [Rebuild historical versions](#rebuild-all-historical-versions-after-a-fresh-clone)
- [Restore an older version](#restore-an-older-code-and-data-version)
- [Troubleshooting](#common-mistakes-and-solutions)
- [Additional DVC commands](#additional-useful-dvc-commands)

## Tutorial at a glance

| Question | Answer |
| --- | --- |
| What does the Python script produce? | `data/sample_data.csv` |
| What does Git track? | Code, configuration, README, and `data.dvc` |
| What does DVC track? | The generated `data/` directory |
| Where is the DVC cache? | `.dvc/cache/` |
| Where is the tutorial remote? | `../S3/` |
| How many data versions exist? | Three: V1, V2, and V3 |
| How do I save a changed dataset? | `dvc add data/` followed by `dvc push` |
| How do I recover the selected dataset? | `dvc pull` or `dvc checkout` |

---

## Why do we need DVC?

Git is excellent for source code because code files are usually small and text-based. Datasets and trained models are often much larger and may change many times. Storing every large data version directly in Git can make a repository slow and difficult to clone.

DVC solves this by separating the **data itself** from the **small file that identifies the data**:

1. The actual dataset is stored in DVC's cache and remote storage.
2. DVC calculates a unique content hash for that dataset.
3. The hash is written into a small file such as `data.dvc`.
4. Git tracks and versions `data.dvc` alongside the code.
5. When you switch Git commits, you also switch to the pointer for the corresponding data version.
6. `dvc checkout` or `dvc pull` uses that pointer to restore the correct dataset.

This produces a connection between each code version and the data version used with it.

## A simple mental model

Think of Git and DVC as two cooperating librarians:

- **Git** keeps the instruction book (`mycode.py`) and a catalogue card (`data.dvc`).
- **DVC** keeps the large box containing the actual dataset.
- **The hash inside `data.dvc`** is the catalogue number that tells DVC which box to retrieve.

The normal versioning cycle is:

```text
Change code → Generate data → dvc add → Git commit → dvc push → Git push
```

To recover a version, the cycle is reversed:

```text
Switch Git commit → Read historical data.dvc → dvc pull/checkout → Restore data
```

## Important DVC terms

| Term | Beginner-friendly meaning |
| --- | --- |
| Workspace | The files and directories you currently see in the project |
| DVC-tracked data | Data described by a `.dvc` file instead of being committed directly to Git |
| Cache | DVC's local content store, normally inside `.dvc/cache/` |
| Remote | A second storage location used by `dvc push` and `dvc pull` |
| Hash | A unique fingerprint calculated from file contents |
| `data.dvc` | A small YAML metadata file containing the hash and path of the tracked data |
| Git remote | A Git repository location such as GitHub; this stores code and metadata |
| DVC remote | Storage for the actual data objects; in this tutorial it is `../S3` |

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

> **Beginner checkpoint:** By the end, you should be able to explain why Git stores `data.dvc` while DVC stores the CSV contents.

---

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

### Why are two pushes required?

`git push` and `dvc push` send different things to different places:

| Command | What it sends | Destination in this tutorial |
| --- | --- | --- |
| `git push` | Code, README, `.dvc` files, and Git history | GitHub |
| `dvc push` | Actual contents of `data/` stored as DVC objects | Local `../S3/` folder |

Running only `git push` does not upload the CSV to DVC storage. Running only `dvc push` does not upload your code or `data.dvc` to GitHub. A complete version normally requires both.

> **Key rule:** For every meaningful data version, preserve the DVC object with `dvc push` and preserve its pointer with `git push`.

---

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

### What the important files contain

- **`mycode.py`** creates a pandas DataFrame and writes `data/sample_data.csv`.
- **`data.dvc`** records the hash, size, number of files, and tracked path for the current dataset.
- **`.dvc/config`** declares `myremote` as the default DVC remote and points it to `../S3`.
- **`.gitignore`** contains `/data`, so Git will not accidentally store the generated dataset.
- **`.dvcignore`** can exclude files that DVC should not scan or track.
- **`requirements.txt`** records the Python packages required to reproduce the exercise.

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

The short values such as `91439fe` are Git commit identifiers. They are shortened versions of longer unique hashes. Git accepts these short identifiers as long as they remain unambiguous in the repository.

---

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

Use this section if you want to run the completed project. Use [Build the project from scratch](#build-the-project-from-scratch) if you want to recreate every learning step yourself.

### 1. Clone the repository

```bash
git clone https://github.com/Tosif-Ahmad/DVC_tutorial_from_scratch.git
cd DVC_tutorial_from_scratch
```

`git clone` downloads the Git history, code, configuration, and `data.dvc`. It does **not** download the actual DVC-tracked CSV because the configured DVC remote is a local folder on each user's computer.

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

A virtual environment keeps this project's packages separate from other Python projects. After activation, your terminal usually shows `(.venv)` before the command prompt.

### 3. Install the dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
dvc version
```

The final command confirms that DVC is installed. If `dvc` is not recognized, confirm that the virtual environment is active and rerun the installation command.

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

The path is interpreted relative to the repository. `..` means “one directory above the current repository,” so this layout keeps the storage folder outside Git's working tree.

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

What each command does:

1. `python mycode.py` generates the CSV in the workspace.
2. `dvc add data/` calculates its hash, places its content in the cache, and verifies/updates `data.dvc`.
3. `dvc status` checks whether workspace data differs from the pointer.
4. `dvc push` copies missing objects from the cache to `../S3`.
5. `git status` checks whether any Git-tracked file changed unexpectedly.

> **Quick-start success check:** `data/sample_data.csv` exists, `dvc status` reports no data changes, and `dvc status -c` reports that the cache and remote are synchronized.

---

## Build the project from scratch

This section explains the workflow used to create the repository.

> **Learning mode:** These steps intentionally track the CSV with Git first and then transfer it to DVC. In a new real project, you can usually initialize DVC and run `dvc add` before ever committing a large dataset to Git.

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

The `.dvc/` directory is not the dataset. It contains DVC configuration and internal files. Most of it is managed automatically, so beginners should avoid editing it manually.

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

Without `-d`, the remote would exist but would not automatically be selected. You would need commands such as `dvc push -r myremote`.

### Step 6: Stop tracking the dataset with Git

Because `data/` was committed earlier, remove it from Git's index while keeping it on disk:

```bash
git rm -r --cached data/
git commit -m "Stop tracking data with Git"
git push origin main
```

`--cached` is important: it tells Git to stop tracking the directory without deleting your local dataset.

This command may look destructive, but here it removes `data/` only from Git's staging index. Always include `--cached` in this step if you want the local files to remain available for `dvc add`.

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

At this point:

- GitHub receives `data.dvc`, not `data/sample_data.csv`.
- `.dvc/cache/` contains a local DVC object for the dataset.
- `../S3/` receives another copy when `dvc push` runs.
- `/data` in `.gitignore` prevents accidental Git tracking.

### Is `dvc commit` required here?

No. A normal `dvc add data/` already stores the data in DVC's local cache and updates `data.dvc`. Running `dvc commit` immediately afterward is redundant.

`dvc commit` is useful in special workflows—for example, after `dvc add --no-commit`, which creates the metadata without storing the data in the cache.

> **First-version checkpoint:** Git tracks `mycode.py`, `data.dvc`, and `.gitignore`; Git ignores `data/`; and the data object exists in both `.dvc/cache/` and `../S3/`.

---

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

### Why commit the code and `data.dvc` together?

Suppose the new code creates five rows but Git stores a `data.dvc` pointer for the previous four-row dataset. Anyone checking out that commit would receive mismatched code and data. Committing both files together makes the commit a reproducible snapshot.

### What should `dvc status` show before and after `dvc add`?

After changing and regenerating the CSV—but before `dvc add`—DVC should report that `data/` has changed. After `dvc add data/`, the workspace data and the updated pointer should agree, so `dvc status` should report that data and pipelines are up to date. Git should then show `mycode.py` and `data.dvc` as modified until they are committed.

> **Versioning checkpoint:** A data version is not fully shareable until its updated `data.dvc` is committed with Git and its data object is pushed with DVC.

---

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

These commands inspect three different relationships:

- `git status` compares your Git working tree with the current Git commit.
- `dvc status` compares workspace data with the DVC pointer.
- `dvc status -c` compares the local DVC cache with the configured remote.

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

“Detached HEAD” means Git is showing a historical commit directly instead of placing you on a normal branch. It is safe for viewing and rebuilding old versions. Return to `main` before continuing normal development.

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

In short:

- `dvc checkout` works from the **local cache**.
- `dvc pull` first obtains missing objects from the **DVC remote**, then updates the workspace.

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

> **Restoration checkpoint:** Always run `git status` before switching versions and again after returning to `main`. This prevents accidental commits of a historical pointer.

---

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

---

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

---

## Additional useful DVC commands

The following commands are not all required for this small exercise, but they are valuable as you move toward larger machine-learning projects.

### Project and environment information

| Command | What it does | When it is useful |
| --- | --- | --- |
| `dvc version` | Shows the installed DVC version and platform information | Confirming installation or reporting a problem |
| `dvc doctor` | Displays diagnostic information about DVC and the environment | Troubleshooting unexpected behavior |
| `dvc root` | Prints the root directory of the current DVC project | Checking whether you are inside the correct project |
| `dvc config --list` | Lists effective DVC configuration values | Understanding the current configuration |

### Tracking and inspecting data

| Command | What it does | When it is useful |
| --- | --- | --- |
| `dvc add <path>` | Starts tracking or updates a data file/directory | Saving a new data version |
| `dvc status` | Compares workspace data with DVC metadata | Checking whether tracked data changed |
| `dvc diff` | Compares DVC-tracked data between Git revisions | Understanding which data files were added, deleted, or modified |
| `dvc list .` | Lists DVC-tracked files available in a DVC repository | Inspecting tracked outputs without manually reading metadata |
| `dvc check-ignore <path>` | Checks whether a path is ignored by DVC | Debugging `.dvcignore` rules |

Examples:

```bash
dvc status
dvc diff HEAD~1 HEAD
dvc list .
dvc check-ignore data/temporary.csv
```

### Cache and workspace commands

| Command | What it does | When it is useful |
| --- | --- | --- |
| `dvc checkout` | Restores tracked data from the local cache | After switching Git commits when objects are cached |
| `dvc fetch` | Downloads data objects to the cache without changing workspace files | Preparing data before a later checkout |
| `dvc pull` | Fetches required objects and checks them out | Reconstructing the workspace from remote storage |
| `dvc unprotect <path>` | Makes a cached/linked file safely writable | Before directly editing certain DVC-linked files |

Example difference between `fetch` and `pull`:

```bash
dvc fetch     # Download objects into .dvc/cache/
dvc checkout  # Materialize them in the workspace

# dvc pull effectively performs both operations for required outputs
dvc pull
```

### Remote-storage commands

| Command | What it does | When it is useful |
| --- | --- | --- |
| `dvc remote list` | Lists configured DVC remotes | Confirming remote names and paths |
| `dvc remote add <name> <url>` | Adds a DVC remote | Configuring local or shared storage |
| `dvc remote default <name>` | Selects the default remote | Changing which remote normal commands use |
| `dvc remote modify <name> <option> <value>` | Changes remote settings | Configuring credentials, endpoints, or behavior |
| `dvc push` | Uploads needed objects from cache to the remote | Publishing a new data version |
| `dvc status -c` | Compares local cache with remote storage | Checking whether `dvc push` is needed |

Examples for this repository:

```bash
dvc remote list
dvc remote default myremote
dvc status -c
dvc push
```

### Pipeline commands for your next DVC project

This repository tracks data with `data.dvc`; it does not yet define a `dvc.yaml` pipeline. When you later create reproducible ML pipelines, these commands become important:

| Command | What it does |
| --- | --- |
| `dvc stage add ...` | Defines a reproducible pipeline stage |
| `dvc repro` | Runs stages whose dependencies have changed |
| `dvc dag` | Displays the pipeline dependency graph |
| `dvc params diff` | Compares parameter values between Git revisions |
| `dvc metrics show` | Displays tracked model metrics |
| `dvc metrics diff` | Compares metrics between revisions |

### Cleanup commands—use carefully

| Command | What it does | Safety note |
| --- | --- | --- |
| `dvc gc --workspace` | Removes unused cache objects not needed by the current workspace | Older versions may stop working locally unless their objects exist in the remote |
| `dvc remove <file>.dvc` | Stops tracking the output described by a `.dvc` file | Review Git and DVC changes before committing |
| `dvc destroy` | Removes DVC metadata and configuration from the project | Destructive; do not use casually |

Before any cleanup, verify that important data versions have been pushed:

```bash
dvc status -c
dvc push
```

For this tutorial, you normally do **not** need `dvc gc`, `dvc remove`, or `dvc destroy`. They are listed so you recognize them, not as routine steps.

---

## Final learning check

You have completed the tutorial when you can do all of the following without copying the full workflow:

- Explain the difference between Git storage and DVC storage.
- Create a changed dataset and save it as a new version.
- Identify why `data.dvc` changes even though Git ignores `data/`.
- Push code and data to their correct destinations.
- Switch to V1 or V2 and restore its matching CSV.
- Return to `main` and restore V3.
- Diagnose whether a missing version is absent from the workspace, cache, or remote.
