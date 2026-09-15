
## Phase 5.3 — Verify the application

Run these commands from the project root.

### 1. Check the Pods

```powershell
kubectl get pods -n devops-app -o wide
```

We want:

```text
READY   STATUS
1/1     Running
1/1     Running
```

### 2. Check the Deployment

```powershell
kubectl get deployment -n devops-app
```

Expected:

```text
READY   UP-TO-DATE   AVAILABLE
2/2     2            2
```

### 3. Check the ReplicaSet

```powershell
kubectl get rs -n devops-app
```

This lets us see the ReplicaSet created by the Deployment.

### 4. Check the Service

```powershell
kubectl get service -n devops-app
```

You should see something like:

```text
NAME         TYPE           CLUSTER-IP     EXTERNAL-IP
devops-app   LoadBalancer   10.x.x.x       ...
```

The `EXTERNAL-IP` may initially show:

```text
<pending>
```

That's normal. AWS may need a few minutes to provision the Load Balancer.

### 5. Check Deployment events if necessary

If either Pod isn't `Running`, immediately run:

```powershell
kubectl describe pods -n devops-app
```

And:

```powershell
kubectl get events -n devops-app --sort-by=.lastTimestamp
```

---

### What we're particularly testing

Your Deployment references the ECR image:

```text
194154437225.dkr.ecr.ap-south-1.amazonaws.com/devops-production-dev-app:1.0.0
```

So if both Pods become `Running`, we've proven an important piece of the architecture:

```text
ECR
 │
 │ image pull
 ▼
EKS Worker Node
 │
 ▼
Container
 │
 ▼
Flask :5000
```

Then the LoadBalancer will give us:

```text
Internet
   │
   ▼
AWS Load Balancer
   │
   ▼
Kubernetes Service :80
   │
   ├── Pod 1 :5000
   └── Pod 2 :5000
```

**Run commands 1–4 and send me the output.** If the external address is still `<pending>`, that's okay—we'll wait/check it rather than changing anything prematurely.
