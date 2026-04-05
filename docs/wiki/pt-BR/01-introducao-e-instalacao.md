# Introdução, escopo e instalação

**Idioma:** pt-BR. **English (en-US):** [../en-US/01-introduction-and-installation.md](../en-US/01-introduction-and-installation.md)

## Para que serve o FirewallXPL-Forge

É um **framework modular** em Python para apoiar testes de intrusão **autorizados** contra equipamentos de rede embutidos (roteadores, switches, TAPs, firewalls, NGFW). Os módulos implementam, por exemplo:

- tentativas de login com listas de credenciais;
- exploração de vulnerabilidades públicas documentadas;
- varreduras que sugerem módulos aplicáveis;
- utilitários (PCAP, consulta a CVE embutidas, wordlists, SNMP, etc.).

**Visão de arquitetura (exemplo router SOHO — galeria completa no [README da wiki](../README.md)):**

![Router SOHO — superfície de ataque e cobertura da ferramenta](../../img/architecture/rxf_arch_router_soho.png)

## Uso legal e ético

**Utilize apenas em redes e equipamentos para os quais você tenha autorização explícita.** O mantenedor e colaboradores **não** se responsabilizam pelo uso indevido. Em ambientes corporativos, siga o contrato de pentest e o roteiro aprovado.

## Requisitos

- **Python 3.8 a 3.13**
- Dependências em `requirements.txt` (instale com `pip install -r requirements.txt`)
- Em **Python 3.13+**, o pacote `telnetlib3` substitui o `telnetlib` removido da biblioteca padrão
- Módulos **PCAP** dependem de **Scapy**; instalação do Scapy no Windows pode exigir Npcap/WinPcap para captura ao vivo — para análise **offline** de arquivos `.pcap` costuma bastar o interpretador Python

## Instalação

```bash
git clone https://github.com/mrhenrike/FirewallXPL-Forge.git
cd FirewallXPL-Forge
python3 -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows
python3 -m pip install -r requirements.txt
```

## Diagnóstico

```bash
python tools/env_doctor.py
```

Verifica importação de depend núcleo (`requests`, `paramiko`, `pysnmp`, `Crypto`, `setuptools`). **Scapy** não aparece no *doctor* atual; se módulos `generic/pcap/*` falharem ao importar, instale/resolva o Scapy manualmente.

## Iniciar o programa

```bash
python rxf.py
```

O shell interativo exige **TTY** (`stdin` interativo). Para automação use o modo `-m`/`-s` (ver [04-modo-nao-interativo.md](04-modo-nao-interativo.md)).

## Arquivo de log

O arquivo **`firewallxpl.log`** (na pasta de trabalho de onde você invocou `rxf.py`) recebe mensagens de logging do bootstrap. Gire ou apague o arquivo em ambientes de laboratório para não acumular dados sensíveis.

## Histórico de comandos

O interpretador usa `~/.rxf_history` (ou equivalente no perfil do usuário) para histórico do *readline*, quando disponível.

---

[Wiki hub](../README.md)
