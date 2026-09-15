Excellent. ✅ Your Terraform foundation is clean:

* `terraform init` → ✅
* AWS provider installed → ✅ `v6.64.0`
* `terraform validate` → ✅
* `terraform plan` → ✅ no resources yet

One small point: the Registry currently shows the VPC module at **6.7.2**, and it supports the AWS provider 6.x series, so we'll use that rather than writing dozens of low-level VPC resources ourselves. ([Terraform Registry][1])

# Phase 4.2 — AWS VPC

We're going to create a **production-style VPC suitable for EKS**:

```text
                    Internet
                       │
                Internet Gateway
                       │
              ┌────────┴────────┐
              │       VPC       │
              │   10.0.0.0/16  │
              │                 │
       ┌──────┴──────┐   ┌──────┴──────┐
       │ Public      │   │ Public      │
       │ Subnet      │   │ Subnet      │
       │ AZ-1        │   │ AZ-2        │
       │10.0.1.0/24  │   │10.0.2.0/24  │
       └─────────────┘   └─────────────┘
              │                 │
          NAT Gateway       NAT Gateway
              │                 │
       ┌──────┴──────┐   ┌──────┴──────┐
       │ Private     │   │ Private     │
       │ Subnet      │   │ Subnet      │
       │ AZ-1        │   │ AZ-2        │
       │10.0.11.0/24 │   │10.0.12.0/24 │
       └─────────────┘   └─────────────┘
```

The **private subnets** will eventually host our EKS worker nodes.

## ⚠️ Cost warning

We're going to use NAT Gateway(s) because this is a production-style architecture, but NAT gateways incur AWS charges. Don't leave the infrastructure running unnecessarily.

For learning, we'll eventually have a `terraform destroy` workflow so you can clean everything up.

---

# Step 1 — Update `variables.tf`

Replace the current contents with:

```hcl
variable "aws_region" {
  description = "AWS region where infrastructure will be created"
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Project name used for AWS resource naming"
  type        = string
  default     = "devops-production"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}
```

---

# Step 2 — Add the VPC module

Replace `main.tf` with:

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "6.7.2"

  name = "${var.project_name}-${var.environment}-vpc"

  cidr = "10.0.0.0/16"

  azs = [
    "ap-south-1a",
    "ap-south-1b"
  ]

  public_subnets = [
    "10.0.1.0/24",
    "10.0.2.0/24"
  ]

  private_subnets = [
    "10.0.11.0/24",
    "10.0.12.0/24"
  ]

  enable_nat_gateway = true
  single_nat_gateway = true

  enable_dns_hostnames = true
  enable_dns_support   = true

  public_subnet_tags = {
    "kubernetes.io/role/elb" = "1"
  }

  private_subnet_tags = {
    "kubernetes.io/role/internal-elb" = "1"
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}
```

### Why `single_nat_gateway = true`?

For a highly available production environment, we'd normally consider one NAT Gateway per AZ.

For **this learning project**, we're deliberately using:

```hcl
single_nat_gateway = true
```

That reduces cost while still giving us the private/public subnet architecture needed for the project.

---

# Step 3 — Add useful outputs

Replace `outputs.tf` with:

```hcl
output "vpc_id" {
  description = "ID of the VPC"
  value       = module.vpc.vpc_id
}

output "vpc_cidr_block" {
  description = "CIDR block of the VPC"
  value       = module.vpc.vpc_cidr_block
}

output "public_subnet_ids" {
  description = "IDs of the public subnets"
  value       = module.vpc.public_subnets
}

output "private_subnet_ids" {
  description = "IDs of the private subnets"
  value       = module.vpc.private_subnets
}

output "availability_zones" {
  description = "Availability zones used by the VPC"
  value       = module.vpc.azs
}
```

These outputs will be very useful later when we create EKS.

---

# Step 4 — Initialize the new module

Run:

```powershell
terraform init
```

Terraform should detect the new VPC module and download it.

You should see something similar to:

```text
Initializing modules...
Downloading registry.terraform.io/terraform-aws-modules/vpc/aws 6.7.2...

Initializing provider plugins...

Terraform has been successfully initialized!
```

---

# Step 5 — Validate

Run:

```powershell
terraform validate
```

Expected:

```text
Success! The configuration is valid.
```

---

# Step 6 — Create the Terraform plan

Now run:

```powershell
terraform plan
```

**Do not run `terraform apply` yet.**

This is an important learning step.

Terraform should show resources such as:

```text
Plan: XX to add, 0 to change, 0 to destroy.
```

You'll see resources for things like:

* VPC
* 2 public subnets
* 2 private subnets
* Internet Gateway
* NAT Gateway
* Elastic IP
* Route tables
* Route associations

The exact resource count can vary with the module version/configuration.

---

## Your checkpoint

Run these three commands:

```powershell
terraform init
terraform validate
terraform plan
```

Then send me the **full `terraform plan` summary and any errors/warnings**.

We'll review the plan together **before creating anything in AWS**.

[1]: https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/latest?tab=resources&utm_source=chatgpt.com "terraform-aws-modules/vpc/aws | Terraform Registry"
