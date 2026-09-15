Absolutely. **Phase 3 is where our project starts behaving like a real DevOps project.** We’ll put the code under Git version control, create a GitHub repository, and push our first version.

> **Important:** We’ll do this from the **project root**, not from `tests`.

# Phase 3 — Git + GitHub 🚀

Our flow:

```text
VS Code
   │
   │ git add
   ▼
Local Git Repository
   │
   │ git commit
   ▼
Git History
   │
   │ git push
   ▼
GitHub Repository
```

Eventually:

```text
Developer
    │
    ▼
GitHub
    │
    ▼
GitHub Actions
    │
    ▼
Docker
    │
    ▼
ECR
    │
    ▼
EKS
```

---

# 3.1 Make sure you're in the project root

Your terminal should look approximately like:

```text
(venv) PS G:\DevOps-Data\DevOps Project\DevOps-Project-Production-Style-CI-CD-on-AWS-EKS>
```

Run:

```powershell
Get-Location
```

Then:

```powershell
dir
```

You should see something like:

```text
app
tests
Dockerfile
.dockerignore
.gitignore
```

---

# 3.2 Check Git

Run:

```powershell
git --version
```

You should get something like:

```text
git version 2.x.x
```

Then check whether this directory is already a Git repository:

```powershell
git status
```

### If you get:

```text
fatal: not a git repository
```

That's actually what we expect if this is a new project.

---

# 3.3 Initialize Git

Run:

```powershell
git init
```

You should see:

```text
Initialized empty Git repository in ...
```

Now run:

```powershell
git status
```

You should see something similar to:

```text
On branch master

No commits yet

Untracked files:
    .dockerignore
    .gitignore
    Dockerfile
    app/
    tests/
```

---

# 3.4 Set the default branch to `main`

Modern projects generally use `main`.

Run:

```powershell
git branch -M main
```

Verify:

```powershell
git branch
```

You should see:

```text
* main
```

---

# 3.5 Check your `.gitignore`

Before committing anything, let's make sure we aren't accidentally committing our virtual environment.

Run:

```powershell
Get-Content .gitignore
```

It should contain:

```text
.venv/
venv/
__pycache__/
*.pyc
.pytest_cache/
.vscode/
.env
```

### Why this matters

We **do not** want:

```text
.venv/
```

in GitHub.

Also:

```text
.env
```

is important because later we may have secrets/environment variables.

We never want things such as:

```text
AWS_SECRET_ACCESS_KEY=...
DATABASE_PASSWORD=...
```

committed to GitHub.

---

# 3.6 Check what Git sees

Run:

```powershell
git status
```

You should see your project files as untracked.

Now stage everything:

```powershell
git add .
```

Then:

```powershell
git status
```

You should see:

```text
Changes to be committed:
    new file: .dockerignore
    new file: .gitignore
    new file: Dockerfile
    new file: app/app.py
    new file: app/requirements.txt
    new file: app/templates/index.html
    new file: tests/test_app.py
```

### Important

Before continuing, look carefully at the list.

You **should NOT see**:

```text
.venv/
```

If `.venv` appears, **stop and tell me** before committing.

---

# 3.7 Configure your Git identity

If this is your first Git setup on this PC, run:

```powershell
git config --global user.name "YOUR NAME"
```

For example:

```powershell
git config --global user.name "Farhan Shaikh"
```

Then configure the email associated with your GitHub account:

```powershell
git config --global user.email "YOUR_GITHUB_EMAIL"
```

For example:

```powershell
git config --global user.email "your-email@example.com"
```

Use the email you actually want associated with your Git commits.

Check:

```powershell
git config --global --list
```

You should see:

```text
user.name=...
user.email=...
```

---

# 3.8 Create our first commit

Now commit the project:

```powershell
git commit -m "Initial DevOps application"
```

You should get something similar to:

```text
[main (root-commit) abc1234] Initial DevOps application
 7 files changed
 ...
```

🎉 We now have our first version.

---

# 3.9 Verify Git history

Run:

```powershell
git log --oneline
```

You should see:

```text
abc1234 (HEAD -> main) Initial DevOps application
```

This is important.

Git is now tracking:

```text
Version 1
   │
   └── Initial DevOps application
```

Later we'll have:

```text
Version 1
   │
   ├── Docker
   │
   ├── CI/CD
   │
   ├── Kubernetes
   │
   └── Production
```

---

# 3.10 Create the GitHub repository

Now go to GitHub:

[GitHub](https://github.com/?utm_source=chatgpt.com)

Sign in.

Click:

**New repository**

Create:

```text
Repository name:
devops-production-style-cicd-eks
```

I recommend this name rather than putting your entire project description in the repository name.

Description:

```text
Production-style DevOps CI/CD project using Docker, GitHub Actions, AWS ECR and Amazon EKS.
```

Choose:

```text
Public
```

for this learning project if you're comfortable making the code public.

### Very important

On the repository creation page, **do NOT initialize**:

```text
☐ Add a README file
☐ Add .gitignore
☐ Choose a license
```

Leave those unchecked.

Why?

Because we've already created the local repository and committed it.

We don't want GitHub creating another initial commit that we'll have to merge.

Then click:

**Create repository**

---

# 3.11 Connect local Git to GitHub

GitHub will show you commands for an existing repository.

We'll use:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/devops-production-style-cicd-eks.git
```

Replace:

```text
YOUR_USERNAME
```

with your actual GitHub username.

For example, if your GitHub username were:

```text
farhan123
```

the command would be:

```powershell
git remote add origin https://github.com/farhan123/devops-production-style-cicd-eks.git
```

---

# 3.12 Verify the remote

Run:

```powershell
git remote -v
```

You should see:

```text
origin  https://github.com/YOUR_USERNAME/devops-production-style-cicd-eks.git (fetch)
origin  https://github.com/YOUR_USERNAME/devops-production-style-cicd-eks.git (push)
```

---

# 3.13 Push to GitHub

Now the exciting part.

Run:

```powershell
git push -u origin main
```

The first push may ask you to authenticate with GitHub.

Complete the GitHub authentication in the browser if prompted.

You should eventually see something similar to:

```text
Enumerating objects...
Counting objects...
Writing objects...
To https://github.com/...
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'
```

---

# 3.14 Verify on GitHub

Refresh your GitHub repository.

You should now see:

```text
devops-production-style-cicd-eks
│
├── app
│   ├── app.py
│   ├── requirements.txt
│   └── templates
│       └── index.html
│
├── tests
│   └── test_app.py
│
├── Dockerfile
├── .dockerignore
└── .gitignore
```

🎉 **Your first DevOps project is now on GitHub.**

---

# 3.15 One important improvement — README

Before we move toward AWS, I'd like us to add a professional README.

Create:

```text
README.md
```

at the project root.

Use:

````markdown
# Production-Style CI/CD on AWS EKS

A hands-on DevOps project demonstrating a production-style CI/CD pipeline using Python, Flask, Docker, GitHub Actions, Amazon ECR and Amazon EKS.

## Current Status

Phase 1 - Flask Application: Completed

Phase 2 - Dockerization: Completed

Phase 3 - Git + GitHub: Completed

## Application Endpoints

- `/` - Application homepage
- `/health` - Health check
- `/version` - Application version

## Technology Stack

- Python
- Flask
- Pytest
- Docker
- Git
- GitHub
- GitHub Actions
- AWS
- Amazon ECR
- Amazon EKS
- Kubernetes
- Terraform
- Prometheus
- Grafana

## Project Structure

```text
app/
├── app.py
├── requirements.txt
└── templates/
    └── index.html

tests/
└── test_app.py

Dockerfile
.dockerignore
.gitignore
README.md
````

## Project Roadmap

* [x] Flask application
* [x] Automated tests
* [x] Docker container
* [x] Git repository
* [x] GitHub repository
* [ ] AWS infrastructure with Terraform
* [ ] Amazon ECR
* [ ] Amazon EKS
* [ ] Kubernetes deployment
* [ ] GitHub Actions CI/CD
* [ ] Security scanning
* [ ] Monitoring with Prometheus/Grafana
* [ ] Deployment rollback

````

Save it.

Then:

```powershell
git add README.md
````

Commit:

```powershell
git commit -m "Add project documentation"
```

Push:

```powershell
git push
```

---

# ✅ Phase 3 complete

Our architecture has now evolved to:

```text
                   GitHub
                     ▲
                     │
                  git push
                     │
                     │
              ┌──────┴──────┐
              │             │
          Dockerfile      Flask
              │             │
              └──────┬──────┘
                     │
                Local Project
                     │
                     ▼
                 Git History
```

And our development workflow is now:

```text
                    Developer
                       │
                       ▼
                   VS Code
                       │
                       ▼
                    Git
                       │
                 git commit
                       │
                       ▼
                    GitHub
```

## 🔜 Next: Phase 4 — AWS Infrastructure

This is where the project gets much more interesting.

We'll set up:

```text
                    AWS
                     │
                     ▼
                 Terraform
                     │
              ┌──────┴──────┐
              ▼             ▼
             VPC            ECR
              │
              ▼
             EKS
              │
              ▼
       Kubernetes Cluster
```

We'll first install/check **AWS CLI + Terraform**, configure AWS securely, and then build the infrastructure **with Terraform rather than manually clicking around the AWS Console**.

### For now, do Phase 3 up through:

```powershell
git push -u origin main
```

Then tell me **your GitHub repository URL** (the repository itself, not any password/token), and I'll walk you through verifying the repository before we start Phase 4.
