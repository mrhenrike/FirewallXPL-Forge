# Interactive shell — core commands

**Language:** English (en-US). **pt-BR:** [../pt-BR/02-shell-interativo-comandos.md](../pt-BR/02-shell-interativo-comandos.md)

The default prompt is configurable via `FXF_RAW_PROMPT` and `FXF_MODULE_PROMPT`.

---

## Global commands (always available)

| Command | Syntax | Description |
|---------|--------|-------------|
| `help` | `help` | Print global help; with a loaded module, also shows module commands |
| `use` | `use <module/path>` | Load a module using forward slashes |
| `search` | `search [filters] <keyword>` | Search for modules |
| `show` | `show <subcommand>` | List modules or get info |
| `exec` | `exec <shell command>` | Run an OS shell command |
| `install-nse` | `install-nse [flags]` | Install bundled NSE scripts into nmap |
| `exit` | `exit` | Quit (EOF / Ctrl+D also works) |

---

## `use` — load a module

```
use <module/path>
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `module/path` | `string` | yes | Module path using `/` separators (e.g. `exploits/perimeter/paloalto/globalprotect_auth_bypass_cve_2026_0257`) |

**Examples:**
```
fxf > use exploits/perimeter/fortinet/fortios_auth_bypass_cve_2022_40684
fxf > use creds/generic/ssh_default
fxf > use scanners/autopwn
fxf > use exploits/perimeter/paloalto/globalprotect_auth_bypass_cve_2026_0257
```

Tab completion is available after typing `use `.

---

## Module commands (available when a module is loaded)

| Command | Syntax | Description |
|---------|--------|-------------|
| `run` / `exploit` | `run` | Execute the current module |
| `check` | `check` | Run the lighter `check()` method if implemented |
| `set` | `set <option> <value>` | Set an option for the current module |
| `setg` | `setg <option> <value>` | Set a **global** option (persists across modules) |
| `unsetg` | `unsetg <option>` | Remove a global option |
| `show info` | `show info` | Print `__info__` metadata (name, description, authors, references) |
| `show options` | `show options` | Print all standard options with current values |
| `show advanced` | `show advanced` | Print hidden/advanced options |
| `show devices` | `show devices` | Print target device list from `__info__` |
| `back` | `back` | Unload current module, return to root prompt |

---

## `set` — setting options

```
set <option_name> <value>
```

The first whitespace-separated token is the option name; everything after is the value.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `option_name` | `string` | yes | Option name as shown by `show options` |
| `value` | varies | yes | See option type (IP, port, boolean, string, integer) |

**Common option types and accepted values:**

| Option type | Example values | Notes |
|-------------|---------------|-------|
| `OptIP` | `192.168.1.1`, `10.0.0.50` | Target IPv4 address |
| `OptPort` | `443`, `8443`, `22` | Integer 1-65535 |
| `OptBool` | `true`, `false`, `1`, `0` | Case-insensitive |
| `OptString` | `admin`, `mypassword` | Arbitrary string |
| `OptInteger` | `4`, `300`, `10` | Positive integer |
| `OptWordList` | `/path/to/list.txt` | Path to wordlist file |

**Examples:**
```
fxf (module) > set target 10.0.0.1
fxf (module) > set port 443
fxf (module) > set ssl true
fxf (module) > set threads 10
fxf (module) > set forge_user admin
fxf (module) > set dump_session true
```

**Output:**
```
target => 10.0.0.1
port => 443
ssl => true
```

---

## `setg` / `unsetg` — global options

```
setg <option_name> <value>
unsetg <option_name>
```

`setg` applies the value to all subsequently loaded modules that have that option.
`unsetg` removes it.

**Example:**
```
fxf > setg target 192.168.1.1
target => 192.168.1.1
fxf > use exploits/perimeter/cisco/asa_ftd_path_traversal_cve_2020_3452
fxf (module) > show options
# target already set to 192.168.1.1
fxf (module) > unsetg target
{'target': '192.168.1.1'}
```

---

## `check` — vulnerability pre-check

```
check
```

Calls the module's `check()` method (lighter than `run`, may be read-only).

**Return values:**

| Output | Meaning |
|--------|---------|
| `[+] Target is vulnerable` | `check()` returned `True` |
| `[-] Target is not vulnerable` | `check()` returned `False` |
| `[*] Target could not be verified` | `check()` returned anything else |

---

## `install-nse` — install NSE scripts

```
install-nse [--check] [--force] [--path <dir>] [--list]
```

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| *(no flag)* | — | — | Detect nmap, install all bundled scripts automatically |
| `--check` | flag | false | Dry-run: show what would be installed |
| `--force` | flag | false | Overwrite existing scripts |
| `--path <dir>` | `string` (path) | auto | Custom NSE scripts directory |
| `--list` | flag | false | List bundled scripts, exit without installing |

**Full reference:** [12-nse-scripts.md](12-nse-scripts.md)

**Example session:**
```
fxf > install-nse
[+] nmap found: /usr/bin/nmap (7.95)
[*] NSE scripts directory: /usr/share/nmap/scripts
[+] Installed: fxf-globalprotect-detect.nse
[+] Installed: fxf-globalprotect-auth-bypass-cve-2026-0257.nse
[+] Installed: fxf-fortios-detect.nse
[+] Installed: fxf-cisco-asa-detect.nse
[+] Installed: fxf-firewall-fingerprint.nse
[+] nmap --script-updatedb completed.
[+] All scripts installed.
```

---

## Keyboard shortcuts

| Key | Action |
|-----|--------|
| `Tab` | Auto-complete commands, module paths, option names |
| `Ctrl+C` | Interrupt current `run` (behavior is module-dependent) |
| `Ctrl+D` | Exit interpreter (same as `exit`) |
| `Up / Down` | Navigate command history |

---

## Prompt customization

| Variable | Default template | Description |
|----------|-----------------|-------------|
| `FXF_RAW_PROMPT` | `{host} > ` (underlined) | Prompt without a loaded module |
| `FXF_MODULE_PROMPT` | `{host} ({module}) > ` | Prompt with a loaded module |

`{host}` defaults to `fxf`. `{module}` is the module's `name` from `__info__`.

---

[Wiki hub](../README.md)
