Perfect. ✅ **Phase 4 prerequisites are ready.**

Your environment is good:

| Tool               | Status          |
| ------------------ | --------------- |
| AWS CLI            | ✅ v2.34.59      |
| AWS authentication | ✅ Working       |
| Terraform          | ✅ v1.15.8       |
| kubectl            | ✅ v1.36.3       |
| AWS Account        | ✅ Authenticated |

The Terraform update to 1.16.2 is **not required right now**. We can continue with 1.15.8.

One important note: your `sts get-caller-identity` shows an IAM user. **Do not paste any access keys or secret keys here.** We'll let Terraform use your existing AWS CLI authentication rather than putting credentials in Terraform files. AWS recommends short-lived credentials where possible.

# Phase 4.1 — Prepare Terraform

We're going to build the AWS infrastructure incrementally rather than creating everything at once.

Our target will eventually look like:

```text
AWS
│
├── VPC
│   ├── Public Subnets
│   ├── Private Subnets
│   ├── Internet Gateway
│   └── NAT Gateway
│
├── ECR
│   └── devops-app
│
└── EKS
    ├── Control Plane
    └── Worker Nodes
```

For now, **don't create any AWS resources yet**.

## Step 1 — Create the Terraform directory

From your current project root:

```powershell
mkdir terraform
cd terraform
```

Then verify:

```powershell
pwd
```

You should see something similar to:

```text
G:\DevOps-Data\DevOps Project\DevOps-Project-Production-Style-CI-CD-on-AWS-EKS\terraform
```

---

## Step 2 — Create the Terraform files

Inside `terraform`, create these five files:

```text
terraform/
├── versions.tf
├── providers.tf
├── variables.tf
├── main.tf
└── outputs.tf
```

In VS Code you can simply create them from the Explorer.

### `versions.tf`

```hcl
terraform {
  required_version = ">= 1.15.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}
```

### `providers.tf`

```hcl
provider "aws" {
  region = var.aws_region
}
```

### `variables.tf`

```hcl
variable "aws_region" {
  description = "AWS region where infrastructure will be created"
  type        = string
  default     = "ap-south-1"
}
```

We're using **Mumbai (`ap-south-1`)** for this project.

### `main.tf`

For now:

```hcl
# AWS infrastructure will be added here
```

### `outputs.tf`

For now:

```hcl
# Terraform outputs will be added here
```

---

## Step 3 — Protect Terraform state

Before running Terraform, update your **root `.gitignore`**.

Add:

```text
# Terraform
.terraform/
*.tfstate
*.tfstate.*
*.tfvars
crash.log
crash.*.log
```

This is important because Terraform state can contain sensitive infrastructure information.

---

# Step 4 — Initialize Terraform

Make sure you're inside:

```text
...\DevOps-Project-Production-Style-CI-CD-on-AWS-EKS\terraform
```

Run:

```powershell
terraform init
```

You should see something along the lines of:

```text
Initializing the backend...

Initializing provider plugins...

- Finding hashicorp/aws versions matching "~> 6.0"...
- Installing hashicorp/aws ...

Terraform has been successfully initialized!
```

Then run:

```powershell
terraform validate
```

Expected:

```text
Success! The configuration is valid.
```

And finally:

```powershell
terraform plan
```

At this point, because we haven't defined any resources yet, Terraform should essentially say:

```text
No changes. Your infrastructure matches the configuration.
```

### 🚨 Important

**Do not run `terraform apply` yet.**

We're deliberately doing this incrementally so you understand exactly what Terraform is creating and how much it can cost.

---

### Your checkpoint

Run these:

```powershell
cd "G:\DevOps-Data\DevOps Project\DevOps-Project-Production-Style-CI-CD-on-AWS-EKS\terraform"

terraform init
terraform validate
terraform plan
```

**Send me the complete output of those three commands.**

Then we'll move to **Phase 4.2 — AWS VPC**, where we'll create the networking foundation for EKS.
