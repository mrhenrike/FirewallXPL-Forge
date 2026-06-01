# Catalogs and `tools/`

**Language:** English (en-US). **pt-BR:** [../pt-BR/10-catalogos-e-ferramentas.md](../pt-BR/10-catalogos-e-ferramentas.md)

---

## `firewallxpl/resources/catalogs/`

| File | Role |
|------|------|
| `cve_extended_catalog.json` | Extended CVE DB: merged static entries, module references, and PoC links |
| `module_target_scope.json` | AutoPwn scope policy — defines allowed device classes and ethical constraints |
| `coverage_devices_2010_2026.json` | Market device pool and yearly coverage lists |
| `market_priority_devices_2010_2026.json` | Market priority weighting for coverage gap analysis |
| `discord_requested_devices.json` | Community-requested devices backlog |
| `external_tool_intel_sources.json` | External intel URLs (Metasploit / Exploit-DB bridges) |
| `external_framework_clones.json` | Curated official clone URLs with license notes |
| `integrated_modules_index.json` | Index of vendored PoC mirrors under `arsenal/pocs/integrated_modules/` |
| `arsenal_index.json` | Arsenal catalog index |
| `arsenal_layout.json` | Arsenal directory layout |
| `deep_intel_backlog.json` | Intel backlog items for future module development |

### NSE arsenal

```
firewallxpl/resources/arsenal/nse/
├── fxf-firewall-fingerprint.nse
├── fxf-globalprotect-detect.nse
├── fxf-globalprotect-auth-bypass-cve-2026-0257.nse
├── fxf-fortios-detect.nse
└── fxf-cisco-asa-detect.nse
```

Install via: `fxf > install-nse` — see [12-nse-scripts.md](12-nse-scripts.md).

---

## Architecture diagrams

Device-class attack-surface PNGs and Mermaid sources in:

```
docs/diagrams/architecture/
docs/img/architecture/
```

Reference: [../../diagrams/architecture/README.md](../../diagrams/architecture/README.md)

---

## Generated documentation

| File | Regenerate with |
|------|-----------------|
| `docs/COVERAGE_MATRIX.md` | `python tools/generate_coverage_matrix.py` |
| `docs/FULL_CATALOG.md` | `python tools/generate_full_catalog.py` |
| `docs/wiki/ANEXO-INDICE-MODULOS.md` | `python tools/gen_wiki_module_index.py` |

---

## `tools/` — maintenance scripts

| Script | Role |
|--------|------|
| `env_doctor.py` | Dependency smoke test (core imports) |
| `check_env_readiness.py` | Full environment readiness check (modules, resources) |
| `compile_modules.py` | `compileall` for core, modules, libs |
| `validate_coverage_minimums.py` | Market catalog minimum coverage validation |
| `validate_arsenal.py` | Validate arsenal JSON structure |
| `validate_governance.py` | Check for required governance files (LICENSE, CONTRIBUTING, etc.) |
| `validate_honeypot_traps.py` | Honeypot campaign validation |
| `refresh_cve_catalog.py` | Regenerate `cve_extended_catalog.json` |
| `ingest_cve_pocs.py` | Ingest CVE PoC content |
| `ingest_cve_poc_links.py` | Ingest CVE PoC links |
| `merge_oui.py` | Merge OUI databases (IEEE + Wireshark + Nmap) |
| `sync_wordlists.py` | Sync wordlist resources |
| `sync_mibs.py` | Sync SNMP MIB files |
| `sync_intel_sources.py` | External intel snapshot |
| `generate_full_catalog.py` | Regenerate FULL_CATALOG docs |
| `generate_coverage_matrix.py` | Regenerate COVERAGE_MATRIX docs |
| `build_catalog_index.py` | Build catalog index |
| `build_arsenal_index.py` | Build arsenal index |
| `build_attack_matrix.py` | Build ATT&CK coverage matrix |
| `gen_wiki_module_index.py` | Regenerate wiki module index annex |
| `coverage_check_modern.py` | Modern coverage check with market weights |
| `report_coverage_gaps.py` | Output coverage gap CSV |
| `intel_matrix.py` | Intelligence matrix report |
| `intel_backlog.py` | Intelligence backlog management |
| `triage_reconcile.py` | Module triage reconciliation |

---

## CVE refresh workflow

```bash
# Refresh the extended CVE catalog
python tools/refresh_cve_catalog.py

# Ingest new PoC links
python tools/ingest_cve_poc_links.py

# Regenerate coverage matrix
python tools/generate_coverage_matrix.py

# Regenerate module index
python tools/gen_wiki_module_index.py
```

---

[Wiki hub](../README.md)
