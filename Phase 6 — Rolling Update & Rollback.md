Excellent — **Phase 5 application deployment is fully verified.** ✅

All three production-style checks passed through the AWS Load Balancer:

| Endpoint   | Result                     |
| ---------- | -------------------------- |
| `/health`  | `200` → `healthy`          |
| `/version` | `1.0.0`, development       |
| `/`        | HTML page served correctly |

So the flow is working end-to-end:

**Browser/curl → AWS Load Balancer → Kubernetes Service → Pod → Flask application → ECR image**

We can now move to an important DevOps exercise: **rolling update + rollback**.

## Phase 6 — Rolling Update & Rollback

Before introducing GitHub Actions, we want to prove that Kubernetes can safely deploy a new application version and recover from a bad deployment.

### Step 1 — Create version 1.0.1

Open:

```text
app/app.py
```

Change only the `/version` response from:

```python
"version": "1.0.0",
```

to:

```python
"version": "1.0.1",
```

Also change:

```text
app/templates/index.html
```

so the visible version changes from:

```html
<p>Version: 1.0.0</p>
```

to:

```html
<p>Version: 1.0.1</p>
```

Don't change anything else yet.

---

### Step 2 — Run the tests

From the project root:

```powershell
pytest
```

We should still get:

```text
3 passed
```

### Step 3 — Build the new Docker image

Because your ECR repository is **immutable**, we must use a new tag rather than overwrite `1.0.0`.

Run:

```powershell
docker build -t devops-app:1.0.1 .
```

Then:

```powershell
docker images devops-app
```

### Step 4 — Tag it for ECR

```powershell
docker tag devops-app:1.0.1 194154437225.dkr.ecr.ap-south-1.amazonaws.com/devops-production-dev-app:1.0.1
```

Then push:

```powershell
docker push 194154437225.dkr.ecr.ap-south-1.amazonaws.com/devops-production-dev-app:1.0.1
```

### Step 5 — Verify ECR

```powershell
aws ecr describe-images `
  --repository-name devops-production-dev-app `
  --region ap-south-1 `
  --query "imageDetails[].imageTags"
```

We should see both:

```text
1.0.0
1.0.1
```

---

**Stop there and send me the outputs of Steps 2–5.**

Don't modify the Kubernetes Deployment yet. Once we confirm the `1.0.1` image is safely in ECR, we'll perform the actual **Kubernetes rolling update**, watch the rollout, test the new version, and then deliberately practice **rollback**.
