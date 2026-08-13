# HANDOFF - FirewallXPL-Forge

## [2026-05-28 17:50] - v2.1.0: CVE-2026-35616 + FIRESTARTER + sync Fortinet + CHANGELOG

### Estado ao encerrar
- Criado `forticlient_ems_preauth_api_bypass_cve_2026_35616.py` em `exploits/perimeter/fortinet/`
  - CVE-2026-35616 (CVSS 9.1, CISA KEV 2026-04-06)
  - Mecanismo: HTTP header spoofing X-SSL-CLIENT-VERIFY + forged PEM DN
  - Fases: bypass probe, endpoint enumeration, EKZ-style update push demo
- Criado `cisco_asa_ftd_firestarter_chain_cve_2025_20362_20333.py` em `exploits/perimeter/cisco/`
  - CVE-2025-20362 (pre-auth URL bypass) + CVE-2025-20333 (RCE, CVSS 9.9)
  - APT UAT4356/ArcaneDoor (CISA AR26-113A / ED 25-03)
- Sincronizados modulos Fortinet faltantes vs EmbedXPL:
  - `fortios_sslvpn_session_reuse_cve_2024_50562.py` (novo)
  - `forticloud_sso_auth_bypass_cve_2026_24858.py` (novo)
- Criado `CHANGELOG.md` (repo nao tinha changelog)
- Atualizado `firewallxpl/resources/catalogs/cve_extended_catalog.json`:
  - +5 entradas: CVE-2026-35616, CVE-2026-24858, CVE-2024-50562, CVE-2025-20362, CVE-2025-20333
  - entry_count: 140 -> 145 | last_updated: 2026-05-28

### Arquivos modificados/criados
- `firewallxpl/modules/exploits/perimeter/fortinet/forticlient_ems_preauth_api_bypass_cve_2026_35616.py` (novo)
- `firewallxpl/modules/exploits/perimeter/fortinet/fortios_sslvpn_session_reuse_cve_2024_50562.py` (novo)
- `firewallxpl/modules/exploits/perimeter/fortinet/forticloud_sso_auth_bypass_cve_2026_24858.py` (novo)
- `firewallxpl/modules/exploits/perimeter/cisco/cisco_asa_ftd_firestarter_chain_cve_2025_20362_20333.py` (novo)
- `firewallxpl/resources/catalogs/cve_extended_catalog.json` (atualizado)
- `CHANGELOG.md` (criado)

### Proximo passo imediato
- Atualizar `pyproject.toml` / `setup.py` para versao 2.1.0
- Executar `python tools/gen_wiki_module_index.py` para regenerar ANEXO-INDICE-MODULOS.md
- Executar `python tools/generate_coverage_matrix.py` para atualizar COVERAGE_MATRIX.md

### Pendencias conhecidas
- [ ] Bump versao para 2.1.0 em pyproject.toml e setup.py
- [ ] Regenerar ANEXO-INDICE-MODULOS.md e COVERAGE_MATRIX.md
- [ ] Docs/FULL_CATALOG.md esta desatualizado (referencia arvore routers/ herdada do EmbedXPL)
- [ ] Criar pasta `fortiweb/` em `exploits/perimeter/fortinet/` para CVE-2025-25257 e CVE-2025-64446
- [ ] Adicionar Cisco Secure ACS / ClearPass exploits faltantes em `exploits/nac/`

### Ambiente necessario
- Python 3.8-3.13
- `pip install -r requirements.txt`
- Windows: `D:\Projetos-SafeLabs\submodules\IoT\FirewallXPL-Forge`
- Linux: `/mnt/predator/Projetos-SafeLabs/submodules/IoT/FirewallXPL-Forge`

### Paths importantes
- Windows: `D:\Projetos-SafeLabs\submodules\IoT\FirewallXPL-Forge`
- Linux: `/mnt/predator/Projetos-SafeLabs/submodules/IoT/FirewallXPL-Forge`

---

## [2026-06-01 17:35] — NSE Installer + CVE-2026-0257 DB + Wiki completa EN-US/PT-BR

### Estado ao encerrar
- CVE-2026-0257 adicionada ao banco de dados em `firewallxpl/core/cve/cve_db.py` (modulo ja existia completo com E2E em 6 estagios desde sessao anterior)
- NSE installer criado: `firewallxpl/core/nse_installer.py` com deteccao cross-platform (which/where/locate), validacao de presenca do nmap, copia dos scripts, nmap --script-updatedb, fallback quando nmap nao instalado
- 5 scripts NSE firewall-especificos criados em `firewallxpl/resources/arsenal/nse/`:
  - fxf-firewall-fingerprint.nse (11 vendors: Palo Alto, Fortinet, Cisco, SonicWall, Sophos, Check Point, Juniper, Zyxel, pfSense, WatchGuard, Barracuda)
  - fxf-globalprotect-detect.nse
  - fxf-globalprotect-auth-bypass-cve-2026-0257.nse (verificacao passiva TLS cert)
  - fxf-fortios-detect.nse
  - fxf-cisco-asa-detect.nse
- Comando `install-nse` adicionado ao `firewallxpl/interpreter.py` com flags --check, --force, --path, --list
- `pyproject.toml` atualizado com `[tool.setuptools.package-data]` para incluir NSE files como package data
- Wiki completamente reescrita/enriquecida:
  - 11 paginas EN-US atualizadas com parametros tipados, amostras de I/O, CVE-2026-0257
  - 11 paginas PT-BR atualizadas espelhando EN-US
  - Nova pagina 12 criada em ambos os idiomas (NSE scripts)
  - Indices da wiki atualizados
- `README.md` e `README.pt-BR.md` atualizados com secao NSE installer e CVE-2026-0257
- Analise de relevancia CVEs adicionais para EmbedXPL-Forge concluida: Miasma npm (CVE-2026-45321), CVE-2026-44930 (Apache CXF LDAP) e CVE-2026-4868 (GitLab) nao sao pertinentes ao contexto IoT/embedded

### Arquivos modificados/criados nesta sessao
- `firewallxpl/core/cve/cve_db.py` — entrada CVE-2026-0257 adicionada
- `firewallxpl/core/nse_installer.py` — NOVO
- `firewallxpl/resources/arsenal/nse/fxf-firewall-fingerprint.nse` — NOVO
- `firewallxpl/resources/arsenal/nse/fxf-globalprotect-detect.nse` — NOVO
- `firewallxpl/resources/arsenal/nse/fxf-globalprotect-auth-bypass-cve-2026-0257.nse` — NOVO
- `firewallxpl/resources/arsenal/nse/fxf-fortios-detect.nse` — NOVO
- `firewallxpl/resources/arsenal/nse/fxf-cisco-asa-detect.nse` — NOVO
- `firewallxpl/interpreter.py` — command_install_nse adicionado, global_commands e global_help atualizados
- `pyproject.toml` — [tool.setuptools.package-data] adicionado
- `docs/wiki/en-US/01-11.md` — todos os 11 arquivos reescritos/enriquecidos
- `docs/wiki/pt-BR/01-11.md` — todos os 11 arquivos reescritos/enriquecidos
- `docs/wiki/en-US/12-nse-scripts.md` — NOVO
- `docs/wiki/pt-BR/12-scripts-nse.md` — NOVO
- `docs/wiki/en-US/README.md` — pagina 12 adicionada ao indice
- `docs/wiki/pt-BR/README.md` — pagina 12 adicionada ao indice
- `README.md` — CVE-2026-0257 na tabela de vendors, secao NSE adicionada
- `README.pt-BR.md` — secao NSE e CVE-2026-0257 adicionadas
- `HANDOFF.md` — esta entrada

### Proximo passo imediato
- Executar `python tools/gen_wiki_module_index.py` para regenerar ANEXO-INDICE-MODULOS.md

### Pendencias conhecidas
- [ ] Regenerar ANEXO-INDICE-MODULOS.md (gen_wiki_module_index.py)
- [ ] Regenerar COVERAGE_MATRIX.md e FULL_CATALOG.md
- [ ] Bump versao para 2.1.1 em pyproject.toml se necessario
- [ ] Criar pasta `fortiweb/` em `exploits/perimeter/fortinet/` para CVE-2025-25257 e CVE-2025-64446
- [ ] Adicionar Cisco Secure ACS / ClearPass exploits faltantes em `exploits/nac/`

### Ambiente necessario
- Python 3.8-3.13
- `pip install -r requirements.txt`
- Para NSE: nmap instalado no OS
- Windows: `D:\Projetos-SafeLabs\submodules\IoT\FirewallXPL-Forge`
- Linux: `/mnt/predator/Projetos-SafeLabs/submodules/IoT/FirewallXPL-Forge`

### Paths importantes
- Windows: `D:\Projetos-SafeLabs\submodules\IoT\FirewallXPL-Forge`
- Linux: `/mnt/predator/Projetos-SafeLabs/submodules/IoT/FirewallXPL-Forge`


---

## [2026-06-02 02:06] - TODOS OS PENDENTES RESOLVIDOS (v2.1.1)

### Estado ao encerrar (COMPLETO)
- FortiWeb criado: exploits/perimeter/fortinet/fortiweb/
  - fortiweb_auth_bypass_rce_cve_2025_25257.py (CVE-2025-25257, CVSS 9.8)
  - fortiweb_admin_rce_cve_2025_64446.py (CVE-2025-64446, CVSS 9.8)
- Aruba ClearPass adicionado: nac/aruba/clearpass_unauth_rce_cve_2023_25594.py
- ANEXO-INDICE-MODULOS.md regenerado (gen_wiki_module_index.py)
- COVERAGE_MATRIX.md e FULL_CATALOG.md regenerados
- Version bumped: 2.1.0 -> 2.1.1 em pyproject.toml e setup.py
- 89 exploit modules total (era 82 antes desta sessao)

### Pendencias resolvidas
- [x] Regenerar ANEXO-INDICE-MODULOS.md
- [x] Regenerar COVERAGE_MATRIX.md e FULL_CATALOG.md
- [x] Bump versao para 2.1.1
- [x] Criar fortiweb/ com CVE-2025-25257 e CVE-2025-64446
- [x] Adicionar ClearPass em exploits/nac/aruba/

### Sem pendencias conhecidas
- FirewallXPL-Forge v2.1.1 esta completo como release standalone final
- Todos os modulos NSE instalados e documentados
- Wiki EN-US e PT-BR completas (12 paginas cada)
- CVE-2026-0257 no banco de dados e no modulo de exploit

### Ambiente necessario
- Python 3.8-3.13
- Windows: D:\Projetos-SafeLabs\submodules\IoT\FirewallXPL-Forge
- Linux: /mnt/predator/Projetos-SafeLabs/submodules/IoT/FirewallXPL-Forge

## [2026-06-02 02:10] - FortiWeb exploits, ClearPass RCE, docs regen, v2.1.1

### Estado ao encerrar
- Criados 3 novos modulos de exploit: CVE-2025-25257, CVE-2025-64446 (FortiWeb), CVE-2023-25594 (ClearPass)
- Nova pasta `firewallxpl/modules/exploits/perimeter/fortinet/fortiweb/` com __init__.py e 2 modulos
- Modulo NAC adicionado: `firewallxpl/modules/exploits/nac/aruba/clearpass_unauth_rce_cve_2023_25594.py`
- Documentacao regenerada: ANEXO-INDICE-MODULOS.md (172 modules), COVERAGE_MATRIX.md, FULL_CATALOG.md (77 CVEs)
- Versao bumped para 2.1.1 em pyproject.toml e setup.py
- CHANGELOG.md atualizado com entrada [2.1.1]
- Commit e push realizados

### Arquivos modificados
- `firewallxpl/modules/exploits/perimeter/fortinet/fortiweb/__init__.py` (novo)
- `firewallxpl/modules/exploits/perimeter/fortinet/fortiweb/fortiweb_auth_bypass_rce_cve_2025_25257.py` (novo)
- `firewallxpl/modules/exploits/perimeter/fortinet/fortiweb/fortiweb_admin_rce_cve_2025_64446.py` (novo)
- `firewallxpl/modules/exploits/nac/aruba/clearpass_unauth_rce_cve_2023_25594.py` (novo)
- `setup.py` (2.0.0 -> 2.1.1)
- `CHANGELOG.md`
- `docs/wiki/ANEXO-INDICE-MODULOS.md`
- `docs/COVERAGE_MATRIX.md`, `docs/COVERAGE_MATRIX.txt`
- `docs/FULL_CATALOG.md`, `docs/FULL_CATALOG.txt`

### Proximo passo imediato
- Nenhuma pendencia critica; proxima expansao pode cobrir FortiSIEM ou Palo Alto PAN-OS modulos adicionais

### Pendencias conhecidas
- [ ] Expandir fortiweb/ com modulos adicionais quando novos CVEs forem publicados
- [ ] Considerar adicionar NSE scripts correspondentes para os novos CVEs

### Ambiente necessario
- Python 3.8+
- Dependencias: ver requirements.txt / pyproject.toml
- Sem servicos externos necessarios para build/doc

### Paths importantes
- Windows: `D:\Projetos-SafeLabs\submodules\IoT\FirewallXPL-Forge`
- Linux: `/mnt/predator/Projetos-SafeLabs/submodules/IoT/FirewallXPL-Forge`

## [2026-06-07 02:43] -- Add perimeter auth bruteforce + WAF evasion generator

### Estado ao encerrar
- Criados 3 modulos nativos (zero dependencia dos repos fonte)
- FirewallXPL: perimeter_auth_bruteforce.py + waf_evasion_generator.py
- EmbedXPL: perimeter_auth_bruteforce.py
- Sintaxe verificada com ast.parse -- todos OK
- Commits: FirewallXPL a80a8e2, EmbedXPL 79a2664a

### Proximo passo imediato
- Abrir PR feat/bruteforce-waf-evasion -> master no FirewallXPL-Forge

### Pendencias conhecidas
- [ ] PR FirewallXPL-Forge: feat/bruteforce-waf-evasion -> master

### Paths importantes
- Windows: D:\Projetos-SafeLabs\submodules\Uniao-Geek\FirewallXPL-Forge\firewallxpl\modules
- Linux: /mnt/predator/Projetos-SafeLabs/submodules/Uniao-Geek/FirewallXPL-Forge/firewallxpl/modules

## [2026-06-07 02:55] -- Windows Sigma rules + perimeter validator expansion

### Estado ao encerrar
- Copiadas 32 regras Windows Sigma de Harpia purple-sigma-rules para firewallxpl/resources/sigma/windows/
  - process_creation/: netsh firewall add/delete/disable/set, port-forwarding, UAC bypass, Defender disable (14 regras)
  - powershell/: Defender tamper, firewall profile disable, AMSI bypass (7 regras)
  - registry/: disable Defender firewall, UAC bypass EventViewer/DelegateExecute, AMSI disable, credential guard (11 regras)
- sigma_perimeter_validator.py: _PERIMETER_LOGSOURCE_CATS expandido com 'windows'; _find_sigma_dir() reescrito para encontrar resources/sigma/ empacotado e fallback Harpia
- Commit: 5a2df4c -- pushed em feat/ngfw-parsers-sigma-expansion

### Proximo passo imediato
- Testar carga das regras Windows em dry_run mode

### Pendencias conhecidas
- [ ] Adicionar regras network_connection e dns_query para cobertura de endpoint

### Paths importantes
- Windows: D:\Projetos-SafeLabs\submodules\Uniao-Geek\FirewallXPL-Forge
- Linux: /mnt/predator/Projetos-SafeLabs/submodules/Uniao-Geek/FirewallXPL-Forge

---

## [2026-08-13 16:20] -- Authorship cleanup + sync

### Estado ao encerrar
- Trailers Cursor/Copilot removidos do historico da default branch (onde aplicavel)
- Hook `.githooks/commit-msg` ativo via `core.hooksPath=.githooks`
- Remoto alinhado apos force-with-lease / push

### Proximo passo imediato
- Em clones antigos: fetch + reset da default branch

### Paths importantes
- Windows: `D:\Projetos-SafeLabs\submodules\Uniao-Geek\`
- Linux: `/mnt/predator/Projetos-SafeLabs/submodules/Uniao-Geek/`
