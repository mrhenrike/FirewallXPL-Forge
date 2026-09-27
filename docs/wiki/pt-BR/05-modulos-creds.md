# Módulos `creds`

**Idioma:** Português (pt-BR). **English:** [../en-US/05-creds-modules.md](../en-US/05-creds-modules.md)

Módulos de credenciais testam serviços de autenticação usando credenciais padrão ou ataques de dicionário. Protocolos suportados: SSH, Telnet, FTP/SFTP, HTTP (básico, digest, formulário), SNMP e outros.

---

## Fluxo típico

```text
fxf > use creds/generic/ssh_default
fxf (SSH Default Credentials) > set target 192.168.1.1
fxf (SSH Default Credentials) > set port 22
fxf (SSH Default Credentials) > set threads 4
fxf (SSH Default Credentials) > show options
fxf (SSH Default Credentials) > run
```

**Saída de exemplo:**
```
[*] Running module creds.generic.ssh_default...
[+] 192.168.1.1:22 — Found credentials: admin / admin
[+] 192.168.1.1:22 — Found credentials: root / root
```

---

## Opções comuns

| Opção | Tipo | Padrão | Descrição |
|-------|------|--------|-----------|
| `target` | `OptIP` / `string` | `""` | IP, IPv6, hostname ou `file://caminho` com entradas `ip:porta` |
| `port` | `OptPort` | padrão do protocolo | Porta do serviço (inteiro 1–65535) |
| `threads` | `OptInteger` | `8` | Threads de conexão concorrentes |
| `defaults` | `OptString` | lista embutida | Lista `usuario:senha` embutida ou `file://caminho/lista.txt` |
| `stop_on_success` | `OptBool` | `false` | Parar após a primeira credencial encontrada |
| `verbosity` | `OptBool` | `false` | Exibir cada tentativa |
| `timeout` | `OptInteger` | `10` | Timeout por tentativa em segundos |
| `ssl` | `OptBool` | `false` | Usar TLS/SSL quando aplicável |

> **Nota:** Os nomes das opções variam por módulo. Sempre execute `show options` após carregar um módulo.

---

## Módulos genéricos de credenciais

| Caminho do módulo | Protocolo | Observações |
|-------------------|-----------|-------------|
| `creds/generic/ssh_default` | SSH | Baseado em Paramiko |
| `creds/generic/telnet_default` | Telnet | Simples + `telnetlib3` no Python 3.13+ |
| `creds/generic/ftp_default` | FTP | ftplib |
| `creds/generic/http_basic_digest_default` | HTTP Basic/Digest | `requests` |
| `creds/generic/http_basic_digest_bruteforce` | HTTP Basic/Digest | Ataque de dicionário |
| `creds/generic/http_multi_auth_default` | HTTP (multi-modo) | Basic, Digest, NTLM |
| `creds/generic/http_web_form_bruteforce` | Formulário HTTP | Nomes de campos e regras de sucesso/falha configuráveis |
| `creds/generic/snmp_default` | SNMP v1/v2c | Brute-force de community string |

---

## Módulos de credenciais por vendor

| Prefixo do módulo | Vendor / foco |
|-------------------|---------------|
| `creds/perimeter/cisco/` | Cisco ASA, IOS |
| `creds/perimeter/fortinet/` | FortiGate, FortiOS |
| `creds/perimeter/juniper/` | Juniper SRX, JunOS |
| `creds/perimeter/ipfire/` | IPFire |
| `creds/perimeter/pfsense/` | pfSense |

Lista completa: [../ANEXO-INDICE-MODULOS.md](../ANEXO-INDICE-MODULOS.md)

---

## Usando `setg` entre múltiplos módulos

```text
fxf > setg target 10.0.0.1
target => 10.0.0.1
fxf > use creds/generic/ssh_default
fxf (SSH Default Credentials) > run

fxf > use creds/generic/ftp_default
fxf (FTP Default Credentials) > run
# target já está definido como 10.0.0.1
```

---

## Opções de formulário web (`http_web_form_bruteforce`)

| Opção | Tipo | Descrição |
|-------|------|-----------|
| `url` | `OptString` | URL completa de login |
| `username_field` | `OptString` | Nome do campo HTML para usuário |
| `password_field` | `OptString` | Nome do campo HTML para senha |
| `success_pattern` | `OptString` | Regex ou string indicando sucesso |
| `failure_pattern` | `OptString` | Regex ou string indicando falha |
| `usernames` | `OptString` | `file://caminho` ou lista separada por vírgulas |
| `passwords` | `OptString` | `file://caminho` ou lista separada por vírgulas |

---

## Uso em batch (não-interativo)

```bash
python fxf.py \
    -m creds/generic/ssh_default \
    -s "target 192.168.0.50" \
    -s "port 22" \
    -s "threads 8" \
    -s "stop_on_success true"
```

---

[Hub da wiki](../README.md)
