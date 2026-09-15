
## 🚀 Next: Phase 4.4 — Amazon EKS

This is the major infrastructure step.

We'll build the EKS foundation with Terraform rather than creating the cluster manually. We'll do it incrementally:

1. **EKS IAM roles**
2. **EKS cluster**
3. **EKS managed node group**
4. Connect `kubectl` to the cluster
5. Verify nodes
6. Deploy our ECR image to Kubernetes

We'll keep the configuration production-style while avoiding unnecessary complexity/cost at this stage.

**Important:** EKS and the existing NAT Gateway incur AWS charges, so once the infrastructure is running, we'll keep an eye on resources and clean up anything we don't need.

When you're ready, we'll start with **Phase 4.4.1 — EKS IAM roles**.
