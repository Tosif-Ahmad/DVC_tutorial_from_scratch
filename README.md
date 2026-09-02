# Build a DVC Data-Versioning Project from Scratch

This is a copy-and-paste tutorial for complete beginners. You will create **your own GitHub repository**, generate a small chemistry dataset with Python, and save three versions of that dataset using Git and DVC.

You do **not** need to clone this tutorial repository. Start with an empty GitHub repository and follow the steps in order.

> **Level:** Beginner  
> **Time:** Approximately 30–45 minutes  
> **Tools:** Git, GitHub, Python, pandas, and DVC  
> **Result:** Three recoverable versions of a chemistry dataset

---

## What you will learn

By completing this tutorial, you will learn how to:

- Create and clone a GitHub repository.
- Generate a CSV dataset with Python.
- Track code with Git.
- Stop Git from tracking a dataset without deleting it.
- Track the dataset with DVC.
- Configure a local DVC remote.
- Save V1, V2, and V3 of the dataset.
- Check Git and DVC status.
- Restore an older code-and-data version.
- Return to the latest version.

## The main idea

Git and DVC work together, but they store different things:

| Tool | What it tracks in this tutorial |
| --- | --- |
| Git | `mycode.py`, `data.dvc`, `.gitignore`, and project history |
| DVC | `data/sample_data.csv` |
| GitHub | The Git-tracked files and commits |
| Local DVC remote | The actual saved data objects |

The workflow you will repeat is:

```text
Change Python code
        ↓
Generate new CSV data
        ↓
dvc status
        ↓
dvc add data/
        ↓
Commit mycode.py + data.dvc with Git
        ↓
dvc push + git push
```

> **Important:** `git push` sends code and `data.dvc` to GitHub. `dvc push` sends the actual data object to DVC storage. A complete version needs both.

---

## Prerequisites

Install the following before starting:

- [Git](https://git-scm.com/downloads)
- [Python](https://www.python.org/downloads/) 3.10 or newer
- A [GitHub](https://github.com/) account
- A code editor such as Visual Studio Code

Check your installation:

```bash
git --version
python --version
python -m pip --version
```

If `python` does not work on macOS or Linux, try `python3` throughout the tutorial.

---

# Part 1 — Create the project

## Step 1: Create an empty GitHub repository

On GitHub:

1. Select **New repository**.
2. Name it `dvc-tutorial-from-scratch`.
3. Choose Public or Private.
4. Do not add a `.gitignore` or license yet.
5. You may initialize it with a README so it can be cloned immediately.
6. Select **Create repository**.

Copy the repository URL. It will look like:

```text
https://github.com/YOUR-USERNAME/dvc-tutorial-from-scratch.git
```

## Step 2: Clone your new repository

Replace `YOUR-USERNAME` with your GitHub username:

```bash
git clone https://github.com/YOUR-USERNAME/dvc-tutorial-from-scratch.git
cd dvc-tutorial-from-scratch
```

Confirm that you are inside the repository:

```bash
git status
```

Expected result:

```text
On branch main
nothing to commit, working tree clean
```

If GitHub created the default branch as `master`, replace `main` with `master` in later commands.

## Step 3: Create a Python virtual environment

Create the environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

Your terminal will normally show `(.venv)` after activation.

## Step 4: Install pandas and DVC

```bash
python -m pip install --upgrade pip
python -m pip install pandas "dvc>=3,<4"
```

Verify both packages:

```bash
python -c "import pandas; print('pandas:', pandas.__version__)"
dvc version
```

Save the required packages:

```bash
python -m pip freeze > requirements.txt
```

Create a `.gitignore` file and add this line so Git does not track the virtual environment:

```text
.venv/
```

---

# Part 2 — Create and save the initial dataset with Git

## Step 5: Create `mycode.py` for dataset V1

Create a file named `mycode.py` and copy this code into it:

```python
from pathlib import Path

import pandas as pd


# Dataset V1: three example molecules
data = {
    "Compound": ["Benzene", "Toluene", "Naphthalene"],
    "Molecular weight": [78.11, 92.14, 128.17],
    "TPSA": [0.0, 0.0, 0.0],
}

df = pd.DataFrame(data)

# Create the data directory if it does not already exist
data_directory = Path("data")
data_directory.mkdir(exist_ok=True)

# Save the dataset as a CSV file
output_path = data_directory / "sample_data.csv"
df.to_csv(output_path, index=False)

print(f"CSV file saved to {output_path}")
print(df)
```

## Step 6: Run the Python script

```bash
python mycode.py
```

Expected output:

```text
CSV file saved to data/sample_data.csv
      Compound  Molecular weight  TPSA
0      Benzene             78.11   0.0
1      Toluene             92.14   0.0
2  Naphthalene            128.17   0.0
```

Your project should now contain:

```text
dvc-tutorial-from-scratch/
├── data/
│   └── sample_data.csv
├── .gitignore
├── mycode.py
├── requirements.txt
└── README.md
```

## Step 7: Track the initial code and data with Git

For learning purposes, we will first commit the CSV with Git. Later, we will transfer responsibility for `data/` from Git to DVC.

```bash
git add mycode.py data/ requirements.txt .gitignore
git commit -m "Create initial chemistry dataset"
git push origin main
```

Check the result:

```bash
git status
```

Expected result:

```text
nothing to commit, working tree clean
```

> In a real project with large data, initialize DVC before committing the dataset to Git. We track it with Git first here only to demonstrate how to transfer an existing dataset to DVC.

---

# Part 3 — Initialize DVC and configure storage

## Step 8: Initialize DVC

```bash
dvc init
```

This creates:

- `.dvc/` — DVC configuration and internal project files.
- `.dvcignore` — patterns that DVC should ignore.

Check the new files:

```bash
git status
```

Commit the DVC initialization:

```bash
git add .dvc/ .dvcignore
git commit -m "Initialize DVC"
git push origin main
```

## Step 9: Create a local DVC remote

Run this command from inside your Git repository:

```bash
mkdir ../S3
```

The `..` means “one directory above the current repository.” The structure will look like:

```text
parent-folder/
├── dvc-tutorial-from-scratch/    # Git repository
└── S3/                           # Local DVC remote
```

The folder is called `S3` for learning, but it is **not Amazon S3**. It is only a local directory.

Keeping it outside the Git repository prevents Git from detecting DVC's storage objects.

## Step 10: Register the local folder as the default DVC remote

```bash
dvc remote add -d myremote ../S3
```

Meaning of each part:

| Part | Meaning |
| --- | --- |
| `dvc remote add` | Create a DVC remote configuration |
| `-d` | Make this the default remote |
| `myremote` | Name assigned to the remote |
| `../S3` | Location of the storage directory |

Confirm the remote:

```bash
dvc remote list
```

Expected result:

```text
myremote    ../S3
```

Commit the remote configuration:

```bash
git add .dvc/config
git commit -m "Configure local DVC remote"
git push origin main
```

---

# Part 4 — Transfer data tracking from Git to DVC

## Step 11: Try to add the Git-tracked data to DVC

Run:

```bash
dvc add data/
```

DVC should report that `data/` is already tracked by Git and suggest a command similar to:

```text
git rm -r --cached data
```

This is expected. One dataset should not be tracked directly by both Git and DVC.

## Step 12: Stop Git from tracking `data/`

```bash
git rm -r --cached data/
git commit -m "Stop tracking data with Git"
git push origin main
```

The `--cached` option removes `data/` from Git's tracking index but keeps the directory and CSV on your computer.

Confirm that the CSV still exists:

Windows PowerShell:

```powershell
Get-ChildItem data
```

macOS/Linux:

```bash
ls data
```

You should still see `sample_data.csv`.

## Step 13: Add the dataset to DVC

Now repeat:

```bash
dvc add data/
```

This time DVC will:

1. Calculate a content hash for the dataset.
2. Store the data object in `.dvc/cache/`.
3. Create `data.dvc` as a small pointer file.
4. Add `/data` to `.gitignore` so Git will not track the CSV again.

Inspect the pointer:

Windows PowerShell:

```powershell
Get-Content data.dvc
```

macOS/Linux:

```bash
cat data.dvc
```

It will look similar to:

```yaml
outs:
- md5: <UNIQUE-DATA-HASH>.dir
  size: <SIZE-IN-BYTES>
  nfiles: 1
  hash: md5
  path: data
```

> The exact hash may differ if your CSV contents differ. Do not manually edit the hash.

## Step 14: Commit the V1 DVC pointer and push the data

First commit the small DVC metadata files with Git:

```bash
git add data.dvc .gitignore
git commit -m "Track dataset V1 with DVC"
```

Push the actual data object to the DVC remote:

```bash
dvc push
```

Push the Git commit to GitHub:

```bash
git push origin main
```

Verify everything:

```bash
git status
dvc status
dvc status -c
```

Expected results:

- Git working tree is clean.
- DVC reports that data and pipelines are up to date.
- The cache and remote are up to date.

## Do we need `dvc commit`?

Not in this workflow. A normal:

```bash
dvc add data/
```

already copies the data into DVC's cache and updates `data.dvc`.

`dvc commit` is mainly useful after special commands such as:

```bash
dvc add --no-commit data/
dvc commit
```

For this beginner tutorial, consistently use `dvc add data/` when the dataset changes.

---

# Part 5 — Create dataset V2

## Step 15: Replace `mycode.py` with the V2 code

V2 adds Acetone to the dataset. Replace the entire content of `mycode.py` with:

```python
from pathlib import Path

import pandas as pd


# Dataset V2: V1 plus Acetone
data = {
    "Compound": ["Benzene", "Toluene", "Naphthalene", "Acetone"],
    "Molecular weight": [78.11, 92.14, 128.17, 58.08],
    "TPSA": [0.0, 0.0, 0.0, 20.23],
}

df = pd.DataFrame(data)

data_directory = Path("data")
data_directory.mkdir(exist_ok=True)

output_path = data_directory / "sample_data.csv"
df.to_csv(output_path, index=False)

print(f"CSV file saved to {output_path}")
print(df)
```

## Step 16: Generate V2 and inspect the change

```bash
python mycode.py
dvc status
```

DVC should report that `data/` has changed because the workspace CSV no longer matches the V1 hash in `data.dvc`.

Save V2 in the DVC cache and update the pointer:

```bash
dvc add data/
```

See which Git-tracked files changed:

```bash
git status
git diff -- data.dvc
```

You should see:

- `mycode.py` changed because the Python code now includes Acetone.
- `data.dvc` changed because V2 has a different data hash.
- `data/sample_data.csv` is not shown by Git because DVC placed `/data` in `.gitignore`.

## Step 17: Save V2

```bash
git add mycode.py data.dvc
git commit -m "Create dataset V2"
dvc push
git push origin main
```

Verify V2:

```bash
git status
dvc status
dvc status -c
```

---

# Part 6 — Create dataset V3

## Step 18: Replace `mycode.py` with the V3 code

V3 adds Ethanol. Replace `mycode.py` with:

```python
from pathlib import Path

import pandas as pd


# Dataset V3: V2 plus Ethanol
data = {
    "Compound": [
        "Benzene",
        "Toluene",
        "Naphthalene",
        "Acetone",
        "Ethanol",
    ],
    "Molecular weight": [78.11, 92.14, 128.17, 58.08, 46.07],
    "TPSA": [0.0, 0.0, 0.0, 20.23, 20.23],
}

df = pd.DataFrame(data)

data_directory = Path("data")
data_directory.mkdir(exist_ok=True)

output_path = data_directory / "sample_data.csv"
df.to_csv(output_path, index=False)

print(f"CSV file saved to {output_path}")
print(df)
```

## Step 19: Generate and save V3

```bash
python mycode.py
dvc status
dvc add data/
git status
git diff -- data.dvc
git add mycode.py data.dvc
git commit -m "Create dataset V3"
dvc push
git push origin main
```

Verify the final version:

```bash
git status
dvc status
dvc status -c
```

You have now created three connected Git and DVC versions.

---

# Part 7 — View and restore data versions

## Step 20: Find the commit hashes

```bash
git log --oneline
```

Your history will look similar to:

```text
abc1234 Create dataset V3
def5678 Create dataset V2
ghi9012 Track dataset V1 with DVC
```

Your hashes will be different. Copy the real short hash shown for each version.

## Step 21: Restore an older code-and-data version

First confirm that the current work is clean:

```bash
git status
```

Replace `<V1-COMMIT-HASH>` with the real V1 hash:

```bash
git switch --detach <V1-COMMIT-HASH>
dvc checkout
```

`git switch` restores historical `mycode.py` and `data.dvc`. `dvc checkout` reads that historical pointer and restores the correct CSV from the local DVC cache.

Inspect V1:

```bash
python -c "import pandas as pd; print(pd.read_csv('data/sample_data.csv'))"
```

You should see three rows.

If DVC reports that the object is missing from the cache, use:

```bash
dvc pull
```

`dvc pull` retrieves the required object from `../S3` and places the correct data in the workspace.

## Step 22: Return to the latest version

```bash
git switch main
dvc checkout
```

Inspect V3:

```bash
python -c "import pandas as pd; print(pd.read_csv('data/sample_data.csv'))"
```

You should see five rows.

## Restore only an old dataset while keeping the current code

Replace `<V1-COMMIT-HASH>` with the correct hash:

```bash
git switch main
git checkout <V1-COMMIT-HASH> -- data.dvc
dvc checkout
```

The current `mycode.py` remains, but DVC restores the V1 dataset.

Return the pointer and data to the latest version:

```bash
git restore --source=HEAD --staged --worktree data.dvc
dvc checkout
git status
```

Do not commit the old `data.dvc` unless you intentionally want to make that old dataset current.

---

# Part 8 — Common beginner mistakes

## DVC says `data/` is already tracked by Git

Cause: You committed `data/` with Git before using DVC.

Solution:

```bash
git rm -r --cached data/
git commit -m "Stop tracking data with Git"
dvc add data/
```

## Git does not show changes inside `data/`

This is correct after `dvc add`. Git ignores `data/` and tracks `data.dvc` instead.

Use this command to check data changes:

```bash
dvc status
```

## `dvc pull` says the data object is missing

Confirm the remote path:

```bash
dvc remote list
```

Confirm that each version was pushed when it was created:

```bash
dvc status -c
dvc push
```

## Switching Git commits did not change the CSV

Git changes `data.dvc`, but DVC restores the actual CSV separately:

```bash
dvc checkout
```

Use `dvc pull` if the object is not in the cache.

## `dvc status` still shows modified data after `dvc add`

Check that:

- The script finished without an error.
- You ran `dvc add data/` after generating the CSV.
- You are in the project root.
- The tracked path inside `data.dvc` is `data`.

## `git push origin main` fails

Your default branch might be named `master`. Check:

```bash
git branch --show-current
```

Then push the displayed branch name.

---

# Part 9 — Useful DVC commands

## Essential commands

| Command | Purpose |
| --- | --- |
| `dvc init` | Initialize DVC in a Git repository |
| `dvc add data/` | Track a dataset or save its changed version |
| `dvc status` | Compare workspace data with `data.dvc` |
| `dvc push` | Copy cached data objects to the DVC remote |
| `dvc pull` | Download required objects and restore workspace data |
| `dvc checkout` | Restore workspace data from the local cache |
| `dvc remote list` | Show configured DVC remotes |
| `dvc status -c` | Compare the local cache with the remote |

## Inspection and troubleshooting

| Command | Purpose |
| --- | --- |
| `dvc version` | Show the installed DVC version |
| `dvc doctor` | Display DVC diagnostic information |
| `dvc root` | Print the root directory of the DVC project |
| `dvc config --list` | Display DVC configuration values |
| `dvc diff HEAD~1 HEAD` | Compare tracked data between two Git revisions |
| `dvc check-ignore <path>` | Check whether DVC ignores a path |

## Cache and remote commands

| Command | Purpose |
| --- | --- |
| `dvc fetch` | Download data objects into the cache without changing the workspace |
| `dvc remote add <name> <url>` | Add a DVC storage location |
| `dvc remote default <name>` | Select the default remote |
| `dvc remote modify <name> <option> <value>` | Change a remote setting |

## Future pipeline commands

This tutorial tracks data with `data.dvc`; it does not create a `dvc.yaml` pipeline. In a future ML pipeline project, you may use:

| Command | Purpose |
| --- | --- |
| `dvc stage add ...` | Define a reproducible pipeline stage |
| `dvc repro` | Re-run stages affected by changed dependencies |
| `dvc dag` | Display the pipeline dependency graph |
| `dvc metrics show` | Display tracked model metrics |
| `dvc metrics diff` | Compare metrics between revisions |

---

# Final checklist

You have completed the tutorial if:

- [ ] You created your own GitHub repository.
- [ ] V1 contains three molecules.
- [ ] Git stopped tracking the `data/` directory.
- [ ] DVC created and Git tracked `data.dvc`.
- [ ] `../S3` is configured as the default DVC remote.
- [ ] V2 contains Acetone.
- [ ] V3 contains Ethanol.
- [ ] `git status`, `dvc status`, and `dvc status -c` are clean.
- [ ] You restored V1 successfully.
- [ ] You returned safely to V3 on `main`.

## Official DVC documentation

- [Get Started](https://dvc.org/doc/start)
- [`dvc init`](https://dvc.org/doc/command-reference/init)
- [`dvc add`](https://dvc.org/doc/command-reference/add)
- [DVC remote storage](https://dvc.org/doc/user-guide/data-management/remote-storage)
- [`dvc push`](https://dvc.org/doc/command-reference/push)
- [`dvc pull`](https://dvc.org/doc/command-reference/pull)
- [`dvc checkout`](https://dvc.org/doc/command-reference/checkout)
