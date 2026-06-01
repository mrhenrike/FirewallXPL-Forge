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
