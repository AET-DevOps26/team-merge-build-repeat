output "public_ip_address" {
  description = "Public IP address of the VM."
  value       = azurerm_public_ip.main.ip_address
}

output "ssh_command" {
  description = "SSH command for connecting to the VM."
  value       = "ssh -i ${trimsuffix(var.ssh_public_key_path, ".pub")} ${var.admin_username}@${azurerm_public_ip.main.ip_address}"
}

output "resource_group_name" {
  description = "Resource group name."
  value       = azurerm_resource_group.main.name
}
