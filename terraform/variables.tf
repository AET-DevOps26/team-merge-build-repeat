variable "subscription_id" {
  description = "Azure Subscription ID where the resources will be created."
  type        = string

  validation {
    condition     = can(regex("^[0-9a-fA-F-]{36}$", var.subscription_id))
    error_message = "subscription_id must be a valid Azure Subscription ID."
  }
}

variable "location" {
  description = "Azure region for the VM."
  type        = string
  default     = "swedencentral"

  validation {
    condition = contains([
      "swedencentral",
      "spaincentral",
      "germanywestcentral",
      "uaenorth",
      "italynorth"
    ], var.location)
    error_message = "location must be one of the allowed regions: swedencentral, spaincentral, germanywestcentral, uaenorth, italynorth."
  }
}

variable "resource_prefix" {
  description = "Prefix for all Azure resources."
  type        = string
  default     = "tmbr-docker"
}

variable "vm_size" {
  description = "Azure VM size."
  type        = string
  default     = "Standard_D2s_v3"
}

variable "admin_username" {
  description = "Admin username for SSH."
  type        = string
  default     = "azureuser"
}

variable "ssh_public_key" {
  description = "Public SSH key used for the VM admin user."
  type        = string

  validation {
    condition     = can(regex("^(ssh-rsa|ssh-ed25519|ecdsa-sha2-nistp[0-9]+) ", var.ssh_public_key))
    error_message = "ssh_public_key must be a valid OpenSSH public key."
  }
}

variable "ssh_source_address_prefix" {
  description = "Allowed source IP for SSH, for example 203.0.113.10/32. Use '*' only for testing."
  type        = string
}

variable "tags" {
  description = "Tags for Azure resources."
  type        = map(string)
  default = {
    project     = "team-merge-build-repeat"
    environment = "prod"
    managed_by  = "terraform"
  }
}
