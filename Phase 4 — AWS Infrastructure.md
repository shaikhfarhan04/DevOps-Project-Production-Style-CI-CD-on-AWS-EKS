Absolutely. **Phase 4 is where we move from local development into AWS.** We'll do this carefully because this phase can create real AWS charges.

We'll use **Terraform** to create the infrastructure rather than manually clicking through AWS.

HashiCorp's current EKS guidance also uses Terraform for provisioning EKS, and notes that an EKS cluster itself incurs hourly charges, so we'll keep the environment intentionally small and destroy it when we're done. ([HashiCorp Developer][1])

# Phase 4 — AWS Infrastructure

Our target architecture:

```text
                         AWS
                          │
                    ┌─────▼─────┐
                    │    VPC    │
                    └─────┬─────┘
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
             │                    └─────────┘
             │
             ▼
        Internet Gateway

             +
             
        ┌─────────────┐
        │     ECR     │
        │ Docker Image│
        └─────────────┘
```

We're going to build this in **small checkpoints**.

---

# Phase 4 Roadmap

We'll do:

### 4.1 — AWS CLI

### 4.2 — AWS authentication

### 4.3 — Terraform installation

### 4.4 — Create Terraform project structure

### 4.5 — Terraform provider

### 4.6 — VPC

### 4.7 — ECR

### 4.8 — EKS

### 4.9 — kubectl

### 4.10 — Verify the cluster

**Don't jump ahead.** We'll validate each stage.

---

# 4.1 Check AWS CLI

Open your VS Code terminal.

You're already using PowerShell, so that's perfect.

Run:

```powershell
aws --version
```

We want something similar to:

```text
aws-cli/2.x.x ...
```

AWS recommends AWS CLI v2 for current CLI usage. ([AWS Documentation][2])

### If you get:

```text
aws : The term 'aws' is not recognized...
```

then AWS CLI isn't installed and we'll install it before proceeding.

---

# 4.2 Check AWS authentication

**Do not paste AWS credentials into this chat.**

First run:

```powershell
aws sts get-caller-identity
```

If you're already configured, you'll get something similar to:

```json
{
    "UserId": "...",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/..."
}
```

The account number is okay to keep private; you don't need to send it to me.

---

## If authentication isn't configured

AWS currently recommends short-lived console credentials for local development where possible, rather than long-lived IAM access keys. ([AWS Documentation][3])

If you already have an AWS CLI profile, we can use that.

Check:

```powershell
aws configure list
```

And:

```powershell
aws configure list-profiles
```

If you have a profile such as:

```text
default
```

you can test:

```powershell
aws sts get-caller-identity --profile default
```

---

# ⚠️ Important AWS security rule

Do **not** send me:

```text
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_SESSION_TOKEN
```

If we need to configure credentials, enter them **locally in your terminal/browser**.

AWS explicitly warns that secret access keys are only available at creation time and must be stored securely. ([AWS Documentation][4])

Also, never put credentials in:

```text
.env
Terraform files
GitHub
README.md
Git commits
```

Our existing `.gitignore` already protects `.env`, which is good.

---

# 4.3 Choose our AWS Region

For this project, I recommend:

```text
ap-south-1
```

which is the **Mumbai** AWS Region.

We'll use:

```text
AWS_REGION=ap-south-1
```

You can verify the region your profile currently uses:

```powershell
aws configure get region
```

If you want to set it to Mumbai:

```powershell
aws configure set region ap-south-1
```

Then:

```powershell
aws configure get region
```

Expected:

```text
ap-south-1
```

---

# 4.4 Install/check Terraform

Now run:

```powershell
terraform version
```

We want something like:

```text
Terraform v1.x.x
```

If Terraform isn't installed, don't install a random version from an unofficial site. We'll use the official HashiCorp distribution.

[HashiCorp Terraform](https://developer.hashicorp.com/terraform/install?utm_source=chatgpt.com)

---

# 4.5 Check kubectl

We'll need Kubernetes CLI later.

Run:

```powershell
kubectl version --client
```

It doesn't matter if the EKS cluster isn't available yet.

We're only checking that the command exists.

---

# 4.6 Check your AWS identity

This is the **most important checkpoint before Terraform**.

Run:

```powershell
aws sts get-caller-identity
```

Then:

```powershell
aws configure get region
```

Then:

```powershell
terraform version
```

Then:

```powershell
kubectl version --client
```

---

# Our target

We want something approximately like:

```text
AWS CLI
aws-cli/2.x.x

AWS Region
ap-south-1

Terraform
Terraform v1.x.x

kubectl
Client Version: ...
```

Once these are working, we'll create:

```text
terraform/
├── providers.tf
├── variables.tf
├── main.tf
├── outputs.tf
└── versions.tf
```

and then start provisioning AWS.

### 🚦Your checkpoint now

**Run only these four commands and send me the output:**

```powershell
aws --version
```

```powershell
aws sts get-caller-identity
```

```powershell
terraform version
```

```powershell
kubectl version --client
```

Don't send any credentials or secret values. If one of them fails, paste the error and we'll fix that first.

[1]: https://developer.hashicorp.com/terraform/tutorials/kubernetes/eks?utm_source=chatgpt.com "Provision an EKS cluster (AWS) | Terraform | HashiCorp Developer"
[2]: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html?utm_source=chatgpt.com "Getting started with the AWS CLI - AWS Command Line Interface"
[3]: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-authentication.html?utm_source=chatgpt.com "Authentication and access credentials for the AWS CLI - AWS Command Line Interface"
[4]: https://docs.aws.amazon.com/cli/latest/reference/iam/create-access-key.html?utm_source=chatgpt.com "create-access-key — AWS CLI 2.36.44 Command Reference"
