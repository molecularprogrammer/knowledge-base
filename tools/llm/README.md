# Local LLM Cluster Infrastructure (GMKtec K12 Rig)

This directory manages configurations, orchestration, and IDE integrations for our self-hosted, 
headless LLM environment. The host hardware utilizes a GMKtec K12 mini-PC running bare-metal 
Ubuntu Server LTS, leveraging 96GB of unified memory to serve low-latency models locally.

---

## 1. Network Identity & Resolution
To avoid handling changing DHCP leases across dev environments, the server is identified on 
the local network using mDNS or local host aliases.

* **Target Cluster URL (API):** `http://gmktec.local:11434`
* **Target UI Dashboard:** `http://gmktec.local:3000`

### Host Resolution Override (Fallback)
If network infrastructure drops multicast packets, explicitly map the target address within 
your local development desktop's `/etc/hosts` file:

```text
# Local Headless LLM Server Definition
<SERVER_IP_ADDRESS>    gmktec gmktec.local
```

---

## 2. Server Stack Installation

### Step A: Official Docker Engine (Host Service)
Execute on the server to provision the isolated runtime dependencies container engine:

```bash
# Core Prerequisites
sudo apt update && sudo apt install -y ca-certificates curl

# Register GPG Authentication Keys
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL [https://download.docker.com/linux/ubuntu/gpg](https://download.docker.com/linux/ubuntu/gpg) -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add Source Repositories
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF> /dev/null
Types: deb
URIs: [https://download.docker.com/linux/ubuntu](https://download.docker.com/linux/ubuntu)
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF

# Install Core Components
sudo apt update && sudo apt install -y docker-ce docker-ce-cli \
  containerd.io docker-buildx-plugin docker-compose-plugin

# Configure Non-Root Management Privileges
sudo usermod -aG docker $USER
newgrp docker
```

### Step B: Bare-Metal Ollama Setup
Ollama runs directly on the bare-metal OS host filesystem to maximize DDR5 memory channel bandwidth.

```bash
# Pull installation binaries
curl -fsSL [https://ollama.com/install.sh](https://ollama.com/install.sh) | sh
```

Create a systemd service override file to bind the API daemon to all local network interfaces 
and lock the execution cache to system memory:

```bash
sudo mkdir -p /etc/systemd/system/ollama.service.d
sudo nano /etc/systemd/system/ollama.service.d/override.conf
```

*Inject the following environmental definitions into override.conf:*

```ini
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
Environment="OLLAMA_NUM_PARALLEL=4"
Environment="OLLAMA_MAX_LOADED_MODELS=3"
```

Reload daemon allocations and restart your worker instances:

```bash
sudo systemctl daemon-reload && sudo systemctl restart ollama
```

### Step C: Seed Model Weights
Pre-cache the target language models to system disk:

```bash
# Inline Autocomplete (Low latency)
ollama run llama3.1:8b

# Master Coding Assistant (Flagship Context Engine)
ollama run qwen2.5-coder:32b

# Heavy Reasoning Engine (Isolated Logic & Complex Bugs)
ollama run deepseek-r1:70b
```

---

## 3. Web Dashboard Orchestration
Open WebUI runs inside Docker, connecting back to the host system layer via the internal virtual 
gateway proxy interface.

### Deployment Configuration (`tools/llm/docker-compose.yml`)
Navigate to the server deployment root, generate a secure web verification key token inline:

```bash
sed -i "s/WEBUI_SECRET_KEY=.*/WEBUI_SECRET_KEY=$(openssl rand -hex 32)/" \
  docker-compose.yml
```

The underlying target YAML construction configuration:

```yaml
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: open-webui
    ports:
      - "3000:8080"
    environment:
      - OLLAMA_BASE_URL=[http://host.docker.internal:11434](http://host.docker.internal:11434)
      # Inline-Modified Security Key:
      - WEBUI_SECRET_KEY=b9c4f1e3a7d8c2e9b5f6a1d4c8e3f0b2a5d7c1e6b9f4a8d
      - AIOHTTP_CLIENT_TIMEOUT=60
    extra_hosts:
      - "host.docker.internal:host-gateway"
    volumes:
      - open-webui:/app/backend/data
    restart: unless-stopped

volumes:
  open-webui:
```

Launch the daemon network stack:

```bash
docker compose up -d
```

*Note: The primary account registered at http://gmktec.local:3000 inherits full Admin access.* 
*Go immediately to Admin Settings -> General -> Disable Public Signups.*

---

## 4. IDE & Terminal Tool Integrations

### VS Code Client Setup (`Continue.dev`)
Drop these target configurations directly into your desktop workstation configuration map file 
(`~/.continue/config.json`):

```json
{
  "models": [
    {
      "title": "Qwen 2.5 Coder 32B (Chat)",
      "provider": "ollama",
      "model": "qwen2.5-coder:32b",
      "apiBase": "[http://gmktec.local:11434](http://gmktec.local:11434)"
    },
    {
      "title": "DeepSeek R1 70B (Hard Logic)",
      "provider": "ollama",
      "model": "deepseek-r1:70b",
      "apiBase": "[http://gmktec.local:11434](http://gmktec.local:11434)"
    }
  ],
  "tabAutocompleteModel": {
    "title": "Llama 3.1 8B (Ghost Text)",
    "provider": "ollama",
    "model": "llama3.1:8b",
    "apiBase": "[http://gmktec.local:11434](http://gmktec.local:11434)"
  }
}
```

### Aider Terminal-Agent Workflows
To assign larger architectural sweeps or bulk debugging operations directly over the local network 
via standard OpenAI-compatible API bindings, execute these command parameters from workspace roots:

```bash
# Complex Logic / Multi-File Changes (DeepSeek 70B Reasoner)
aider --openai-api-base [http://gmktec.local:11434/v1](http://gmktec.local:11434/v1) \
  --openai-api-key none --model openai/deepseek-r1:70b

# General Implementation / Routine Structural Work (Qwen 32B Coder)
aider --openai-api-base [http://gmktec.local:11434/v1](http://gmktec.local:11434/v1) \
  --openai-api-key none --model openai/qwen2.5-coder:32b
```
