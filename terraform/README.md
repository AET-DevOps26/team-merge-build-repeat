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
- `ssh_public_key`: your existing public SSH key value, for example the output of `cat ~/.ssh/azure.pub`
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

## GitHub Actions

The workflow in `.github/workflows/terraform.yaml` runs Terraform for this directory:

- Pull requests: `fmt`, `init`, `validate`, and `plan`
- Pushes to `main`: `fmt`, `init`, `validate`, `plan`, then `apply`
- Apply uses the reviewed plan artifact and the protected GitHub Environment `production`

### One-time Azure state backend

Create the remote state storage before running the workflow. Use globally unique storage account names.

```bash
az group create \
  --name "<state-resource-group>" \
  --location "swedencentral"

az storage account create \
  --name "<state-storage-account>" \
  --resource-group "<state-resource-group>" \
  --location "swedencentral" \
  --sku Standard_LRS \
  --kind StorageV2 \
  --https-only true \
  --allow-blob-public-access false

az storage container create \
  --name "tfstate" \
  --account-name "<state-storage-account>" \
  --auth-mode login
```

### GitHub variables

Configure these repository or `production` environment variables:

| Variable                           | Value                                                 |
| ---------------------------------- | ----------------------------------------------------- |
| `AZURE_CLIENT_ID`                  | App registration / service principal client ID        |
| `AZURE_TENANT_ID`                  | Azure tenant ID                                       |
| `AZURE_SUBSCRIPTION_ID`            | Azure subscription ID                                 |
| `TF_STATE_RESOURCE_GROUP`          | Resource group containing the state storage account   |
| `TF_STATE_STORAGE_ACCOUNT`         | State storage account name                            |
| `TF_STATE_CONTAINER`               | State blob container name, for example `tfstate`      |
| `TF_VAR_ssh_public_key`            | Public SSH key for the VM admin user                  |
| `TF_VAR_ssh_source_address_prefix` | SSH source prefix; currently `*` for open test access |
