# Busca e listagem de módulos

**Idioma:** pt-BR. **English (en-US):** [../en-US/03-search-and-listing.md](../en-US/03-search-and-listing.md)

## `search`

### Uso mínimo

```text
search tplink
```

O interpretador converte o termo em minúsculas. **Todas** as palavras separadas por espaço devem aparecer no **caminho interno** do módulo (condição **E** lógico). Exemplo:

```text
search type=exploits vendor=linksys wrt
```

### Filtros nomeados (kwargs)

Passados como `chave=valor` na linha (o parser usa `=` dentro de cada token):

| Chave | Efeito |
|-------|--------|
| `type=` | Restringe ao tipo de topo: `exploits`, `creds`, `scanners`, `generic`, `payloads`, `encoders` |
| `device=` | Subpasta sob `exploits` (ex.: `routers`) |
| `language=` | Linguagem sob `encoders` |
| `payload=` | Tipo sob `payloads` |
| `vendor=` | Segmento de caminho (ex.: `vendor=dlink`) |

Se um valor for inválido para o filtro, o interpretador exibe erro e não lista nada.

### Realce

Palavras encontradas podem aparecer com realce ANSI no terminal.

## `show` (inventário)

Subcomandos úteis (definidos em `FirewallXPLInterpreter.show_sub_commands`):

| Subcomando | Resultado |
|------------|-----------|
| `show all` | Lista módulos (equivalente interno amplo) |
| `show scanners` | Caminhos sob `scanners/` |
| `show exploits` | Caminhos sob `exploits/` |
| `show creds` | Caminhos sob `creds/` |
| `show wordlists` | Recursos de wordlists disponíveis |
| `show encoders` | Encoders |
| `show info` / `show options` | Exigem módulo selecionado |

Para listagem **completa** e estável em texto, use também o anexo gerado: [ANEXO-INDICE-MODULOS.md](../ANEXO-INDICE-MODULOS.md) ou rode `python tools/gen_wiki_module_index.py`.

## Correspondência `use` ↔ ficheiro

O caminho em `use` mapeia para o pacote Python `firewallxpl.modules.<tipo>.<...>`. Exemplo:

```text
use creds/generic/ssh_default
```

equivale ao módulo `firewallxpl.modules.creds.generic.ssh_default`.

---

[Wiki hub](../README.md)
