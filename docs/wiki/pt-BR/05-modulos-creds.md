# Módulos `creds` — credenciais

**Idioma:** pt-BR. **English (en-US):** [../en-US/05-creds-modules.md](../en-US/05-creds-modules.md)

Os módulos de credenciais testam **autenticação** contra serviços de rede: SSH, Telnet, FTP/SFTP, HTTP (Basic/Digest/form), SNMP, etc.

## Padrão de uso

```text
use creds/generic/ssh_default
set target 192.168.1.1
show options
run
```

## Opções frequentes (exemplo: `creds/generic/ssh_default`)

| Opção | Significado típico |
|-------|---------------------|
| `target` | IP, IPv6 ou `file://lista.txt` com `ip:porta` |
| `port` | Porta do serviço |
| `threads` | Paralelismo |
| `defaults` | Wordlist *User:Pass* embutida ou `file://...` |
| `stop_on_success` | Parar no primeiro login válido |
| `verbosity` | Mostrar tentativas |

**Importante:** cada módulo declara as suas opções em `show options`. Não assuma que todos usam os mesmos nomes (alguns usam `rhost` herdado de bases antigas).

## Genéricos vs por fabricante

- **`creds/generic/*`**: bruteforce ou defaults aplicáveis a vários fabricantes.
- **`creds/routers/<vendor>/*`**: listas de credenciais comuns para esse *vendor*.

## SNMP

- `creds/generic/snmp_bruteforce` — comunidades comuns
- `creds/generic/snmpv3_default` — conjuntos de utilizador/autenticação comuns em SNMPv3

## HTTP

- `creds/generic/http_basic_digest_default` / `http_basic_digest_bruteforce`
- `creds/generic/http_multi_auth_default` — vários esquemas
- `creds/generic/http_web_form_bruteforce` — formulário web com regras estilo Hydra (F=/S=, códigos HTTP, Location)
- Formulários específicos: ex. `creds/routers/pfsense/webinterface_http_form_default_creds.py`

## Wordlists embutidas

O pacote `firewallxpl.resources.wordlists` resolve caminhos relativos ao projeto. Consulte `show wordlists` no CLI para inventário.

## Integração com `setg`

Para um alvo fixo durante vários módulos:

```text
setg target 10.0.0.1
use creds/routers/tplink/ssh_default_creds
run
back
use creds/routers/tplink/telnet_default_creds
run
```

---

[Wiki hub](../README.md)
