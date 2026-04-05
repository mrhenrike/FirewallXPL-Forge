# Interactive shell — core commands

**Language:** English (en-US). **pt-BR:** [../pt-BR/02-shell-interativo-comandos.md](../pt-BR/02-shell-interativo-comandos.md)

The default prompt is configurable via `FXF_RAW_PROMPT` and `FXF_MODULE_PROMPT` in `firewallxpl/interpreter.py`.

## Global commands

| Command | Description |
|---------|-------------|
| `help` | Global help; with a loaded module, also shows module commands |
| `use <path>` | Load module using slashes: `use exploits/routers/dlink/multi_hnap_rce` |
| `search ...` | Search modules ([03-search-and-listing.md](03-search-and-listing.md)) |
| `show <sub>` | Global inventory ([03-search-and-listing.md](03-search-and-listing.md)) |
| `exec <cmd>` | Run OS shell command (avoid untrusted input) |
| `exit` | Quit (EOF / Ctrl+D also) |

## With a module selected

| Command | Description |
|---------|-------------|
| `run` / `exploit` | Execute current module |
| `set option value` | Set option |
| `setg option value` | Set **global** option |
| `unsetg option` | Remove global option |
| `show info` | `__info__` metadata |
| `show options` / `show advanced` | Option sets |
| `check` | Call `check()` if implemented |
| `back` | Unload module |

## `set` syntax

First word is the option name; remainder is the value:

```text
set target 192.168.0.10
set port 443
set ssl true
```

Use `show options` to see exact option names per module.

## Global options

`setg` persists across modules until `unsetg`.

## Keys

- **Tab:** completion
- **Ctrl+C** during `run`: interrupt attempt (module-dependent)
- **Ctrl+D:** exit interpreter

---

[Wiki hub](../README.md)
