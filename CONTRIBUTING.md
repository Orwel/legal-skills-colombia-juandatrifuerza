# Cómo contribuir a legal-skills-hispanoamerica

Proyecto abierto para abogados, estudiantes de derecho y legaltech de toda Hispanoamérica.

## Reglas antes de contribuir

1. **Leer `.cursorrules`** — reglas absolutas del proyecto
2. **Leer `normas-base.md`** de la jurisdicción antes de escribir cualquier skill
3. **Aislamiento total** — nunca mezclar legislación entre países
4. **No inventar normas** — usar `[VERIFICAR]` si hay duda

## Requisitos para contribuir un skill

1. Fork del repositorio
2. Crear carpeta: `jurisdicciones/[país]/[area]/[nombre-skill]/`
3. Crear `SKILL.md` usando la plantilla en `/templates/SKILL-template.md`
4. El skill debe tener las **7 secciones obligatorias** + sección **Advertencia** final
5. Fundamentado en normas de `normas-base.md` de esa jurisdicción
6. Jurisprudencia **verificable** o marcada `[VERIFICAR]`
7. Pull request con descripción del skill, jurisdicción y área

## Checklist antes de abrir el PR

- [ ] Frontmatter completo: `author`, `jurisdiction`, `legal-basis`, `last-verified`, `warning`
- [ ] Description con palabras clave de activación y declaración de jurisdicción
- [ ] Se leyó `normas-base.md` de la jurisdicción
- [ ] Todos los artículos citados están en `normas-base.md` o marcados `[VERIFICAR]`
- [ ] Sección de información requerida — la IA pregunta antes de actuar
- [ ] Formato de respuesta con ejemplo
- [ ] Advertencias obligatorias al final
- [ ] Sección `## Advertencia` final según `.cursorrules`
- [ ] Mínimo 4 errores comunes específicos del área y jurisdicción
- [ ] No se mezcló legislación de otros países

## Contribuir normas-base.md

El archivo `normas-base.md` es la fuente de verdad de cada jurisdicción:

1. Solo incluir normas confirmables con alta certeza
2. Incluir número de artículo específico
3. Marcar con `[VERIFICAR]` las normas con menor certeza
4. Incluir advertencia crítica del sistema jurídico del país
5. NO incluir montos de salario mínimo ni tasas de interés
6. SÍ incluir estructura normativa y equivalencias funcionales

## Proceso de revisión

1. Abrir PR con descripción clara
2. Un revisor verifica que los artículos citados existen en `normas-base.md`
3. Preferible revisión por abogado del área y jurisdicción
4. Merge cuando pasa checklist

## Áreas prioritarias

| Prioridad | Jurisdicción | Área |
|---|---|---|
| Alta | México, Argentina, Chile | Derecho laboral, civil, procesal |
| Alta | Perú, Ecuador | Derecho de familia |
| Media | Todos Tier 1 | Skills sustantivos por área |
| Media | Módulo anglosajón | Contratos bilingües, traducción |
| Baja | Tier 2 (14 países) | Skills transversales |

## Estándar de calidad

Los skills deben probarse con al menos 3 casos reales antes de publicar.
Un skill con artículos falsos es peor que uno con `[VERIFICAR]`.
