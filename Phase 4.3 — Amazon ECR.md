# Phase 4.3 — Amazon ECR

Now we'll create our **private Docker image registry** in AWS.

The architecture becomes:

```text
                   GitHub
                      │
                      ▼
              GitHub Actions
                      │
                Docker Build
                      │
                      ▼
             ┌─────────────────┐
             │      ECR        │
             │                 │
             │  devops-app     │
             │     :1.0.0      │
             └────────┬────────┘
                      │
                      ▼
                    EKS
```

ECR will eventually store the Docker images that our EKS cluster pulls.

---

## Step 1 — Create `ecr.tf`

Inside your `terraform` directory, create:

```text
terraform/
├── versions.tf
├── providers.tf
├── variables.tf
├── main.tf
├── outputs.tf
└── ecr.tf
```

Put this in `ecr.tf`:

```hcl
resource "aws_ecr_repository" "app" {
  name                 = "${var.project_name}-${var.environment}-app"
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "AES256"
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}
```

### Why these settings?

**Immutable tags**

```hcl
image_tag_mutability = "IMMUTABLE"
```

This prevents someone from accidentally overwriting an existing image tag.

For example, once:

```text
devops-production-dev-app:1.0.0
```

exists, another image can't simply replace the `1.0.0` tag.

That's useful for reproducible deployments.

**Scan on push**

```hcl
scan_on_push = true
```

AWS ECR will scan images when they're pushed. Later we'll also add **Trivy** to our CI/CD pipeline, giving us security scanning before deployment.

**Encryption**

```hcl
encryption_type = "AES256"
```

The images are encrypted at rest using ECR's server-side encryption.

---

# Step 2 — Add ECR outputs

Add the following to your existing `outputs.tf`:

```hcl
output "ecr_repository_name" {
  description = "ECR repository name"
  value       = aws_ecr_repository.app.name
}

output "ecr_repository_url" {
  description = "ECR repository URL"
  value       = aws_ecr_repository.app.repository_url
}
```

Your `outputs.tf` should now contain both the VPC outputs and these ECR outputs.

---

# Step 3 — Format the Terraform

Run:

```powershell
terraform fmt
```

You should see files such as:

```text
ecr.tf
main.tf
outputs.tf
providers.tf
variables.tf
versions.tf
```

---

# Step 4 — Validate

Run:

```powershell
terraform validate
```

Expected:

```text
Success! The configuration is valid.
```

---

# Step 5 — Review the plan

Run:

```powershell
terraform plan
```

This time Terraform should recognize the VPC as already managed.

You should see something similar to:

```text
Plan: 1 to add, 0 to change, 0 to destroy.
```

Most importantly, you **should NOT see Terraform trying to recreate your VPC**.

You want:

```text
aws_ecr_repository.app will be created
```

and:

```text
Plan: 1 to add, 0 to change, 0 to destroy.
```

---

## 🚫 Don't apply yet

Just run:

```powershell
terraform fmt
terraform validate
terraform plan
```

Send me the final plan summary.

Perfect. ✅ Your Terraform plan is exactly what we expected:

* **1 resource to create**
* ECR repository: `devops-production-dev-app`
* Region: `ap-south-1`
* Immutable image tags
* Scan on push enabled
* AES256 encryption
* **0 changes / 0 destroys**

Let's continue with **Phase 4.3.1 — Create ECR → Push Docker Image → Verify**.

### Step 1 — Create the ECR repository

You are already inside the `terraform` directory.

Run:

```powershell
terraform apply -auto-approve
```

You should eventually see:

```text
Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
```

Then run:

```powershell
terraform output
```

You should get something similar to:

```text
ecr_repository_name = "devops-production-dev-app"
ecr_repository_url = "194154437225.dkr.ecr.ap-south-1.amazonaws.com/devops-production-dev-app"
```

**Send me the output of `terraform output`.**

Then we'll move to **Step 2 — authenticate Docker with ECR and push your existing image**.


Once we confirm the ECR plan is clean, we'll do:

**Phase 4.3.1 — Create ECR → Push your existing Docker image → Verify it in AWS.**

That will be the first point where the Docker application from our earlier phases actually enters AWS. 🚀
