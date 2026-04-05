# Shell interativo — comandos essenciais

**Idioma:** pt-BR. **English (en-US):** [../en-US/02-interactive-shell-commands.md](../en-US/02-interactive-shell-commands.md)

O prompt padrão é configurável via variáveis de ambiente `FXF_RAW_PROMPT` e `FXF_MODULE_PROMPT` (veja `firewallxpl/interpreter.py`). Exemplo conceitual:

- sem módulo: `rxf >`
- com módulo: `rxf (Nome do Módulo) >`

## Comandos globais (sempre disponíveis)

| Comando | Descrição |
|---------|-----------|
| `help` | Ajuda global; com um módulo carregado, também lista comandos de módulo |
| `use <caminho>` | Carrega módulo. O caminho usa **barras** como no sistema de ficheiros: `use exploits/routers/dlink/multi_hnap_rce` |
| `search ...` | Procura módulos (ver [03-busca-e-listagem.md](03-busca-e-listagem.md)) |
| `show <subcomando>` | Lista informações globais ou inventário de módulos |
| `exec <cmd>` | Executa comando no shell do sistema operacional (**cuidado** com injeção se passar entrada não confiável) |
| `exit` | Sai (também **Ctrl+D** / EOF) |

## Comandos com módulo selecionado

| Comando | Descrição |
|---------|-----------|
| `run` ou `exploit` | Executa o módulo atual |
| `set <opção> <valor>` | Define opção (ex.: `set target 192.168.1.1`) |
| `setg <opção> <valor>` | Define opção **global** reutilizada por módulos |
| `unsetg <opção>` | Remove opção global |
| `show info` | Metadados (`__info__`): nome, descrição, autores, referências, dispositivos |
| `show options` | Opções principais e valores atuais |
| `show advanced` | Opções marcadas como avançadas |
| `show devices` | Dispositivos associados ao módulo, se aplicável |
| `check` | Chama `check()` do módulo quando implementado (deteção de vulnerabilidade sem exploração completa, conforme o módulo) |
| `back` | Descarrega o módulo atual |

## Sintaxe de `set`

O parser trata a primeira palavra como nome da opção e o resto como valor:

```text
set target 192.168.0.10
set port 443
set ssl true
```

Valores com espaços podem depender de como o módulo interpreta a string; em caso de dúvida, consulte `show options` e o código da opção.

## Opções globais (`GLOBAL_OPTS`)

Opções definidas com `setg` ficam disponíveis para módulos subsequentes até `unsetg`. Útil para `target`, `port` ou caminhos de wordlist repetidos em vários módulos.

## Atalhos e leitura de linha

- **Tab**: completa comandos e, em muitos contextos, nomes de opções ou caminhos de módulos após `use` / `search`.
- **Ctrl+C** durante `run`: tentativa de cancelamento (tratamento depende do módulo).
- **Ctrl+D**: encerra o interpretador.

---

[Wiki hub](../README.md)
