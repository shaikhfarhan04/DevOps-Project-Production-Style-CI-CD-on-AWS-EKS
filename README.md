# DevOps-Project-Production-Style-CI-CD-on-AWS-EKS
We'll build a containerized web application and implement the complete DevOps lifecycle:
Absolutely. Let’s build **one realistic, end-to-end DevOps project** that you can actually implement on AWS and later put on your resume/GitHub.

## 🚀 Project: Production-Style CI/CD on AWS EKS

We'll build a **containerized web application** and implement the complete DevOps lifecycle:

```text
Developer
   │
   │ git push
   ▼
┌──────────────┐
│    GitHub    │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│ GitHub Actions   │
│ CI/CD Pipeline   │
└────────┬─────────┘
         │
    ┌────┴─────────┐
    │              │
    ▼              ▼
 Docker Build   Tests/Security
    │
    ▼
┌──────────────────┐
│ Amazon ECR       │
│ Docker Registry  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Amazon EKS       │
│ Kubernetes       │
└────────┬─────────┘
         │
         ▼
   ┌────────────┐
   │ Application│
   │ LoadBalancer│
   └────────────┘
         │
         ▼
       Users
```

### Technologies we'll use

| Area               | Technology             |
| ------------------ | ---------------------- |
| Source Control     | Git + GitHub           |
| Application        | Python/Flask           |
| Containerization   | Docker                 |
| CI/CD              | GitHub Actions         |
| Container Registry | Amazon ECR             |
| Cloud              | AWS                    |
| Kubernetes         | Amazon EKS             |
| Infrastructure     | Terraform              |
| Configuration      | Kubernetes YAML / Helm |
| Security           | Trivy                  |
| Monitoring         | Prometheus + Grafana   |
| Logging            | CloudWatch             |
| Secrets            | AWS Secrets Manager    |
| Deployment         | Rolling deployment     |
| DNS                | Route 53               |
| Load Balancing     | AWS Load Balancer      |

---

# Phase 1 — Create the application

We'll start with a small but realistic application.

```text
devops-project/
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
├── Dockerfile
├── .dockerignore
├── .gitignore
│
├── k8s/
│   ├── namespace.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
│
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── providers.tf
│
└── .github/
    └── workflows/
        └── ci-cd.yml
```

The application can expose:

```text
GET /
GET /health
GET /version
```

For example:

```text
Application: DevOps Demo Application
Version: 1.0.0
Environment: Production
Status: Healthy
```

---

# Phase 2 — Dockerize it

We'll create a production-style Dockerfile.

Example:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

EXPOSE 5000

CMD ["python", "app.py"]
```

Build:

```bash
docker build -t devops-app:1.0 .
```

Run:

```bash
docker run -p 5000:5000 devops-app:1.0
```

Test:

```bash
curl http://localhost:5000/health
```

Expected:

```text
{"status":"healthy"}
```

---

# Phase 3 — GitHub

Create:

```text
devops-real-world-project
```

Then:

```bash
git init

git add .

git commit -m "Initial application"

git branch -M main

git remote add origin <YOUR_GITHUB_REPO>

git push -u origin main
```

From this point onward, **GitHub becomes our source of truth**.

---

# Phase 4 — Terraform AWS Infrastructure

Instead of manually creating everything in the AWS console, we'll use Terraform.

Our infrastructure will eventually look like:

```text
                    AWS
                     │
              ┌──────▼──────┐
              │     VPC     │
              └──────┬──────┘
                     │
        ┌────────────┴────────────┐
        │                         │
   Public Subnets            Private Subnets
        │                         │
        │                    ┌────▼────┐
        │                    │   EKS   │
        │                    │ Cluster │
        │                    └────┬────┘
        │                         │
        │                    ┌────▼────┐
        │                    │  Nodes  │
        │                    └────┬────┘
        │                         │
        └──────────────┬──────────┘
                       │
                 Load Balancer
                       │
                    Internet
```

Terraform will create:

* VPC
* Public/private subnets
* Internet Gateway
* NAT Gateway
* Route tables
* Security groups
* EKS cluster
* EKS node group
* IAM roles
* ECR repository

We'll avoid manually creating these resources wherever practical.

---

# Phase 5 — Amazon ECR

Our pipeline will build the Docker image and push it to ECR.

Example:

```text
GitHub
   │
   ▼
GitHub Actions
   │
   ▼
Docker Build
   │
   ▼
Trivy Scan
   │
   ▼
Amazon ECR
   │
   │
   ▼
EKS
```

Image:

```text
ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/devops-app:VERSION
```

---

# Phase 6 — Kubernetes

We'll deploy the application to EKS.

### Deployment

We'll use:

```yaml
replicas: 3
```

So we'll have:

```text
             EKS
              │
       ┌──────┼──────┐
       │      │      │
       ▼      ▼      ▼
     Pod-1  Pod-2  Pod-3
```

This gives us basic high availability.

We'll also configure:

```text
RollingUpdate
readinessProbe
livenessProbe
resources
ConfigMap
Secret
```

For example:

```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxUnavailable: 0
    maxSurge: 1
```

This means Kubernetes can replace old pods gradually rather than taking the application down.

---

# Phase 7 — CI/CD Pipeline

This is where the project becomes **real-world DevOps**.

Every time you execute:

```bash
git push origin main
```

the pipeline runs.

```text
        git push
            │
            ▼
     GitHub Actions
            │
     ┌──────┴──────┐
     ▼             ▼
   Tests        Linting
     │             │
     └──────┬──────┘
            ▼
       Docker Build
            │
            ▼
       Trivy Scan
            │
            ▼
       ECR Push
            │
            ▼
    Update Kubernetes
            │
            ▼
       EKS Deploy
            │
            ▼
      Health Check
            │
       ┌────┴────┐
       ▼         ▼
    SUCCESS     FAIL
       │         │
       ▼         ▼
 Production   Rollback
```

---

# Phase 8 — Security

We'll introduce security into the pipeline rather than treating it as an afterthought.

### Trivy

Scan the Docker image:

```bash
trivy image devops-app:1.0
```

The pipeline can fail if critical vulnerabilities are found.

We'll also avoid storing AWS credentials directly in GitHub.

Instead we'll configure:

```text
GitHub Actions
       │
       ▼
OIDC
       │
       ▼
AWS IAM Role
       │
       ▼
AWS Resources
```

This is much closer to how modern production CI/CD is implemented.

---

# Phase 9 — Monitoring

Once the application is running, we'll monitor it.

```text
                 EKS
                  │
          ┌───────┴────────┐
          │                │
          ▼                ▼
     Application       Kubernetes
       Metrics           Metrics
          │                │
          └───────┬────────┘
                  ▼
             Prometheus
                  │
                  ▼
               Grafana
```

We'll create dashboards for:

* CPU
* Memory
* Pod count
* Request rate
* Error rate
* Application health
* Kubernetes nodes

---

# Phase 10 — Real Deployment Scenario

We'll simulate what happens in an actual company.

Current production:

```text
Version 1.0.0
```

You modify the application:

```text
Version 1.1.0
```

Then:

```bash
git add .
git commit -m "Release version 1.1.0"
git push origin main
```

Pipeline:

```text
Test
 ↓
Build
 ↓
Security Scan
 ↓
ECR
 ↓
EKS
 ↓
Rolling Update
 ↓
Health Check
```

Kubernetes changes:

```text
Old:

Pod 1 → v1.0
Pod 2 → v1.0
Pod 3 → v1.0


Rolling deployment:

Pod 1 → v1.1
Pod 2 → v1.0
Pod 3 → v1.0

Pod 1 → v1.1
Pod 2 → v1.1
Pod 3 → v1.0

Pod 1 → v1.1
Pod 2 → v1.1
Pod 3 → v1.1
```

No planned downtime.

---

# Phase 11 — Failure Scenario

We'll deliberately break version `1.2.0`.

For example:

```text
Application v1.2.0
       ↓
Health checks fail
       ↓
Kubernetes detects unhealthy pods
       ↓
Deployment fails
       ↓
Rollback
       ↓
v1.1.0 restored
```

You'll learn **how DevOps engineers troubleshoot real deployments**, rather than only learning successful commands.

---

# Phase 12 — Troubleshooting

We'll intentionally practice commands such as:

```bash
kubectl get pods
kubectl get deployments
kubectl get svc
kubectl get events
kubectl describe pod <pod>
kubectl logs <pod>
kubectl logs -f <pod>
kubectl rollout status deployment/devops-app
kubectl rollout history deployment/devops-app
kubectl rollout undo deployment/devops-app
```

And AWS:

```bash
aws eks update-kubeconfig \
  --region us-east-1 \
  --name devops-cluster
```

Then:

```bash
kubectl get nodes
```

Expected:

```text
NAME                         STATUS   ROLES
ip-10-0-1-xxx.ec2.internal   Ready    <none>
ip-10-0-2-xxx.ec2.internal   Ready    <none>
```

---

# 🎯 What you'll have at the end

A GitHub repository like:

```text
devops-real-world-project
│
├── application
├── Dockerfile
├── tests
├── Terraform
├── Kubernetes
├── GitHub Actions
├── monitoring
└── README.md
```

And an architecture like:

```text
                       INTERNET
                           │
                           ▼
                     AWS Load Balancer
                           │
                           ▼
                      EKS Ingress
                           │
                 ┌─────────┴─────────┐
                 ▼                   ▼
              Service             Service
                 │                   │
          ┌──────┼──────┐     ┌──────┼──────┐
          ▼      ▼      ▼     ...
         Pod    Pod    Pod
          │
          ▼
       Application
          │
          ▼
      Configuration
          │
     ┌────┴────┐
     ▼         ▼
 ConfigMap   Secrets
```

And CI/CD:

```text
GitHub
  │
  ▼
GitHub Actions
  │
  ├── Unit Tests
  ├── Docker Build
  ├── Trivy Security Scan
  ├── ECR Push
  ├── Kubernetes Deploy
  └── Health Check
           │
           ▼
          EKS
           │
           ▼
       Production
```

## 💼 Resume-worthy project

Once completed, you could describe it as:

> **AWS EKS Production-Style CI/CD Platform** — Designed and implemented an end-to-end DevOps platform using Terraform, Docker, Kubernetes, GitHub Actions, Amazon ECR and EKS. Automated testing, container builds, vulnerability scanning and Kubernetes deployments through CI/CD, implemented rolling deployments and rollback strategies, and integrated Prometheus/Grafana monitoring.

---

## Let's build it hands-on

I recommend **not trying to build everything at once**. We'll do it like a real project, one phase at a time, and I'll give you the exact commands, files, architecture, and troubleshooting for each step.

### Phase 1

**Application → Git → Docker → Local testing**

### Phase 2

**Terraform → AWS VPC → EKS → ECR**

### Phase 3

**Kubernetes → Deployment → Service → Load Balancer**

### Phase 4

**GitHub Actions → CI/CD → ECR → EKS**

### Phase 5

**Security → Trivy → OIDC → IAM**

### Phase 6

**Prometheus → Grafana → Monitoring**

### Phase 7

**Failure injection → Troubleshooting → Rollback**

Since you were just working with **EKS**, we can start directly with **Phase 1 and build the entire project from an empty folder**, rather than giving you a theoretical tutorial.
