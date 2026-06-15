# legal-skills-hispanoamerica

**Skills jurídicos para derecho hispanoamericano y derecho anglosajón — compatibles con Claude, Cursor, GitHub Copilot, OpenAI Codex y cualquier herramienta que soporte el estándar Agent Skills.**

Proyecto abierto. Construido por [Juan David Vanegas Roldán](https://trifuerza.co) — Legal Engineer · Legal Designer · Software Architect.

---

## ¿Qué es esto?

El primer repositorio de skills jurídicos para países hispanohablantes, con un módulo adicional de derecho anglosajón para abogados que trabajan con contrapartes o documentos en inglés.

Cada skill está **aislado por jurisdicción**. Un skill de México nunca cita el CGP colombiano. Un skill de Argentina nunca aplica el Código Civil español. La legislación de cada país vive en su propio espacio, referenciada desde su propio archivo `normas-base.md`.

---

## Skills disponibles por jurisdicción

| Jurisdicción | Skills transversales | Skills sustantivos | Total |
|---|---|---|---|
| 🇨🇴 Colombia | 5 | 20 | **25** |
| 🇲🇽 México | 5 | 19 | **24** |
| 🇦🇷 Argentina | 5 | 19 | **24** |
| 🇨🇱 Chile | 5 | 19 | **24** |
| 🇵🇪 Perú | 5 | 19 | **24** |
| 🇪🇸 España | 5 | 19 | **24** |
| 🇻🇪 Venezuela | 5 | 19 | **24** |
| 🇪🇨 Ecuador | 5 | 19 | **24** |
| 🇧🇴 Bolivia | 5 | 19 | **24** |
| 🇵🇾 Paraguay | 5 | 19 | **24** |
| 🇺🇾 Uruguay | 5 | 19 | **24** |
| 🇵🇦 Panamá | 5 | 19 | **24** |
| 🇨🇷 Costa Rica | 5 | 19 | **24** |
| 🇳🇮 Nicaragua | 5 | 19 | **24** |
| 🇭🇳 Honduras | 5 | 19 | **24** |
| 🇸🇻 El Salvador | 5 | 19 | **24** |
| 🇬🇹 Guatemala | 5 | 19 | **24** |
| 🇨🇺 Cuba | 5 | 19 | **24** |
| 🇩🇴 Rep. Dominicana | 5 | 19 | **24** |
| 🇵🇷 Puerto Rico | 5 | 19 | **24** |
| 🌐 Derecho anglosajón | — | 4 | **4** |

### Skills transversales (20 jurisdicciones)

Disponibles en **todos los países** bajo `jurisdicciones/[país]/analisis-transversal/`:

| Skill | Qué hace |
|---|---|
| `investigacion-juridica` | Plan de investigación, búsqueda normativa y jurisprudencial |
| `analisis-jurisprudencial` | Análisis de sentencias y construcción de líneas jurisprudenciales |
| `elaboracion-concepto-juridico` | Conceptos, memos y consultas formales |
| `due-diligence-general` | Verificación de personas, inmuebles y operaciones |
| `analisis-archivo-documentos` | Análisis integrado de expedientes y documentos |

### Skills sustantivos (19 jurisdicciones + Colombia)

10 áreas en cada país hispanoamericano (salvo anonimizador, exclusivo de Colombia):

| Área | Skills |
|---|---|
| `derecho-civil` | creacion-contrato, analisis-riesgo-contrato |
| `derecho-comercial` | analisis-sociedad, due-diligence-empresa, titulos-valores |
| `derecho-constitucional` | redaccion-tutela (amparo/protección según país) |
| `derecho-administrativo` | derecho-peticion, nulidad-restablecimiento, recurso-reposicion-apelacion |
| `derecho-disciplinario` | queja-disciplinaria |
| `derecho-familia` | custodia-alimentos, proceso-divorcio, sucesiones |
| `derecho-inmobiliario` | contrato-arrendamiento, promesa-compraventa |
| `derecho-laboral` | analisis-contrato-trabajo |
| `derecho-penal` | analisis-tipicidad |
| `derecho-procesal` | calculo-terminos-cgp, redaccion-demanda |

Colombia incluye además `anonimizador-documentos`.

### Skills derecho anglosajón (4)

| Skill | Qué hace |
|---|---|
| `traduccion-conceptos-common-law` | Explica consideration, trust, estoppel, etc. |
| `contrato-bilingue` | Estructura contratos español/inglés |
| `clausulas-boilerplate` | Traducción de cláusulas tipo |
| `comparacion-estructura-contractual` | Mapeo civil law vs common law |

---

## Jurisdicciones cubiertas

| País | Sistema | Estado |
|---|---|---|
| 🇨🇴 Colombia | Civil law | ✅ Completo (25 skills) |
| 🇲🇽 México | Civil law federal | ✅ Completo (24 skills) |
| 🇦🇷 Argentina | Civil law (CCyCN 2015) | ✅ Completo (24 skills) |
| 🇨🇱 Chile | Civil law (Bello) | ✅ Completo (24 skills) |
| 🇵🇪 Perú | Civil law | ✅ Completo (24 skills) |
| 🇪🇸 España | Civil law + foral | ✅ Completo (24 skills) |
| 🇻🇪 Venezuela | Civil law | ✅ Completo (24 skills) ⚠️ verificar vigencia |
| 🇪🇨 Ecuador | Civil law | ✅ Completo (24 skills) |
| 🇧🇴 Bolivia | Civil law plurinacional | ✅ Completo (24 skills) |
| 🇵🇾 Paraguay | Civil law bilingüe | ✅ Completo (24 skills) |
| 🇺🇾 Uruguay | Civil law | ✅ Completo (24 skills) |
| 🇵🇦 Panamá | Civil law + influencia EE.UU. | ✅ Completo (24 skills) |
| 🇨🇷 Costa Rica | Civil law | ✅ Completo (24 skills) |
| 🇳🇮 Nicaragua | Civil law | ✅ Completo (24 skills) ⚠️ verificar vigencia |
| 🇭🇳 Honduras | Civil law | ✅ Completo (24 skills) |
| 🇸🇻 El Salvador | Civil law | ✅ Completo (24 skills) |
| 🇬🇹 Guatemala | Civil law | ✅ Completo (24 skills) |
| 🇨🇺 Cuba | Civil law socialista | ✅ Completo (24 skills) ⚠️ verificar vigencia |
| 🇩🇴 República Dominicana | Civil law napoleónico | ✅ Completo (24 skills) |
| 🇵🇷 Puerto Rico | Mixto civil law + common law | ✅ Completo (24 skills) |
| 🌐 Derecho anglosajón | Common law | ✅ 4 skills (traducción/contratos) |

---

## Estructura del repositorio

```
legal-skills-hispanoamerica/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CHANGELOG.md
├── .cursorrules
├── templates/
│   ├── SKILL-template.md
│   └── normas-base-template.md
├── jurisdicciones/
│   ├── colombia/
│   │   ├── normas-base.md
│   │   ├── system-prompts/
│   │   ├── analisis-transversal/     ← 5 skills
│   │   ├── derecho-civil/            ← skills sustantivos
│   │   └── [10 áreas de derecho]
│   ├── mexico/
│   │   ├── normas-base.md
│   │   ├── system-prompts/
│   │   └── analisis-transversal/     ← 5 skills
│   └── [demás países]/
│       ├── normas-base.md
│       ├── system-prompts/
│       ├── analisis-transversal/     ← 5 skills
│       └── [10 áreas de derecho]     ← 19 skills sustantivos
└── derecho-anglosajon/
    ├── normas-base.md
    └── [4 skills de traducción/contratos]
```

---

## Reglas absolutas — leer antes de contribuir

**1. Aislamiento jurisdiccional total** — nunca mezclar legislación entre países.

**2. Leer `normas-base.md` primero** — solo citar normas que aparezcan ahí.

**3. No inventar legislación** — marcar con `[VERIFICAR: Art. X de la Ley Y]`.

**4. Frontmatter obligatorio** — `jurisdiction`, `legal-basis`, `last-verified`, `warning`.

**5. Advertencia al final** — todo skill termina con sección de advertencia.

Ver `.cursorrules` para el estándar completo.

---

## Instalación

### En Claude.ai — Project por jurisdicción

1. Crea un Project por país
2. Carga el `normas-base.md` del país
3. Carga los skills del área de práctica
4. Configura las instrucciones con el system-prompt de `jurisdicciones/[país]/system-prompts/`

### En Cursor / Claude Code

```bash
git clone https://github.com/tuusuario/legal-skills-hispanoamerica
```

Copia la carpeta de la jurisdicción que necesites al directorio de skills de tu herramienta.

---

## Uso para curso de IA para abogados

Los skills transversales son el punto de entrada ideal:

> *"Arma un plan de investigación sobre responsabilidad contractual por incumplimiento en México."*

> *"Analiza esta sentencia de la CSJN y extrae la ratio decidendi."*

> *"Necesito un concepto jurídico sobre cláusulas abusivas en contratos de consumo en España."*

> *"Haz due diligence de esta sociedad antes de firmar el contrato — es una SRL en Argentina."*

> *"Tengo 15 documentos de un expediente laboral en Chile — arma la cronología y detecta inconsistencias."*

---

## Cómo contribuir

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para el proceso completo.

Prioridades:
- Enriquecer skills generados con jurisprudencia local (Colombia tiene versión detallada)
- Ampliar `normas-base.md` (código penal, administrativo) en países con [VERIFICAR]
- Correcciones de `normas-base.md` por país
- Anonimizador de documentos para otras jurisdicciones

---

## Autor

**Juan David Vanegas Roldán**
Legal Engineer · Legal Designer · Software Architect
[trifuerza.co](https://trifuerza.co)

---

## Licencia

Apache 2.0 — libre para usar, adaptar y redistribuir con atribución.
