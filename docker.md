# Installing Docker

1. Run the installation playbooks

   `ansible-playbook -i inventory playbooks/docker-install.yml`

2. Verify the installation

   `sudo docker run hello-world`
