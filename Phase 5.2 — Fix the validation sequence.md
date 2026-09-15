Good catch — **this is expected behavior with `--dry-run=server` when the namespace doesn't actually exist yet.** Nothing is broken.

What happened:

* `--dry-run=client` validates locally, so it doesn't care that `devops-app` doesn't exist.
* `--dry-run=server` sends each object to the EKS API server.
* Kubernetes did validate the namespace itself, but because it was only a dry run, **the namespace was not persisted**.
* The subsequent Deployment and Service therefore failed with `namespaces "devops-app" not found`.

So this output is actually useful: the manifests themselves are syntactically valid, and the only issue is the dependency between the namespace and the other resources.

## Phase 5.2 — Fix the validation sequence

Let's validate the namespace against the real cluster first.

Run:

```powershell
kubectl apply --dry-run=server -f k8s/namespace.yaml
```

Expected:

```text
namespace/devops-app created (server dry run)
```

Then validate the Deployment and Service together:

```powershell
kubectl apply --dry-run=server -f k8s/deployment.yaml
kubectl apply --dry-run=server -f k8s/service.yaml
```

Expected roughly:

```text
deployment.apps/devops-app created (server dry run)
service/devops-app created (server dry run)
```

### One important point

We're **still not creating anything** with these commands because of `--dry-run=server`.

Once those three checks pass, we'll execute the real deployment in this order:

```powershell
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

Then we'll watch the Pods and LoadBalancer come up.

**Run the three server-side dry-run commands above and send me the output.**
