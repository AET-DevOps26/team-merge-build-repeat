# Ansible Production Deployment

This deploys the production Docker Compose stack to a VM. Ansible only needs the VM's public IP or DNS
name and an SSH user.

## Files

- `inventory/production.example.ini`: example static inventory. Replace
  `CHANGE_ME` with the VM IP or DNS name from Terraform.
- `group_vars/production/main.yml`: non-secret production settings.
- `group_vars/production/vault.example.yml`: example secret variables for
  Ansible Vault or GitHub Actions secrets.
- `playbooks/deploy.yml`: installs Docker, copies the Compose files, writes
  `.env` and secret files, pulls images, and starts the stack.

## Local Deployment

Create an inventory file:

```bash
cp ansible/inventory/production.example.ini ansible/inventory/production.ini
```

Set the VM host in `ansible/inventory/production.ini`.

Set production values in `ansible/group_vars/production/main.yml`:

```yaml
domain: sudoku.example.com
image_tag: v1.2.3
```

Create encrypted secrets:

```bash
cp ansible/group_vars/production/vault.example.yml ansible/group_vars/production/vault.yml
ansible-vault encrypt ansible/group_vars/production/vault.yml
```

Run the deployment:

```bash
ansible-playbook -i ansible/inventory/production.ini ansible/playbooks/deploy.yml --ask-vault-pass
```

## GitHub Actions Later

The same playbook can be used after Terraform creates the VM. The workflow
should pass the Terraform output as inventory, for example:

```bash
terraform output -raw vm_public_ip
```

Then create a temporary inventory and run Ansible against the `production`
group, so the same `group_vars/production` files are loaded:

```bash
printf '[production]\napp ansible_host=%s ansible_user=ubuntu\n' "${VM_PUBLIC_IP}" > /tmp/production.ini

ansible-playbook \
  -i /tmp/production.ini \
  ansible/playbooks/deploy.yml \
  -e "domain=${DOMAIN}" \
  -e "image_tag=${IMAGE_TAG}" \
  -e "app_database_password=${APP_DATABASE_PASSWORD}" \
  -e "chat_database_password=${CHAT_DATABASE_PASSWORD}"
```

Use GitHub repository or environment secrets for SSH credentials, database
passwords, and optional GHCR credentials.
