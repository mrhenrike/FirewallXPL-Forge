# Solução de problemas

**Idioma:** Português (pt-BR). **English:** [../en-US/11-troubleshooting.md](../en-US/11-troubleshooting.md)

---

## Problemas de instalação

### `ModuleNotFoundError: firewallxpl`

Causa: executando de um diretório onde o pacote não está instalado.

```bash
pip install -e .
# ou
pip install firewallxpl
```

### Versão Python antiga

```
FirewallXPL requires Python 3.8+ (detected: 3.7.x)
```

Atualize para Python 3.8 ou superior. Use `pyenv` ou pacotes do sistema.

---

## Shell interativo

### `stdin is not a TTY`

Causa: entrada por pipe ou contexto sem terminal (ex.: CI).

Solução: use o modo não-interativo:
```bash
python fxf.py -m <modulo> -s "opcao valor"
```

### `Unknown command` (Comando desconhecido)

- Comandos são sensíveis a maiúsculas/minúsculas.
- Certifique-se de estar no prompt `fxf >`.
- Comandos de módulo (`run`, `set`, `check`, `back`) só funcionam com um módulo carregado.

### Completamento de Tab não funciona (Windows)

Windows não tem GNU readline por padrão. Os comandos digitados por completo funcionam normalmente.
Instale `pyreadline3` para suporte básico de completamento:
```bash
pip install pyreadline3
```

---

## Instalador de scripts NSE

### `[-] nmap not found in PATH`

Instale o nmap para o seu SO:
```bash
sudo apt-get install nmap        # Debian/Ubuntu
sudo yum install nmap            # RHEL/CentOS
brew install nmap                # macOS Homebrew
# Windows: https://nmap.org/download.html
```

Depois execute novamente `fxf > install-nse`.

### Erro de permissão ao instalar scripts NSE

Linux/macOS: o diretório de scripts do nmap (`/usr/share/nmap/scripts/`) requer root/sudo para escrever.

```bash
sudo python fxf.py -c "install-nse"
# Ou instale em um diretório com permissão de escrita:
python fxf.py -c "install-nse --path ~/.nmap/scripts"
mkdir -p ~/.nmap/scripts
nmap --datadir ~/.nmap --script-updatedb
```

### Scripts NSE instalados mas nmap não os encontra

Execute `nmap --script-updatedb` manualmente:
```bash
nmap --script-updatedb
# ou
sudo nmap --script-updatedb
```

### `No bundled NSE scripts found` (Nenhum script NSE embutido encontrado)

Causa: pacote instalado sem os dados de `resources/` (instalação editable incompleta ou build incompleto).

```bash
# A partir do código-fonte, verifique se os recursos estão presentes:
ls firewallxpl/resources/arsenal/nse/
# Deve listar 5 arquivos .nse

# Se ausente, clone novamente:
git clone https://github.com/mrhenrike/FirewallXPL-Forge.git
```

---

## Problemas de rede / protocolo

### Erros Paramiko / SSL / cryptography

```bash
# Recriar o ambiente virtual com pacotes atualizados:
pip install --upgrade pip
pip install --upgrade paramiko cryptography
```

### Timeouts SNMP

Lista de verificação:
1. UDP/161 aberto no alvo (não bloqueado por firewall).
2. Community string correta (`public` é o padrão, mas frequentemente alterado).
3. Serviço SNMP habilitado no dispositivo.
4. Versão SNMP correta (v1, v2c, v3).

### Python 3.13+ Erros Telnet

```
ImportError: No module named 'telnetlib'
```

Instale o substituto:
```bash
pip install "firewallxpl[telnet]"
# ou diretamente:
pip install telnetlib3
```

### Scapy / PCAP `ImportError`

```bash
pip install scapy
# Windows: captura ao vivo pode precisar de Npcap (https://npcap.com)
# Leitura offline de .pcap frequentemente funciona sem Npcap
```

---

## Problemas no exploit CVE-2026-0257

### `Could not forge cookies — target may use EC certificates`

Causa: O certificado TLS do alvo usa uma chave EC (curva elíptica) em vez de RSA.
O bypass CVE-2026-0257 requer criptografia RSA-PKCS1v15.

Verifique: execute `fxf-globalprotect-auth-bypass-cve-2026-0257.nse` para inspecionar o tipo de certificado.

### Bypass de autenticação não confirmado após forjar

Possíveis causas:
- Cookies de auth override estão **desabilitados** neste dispositivo (não vulnerável).
- O certificado TLS **não é** o mesmo certificado de assinatura de cookies (configuração segura).
- O dispositivo está **corrigido** (PAN-OS 10.2.18-h6+ / 11.1.15+ / 11.2.12+ / 12.1.7+).

---

## Problemas com AutoPwn

### AutoPwn sobrecarrega o alvo / causa DoS

Use um template de timing menor:
```text
fxf (AutoPwn) > set timing_template paranoid
fxf (AutoPwn) > set threads 2
fxf (AutoPwn) > set module_timeout_s 60
```

---

## Gerenciamento do arquivo de log

```bash
# Truncar
> firewallxpl.log
# Rotacionar manualmente
mv firewallxpl.log firewallxpl.log.bak
```

**Nunca faça commit do `firewallxpl.log`** — pode conter credenciais ou banners sensíveis.

---

[Hub da wiki](../README.md)
