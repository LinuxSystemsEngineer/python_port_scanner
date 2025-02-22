# 🔍 Python Port Scanner 📄

## **Public Service Announcement:**

 ⚠️ This tool is provided for educational and authorized use only. **Use it only on systems you own or have explicit permission to scan.** The authors and maintainers of this project are not liable for any misuse or unauthorized activities. Before using this software, please comply with all applicable laws and regulations.

 ---

 ## Overview

Python Port Scanner is a lightweight, command-line tool written in Python that scans a target IP address or hostname for open ports. It provides a user-friendly interface with color-enhanced output to help you quickly identify active services on a system.

 ---

## Functions

✅ Scans ports in the range 1 to 9999 (adjustable via command-line arguments)
  
✅ Displays open ports with clear, colored output for improved readability
  
✅ Provides a helpful usage message when run without the required argument
  
✅ Uses the `concurrent.futures` module for concurrent scanning, significantly improving speed
  
✅ Implements robust error handling and logging (to both console and file)
  
✅ Supports configurable parameters via advanced argument parsing

 ---

## Explanation

Explanation of how to use the port_scanner.py tool:

```bash
python3 port_scanner.py <target hostname or IP address>
```

---

## How to clone this GitHub repository and use the port scanner 

Clone this GitHub repository:

```bash
git clone https://github.com/LinuxSystemsEngineer/python_port_scanner.git
```

Change directories:

```bash
cd python_port_scanner
```

To run the Python Port Scanner, use the following command:

```bash
python3 port_scanner.py 127.0.0.1
```
---
