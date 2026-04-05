# Resolução de problemas (*troubleshooting*)

**Idioma:** pt-BR. **English (en-US):** [../en-US/11-troubleshooting.md](../en-US/11-troubleshooting.md)

## `ModuleNotFoundError: firewallxpl`

**Causa:** a correr o script a partir de uma pasta que não está no `PYTHONPATH` e sem instalação editable.

**Correção:**

```bash
cd FirewallXPL-Forge
python -m pip install -e .
# ou
python rxf.py    # entrypoint espera estar na raiz do clone com deps instaladas
```

## `stdin is not a TTY`

**Causa:** redirecionamento de *stdin* ou execução em CI sem terminal.

**Correção:** use modo não interativo: `python rxf.py -m ... -s "..."`.

## Falhas `paramiko` / `cryptography` / versão OpenSSL

**Causa:** mistura de versões de *wheel* ou Python antigo.

**Correção:** atualize `pip`, recrie o `venv`, reinstale `requirements.txt`. Em Windows, prefira *builds* oficiais de Python.

## SNMP não responde

- *Firewall* bloqueando UDP/161
- Comunidade SNMP errada (tente `public` / `private` só em lab)
- Dispositivo com SNMP desativado

Use `snmp_port`, `snmp_version` nos módulos aplicáveis.

## Telnet no Python 3.13+

O projeto depende de **`telnetlib3`**. Confirme `pip show telnetlib3`.

## Scapy / PCAP

**Sintoma:** `ImportError` ao usar `generic/pcap/*`.

**Correção:** `pip install scapy` (já no `requirements.txt`). No Windows, captura ao vivo pode exigir Npcap; para só ler ficheiros `.pcap` isso muitas vezes não é necessário.

## Histórico / *readline* no Windows

O PowerShell pode ter comportamento diferente do Bash quanto ao *readline*. Se a completização falhar, ainda pode executar comandos manualmente.

## *Threads* a bloquear ou alvo instável

- Reduza `threads` e use `timing_template paranoid` ou `polite` no AutoPwn
- Aumente `module_timeout_s` se módulos terminam cedo demais por *timeout*

## `Unknown command`

Verifique se está na shell do `rxf` e não dentro de outro programa. Comandos são case-sensitive.

## Log `firewallxpl.log` a crescer

Apague ou rode em ambiente limpo; não commite logs com dados reais.

---

[Wiki hub](../README.md)
