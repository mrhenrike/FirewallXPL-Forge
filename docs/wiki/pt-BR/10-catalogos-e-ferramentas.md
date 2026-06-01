# Catálogos e `tools/`

**Idioma:** Português (pt-BR). **English:** [../en-US/10-catalogs-and-tools.md](../en-US/10-catalogs-and-tools.md)

---

## `firewallxpl/resources/catalogs/`

| Arquivo | Função |
|---------|--------|
| `cve_extended_catalog.json` | BD CVE estendido: entradas estáticas mescladas, referências de módulos e links PoC |
| `module_target_scope.json` | Política de escopo do AutoPwn — define classes de dispositivos permitidas e restrições éticas |
| `coverage_devices_2010_2026.json` | Pool de dispositivos de mercado e listas anuais de cobertura |
| `market_priority_devices_2010_2026.json` | Ponderação de prioridade de mercado para análise de lacunas de cobertura |
| `discord_requested_devices.json` | Backlog de dispositivos solicitados pela comunidade |
| `external_tool_intel_sources.json` | URLs de intel externas (bridges Metasploit / Exploit-DB) |
| `external_framework_clones.json` | URLs de clones oficiais curados com notas de licença |
| `integrated_modules_index.json` | Índice de espelhos PoC vendorizados em `arsenal/pocs/integrated_modules/` |
| `arsenal_index.json` | Índice do catálogo arsenal |
| `deep_intel_backlog.json` | Itens de backlog de inteligência para desenvolvimento futuro de módulos |

### Arsenal NSE

```
firewallxpl/resources/arsenal/nse/
├── fxf-firewall-fingerprint.nse
├── fxf-globalprotect-detect.nse
├── fxf-globalprotect-auth-bypass-cve-2026-0257.nse
├── fxf-fortios-detect.nse
└── fxf-cisco-asa-detect.nse
```

Instale via: `fxf > install-nse` — consulte [12-scripts-nse.md](12-scripts-nse.md).

---

## Documentação gerada

| Arquivo | Regenerar com |
|---------|---------------|
| `docs/COVERAGE_MATRIX.md` | `python tools/generate_coverage_matrix.py` |
| `docs/FULL_CATALOG.md` | `python tools/generate_full_catalog.py` |
| `docs/wiki/ANEXO-INDICE-MODULOS.md` | `python tools/gen_wiki_module_index.py` |

---

## `tools/` — scripts de manutenção

| Script | Função |
|--------|--------|
| `env_doctor.py` | Teste de dependências (imports principais) |
| `check_env_readiness.py` | Verificação completa de prontidão do ambiente |
| `compile_modules.py` | `compileall` para core, modules, libs |
| `validate_coverage_minimums.py` | Validação de cobertura mínima do catálogo de mercado |
| `validate_arsenal.py` | Validar estrutura JSON do arsenal |
| `validate_governance.py` | Verificar arquivos de governança obrigatórios |
| `refresh_cve_catalog.py` | Regenerar `cve_extended_catalog.json` |
| `ingest_cve_pocs.py` | Ingerir conteúdo de PoCs de CVEs |
| `merge_oui.py` | Mesclar bases OUI (IEEE + Wireshark + Nmap) |
| `sync_wordlists.py` | Sincronizar recursos de wordlists |
| `sync_mibs.py` | Sincronizar arquivos MIB SNMP |
| `generate_full_catalog.py` | Regenerar documentação FULL_CATALOG |
| `generate_coverage_matrix.py` | Regenerar documentação COVERAGE_MATRIX |
| `gen_wiki_module_index.py` | Regenerar anexo do índice da wiki |
| `coverage_check_modern.py` | Verificação moderna de cobertura com pesos de mercado |
| `report_coverage_gaps.py` | Exportar CSV de lacunas de cobertura |

---

## Fluxo de atualização de CVEs

```bash
# Atualizar o catálogo CVE estendido
python tools/refresh_cve_catalog.py

# Ingerir novos links de PoC
python tools/ingest_cve_poc_links.py

# Regenerar matriz de cobertura
python tools/generate_coverage_matrix.py

# Regenerar índice de módulos
python tools/gen_wiki_module_index.py
```

---

[Hub da wiki](../README.md)
