
# Phase 5 — Deploy the Flask Application to EKS

Now we're moving from **infrastructure** to **application deployment**.

Our flow will be:

```text
                    GitHub
                       │
                       ▼
              Flask Application
                       │
                       ▼
                Docker Image
                       │
                       ▼
                     ECR
                       │
                       │ pull
                       ▼
                ┌─────────────┐
                │     EKS     │
                │             │
                │ ┌─────────┐ │
                │ │ Pod 1   │ │
                │ │ Flask   │ │
                │ └─────────┘ │
                │ ┌─────────┐ │
                │ │ Pod 2   │ │
                │ │ Flask   │ │
                │ └─────────┘ │
                └──────┬──────┘
                       │
                       ▼
                   Kubernetes
                    Service
```

We'll **first deploy manually**. This is important because you'll understand Kubernetes before GitHub Actions starts doing it automatically.

---

## Phase 5.1 — Create Kubernetes manifests

From your project root, create a new directory:

```text
k8s/
```

Your project will now look roughly like:

```text
DevOps-Project-Production-Style-CI-CD-on-AWS-EKS
│
├── app/
├── tests/
├── terraform/
├── k8s/
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

### Create `k8s/namespace.yaml`

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: devops-app
  labels:
    project: devops-production
    environment: dev
```

### Create `k8s/deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment

metadata:
  name: devops-app
  namespace: devops-app

spec:
  replicas: 2

  selector:
    matchLabels:
      app: devops-app

  template:
    metadata:
      labels:
        app: devops-app

    spec:
      containers:
        - name: devops-app

          image: 194154437225.dkr.ecr.ap-south-1.amazonaws.com/devops-production-dev-app:1.0.0

          ports:
            - containerPort: 5000

          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"

            limits:
              cpu: "500m"
              memory: "256Mi"

          readinessProbe:
            httpGet:
              path: /health
              port: 5000

            initialDelaySeconds: 5
            periodSeconds: 10

          livenessProbe:
            httpGet:
              path: /health
              port: 5000

            initialDelaySeconds: 15
            periodSeconds: 20
```

### Create `k8s/service.yaml`

For the first deployment, we'll expose the application through an AWS LoadBalancer:

```yaml
apiVersion: v1
kind: Service

metadata:
  name: devops-app
  namespace: devops-app

spec:
  type: LoadBalancer

  selector:
    app: devops-app

  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
```

So the traffic flow will be:

```text
Internet
   │
   ▼
AWS Load Balancer
   │
   ▼
Kubernetes Service :80
   │
   ├──────────────┐
   ▼              ▼
Pod 1           Pod 2
:5000           :5000
```

## Phase 5.2 — Validate the manifests

Before touching the cluster, run from the **project root**:

```powershell
kubectl apply --dry-run=client -f k8s/
```

You should see something similar to:

```text
namespace/devops-app created (dry run)
deployment.apps/devops-app created (dry run)
service/devops-app created (dry run)
```

Then inspect the manifests:

```powershell
kubectl apply --dry-run=server -f k8s/
```

This performs validation against your actual EKS API server without creating the resources.

### Don't apply them yet.

Run those two commands and send me their output.

Once validation passes, we'll actually deploy the application and watch:

```text
Deployment
    ↓
ReplicaSet
    ↓
2 Pods
    ↓
Readiness / Liveness
    ↓
LoadBalancer
    ↓
External URL
```

That will be our first real application running on your EKS cluster.
