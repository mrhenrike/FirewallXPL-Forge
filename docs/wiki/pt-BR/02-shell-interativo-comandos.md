# Shell interativo — comandos principais

**Idioma:** Português (pt-BR). **English:** [../en-US/02-interactive-shell-commands.md](../en-US/02-interactive-shell-commands.md)

O prompt padrão é configurável via `FXF_RAW_PROMPT` e `FXF_MODULE_PROMPT`.

---

## Comandos globais (sempre disponíveis)

| Comando | Sintaxe | Descrição |
|---------|---------|-----------|
| `help` | `help` | Exibe ajuda global; com módulo carregado, exibe também os comandos de módulo |
| `use` | `use <modulo/caminho>` | Carrega um módulo usando barras |
| `search` | `search [filtros] <palavra-chave>` | Busca módulos |
| `show` | `show <subcomando>` | Lista módulos ou obtém informações |
| `exec` | `exec <comando shell>` | Executa um comando do SO |
| `install-nse` | `install-nse [flags]` | Instala scripts NSE embutidos no nmap |
| `exit` | `exit` | Encerra (EOF / Ctrl+D também funciona) |

---

## `use` — carregar um módulo

```
use <modulo/caminho>
```

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `modulo/caminho` | `string` | sim | Caminho do módulo com separadores `/` |

**Exemplos:**
```
fxf > use exploits/perimeter/fortinet/fortios_auth_bypass_cve_2022_40684
fxf > use creds/generic/ssh_default
fxf > use scanners/autopwn
fxf > use exploits/perimeter/paloalto/globalprotect_auth_bypass_cve_2026_0257
```

Completamento automático com Tab disponível após digitar `use `.

---

## Comandos de módulo (disponíveis com módulo carregado)

| Comando | Sintaxe | Descrição |
|---------|---------|-----------|
| `run` / `exploit` | `run` | Executa o módulo atual |
| `check` | `check` | Executa o método `check()` mais leve, se implementado |
| `set` | `set <opcao> <valor>` | Define uma opção do módulo atual |
| `setg` | `setg <opcao> <valor>` | Define uma opção **global** (persiste entre módulos) |
| `unsetg` | `unsetg <opcao>` | Remove uma opção global |
| `show info` | `show info` | Exibe metadados `__info__` (nome, descrição, autores, referências) |
| `show options` | `show options` | Exibe todas as opções padrão com valores atuais |
| `show advanced` | `show advanced` | Exibe opções avançadas/ocultas |
| `show devices` | `show devices` | Exibe lista de dispositivos-alvo do `__info__` |
| `back` | `back` | Descarrega o módulo, retorna ao prompt raiz |

---

## `set` — definindo opções

```
set <nome_opcao> <valor>
```

O primeiro token separado por espaço é o nome da opção; todo o restante é o valor.

**Tipos de opção e valores aceitos:**

| Tipo de opção | Exemplos de valor | Notas |
|---------------|------------------|-------|
| `OptIP` | `192.168.1.1`, `10.0.0.50` | Endereço IPv4 alvo |
| `OptPort` | `443`, `8443`, `22` | Inteiro 1–65535 |
| `OptBool` | `true`, `false`, `1`, `0` | Insensível a maiúsculas/minúsculas |
| `OptString` | `admin`, `minha_senha` | String arbitrária |
| `OptInteger` | `4`, `300`, `10` | Inteiro positivo |
| `OptWordList` | `/caminho/para/lista.txt` | Caminho para arquivo de wordlist |

**Exemplos:**
```
fxf (modulo) > set target 10.0.0.1
fxf (modulo) > set port 443
fxf (modulo) > set ssl true
fxf (modulo) > set threads 10
fxf (modulo) > set forge_user admin
fxf (modulo) > set dump_session true
```

**Saída:**
```
target => 10.0.0.1
port => 443
ssl => true
```

---

## `setg` / `unsetg` — opções globais

```
setg <nome_opcao> <valor>
unsetg <nome_opcao>
```

`setg` aplica o valor a todos os módulos carregados subsequentemente que possuam aquela opção.
`unsetg` remove a configuração global.

**Exemplo:**
```
fxf > setg target 192.168.1.1
target => 192.168.1.1
fxf > use exploits/perimeter/cisco/asa_ftd_path_traversal_cve_2020_3452
fxf (modulo) > show options
# target já está definido como 192.168.1.1
fxf (modulo) > unsetg target
{'target': '192.168.1.1'}
```

---

## `check` — verificação de vulnerabilidade

**Valores de retorno:**

| Saída | Significado |
|-------|-------------|
| `[+] Target is vulnerable` | `check()` retornou `True` |
| `[-] Target is not vulnerable` | `check()` retornou `False` |
| `[*] Target could not be verified` | Inconclusivo ou não suportado |

---

## `install-nse` — instalar scripts NSE

```
install-nse [--check] [--force] [--path <dir>] [--list]
```

| Flag | Tipo | Padrão | Descrição |
|------|------|--------|-----------|
| *(sem flag)* | — | — | Detecta nmap e instala todos os scripts automaticamente |
| `--check` | flag | false | Simulação: exibe o que seria instalado |
| `--force` | flag | false | Sobrescreve scripts existentes |
| `--path <dir>` | `string` (caminho) | auto | Diretório NSE personalizado |
| `--list` | flag | false | Lista scripts embutidos e encerra sem instalar |

**Referência completa:** [12-scripts-nse.md](12-scripts-nse.md)

**Exemplo de sessão:**
```
fxf > install-nse
[+] nmap encontrado: /usr/bin/nmap (7.95)
[*] Diretório de scripts NSE: /usr/share/nmap/scripts
[+] Instalado: fxf-globalprotect-detect.nse
[+] Instalado: fxf-globalprotect-auth-bypass-cve-2026-0257.nse
[+] Instalado: fxf-fortios-detect.nse
[+] Instalado: fxf-cisco-asa-detect.nse
[+] Instalado: fxf-firewall-fingerprint.nse
[+] nmap --script-updatedb concluído.
[+] Todos os scripts instalados.
```

---

## Atalhos de teclado

| Tecla | Ação |
|-------|------|
| `Tab` | Autocompletar comandos, caminhos de módulos, nomes de opções |
| `Ctrl+C` | Interromper o `run` atual (comportamento depende do módulo) |
| `Ctrl+D` | Sair do interpretador (igual a `exit`) |
| `Seta para cima/baixo` | Navegar pelo histórico de comandos |

---

## Personalização do prompt

| Variável | Template padrão | Descrição |
|----------|----------------|-----------|
| `FXF_RAW_PROMPT` | `{host} > ` (sublinhado) | Prompt sem módulo carregado |
| `FXF_MODULE_PROMPT` | `{host} ({module}) > ` | Prompt com módulo carregado |

`{host}` padrão é `fxf`. `{module}` é o campo `name` do `__info__` do módulo.

---

[Hub da wiki](../README.md)
