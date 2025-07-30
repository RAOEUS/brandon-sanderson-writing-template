# Brandon Sanderson-Inspired Novel Writing Template

A guided project template that walks you through the professional novel writing process using Brandon Sanderson’s methods—and provides a built-in web GUI to manage your planning files (`plan/`) and your chapters (`chapters/`) with a WYSIWYG Markdown editor and Git integration.

---

## Table of Contents

1. [Benefits for Authors](#benefits-for-authors)
2. [System Requirements](#system-requirements)
3. [Installation & Launch](#installation--launch)
4. [Using the Web Editor](#using-the-web-editor)
   * [File Management](#file-management)
   * [Git Integration](#git-integration)
5. [Main Steps](#main-steps)
6. [Why Use Git](#why-use-git)
7. [Collaboration Workflow](#collaboration-workflow)

---

## Benefits for Authors

* Structured workflow covering goals, idea development, worldbuilding, character creation, plotting, drafting, revision, and publishing.
* Checklist-driven files with examples and worksheets to keep you on track.
* Browser-based editing with live Markdown preview—no local text editor required.
* Built-in version control: track changes, revert edits, and collaborate securely using Git commands from the UI.
* Single-step setup script to configure the environment, customize project title and author name, and launch the application.

---

## System Requirements

* Python 3.8 or later
* Git (for version control)

---

## Installation & Launch

1. On GitHub, navigate to this repository and click **Use this template**, then **Create a new repository** under your account.
2. Copy the clone URL of *your* new repo (e.g. `https://github.com/your-username/my-novel-project.git`).
3. In your terminal, clone your repo and enter its directory:

   ```bash
   git clone https://github.com/your-username/my-novel-project.git
   cd my-novel-project
   ```
4. Make the setup script executable and run it:

   ```bash
   chmod +x run.sh
   ./run.sh
   ```
5. Follow the prompts to customize the project title and author name (only if defaults are unchanged).
6. Once setup completes, your browser will open [http://localhost:8000](http://localhost:8000), where you can start writing.

---

## Using the Web Editor

### File Management

* **Select** a plan file or a chapter from the dropdown menus.
* **Create New** by clicking **+ New Plan File** or **+ New Chapter**.
* **Save** or **Delete** the current file using the File Actions panel.
* **Stage** and **Unstage** the current file to prepare changes for commit.

### Git Integration

The web UI surfaces essential Git commands so you can:

* **Stage All**: stage all changed files at once.
* **Status**: view three categories of files—staged, unstaged, and untracked.
* **Log**: review the last 10 commits with commit hashes and messages.
* **Diff**: display color-highlighted additions and deletions.
* **Commit**: save staged changes with a custom message.
* **Push / Pull**: synchronize with the remote repository (`origin`).

For more advanced workflows, including branching and feature development, see the next section.

### Branching Locally (Command‑Line)

Even though branch management isn’t exposed in the web UI, you can create branches using Git on your local machine:

```bash
# List existing branches
git branch

# Create and switch to a new branch named "chapter-5-rewrite"
git checkout -b chapter-5-rewrite

# Work on your branch, then return to main when you’re ready
git checkout main
```

Once you’ve created a branch, you can continue to use the web editor to stage, commit, and push changes in that branch. To switch branches in the UI, first checkout your branch in your terminal, then refresh the web page.

---

The web UI surfaces essential Git commands so you can:

* **Stage All**: stage all changed files at once.
* **Status**: view three categories of files—staged, unstaged, and untracked.
* **Log**: review the last 10 commits with commit hashes and messages.
* **Diff**: display color-highlighted additions and deletions.
* **Commit**: save staged changes with a custom message.
* **Push / Pull**: synchronize with the remote repository (`origin`).

---

## Main Steps

1. [Getting Started](plan/00-Getting-Started.md)
2. [Idea Development](plan/01-Idea-Development.md)
3. [Worldbuilding](plan/02-Worldbuilding.md)
4. [Character Creation](plan/03-Characters.md)
5. [Plotting](plan/04-Plotting.md)
6. [First Draft](plan/05-First-Draft.md)
7. [Revision Process](plan/06-Revisions.md)
8. [Publishing Plan](plan/07-Publishing-Plan.md)

Each file includes checklists, examples, and worksheets to guide you through that phase of novel development.

---

## Why Use Git

* **Change History**: recover earlier drafts or compare revisions.
* **Branching**: experiment with new ideas without affecting your main draft.
* **Collaboration**: merge changes safely when working with beta readers or co-authors.

The integrated Git controls let you perform these tasks without leaving the browser.

---

## Collaboration Workflow

When working with others (beta readers, co-authors, or editors), follow this straightforward Git flow:

1. **Fork the Repository (Optional):** If you don’t have write access to the main project—such as when collaborating via GitHub—click **Fork** on the project page to create your own copy. Work in your forked repo and open PRs back to the original.
2. **Create a Branch:** In the web UI or on your Git host, start a new branch for your feature or revision (for example, `chapter-5-rewrite`).
3. **Make and Commit Changes:** Edit your files in the branch, then use **Stage** and **Commit** to record your work.
4. **Push & Open a Pull Request (PR):** Push your branch to the remote repository (your fork or the main project if you have access) and open a PR for review.
5. **Review & Revise:** Reviewers can comment on specific lines. Make additional commits to the same branch until everyone agrees.
6. **Merge:** Once approved, merge the PR into the `main` branch of the target repository to integrate the changes.

### Handling Merge Conflicts

If two people edit the same section, a conflict may appear when merging:

* Conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) show the differing sections.
* Choose which version to keep (yours, theirs, or a combined edit), remove the markers, and save.
* Use **Stage** and **Commit** to record the conflict resolution. The PR will update automatically.

This flow keeps contributions organized and makes it easy for non-developers to collaborate safely.

