
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

Absolutely. 🚀 We'll start **Phase 4.4.1 — EKS IAM Roles**.

For EKS, we'll create two IAM roles:

```text
                 AWS Account
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
   EKS Cluster Role       EKS Node Role
          │                     │
          ▼                     ▼
   EKS control plane       EC2 worker nodes
                              │
                              ▼
                         ECR / CNI / EKS
```

The distinction is important:

* **Cluster role** → permissions needed by the EKS control plane.
* **Node role** → permissions needed by worker nodes, including pulling images from ECR.

We'll manage both through Terraform.

## 4.4.1.1 — Create `iam.tf`

Inside:

```text
terraform/
```

create a new file:

```text
iam.tf
```

Put this in it:

```hcl
# ---------------------------------------------------------
# EKS Cluster IAM Role
# ---------------------------------------------------------

resource "aws_iam_role" "eks_cluster" {
  name = "${var.project_name}-${var.environment}-eks-cluster-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          Service = "eks.amazonaws.com"
        }

        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_iam_role_policy_attachment" "eks_cluster_policy" {
  role       = aws_iam_role.eks_cluster.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
}


# ---------------------------------------------------------
# EKS Node IAM Role
# ---------------------------------------------------------

resource "aws_iam_role" "eks_node" {
  name = "${var.project_name}-${var.environment}-eks-node-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          Service = "ec2.amazonaws.com"
        }

        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_iam_role_policy_attachment" "eks_worker_node" {
  role       = aws_iam_role.eks_node.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
}

resource "aws_iam_role_policy_attachment" "eks_cni" {
  role       = aws_iam_role.eks_node.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
}

resource "aws_iam_role_policy_attachment" "eks_ecr_read_only" {
  role       = aws_iam_role.eks_node.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}
```

### Why these policies?

| Role        | Policy                               | Purpose                       |
| ----------- | ------------------------------------ | ----------------------------- |
| EKS Cluster | `AmazonEKSClusterPolicy`             | EKS control-plane permissions |
| EKS Node    | `AmazonEKSWorkerNodePolicy`          | Worker-node EKS permissions   |
| EKS Node    | `AmazonEKS_CNI_Policy`               | Kubernetes networking         |
| EKS Node    | `AmazonEC2ContainerRegistryReadOnly` | Pull Docker images from ECR   |

This gives us the permissions required for the architecture we're building without putting broad administrator permissions on the worker nodes.

---

## 4.4.1.2 — Add IAM outputs

Open:

```text
terraform/outputs.tf
```

Add:

```hcl
output "eks_cluster_role_arn" {
  description = "ARN of the EKS cluster IAM role"
  value       = aws_iam_role.eks_cluster.arn
}

output "eks_node_role_arn" {
  description = "ARN of the EKS node IAM role"
  value       = aws_iam_role.eks_node.arn
}
```

---

## 4.4.1.3 — Format and validate

Run from your `terraform` directory:

```powershell
terraform fmt
```

Then:

```powershell
terraform validate
```

Expected:

```text
Success! The configuration is valid.
```

Then:

```powershell
terraform plan
```

At this point, Terraform should show approximately:

```text
Plan: 6 to add, 0 to change, 0 to destroy.
```

The six resources are:

```text
2 IAM roles
4 IAM policy attachments
```

### ⛔ Checkpoint

**Don't run `terraform apply` yet.**

Run:

```powershell
terraform fmt
terraform validate
terraform plan
```

Send me the **plan summary** (especially the final `Plan: ...` line).

If it is clean, we'll apply the IAM roles and verify them before moving to **Phase 4.4.2 — EKS Cluster**.

Exactly. ✅ **Phase 4.4.1 is clean.**

Terraform confirms:

```text
Plan: 6 to add, 0 to change, 0 to destroy.
```

We have the two IAM roles and four required policy attachments ready.

# Phase 4.4.2 — Amazon EKS Cluster

We'll now create the **EKS control plane** using Terraform.

Our target architecture:

```text
                    AWS
                     │
              ┌──────▼──────┐
              │ EKS Cluster │
              │             │
              │ Kubernetes  │
              │ Control     │
              │ Plane       │
              └──────┬──────┘
                     │
             Private Subnets
          ┌──────────┴──────────┐
          ▼                     ▼
      ap-south-1a           ap-south-1b
```

We'll create the cluster first, **without the worker nodes**. Then we'll verify the control plane before adding the managed node group.

---

## 4.4.2.1 — Apply the IAM roles first

Since the plan is clean, create the IAM resources:

```powershell
terraform apply -auto-approve
```

Expected:

```text
Apply complete! Resources: 6 added, 0 changed, 0 destroyed.
```

Then verify the outputs:

```powershell
terraform output eks_cluster_role_arn
terraform output eks_node_role_arn
```

You'll get two IAM role ARNs.

---

## 4.4.2.2 — Create `eks.tf`

After the IAM apply succeeds, create:

```text
terraform/eks.tf
```

Add:

```hcl
resource "aws_eks_cluster" "main" {
  name = "${var.project_name}-${var.environment}-eks"

  role_arn = aws_iam_role.eks_cluster.arn

  vpc_config {
    subnet_ids = module.vpc.private_subnets

    endpoint_private_access = true
    endpoint_public_access  = true
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_cluster_policy
  ]
}
```

### Why these settings?

**Private subnets**

The EKS control-plane networking is associated with our existing private subnets:

```text
10.0.11.0/24
10.0.12.0/24
```

**Private endpoint access**

```hcl
endpoint_private_access = true
```

This allows resources inside the VPC to communicate with the Kubernetes API endpoint privately.

**Public endpoint access**

```hcl
endpoint_public_access = true
```

We're keeping this enabled initially so your local machine can connect to the cluster with `kubectl`.

Later, as a production hardening exercise, we can restrict the public endpoint using `public_access_cidrs` or move toward a more restricted access model.

---

## 4.4.2.3 — Add the cluster output

Open:

```text
terraform/outputs.tf
```

Add:

```hcl
output "eks_cluster_name" {
  description = "EKS cluster name"
  value       = aws_eks_cluster.main.name
}

output "eks_cluster_endpoint" {
  description = "EKS Kubernetes API endpoint"
  value       = aws_eks_cluster.main.endpoint
}
```

---

## 4.4.2.4 — Format and validate

Run:

```powershell
terraform fmt
```

Then:

```powershell
terraform validate
```

Expected:

```text
Success! The configuration is valid.
```

Then:

```powershell
terraform plan
```

At this point we should see approximately:

```text
Plan: 7 to add, 0 to change, 0 to destroy.
```

The additional resource is:

```text
aws_eks_cluster.main
```

---

### ⛔ Checkpoint — don't create the cluster yet

Let's verify the configuration before starting the EKS cluster, because EKS creation takes several minutes and begins generating AWS charges.

First run:

```powershell
terraform apply -auto-approve
```

**for the IAM resources only**, if you haven't already.

Then create `eks.tf` and update `outputs.tf`, and run:

```powershell
terraform fmt
terraform validate
terraform plan
```

Send me the final:

Excellent — the uploaded log confirms everything is clean. 

### Phase 4.4.1 — IAM: ✅ COMPLETE

Your IAM resources were successfully created:

* EKS cluster role
* EKS node role
* `AmazonEKSClusterPolicy`
* `AmazonEKSWorkerNodePolicy`
* `AmazonEKS_CNI_Policy`
* `AmazonEC2ContainerRegistryReadOnly`

Terraform reported:

```text
Apply complete! Resources: 6 added, 0 changed, 0 destroyed.
```



### Phase 4.4.2 — EKS Cluster: Plan ✅ READY

Your current plan is exactly what we want:

```text
Plan: 1 to add, 0 to change, 0 to destroy.
```

The cluster will be:

```text
Name:   devops-production-dev-eks
Region: ap-south-1
VPC:    vpc-09d3de368ec1f7895
Subnets:
  subnet-0758b04d047bbc266
  subnet-0a2e01141a6f3e048
```

And both API endpoint modes are enabled:

```text
endpoint_private_access = true
endpoint_public_access  = true
```



## 🚀 Create the EKS control plane

We're now at the point where we can actually create the cluster.

Run:

```powershell
terraform apply -auto-approve
```

**Expect this to take several minutes.** EKS cluster creation is considerably slower than creating the IAM roles or ECR repository, so don't interrupt Terraform while AWS is provisioning it.

At the end, we want:

```text
Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
```

Then run:

```powershell
terraform output eks_cluster_name
```

and:

```powershell
terraform output eks_cluster_endpoint
```

### ⛔ Checkpoint

For now, run only:

```powershell
terraform apply -auto-approve
```

Send me the final Terraform output after it completes. Then we'll verify the EKS cluster status before moving to **Phase 4.4.3 — EKS Managed Node Group**.


```text
Plan: X to add, X to change, X to destroy.
```

Once that is clean, we'll create the EKS control plane.
