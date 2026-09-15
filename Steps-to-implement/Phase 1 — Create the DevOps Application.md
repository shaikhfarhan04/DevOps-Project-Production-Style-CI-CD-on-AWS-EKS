Absolutely. We’ll do **Phase 1 from zero on Windows + VS Code**, and I’ll keep this hands-on. You should execute each step and tell me what you get before we move forward.

# Phase 1 — Create the DevOps Application

We’ll build a small **Python Flask application** that later gets Dockerized and deployed to Kubernetes/EKS.

### What we're building

```text
devops-real-world-project/
│
├── app/
│   ├── app.py
│   ├── requirements.txt
│   └── templates/
│       └── index.html
│
├── tests/
│   └── test_app.py
│
├── .gitignore
└── README.md
```

---

## Step 1 — Install/check prerequisites

Open **PowerShell** or the VS Code terminal.

In VS Code:

**Terminal → New Terminal**

Run:

```powershell
python --version
```

You should see something similar to:

```text
Python 3.12.x
```

Then:

```powershell
git --version
```

You should see:

```text
git version 2.x.x
```

### Also check VS Code

You already have VS Code, so we're good there.

**Don't install Docker or AWS yet.** We'll do those in later phases.

---

# Step 2 — Create the project

Choose a location where you keep projects.

For example:

```powershell
cd Desktop
```

Create the project:

```powershell
mkdir devops-real-world-project
cd devops-real-world-project
```

Open it in VS Code:

```powershell
code .
```

Your VS Code Explorer should now show:

```text
DEVOPS-REAL-WORLD-PROJECT
```

---

# Step 3 — Create the folders

In the VS Code terminal, run:

```powershell
mkdir app
mkdir tests
mkdir app\templates
```

You should now have:

```text
devops-real-world-project
│
├── app
│   └── templates
│
└── tests
```

---

# Step 4 — Create a Python virtual environment

This is important. We don't want project dependencies mixed with your global Python installation.

Run:

```powershell
python -m venv .venv
```

Now activate it:

```powershell
.venv\Scripts\Activate.ps1
```

Your terminal should change to something like:

```text
(.venv) PS C:\Users\...\Desktop\devops-real-world-project>
```

### If PowerShell gives you an execution-policy error

If you see something like:

```text
running scripts is disabled on this system
```

run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Press:

```text
Y
```

Then activate again:

```powershell
.venv\Scripts\Activate.ps1
```

---

# Step 5 — Install Flask

Run:

```powershell
pip install flask
```

Then verify:

```powershell
pip show flask
```

You should see Flask information.

---

# Step 6 — Create `requirements.txt`

In VS Code Explorer:

**app → New File**

Name it:

```text
requirements.txt
```

Put this inside:

```text
Flask
```

Save it.

Our structure is now:

```text
devops-real-world-project
│
├── app
│   ├── requirements.txt
│   └── templates
│
└── tests
```

---

# Step 7 — Create `app.py`

Inside the `app` folder create:

```text
app.py
```

Put this code inside:

```python
from flask import Flask, jsonify, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


@app.route("/version")
def version():
    return jsonify({
        "application": "DevOps Demo Application",
        "version": "1.0.0",
        "environment": "development"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
```

Save with:

**Ctrl + S**

---

# Step 8 — Create the web page

Open:

```text
app → templates
```

Create:

```text
index.html
```

Put this inside:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DevOps Demo Application</title>
</head>

<body>

    <h1>DevOps Demo Application</h1>

    <p>Welcome to our real-world DevOps project.</p>

    <h2>Application Status</h2>

    <p>Environment: Development</p>
    <p>Version: 1.0.0</p>
    <p>Status: Healthy</p>

</body>
</html>
```

Save it.

---

# Step 9 — Run the application

Go back to your terminal.

Make sure you are inside:

```text
devops-real-world-project
```

and that you see:

```text
(.venv)
```

Then run:

```powershell
python app\app.py
```

You should see something similar to:

```text
* Serving Flask app 'app'
* Debug mode: on
* Running on http://127.0.0.1:5000
```

### Don't close this terminal.

Your application is now running.

---

# Step 10 — Open it in your browser

Open:

[http://127.0.0.1:5000](http://127.0.0.1:5000?utm_source=chatgpt.com)

You should see:

```text
DevOps Demo Application

Welcome to our real-world DevOps project.

Application Status

Environment: Development
Version: 1.0.0
Status: Healthy
```

🎉 **You've just created your first application for the DevOps project.**

---

# Step 11 — Test the health endpoint

Open:

[http://127.0.0.1:5000/health](http://127.0.0.1:5000/health?utm_source=chatgpt.com)

You should get:

```json
{
    "status": "healthy"
}
```

This endpoint will become **very important later**.

Kubernetes will eventually use this type of endpoint to determine whether our application is healthy.

---

# Step 12 — Test the version endpoint

Open:

[http://127.0.0.1:5000/version](http://127.0.0.1:5000/version?utm_source=chatgpt.com)

You should get:

```json
{
    "application": "DevOps Demo Application",
    "environment": "development",
    "version": "1.0.0"
}
```

Later, when we deploy:

```text
v1.0.0
   ↓
v1.1.0
   ↓
v1.2.0
```

we'll use this to verify which version is actually running.

---

# Step 13 — Stop the application

In the terminal running Flask:

```text
Ctrl + C
```

The application should stop.

---

# Step 14 — Create `.gitignore`

In the root of your project create:

```text
.gitignore
```

Put:

```text
.venv/
__pycache__/
*.pyc
.pytest_cache/
.vscode/
.env
```

This prevents unnecessary/local files from being committed to Git.

---

# Step 15 — Create the tests

Create:

```text
tests/test_app.py
```

Put this inside:

```python
import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from app.app import app


def test_home():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200


def test_health():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_version():
    client = app.test_client()

    response = client.get("/version")

    assert response.status_code == 200
    assert response.json["version"] == "1.0.0"
```

Now install pytest:

```powershell
pip install pytest
```

Update `app\requirements.txt` to:

```text
Flask
pytest
```

---

# Step 16 — Run the tests

Run:

```powershell
pytest
```

We want to see:

```text
3 passed
```

Something like:

```text
==================== test session starts ====================

tests/test_app.py ...                                  [100%]

===================== 3 passed =========================
```

🎯 This is our first **CI concept**.

Eventually GitHub Actions will automatically run:

```text
pytest
```

every time you push code.

---

# Your final Phase 1 structure

Your VS Code Explorer should look like this:

```text
DEVOPS-REAL-WORLD-PROJECT
│
├── .gitignore
│
├── app
│   ├── app.py
│   ├── requirements.txt
│   │
│   └── templates
│       └── index.html
│
└── tests
    └── test_app.py
```

We now have:

```text
Python
   │
   ▼
Flask Application
   │
   ├── /
   ├── /health
   └── /version
        │
        ▼
      pytest
```

### 🚦Stop here for now

Don't move to Docker yet.

**Your next action:** run these two commands in the VS Code terminal:

```powershell
python --version
```

and:

```powershell
pytest
```

Send me the **exact output** you get. If you get an error, paste the error exactly as it appears, and we'll troubleshoot it together before moving to the next step.
