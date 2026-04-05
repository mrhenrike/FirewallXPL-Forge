# Política de segurança — RouterXPL-Forge

**Idioma:** **Português (pt-BR).** **English (en-US, padrão):** [SECURITY.md](SECURITY.md)

**Author:** André Henrique ([@mrhenrike](https://github.com/mrhenrike)) \| **União Geek** — [https://github.com/Uniao-Geek](https://github.com/Uniao-Geek)

## Versões e escopo suportados

- **Em escopo:** falhas no **próprio RouterXPL-Forge** (código Python, dependências declaradas, scripts em `tools/`) que afetem quem **executa** o framework (RCE no operador, execução insegura de entradas, etc.).
- **Fora de escopo:** “0-day” em equipamentos de terceiros descobertos *usando* o framework; use canais do fabricante ou programas de *bug bounty* deles.
- **Escopo funcional do repositório:** roteadores, switches, TAPs, firewalls e NGFW. Módulos focados em câmera/impressora/DVR como alvo principal não são prioridade deste fork.

## Como reportar vulnerabilidades

1. Abra um **reporte privado de vulnerabilidade** no GitHub: **Security → Report a vulnerability** no repositório `mrhenrike/RouterXPL-Forge`.
2. Não abra issue pública com *exploit* completo antes da triagem.
3. Inclua:
   - commit ou tag afetada
   - passos mínimos para reproduzir
   - impacto (confidencialidade, integridade, disponibilidade)
   - *patch* sugerido (opcional)
   - trechos de log sem dados sensíveis de terceiros

## Metas de resposta (melhor esforço)

| Fase | Meta |
|------|------|
| Confirmação de recebimento | até ~72 horas |
| Triagem inicial | até ~7 dias úteis |
| Correção | conforme severidade e complexidade |

## Divulgação coordenada

Preferimos **divulgação coordenada**: mantenha detalhes privados até publicarmos correção ou tempo combinado. Divulgação pública imediata com PoC pode ser desaconselhada em casos de risco ao ecossistema de usuários.

## Uso seguro do framework (responsabilidade do operador)

- Utilize **somente** em ativos que você possua ou para os quais tenha **autorização explícita por escrito**.
- Ambientes de produção de terceiros exigem contrato e regras de engajamento claras.
- Não envie para este repositório amostras de dados reais de clientes, credenciais ou dumps.
- Módulos podem ser destrutivos em laboratório; isole redes de teste.

## Comportamento e conduta

Questões de **assédio ou abuso** em canais do projeto: veja [CODE_OF_CONDUCT.pt-BR.md](CODE_OF_CONDUCT.pt-BR.md) ou [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) e use reporte privado quando aplicável.

---

> **Author:** André Henrique ([@mrhenrike](https://github.com/mrhenrike)) \| **União Geek** — [https://github.com/Uniao-Geek](https://github.com/Uniao-Geek)
