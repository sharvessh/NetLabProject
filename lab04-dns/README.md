# Mini Project 4: Querying DNS Records

Python programs that look up the A, AAAA, CNAME, NS, and MX records of a
domain name using the `dnspython` library. There is a command-line version
and a simple window version built with `tkinter`.

## Requirements

- Ubuntu 22.04 or later
- Python 3.10 or later
- Git

`tkinter` is part of Python but is a separate package on Ubuntu, so it is
installed with `apt`, not `pip`, and it does not appear in `requirements.txt`.

## Get the project

Skip this step if you already have the folder or directory.

```bash
git clone <repository-url>
```

## Setup

1. Go to the lab folder and create the virtual environment:

   ```bash
   cd NetLabProject/lab04-dns
   python3 -m venv .venv
   ```

2. Activate it. The prompt will start with `(.venv)`:

   ```bash
   source .venv/bin/activate
   ```

3. With the environment active, install what the lab needs:

   ```bash
   pip install -r requirements.txt
   sudo apt install python3-tk
   ```

If `python3 -m venv .venv` fails, install the venv package first:

```bash
sudo apt install python3-venv
```

To leave the environment, run `deactivate`. The next time you work on the lab,
run only `source .venv/bin/activate`.

## Usage

Command-line version:

```bash
python3 mydnsquery.py
```

Window version:

```bash
python3 mydnsquery-gui.py
```

Type a domain name such as `example.com` when asked, or in the entry box, and
press Enter.

The output lists each record type in this order. The addresses and names
depend on the domain you enter:

```
--- A records ---
<IPv4 addresses>
--- AAAA records ---
<IPv6 addresses>
--- CNAME records ---
<alias target, or "No CNAME record found.">
--- NS records ---
<name servers>
--- MX records ---
<priority and mail servers>
```

## Files

| File | Purpose |
|---|---|
| `mydnsquery.py` | Command-line DNS lookup |
| `mydnsquery-gui.py` | GUI version using tkinter |
| `requirements.txt` | Python packages (dnspython) |

## Notes

- The programs ask the DNS server set in your system (check with
  `resolvectl status`). On Ubuntu this is normally the local stub at
  `127.0.0.53`, which forwards to your network's DNS server.
- "No CNAME record found" is normal. Only names that are set up as aliases
  have a CNAME record.
- A name that exists only in `/etc/hosts` may not be found, because
  `dnspython` queries DNS and does not read the hosts file by itself.
- Compare the results with the command line:
  `dig example.com A`, `dig example.com MX`, `dig example.com NS`.

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'tkinter'` | `sudo apt install python3-tk`, then recreate the virtual environment if it still fails |
| `ModuleNotFoundError: No module named 'dns'` | Activate the virtual environment and run `pip install -r requirements.txt` |
| `externally-managed-environment` error from pip | You are outside the virtual environment. Run `source .venv/bin/activate` first |
| `python3 -m venv` fails | `sudo apt install python3-venv` |
| The window does not open over SSH | The window version needs a desktop session. Use the command-line version instead |

## Author

Your Name, Course, Year
