# Scripts NSE — Integração Nmap do FirewallXPL-Forge

**Idioma:** Português (pt-BR). **English:** [../en-US/12-nse-scripts.md](../en-US/12-nse-scripts.md)

O FirewallXPL-Forge inclui uma suíte de scripts NSE (Nmap Scripting Engine) para
detecção de firewalls, fingerprinting e verificação prévia de CVEs. Os scripts estão
embutidos no pacote Python e são instalados na pasta de scripts do nmap via o comando
`install-nse`.

---

## Requisitos

| Requisito | Detalhes |
|-----------|---------|
| **nmap** | Qualquer versão com suporte a NSE (≥ 5.00 recomendado; ≥ 7.90 para lib `sslcert`) |
| **firewallxpl** | Instalado via `pip install firewallxpl` ou clone editable |
| **Permissões** | Acesso de escrita na pasta de scripts do nmap (pode exigir `sudo` / `RunAs`) |

---

## Instalação

### Via shell interativo

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
[+] Todos os scripts instalados. Use-os com:
     nmap --script fxf-globalprotect-detect <alvo>
     nmap --script fxf-firewall-fingerprint -p 443,80 <alvo>
```

### Via CLI não-interativo

```bash
python fxf.py -c "install-nse"
python fxf.py -c "install-nse --force"
python fxf.py -c "install-nse --path /usr/local/share/nmap/scripts"
python fxf.py -c "install-nse --check"
```

### Quando nmap não está instalado

```
fxf > install-nse
[-] nmap não encontrado no PATH. Instale o nmap primeiro:
     Linux/Debian:  sudo apt-get install nmap
     Linux/RHEL:    sudo yum install nmap
     macOS:         brew install nmap
     Windows:       https://nmap.org/download.html
[*] Scripts embutidos disponíveis em:
     /caminho/para/firewallxpl/resources/arsenal/nse/
     Copie os arquivos .nse manualmente para a pasta de scripts do nmap quando estiver pronto.
```

### Erro de permissão (Linux/macOS)

```bash
# Execute com sudo para escrever em /usr/share/nmap/scripts
sudo python fxf.py -c "install-nse"
# Ou instale em um diretório com permissão de escrita
python fxf.py -c "install-nse --path ~/.nmap/scripts"
```

---

## Referência do comando `install-nse`

```
install-nse [OPÇÕES]
```

| Flag | Tipo | Padrão | Descrição |
|------|------|--------|-----------|
| *(sem flag)* | — | — | Detecta nmap automaticamente e instala todos os scripts |
| `--check` | flag | false | Simulação: exibe o que seria instalado sem copiar nada |
| `--force` | flag | false | Sobrescreve scripts que já existem no diretório de destino |
| `--path <dir>` | `string` (caminho) | detectado automaticamente | Diretório de destino personalizado para os scripts NSE |
| `--list` | flag | false | Lista os scripts embutidos e encerra, sem instalar |

### Exemplos

```
fxf > install-nse
fxf > install-nse --check
fxf > install-nse --force
fxf > install-nse --path /opt/nmap/scripts
fxf > install-nse --list
```

**Saída de exemplo — `--list`:**
```
fxf > install-nse --list
[*] Scripts NSE embutidos (5 no total):
  fxf-cisco-asa-detect.nse
  fxf-firewall-fingerprint.nse
  fxf-fortios-detect.nse
  fxf-globalprotect-auth-bypass-cve-2026-0257.nse
  fxf-globalprotect-detect.nse
```

**Saída de exemplo — `--check` (simulação):**
```
fxf > install-nse --check
[+] nmap encontrado: /usr/bin/nmap (7.95)
[*] Diretório de scripts NSE: /usr/share/nmap/scripts
[*] Scripts NSE embutidos: 5
[*] Simulação — nenhum arquivo será copiado.
     Instalaria: fxf-globalprotect-detect.nse
     Instalaria: fxf-globalprotect-auth-bypass-cve-2026-0257.nse
     Instalaria: fxf-fortios-detect.nse
     Instalaria: fxf-cisco-asa-detect.nse
     Instalaria: fxf-firewall-fingerprint.nse
```

---

## Scripts NSE embutidos

### `fxf-firewall-fingerprint.nse`

Fingerprinting genérico de firewall/NGFW em 11 vendors.

**Vendors suportados:** Palo Alto, Fortinet, Cisco ASA/FTD, SonicWall, Sophos,
Check Point, Juniper, Zyxel, pfSense, WatchGuard, Barracuda.

**Parâmetros:**

| Argumento NSE | Tipo | Padrão | Descrição |
|---------------|------|--------|-----------|
| `fxf.timeout` | `integer` (segundos) | `10` | Timeout HTTP por probe |
| `fxf.verbose` | `"0"` ou `"1"` | `"0"` | Exibe detalhes adicionais de pontuação |

**Uso:**
```bash
nmap -p 443,80,8443 --script fxf-firewall-fingerprint <alvo>
nmap -p 443 --script fxf-firewall-fingerprint \
    --script-args "fxf.timeout=15,fxf.verbose=1" <alvo>
```

**Saída de exemplo:**
```
PORT    STATE SERVICE
443/tcp open  https
| fxf-firewall-fingerprint:
|   Vendor: SonicWall
|   Product: SonicOS
|   Confidence: HIGH (3 padrão(s) correspondido(s))
|   Match path: /auth.html
|
|   CVEs notáveis:
|     CVE-2021-20034 (path traversal, CVSS 9.8)
|     CVE-2024-40766 (controle de acesso SSL-VPN, CVSS 9.3)
|     CVE-2024-53704 (bypass de autenticação)
|
|   Módulos fxf: exploits/perimeter/sonicwall/
|_    fxf> search sonicwall
```

---

### `fxf-globalprotect-detect.nse`

Detecta portal e/ou gateway Palo Alto Networks GlobalProtect.

**Parâmetros:**

| Argumento NSE | Tipo | Padrão | Descrição |
|---------------|------|--------|-----------|
| `fxf.timeout` | `integer` (segundos) | `10` | Timeout HTTP por probe |

**Uso:**
```bash
nmap -p 443 --script fxf-globalprotect-detect <alvo>
nmap -p 443,8443 --script fxf-globalprotect-detect \
    --script-args "fxf.timeout=15" 10.0.0.0/24
```

**Saída de exemplo (detectado):**
```
PORT    STATE SERVICE
443/tcp open  https
| fxf-globalprotect-detect:
|   GlobalProtect: DETECTADO
|   Componente: portal, gateway
|   Versão PAN-OS: não divulgada na resposta de pré-login
|   Auth-override: referenciado na resposta — verificar exposição CVE-2026-0257
|_    Execute: nmap --script fxf-globalprotect-auth-bypass-cve-2026-0257 10.0.0.1
```

---

### `fxf-globalprotect-auth-bypass-cve-2026-0257.nse`

Verificação passiva de exposição à CVE-2026-0257 em alvos PAN-OS GlobalProtect.

> **Nota:** Este script realiza apenas uma verificação **passiva** (confirma presença do
> GlobalProtect e obtém metadados do certificado TLS). **Não forja nem envia cookies.**
> Para exploração E2E ativa, use o módulo Python:
> `use exploits/perimeter/paloalto/globalprotect_auth_bypass_cve_2026_0257`

**Parâmetros:**

| Argumento NSE | Tipo | Padrão | Descrição |
|---------------|------|--------|-----------|
| `fxf.timeout` | `integer` (segundos) | `10` | Timeout HTTP por probe |

**Uso:**
```bash
nmap -p 443 --script fxf-globalprotect-auth-bypass-cve-2026-0257 <alvo>
```

**Saída de exemplo:**
```
PORT    STATE SERVICE
443/tcp open  https
| fxf-globalprotect-auth-bypass-cve-2026-0257:
|   CVE-2026-0257 -- GlobalProtect Auth Override Cookie Bypass
|   CVSS: 7.8 HIGH (CVSS 4.0) | CISA KEV: 2026-05-29 | Exploração ativa confirmada
|   GlobalProtect: DETECTADO (portal + gateway)
|   Certificado TLS CN: vpn.corp.exemplo.com.br (RSA 2048-bit)
|   Certificado exposto publicamente via handshake TLS
|
|   Status: POTENCIALMENTE VULNERÁVEL
|   Condição: vulnerável SE cookies de auth override estiverem habilitados
|     E este certificado TLS for usado para criptografia de cookies (padrão comum)
|
|   Bypass ativo (E2E):
|     fxf> use exploits/perimeter/paloalto/globalprotect_auth_bypass_cve_2026_0257
|     fxf> set target 10.0.0.1
|     fxf> run
|
|   Remediação:
|     Patch: PAN-OS 10.2.18-h6+ / 11.1.15+ / 11.2.12+ / 12.1.7+
|     Ou: use um certificado DEDICADO para cookies de auth override
|     Ou: desabilite os cookies de auth override
|_  Advisory: https://security.paloaltonetworks.com/CVE-2026-0257
```

---

### `fxf-fortios-detect.nse`

Detecta portal SSL-VPN do FortiOS e interface de gerenciamento do FortiGate.

**Parâmetros:**

| Argumento NSE | Tipo | Padrão | Descrição |
|---------------|------|--------|-----------|
| `fxf.timeout` | `integer` (segundos) | `10` | Timeout HTTP por probe |

**Uso:**
```bash
nmap -p 443,10443,8443 --script fxf-fortios-detect <alvo>
nmap -p 443 --script fxf-fortios-detect 192.168.1.0/24
```

**Saída de exemplo:**
```
PORT    STATE SERVICE
443/tcp open  https
| fxf-fortios-detect:
|   FortiOS: DETECTADO
|   Componente: portal SSL-VPN, Interface de gerenciamento
|   Server header: FortiHTTP
|
|   CVEs notáveis (use fxf para explorar):
|     CVE-2018-13379 (path traversal, CVSS 9.8)
|     CVE-2022-40684 (bypass de autenticação, CVSS 9.8)
|     CVE-2023-27997 (heap RCE SSL-VPN, CVSS 9.8)
|     CVE-2024-21762 (OOB write RCE SSL-VPN, CVSS 9.6)
|     CVE-2024-55591 (bypass via WebSocket, CVSS 9.8)
|
|   Módulos fxf: exploits/perimeter/fortinet/
|_    fxf> search vendor=fortinet
```

---

### `fxf-cisco-asa-detect.nse`

Detecta firewalls Cisco ASA e FTD (Firepower Threat Defense).

**Parâmetros:**

| Argumento NSE | Tipo | Padrão | Descrição |
|---------------|------|--------|-----------|
| `fxf.timeout` | `integer` (segundos) | `10` | Timeout HTTP por probe |

**Uso:**
```bash
nmap -p 443,8443 --script fxf-cisco-asa-detect <alvo>
nmap -p 443 --script fxf-cisco-asa-detect 10.0.0.0/24
```

**Saída de exemplo:**
```
PORT    STATE SERVICE
443/tcp open  https
| fxf-cisco-asa-detect:
|   Cisco ASA/FTD: DETECTADO
|   Componente: Clientless SSL-VPN, WebVPN
|
|   CVEs notáveis (use fxf para explorar):
|     CVE-2020-3452 (path traversal, CVSS 7.5)
|     CVE-2023-20269 (brute-force VPN, CVSS 9.1)
|     CVE-2023-20198 (privesc WebUI IOS XE, CVSS 10.0)
|     CVE-2025-20362+20333 (cadeia FIRESTARTER RCE)
|
|   Módulos fxf: exploits/perimeter/cisco/
|_    fxf> search vendor=cisco
```

---

## Executando múltiplos scripts fxf juntos

```bash
# Varredura completa: fingerprint + verificação GlobalProtect
nmap -p 443,80,8443 \
    --script "fxf-firewall-fingerprint,fxf-globalprotect-detect,fxf-globalprotect-auth-bypass-cve-2026-0257" \
    --script-args "fxf.timeout=15" \
    <faixa-de-alvos>

# Varredura de perímetro com NSE + detecção de versão
nmap -sV -p 443 \
    --script "fxf-firewall-fingerprint,fxf-globalprotect-detect,fxf-fortios-detect,fxf-cisco-asa-detect" \
    192.168.0.0/24
```

---

## Instalação manual (sem `install-nse`)

Se o nmap não estiver no PATH ou você quiser copiar os arquivos manualmente:

```bash
# Linux / macOS
cp /caminho/para/firewallxpl/resources/arsenal/nse/*.nse /usr/share/nmap/scripts/
nmap --script-updatedb

# Windows (PowerShell)
Copy-Item "C:\...\firewallxpl\resources\arsenal\nse\*.nse" `
    "C:\Program Files (x86)\Nmap\scripts\"
nmap --script-updatedb
```

---

## Localização dos scripts embutidos no pacote

```
firewallxpl/resources/arsenal/nse/
├── fxf-firewall-fingerprint.nse
├── fxf-globalprotect-detect.nse
├── fxf-globalprotect-auth-bypass-cve-2026-0257.nse
├── fxf-fortios-detect.nse
└── fxf-cisco-asa-detect.nse
```

---

[Hub da wiki](../README.md)
