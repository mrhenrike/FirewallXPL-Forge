# Modo não interativo (CLI batch)

**Idioma:** pt-BR. **English (en-US):** [../en-US/04-non-interactive-mode.md](../en-US/04-non-interactive-mode.md)

Quando `stdin` não é um TTY, o interpretador interativo **não** inicia. Para automação, use argumentos na linha de comando.

## Sintaxe

```bash
python rxf.py -m <caminho/modulo> [-s "opção valor"] [-s "opção2 valor2"] ...
```

- `-m` / `--module`: caminho com **pontos** ou **barras** coerentes com o pacote (o código *pythoniza* o path).
- `-s` / `--set`: repetível; cada string é repassada a `command_set` como no shell interativo (**primeira palavra** = nome da opção, resto = valor).

## Exemplo

```bash
python rxf.py -m creds/generic/ssh_default -s "target 192.168.0.50" -s "port 22" -s "threads 4"
```

Fluxo interno: `use` → cada `set` → `exploit`/`run` uma vez.

## Ajuda

```bash
python rxf.py -h
```

## Integração em *pipelines*

- Encadeie com outros comandos só em ambientes controlados.
- Redirecione *stdout*/*stderr* para ficheiros em disco com cuidado (podem conter credenciais ou banners).
- Para orquestração complexa, prefira **Python** importando classes de módulos só se souber isolar efeitos colaterais; o caminho suportado oficialmente é o CLI acima.

## Limitações

- Não há modo “JSON output” nativo universal; a saída é pensada para humanos.
- Módulos que pressionam confirmação interativa podem não ser adequados ao modo batch sem revisão do código.

---

[Wiki hub](../README.md)
