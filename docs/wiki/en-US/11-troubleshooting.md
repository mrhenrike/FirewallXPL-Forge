# Troubleshooting

**Language:** English (en-US). **pt-BR:** [../pt-BR/11-troubleshooting.md](../pt-BR/11-troubleshooting.md)

## `ModuleNotFoundError: firewallxpl`

Install deps and run from repo root, or `pip install -e .`.

## `stdin is not a TTY`

Use non-interactive mode: `python rxf.py -m ... -s "..."`.

## Paramiko / SSL issues

Recreate venv; upgrade `pip`; match Python and wheel support.

## SNMP timeouts

Firewall UDP/161, wrong community, SNMP disabled on device.

## Python 3.13+ Telnet

Ensure `telnetlib3` is installed.

## Scapy / PCAP `ImportError`

`pip install scapy`. On Windows, live capture may need Npcap; offline reads often work without.

## Windows readline

Tab completion may differ from Linux; commands still work typed fully.

## AutoPwn overloads target

Lower `threads`, use `paranoid`/`polite` template, tune `module_timeout_s`.

## Unknown command

Ensure you are at the `rxf` prompt; commands are case-sensitive.

## Large `firewallxpl.log`

Delete or rotate; never commit secrets.

---

[Wiki hub](../README.md)
