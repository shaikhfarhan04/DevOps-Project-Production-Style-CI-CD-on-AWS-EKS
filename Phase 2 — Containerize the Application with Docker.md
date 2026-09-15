
One small note: you're currently inside the `tests` directory. Before Phase 2, we'll work from the **project root**.

# 🚀 Phase 2 — Containerize the Application with Docker

Before AWS/EKS, we need to turn our Flask application into a Docker container.

Our flow becomes:

```text
Python Flask App
       │
       ▼
    Dockerfile
       │
       ▼
 Docker Image
       │
       ▼
 Docker Container
       │
       ▼
 localhost:5000
```

Later:

```text
GitHub
   │
   ▼
GitHub Actions
   │
   ▼
Docker Image
   │
   ▼
Amazon ECR
   │
   ▼
Amazon EKS
```

---

## Step 2.1 — Go to the project root

You're currently here:

```text
...\DevOps-Project-Production-Style-CI-CD-on-AWS-EKS\tests>
```

Run:

```powershell
cd ..
```

Your prompt should become something like:

```text
(venv) PS G:\DevOps-Data\DevOps Project\DevOps-Project-Production-Style-CI-CD-on-AWS-EKS>
```

Verify:

```powershell
dir
```

You should see something similar to:

```text
app
tests
.gitignore
```

---

# Step 2.2 — Check whether Docker is installed

Run:

```powershell
docker --version
```

Then:

```powershell
docker info
```

### Important

If `docker --version` works but `docker info` gives an error about the Docker daemon not running, **start Docker Desktop** and run `docker info` again.

If Docker isn't installed, tell me before going further and we'll install/configure it on Windows.

---

# Step 2.3 — Create the Dockerfile

In VS Code, at the **project root**, create:

```text
Dockerfile
```

Your structure will become:

```text
DevOps-Project-Production-Style-CI-CD-on-AWS-EKS
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
├── Dockerfile       ← NEW
└── .gitignore
```

Put this in `Dockerfile`:

```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

EXPOSE 5000

CMD ["python", "app.py"]
```

Save it.

---

# Step 2.4 — Create `.dockerignore`

At the project root, create:

```text
.dockerignore
```

Put:

```text
.venv/
venv/
__pycache__/
*.pyc
.pytest_cache/
.git/
.github/
tests/
.vscode/
.env
```

Why?

We don't want things like your virtual environment or Git history inside the Docker image.

---

# Step 2.5 — Build the Docker image

From the **project root**, run:

```powershell
docker build -t devops-app:1.0.0 .
```

Notice the `.` at the end.

Docker will:

```text
Dockerfile
    │
    ├── Python 3.13 base image
    │
    ├── Install Flask + pytest
    │
    ├── Copy application
    │
    └── Create image
```

If successful, you'll see something similar to:

```text
Successfully built ...
Successfully tagged devops-app:1.0.0
```

---

# Step 2.6 — Verify the image

Run:

```powershell
docker images
```

You should see:

```text
REPOSITORY    TAG       IMAGE ID       CREATED
devops-app    1.0.0     xxxxxxxxxxxx   ...
```

---

# Step 2.7 — Run the container

Run:

```powershell
docker run -d --name devops-app-container -p 5000:5000 devops-app:1.0.0
```

Let's break that down:

```text
-d
```

Run in background.

```text
--name devops-app-container
```

Give our container a name.

```text
-p 5000:5000
```

Map:

```text
Windows port 5000
       ↓
Container port 5000
```

---

# Step 2.8 — Check the container

Run:

```powershell
docker ps
```

You should see:

```text
CONTAINER ID   IMAGE              PORTS
xxxxxxxx       devops-app:1.0.0  0.0.0.0:5000->5000/tcp
```

---

# Step 2.9 — Test the application

Open:

[http://localhost:5000](http://localhost:5000?utm_source=chatgpt.com)

Then:

[http://localhost:5000/health](http://localhost:5000/health?utm_source=chatgpt.com)

Expected:

```json
{
  "status": "healthy"
}
```

And:

[http://localhost:5000/version](http://localhost:5000/version?utm_source=chatgpt.com)

Expected:

```json
{
  "application": "DevOps Demo Application",
  "environment": "development",
  "version": "1.0.0"
}
```

---

# Step 2.10 — Check Docker logs

Run:

```powershell
docker logs devops-app-container
```

You should see Flask running on:

```text
0.0.0.0:5000
```

---

# Step 2.11 — Stop and remove the container

When you're finished testing:

```powershell
docker stop devops-app-container
```

Then:

```powershell
docker rm devops-app-container
```

**Don't delete the image yet.** We'll use it again.

---

## 🎯 Phase 2 checkpoint

At the end of this phase, we want:

```text
                    Flask
                      │
                      ▼
                 Dockerfile
                      │
                      ▼
             devops-app:1.0.0
                      │
                      ▼
              Docker Container
                      │
                      ▼
             http://localhost:5000
                      │
             ┌────────┼────────┐
             ▼        ▼        ▼
             /      /health  /version
```

### For now, do only this:

Start with:

```powershell
cd ..
docker --version
docker info
```

**Send me the output of those two Docker commands.** Then we'll build the image together rather than jumping ahead.
