# Search and listing

**Language:** English (en-US). **pt-BR:** [../pt-BR/03-busca-e-listagem.md](../pt-BR/03-busca-e-listagem.md)

## `search`

### Minimal

```text
search tplink
```

Keywords lowercased; **all** space-separated words must appear in the module path (logical **AND**).

```text
search type=exploits vendor=linksys wrt
```

### Named filters

| Key | Effect |
|-----|--------|
| `type=` | Top-level type: `exploits`, `creds`, `scanners`, `generic`, `payloads`, `encoders` |
| `device=` | Subpackage under `exploits` (e.g. `routers`) |
| `language=` | Under `encoders` |
| `payload=` | Under `payloads` |
| `vendor=` | Path segment (e.g. `dlink`) |

Invalid filter values print an error and return without results.

## `show`

Useful subcommands include: `all`, `scanners`, `exploits`, `creds`, `wordlists`, `encoders`; plus with a module loaded: `info`, `options`, `advanced`, `devices`.

For a **full** path list see [../ANEXO-INDICE-MODULOS.md](../ANEXO-INDICE-MODULOS.md) or run:

```bash
python tools/gen_wiki_module_index.py
```

## `use` path mapping

`use creds/generic/ssh_default` maps to Python package `firewallxpl.modules.creds.generic.ssh_default`.

---

[Wiki hub](../README.md)
