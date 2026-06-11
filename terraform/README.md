# Azure Docker Host with Terraform

This Terraform setup creates an Ubuntu 24.04 LTS VM in Azure and installs Docker with cloud-init.

## Resources

- Resource Group
- Virtual Network and Subnet
- Public IP
- Network Security Group
- Network Interface
- Linux VM `Standard_D2s_v3`

## Open Ports

| Name          | Port | Protocol | Priority | Source                      |
| ------------- | ---: | -------- | -------: | --------------------------- |
| `allow-http`  |   80 | TCP      |      100 | `*`                         |
| `allow-https` |  443 | TCP      |      110 | `*`                         |
| `allow-ssh`   |   22 | TCP      |      120 | `ssh_source_address_prefix` |

## Usage

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
```

Then update `terraform.tfvars`:

- `subscription_id`: your Azure Subscription ID
- `ssh_public_key_path`: path to your existing public key
- `ssh_source_address_prefix`: your public IP with `/32`

Then run:

```bash
terraform init
terraform plan --out tfout
terraform apply "tfout"
terraform destroy
```

After apply, Terraform prints the public IP and an SSH command.

## Prerequisites

You must be logged in to Azure locally:

```bash
az login
az account set --subscription "<subscription-id>"
```
