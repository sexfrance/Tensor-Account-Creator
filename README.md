<div align="center">
  <h2 align="center">Tensor Account Creator</h2>
  <p align="center">
    An automated tool for creating Tensor.Art accounts with email verification support, proxy handling, and multi-threading capabilities.
    <br />
    <br />
    <a href="https://discord.cyberious.xyz">💬 Discord</a>
    ·
    <a href="#-changelog">📜 ChangeLog</a>
    ·
    <a href="https://github.com/sexfrance/Tensor-Account-Creator/issues">⚠️ Report Bug</a>
    ·
    <a href="https://github.com/sexfrance/Tensor-Account-Creator/issues">💡 Request Feature</a>
  </p>
</div>

---

### ⚙️ Installation

- Requires: `Python 3.7+`
- Make a python virtual environment: `python3 -m venv venv`
- Source the environment: `venv\Scripts\activate` (Windows) / `source venv/bin/activate` (macOS, Linux)
- Install the requirements: `pip install -r requirements.txt`

---

### 🔥 Features

- Automated Tensor.Art account creation
- Email verification support using bune.pw email service
- Proxy support for avoiding rate limits
- Multi-threaded account generation
- Real-time creation tracking
- Configurable thread count
- Debug mode for troubleshooting
- Proxy/Proxyless mode support
- Automatic Cloudflare solver
- Affiliate code support
- Automatic image generation for affiliate validation

---

### 📝 Usage

1. **Configuration**:
   Edit `input/config.toml`:

   ```toml
   [dev]
   Debug = false
   Proxyless = false
   Threads = 1

   [data]
   Affiliate_Link = "" # Optional: Your Tensor.Art affiliate link
   ```

2. **Proxy Setup** (Optional):

   - Add proxies to `input/proxies.txt` (one per line)
   - Format: `ip:port` or `user:pass@ip:port`

3. **Running the script**:

   ```bash
   python main.py
   ```

4. **Output**:
   - Created accounts are saved to:
     - `output/accounts.txt` (format: `email:user_id`)
     - `output/full_account_capture.txt` (format: `user_id:email:auth_token`)

---

### 📹 Preview
<div align="center">
<blockquote class="imgur-embed-pub" lang="en" data-id="a/OkmhlBO" data-context="false" ><a href="//i.imgur.com/OkmhlBO.gif"></a></blockquote><script async src="//s.imgur.com/min/embed.js" charset="utf-8"></script>
<div>
  ---

### ❗ Disclaimers

- This project is for educational purposes only
- The author is not responsible for any misuse of this tool
- Use responsibly and in accordance with Tensor.Art's terms of service

---

### 📜 ChangeLog

```diff
v0.0.1 ⋮ 12/26/2024
! Initial release
```

<p align="center">
  <img src="https://img.shields.io/github/license/sexfrance/Tensor-Account-Creator.svg?style=for-the-badge&labelColor=black&color=f429ff&logo=IOTA"/>
  <img src="https://img.shields.io/github/stars/sexfrance/Tensor-Account-Creator.svg?style=for-the-badge&labelColor=black&color=f429ff&logo=IOTA"/>
  <img src="https://img.shields.io/github/languages/top/sexfrance/Tensor-Account-Creator.svg?style=for-the-badge&labelColor=black&color=f429ff&logo=python"/>
</p>
