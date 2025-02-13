# Hitch

---

*A lightweight CLI tool for syncing, deploying, and managing remote dev environments*

---

## Overview

Hitch is a command-line tool that helps developers set up and manage remote development environments effortlessly. 

It uses Syncthing for seamless file synchronization, Docker for containerization, and Kubernetes for deployment.

---

## Key Features

✅ Sync files automatically between local and remote environments using Syncthing

✅ Build Docker images locally and save them as .tar archives for easy transfer

✅ Deploy applications on a remote machine using Kubernetes

✅ Manage SSH tunnels for secure access to remote environments

✅ Create and clean up environments with simple commands

---

## Installation

### 1. Install Hitch

```bash
uv pip install git+https://github.com/your-repo/hitch.git
```

---

## Usage

### 1. Build Environment

```bash
hitch build
```

### 2. deploy Environment

```bash 
hitch up
```

### 3. Clean Up Environment

```bash
hitch down
```

---

## Configure `hitch.yaml`

hitch is configured via a 'hitch.yaml' file in your project root

### Example `hitch.yaml`

```yaml
version: 1
project_name: "test_hitch"
images:
  - name: "busybox"
    image: "busybox"
    tag: "latest"
  - name: "hello_world"
    dockerfile_path: "."
    build_context: "."
    tag: "latest"
deployment:
  local_directory: "./deploy"
  remote_directory: "/opt/test_hitch"
  cleanup_commands:
    - "chmod +x cleanup.sh"
    - "sh cleanup.sh"
  install_commands:
    - "chmod +x install.sh"
    - "sh install.sh"
  resources:
    - "./resources/deployment.yaml"
    - "./resources/services.yaml"
remote: 
  - name: "device"
    host: "10.10.10.10"
    user: "root" 
    password: "password"
    port: 22
ssh_tunnels:
  - name: "web-service"
    local_port: 8080
    remote_port: 8080
  - name: "com-service"
    local_port: 8081
    remote_port: 8081
sync:
  local_path: "./project"
  remote_path: "/home/dev/project"
```

---

## Roadmap

#### Planned Features:

✅ hitch status → Check the status of remote deployments

✅ hitch logs → View logs from Syncthing or your containers

✅ hitch restart → Restart the sync service

## License

This project is licensed under the MIT License 