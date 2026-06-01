# Scanners e AutoPwn

**Idioma:** Português (pt-BR). **English:** [../en-US/07-scanners-and-autopwn.md](../en-US/07-scanners-and-autopwn.md)

Módulos scanner orquestram campanhas multi-módulo contra um único alvo ou sub-rede.
`scanners/autopwn` é o principal ponto de entrada para testes automatizados de perímetro.

---

## `scanners/autopwn`

Varredura paralela de credenciais e exploits com **templates de timing estilo Nmap** (T0–T5).

### Uso

```text
fxf > use scanners/autopwn
fxf (AutoPwn) > set target 192.168.50.1
fxf (AutoPwn) > set timing_template polite
fxf (AutoPwn) > set target_device_class ngfw
fxf (AutoPwn) > run
```

### Opções principais

| Opção | Tipo | Padrão | Descrição |
|-------|------|--------|-----------|
| `target` | `OptIP` / `string` | `""` | IP alvo ou sub-rede (CIDR) |
| `target_device_class` | `OptString` | `"multi"` | Filtro de classe de dispositivo: `multi`, `router`, `switch`, `tap`, `fw`, `ngfw`, `isp_cpe` |
| `vendor` | `OptString` | `""` | Filtro de nome do vendor (ex.: `fortinet`, `cisco`) |
| `timing_template` | `OptString` | `"normal"` | `t0`–`t5` ou `paranoid`, `sneaky`, `polite`, `normal`, `aggressive`, `insane` |
| `check_exploits` | `OptBool` | `true` | Executar métodos `check()` dos exploits |
| `check_creds` | `OptBool` | `true` | Executar módulos de credenciais |
| `threads` | `OptInteger` | `8` | Threads de módulo concorrentes |
| `module_timeout_s` | `OptInteger` | `30` | Timeout por módulo em segundos |
| `verify_positive_twice` | `OptBool` | `false` | Re-verificar resultados positivos |

### Referência de templates de timing

| Template | Alias | Velocidade | Furtividade | Caso de uso |
|----------|-------|------------|-------------|------------|
| `t0` | `paranoid` | Mais lento | Máxima | Evasão de IDS, alta sensibilidade de detecção |
| `t1` | `sneaky` | Lento | Alta | Ambientes de baixa detecção |
| `t2` | `polite` | Moderado | Moderada | Auditorias autorizadas padrão |
| `t3` | `normal` | Padrão | Moderada | Uso geral |
| `t4` | `aggressive` | Rápido | Baixa | Redes robustas, laboratório |
| `t5` | `insane` | Mais rápido | Nenhuma | Somente laboratório |

### Opções específicas de protocolo

| Opção | Tipo | Descrição |
|-------|------|-----------|
| `http_use` | `OptBool` | Habilitar verificações HTTP |
| `https_use` | `OptBool` | Habilitar verificações HTTPS |
| `ssh_use` | `OptBool` | Habilitar verificações SSH |
| `ftp_use` | `OptBool` | Habilitar verificações FTP |
| `telnet_use` | `OptBool` | Habilitar verificações Telnet |
| `snmp_use` | `OptBool` | Habilitar verificações SNMP |

---

### Advisor ML opcional (`show advanced`)

**Desabilitado por padrão.** Reordena a fila de módulos e pode sugerir ou aplicar automaticamente um template de timing usando um modelo linear leve.

| Opção | Tipo | Padrão | Descrição |
|-------|------|--------|-----------|
| `ml_advisor` | `OptBool` | `false` | Habilitar advisor ML |
| `ml_auto_timing` | `OptBool` | `false` | Aplicar automaticamente a sugestão de timing |
| `ml_use_gpu` | `OptBool` | `false` | Usar GPU para logits (requer `pip install .[ml-gpu]`) |

---

## Scripts NSE para pré-varredura

Antes de executar o AutoPwn, use os scripts NSE embutidos para fingerprinting leve:

```bash
# Identificar vendor do firewall
nmap -p 443,80,8443 --script fxf-firewall-fingerprint 192.168.0.0/24

# Verificar exposição CVE-2026-0257 no GlobalProtect
nmap -p 443 --script fxf-globalprotect-auth-bypass-cve-2026-0257 10.0.0.1
```

Em seguida, execute o módulo fxf correspondente nos alvos confirmados.
Veja [12-scripts-nse.md](12-scripts-nse.md) para a referência completa de NSE.

---

[Hub da wiki](../README.md)
