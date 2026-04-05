# `creds` modules

**Language:** English (en-US). **pt-BR:** [../pt-BR/05-modulos-creds.md](../pt-BR/05-modulos-creds.md)

Credential modules test authentication against network services (SSH, Telnet, FTP/SFTP, HTTP, SNMP, …).

## Typical flow

```text
use creds/generic/ssh_default
set target 192.168.1.1
show options
run
```

## Common options (example: `ssh_default`)

| Option | Typical meaning |
|--------|-----------------|
| `target` | IP, IPv6, or `file://` list with `ip:port` |
| `port` | Service port |
| `threads` | Parallelism |
| `defaults` | Embedded `user:pass` list or `file://` |
| `stop_on_success` | Stop after first success |
| `verbosity` | Print attempts |

Always run `show options` — names vary (`rhost` on some older bases).

## Generic vs vendor

- `creds/generic/*` — broadly applicable bruteforce/default tests.
- `creds/routers/<vendor>/*` — vendor-focused lists.

## SNMP / HTTP

- `creds/generic/http_basic_digest_default` / `http_basic_digest_bruteforce`
- `creds/generic/http_multi_auth_default` — multiple auth modes including form
- `creds/generic/http_web_form_bruteforce` — web login dictionary attack with Hydra-style success/failure rules (`show options`)

See full paths in [../ANEXO-INDICE-MODULOS.md](../ANEXO-INDICE-MODULOS.md).

## `setg` example

```text
setg target 10.0.0.1
use creds/routers/tplink/ssh_default_creds
run
```

---

[Wiki hub](../README.md)
