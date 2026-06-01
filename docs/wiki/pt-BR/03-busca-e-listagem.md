# Busca e listagem

**Idioma:** Português (pt-BR). **English:** [../en-US/03-search-and-listing.md](../en-US/03-search-and-listing.md)

---

## `search` — encontrar módulos

```
search [type=<tipo>] [device=<dispositivo>] [vendor=<vendor>] [language=<lang>] [payload=<payload>] <palavra(s)-chave>
```

Palavras-chave são convertidas para minúsculas. Múltiplas palavras-chave são combinadas com **E** lógico (todas devem aparecer no caminho do módulo).

### Busca por palavra-chave

```
fxf > search cisco
fxf > search fortinet ssl-vpn
fxf > search paloalto globalprotect
fxf > search cve_2026_0257
```

**Saída de exemplo:**
```
fxf > search paloalto
exploits/perimeter/paloalto/globalprotect_auth_bypass_cve_2026_0257
exploits/perimeter/paloalto/globalprotect_cmd_injection_cve_2024_3400
exploits/perimeter/paloalto/panos_auth_bypass_cve_2025_0108
exploits/perimeter/paloalto/panos_mgmt_auth_bypass_cve_2024_0012
exploits/perimeter/paloalto/panos_privesc_cve_2024_9474
exploits/perimeter/paloalto/panos_saml_auth_bypass_cve_2020_2021
```

### Parâmetros de filtro

| Parâmetro | Tipo | Valores válidos | Descrição |
|-----------|------|-----------------|-----------|
| `type=` | `string` | `exploits`, `creds`, `scanners`, `generic`, `payloads`, `encoders` | Tipo de módulo de nível superior |
| `device=` | `string` | `perimeter`, `waf`, `vpn`, `nac`, `lb` | Subpacote em `exploits/` |
| `vendor=` | `string` | `fortinet`, `cisco`, `paloalto`, `sonicwall`, etc. | Segmento de caminho do vendor |
| `language=` | `string` | `python`, `php`, `perl` | Em `encoders/` |
| `payload=` | `string` | `x86`, `x64`, `arm`, `mips`, `cmd`, `python`, `php` | Em `payloads/` |

**Exemplos:**
```
fxf > search type=exploits vendor=fortinet
fxf > search type=exploits device=perimeter cisco rce
fxf > search type=creds generic ssh
fxf > search type=encoders language=php
```

---

## `show` — listar módulos e categorias

```
show <subcomando>
```

### Subcomandos globais (sem módulo necessário)

| Subcomando | Descrição |
|------------|-----------|
| `all` | Todos os módulos indexados |
| `exploits` | Todos os módulos exploit |
| `scanners` | Todos os módulos scanner |
| `creds` | Todos os módulos de credenciais |
| `generic` | Todos os módulos genéricos |
| `encoders` | Todos os módulos de encoder |
| `payloads` | Todos os módulos de payload |
| `wordlists` | Lista de recursos de wordlist disponíveis |
| `perimeter` | Exploits na categoria `perimeter/` |
| `waf` | Exploits na categoria `waf/` |
| `vpn` | Exploits na categoria `vpn/` |
| `nac` | Exploits na categoria `nac/` |
| `lb` | Exploits na categoria `lb/` (balanceadores) |

### Subcomandos de módulo (requerem módulo carregado)

| Subcomando | Descrição |
|------------|-----------|
| `info` | Metadados `__info__`: nome, descrição, autores, referências |
| `options` | Opções padrão com valores atuais e descrições |
| `advanced` | Todas as opções, incluindo avançadas/ocultas |
| `devices` | Lista de dispositivos-alvo |

**Saída de exemplo — `show options` (CVE-2026-0257):**
```
fxf (PAN-OS GlobalProtect Auth Override Cookie Bypass) > show options
Name              Current settings    Description
target            192.168.1.1         IP ou hostname do alvo
port              443                 Porta HTTPS (padrão: 443)
ssl               true                Usar HTTPS
forge_user        admin               Usuário para forjar no cookie de autenticação
forge_domain                          Domínio para o cookie forjado
probe_gateway     true                Também provar o gateway do GlobalProtect
dump_session      false               Exibir metadados de sessão se bypass confirmado
```

---

## Índice completo de módulos

```bash
# Gerar / atualizar o índice
python tools/gen_wiki_module_index.py
```

Saída: [../ANEXO-INDICE-MODULOS.md](../ANEXO-INDICE-MODULOS.md)

---

## Mapeamento de caminho `use`

| Caminho no shell | Módulo Python |
|-----------------|---------------|
| `exploits/perimeter/paloalto/globalprotect_auth_bypass_cve_2026_0257` | `firewallxpl.modules.exploits.perimeter.paloalto.globalprotect_auth_bypass_cve_2026_0257` |
| `creds/generic/ssh_default` | `firewallxpl.modules.creds.generic.ssh_default` |
| `scanners/autopwn` | `firewallxpl.modules.scanners.autopwn` |

Pontos e barras são intercambiáveis na entrada do shell.

---

[Hub da wiki](../README.md)
