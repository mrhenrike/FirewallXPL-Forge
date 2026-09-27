# Introdução, escopo e instalação

**Idioma:** Português (pt-BR). **English:** [../en-US/01-introduction-and-installation.md](../en-US/01-introduction-and-installation.md)

## O que é o FirewallXPL-Forge

Um **framework Python modular** para testes de segurança **autorizados** em dispositivos de perímetro de rede: NGFW, UTM, WAF, concentradores VPN, NAC, balanceadores de carga e firewalls adjacentes a OT. Segue o modelo de módulos do Metasploit: selecione um módulo, defina as opções, execute `check` e depois `run`.

> **Aviso de migração (v2.1.0):** Todos os 81 módulos estão disponíveis no
> [EmbedXPL-Forge](https://github.com/mrhenrike/EmbedXPL-Forge) (`pip install embedxpl`).
> O FirewallXPL-Forge v2.1.0 é o último release standalone e não receberá novos módulos.

**Exemplo de fluxo:**

```
fxf > use exploits/perimeter/fortinet/fortios_auth_bypass_cve_2022_40684
fxf (FortiOS Auth Bypass CVE-2022-40684) > set target 10.0.0.1
fxf (FortiOS Auth Bypass CVE-2022-40684) > check
[+] Target is vulnerable
fxf (FortiOS Auth Bypass CVE-2022-40684) > run
```

---

## Uso legal e ético

**Use apenas em redes e dispositivos que você possui ou tem permissão escrita explícita para testar.**
Os mantenedores não são responsáveis por uso indevido. Siga seu contrato e as regras de engajamento.

---

## Requisitos

| Item | Mínimo | Observações |
|------|--------|-------------|
| Python | 3.8 | 3.13+ requer extra `telnetlib3` |
| OS | Linux, macOS, Windows | Alvo principal de desenvolvimento é Linux |
| nmap | qualquer | Opcional; necessário para o extra `discovery` e scripts NSE |
| biblioteca cryptography | qualquer | Necessária para o forge de cookie CVE-2026-0257 |

---

## Instalação

### Via PyPI (recomendado)

```bash
pip install firewallxpl
# Com TUI e suporte a descoberta nmap:
pip install "firewallxpl[tui,discovery]"
```

### A partir do código-fonte (desenvolvimento / editável)

```bash
git clone https://github.com/mrhenrike/FirewallXPL-Forge.git
cd FirewallXPL-Forge
python3 -m venv .venv
source .venv/bin/activate       # Linux / macOS
# .venv\Scripts\Activate.ps1   # Windows PowerShell
pip install -e ".[tui,discovery]"
```

### Extras opcionais

| Extra | Instala | Finalidade |
|-------|---------|-----------|
| `tui` | `rich` | Saída colorida TUI |
| `tui-full` | `rich`, `textual` | TUI completo com tabelas interativas |
| `discovery` | `python-nmap` | Descoberta de hosts/serviços via nmap |
| `ml` | `scikit-learn`, `joblib` | Advisor ML para AutoPwn |
| `ml-gpu` | `torch` | Logits de timing via GPU (CUDA) |
| `async` | `aiohttp`, `asyncssh` | Cliente HTTP + SSH assíncrono |
| `full` | todos acima | Tudo incluído |

---

## Instalar scripts NSE

Após instalar o firewallxpl, publique os scripts NSE de firewall embutidos no nmap:

```bash
# Modo interativo
python fxf.py
fxf > install-nse

# Modo não-interativo (requer nmap no PATH)
python fxf.py -c "install-nse"

# Com privilégios elevados (Linux)
sudo python fxf.py -c "install-nse"

# Diretório personalizado
python fxf.py -c "install-nse --path /usr/local/share/nmap/scripts"
```

Se o nmap não estiver instalado, o comando exibe o caminho dos scripts embutidos para
que você possa copiá-los manualmente depois. Consulte [12-scripts-nse.md](12-scripts-nse.md)
para a referência completa de NSE.

---

## Diagnósticos

```bash
python tools/env_doctor.py
```

Verifica imports principais. O Scapy não é verificado; corrija manualmente se os módulos
`generic/pcap/*` falharem ao importar.

```bash
python tools/check_env_readiness.py
```

Valida prontidão do ambiente (indexação de módulos, arquivos de recursos).

---

## Iniciar a aplicação

### Modo interativo

```bash
python fxf.py
```

Requer um **TTY**. O prompt é `fxf >`.

**Personalização do ambiente:**

| Variável | Padrão | Efeito |
|----------|--------|--------|
| `FXF_RAW_PROMPT` | `fxf >` (sublinhado) | Prompt sem módulo carregado |
| `FXF_MODULE_PROMPT` | `fxf (modulo) >` | Prompt com módulo carregado |

### Modo não-interativo / batch

```bash
python fxf.py -m <modulo/caminho> [-s "opcao valor"] ...
python fxf.py -h
```

Veja [04-modo-nao-interativo.md](04-modo-nao-interativo.md).

---

## Arquivo de log

`firewallxpl.log` no diretório de trabalho atual. Handler rotativo, máx. 500 KB.

## Histórico de comandos

`~/.fxf_history` (histórico readline, 100 entradas).

---

[Hub da wiki](../README.md)
