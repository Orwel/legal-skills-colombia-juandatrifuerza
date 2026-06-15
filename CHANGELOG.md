# Changelog

## [0.2.0] — 2025-06

### Cambiado
- Repositorio renombrado de `legal-skills-colombia` a `legal-skills-hispanoamerica`
- Estructura multijurisdiccional: Colombia bajo `jurisdicciones/colombia/`
- Anonimizador movido a `jurisdicciones/colombia/anonimizador-documentos/`

### Agregado
- **14 jurisdicciones adicionales**: 5 skills transversales cada una (70 archivos)
  - Bolivia, Ecuador, Venezuela, Paraguay, Uruguay, Panamá, Costa Rica
  - Nicaragua, Honduras, El Salvador, Guatemala, Cuba, Rep. Dominicana, Puerto Rico
- Script `_generate_tier2.py` para regenerar skills Tier 2

## [0.1.0] — 2025-06

### Agregado
- Estructura multijurisdiccional con 20 países + módulo anglosajón
- `normas-base.md` para 19 jurisdicciones hispanohablantes
- **Colombia**: migración completa de 25 skills desde legal-skills-colombia
- **Tier 1** (México, Argentina, Chile, Perú, España): 5 skills transversales cada uno
  - investigacion-juridica
  - analisis-jurisprudencial
  - elaboracion-concepto-juridico
  - due-diligence-general
  - analisis-archivo-documentos
- Templates: `SKILL-template.md` y `normas-base-template.md`
- System-prompts por jurisdicción Tier 1
- `.cursorrules` con reglas de aislamiento jurisdiccional
- `CONTRIBUTING.md` con protocolo de calidad normativa

### Notas
- Fuentes marcadas con `[VERIFICAR]` requieren confirmación antes de uso profesional
- Venezuela, Cuba y Nicaragua: solo normas-base (advertencia de inestabilidad normativa)
