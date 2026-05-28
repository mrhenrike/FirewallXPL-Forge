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
