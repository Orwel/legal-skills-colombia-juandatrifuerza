# legal-skills-colombia

**Skills jurídicos para derecho colombiano — compatibles con Claude, Cursor, GitHub Copilot, OpenAI Codex y cualquier herramienta que soporte el estándar Agent Skills.**

Proyecto abierto de la comunidad jurídica colombiana.

---

## ¿Qué es esto?

Un repositorio de habilidades especializadas para que cualquier herramienta de IA entienda, razone y produzca documentos con la lógica del derecho colombiano.

No es una colección de prompts genéricos. Es un sistema de instrucciones construido sobre:

- El Código General del Proceso (CGP)
- El Código Civil colombiano
- El Código de Comercio
- La Constitución Política de 1991
- El CPACA
- La jurisprudencia de la Corte Constitucional, la Corte Suprema de Justicia y el Consejo de Estado

Cada skill está diseñado para activarse automáticamente cuando el contexto lo requiere — sin que el usuario tenga que recordar instrucciones ni copiar y pegar prompts.

---

## Áreas cubiertas

| Área | Skills disponibles |
|---|---|
| Análisis transversal | Análisis de archivos · Análisis jurisprudencial · Due diligence general · Elaboración de concepto jurídico |
| Derecho administrativo | Derecho de petición · Nulidad y restablecimiento · Recursos de reposición y apelación |
| Derecho civil | Análisis de riesgo contractual |
| Derecho comercial | Análisis de sociedades · Due diligence de empresa · Títulos valores |
| Derecho constitucional | Redacción de tutela |
| Derecho disciplinario | Queja disciplinaria |
| Derecho de familia | Custodia y alimentos · Divorcio · Sucesiones |
| Derecho inmobiliario | Contrato de arrendamiento · Promesa de compraventa |
| Derecho laboral | Análisis de contrato de trabajo |
| Derecho penal | Análisis de tipicidad |
| Derecho procesal | Cálculo de términos CGP · Redacción de demanda |
| *Próximamente* | Derecho ambiental · Tributario · Propiedad intelectual |

**Total: 22 skills · 10 áreas**

---

## Instalación

### En Claude.ai — Project (recomendado)

1. Crea un nuevo Project en Claude.ai
2. Ve a **Project Knowledge** → **Add content**
3. Sube los archivos `SKILL.md` de las áreas que más uses
4. Configura las instrucciones del proyecto (ver plantillas en `/system-prompts/`)
5. Listo — Claude aplica los skills automáticamente en cada conversación del proyecto

### En Claude.ai — chat ocasional

1. Abre el `SKILL.md` del skill que necesitas
2. Copia el contenido completo
3. Pégalo al inicio del chat antes de tu solicitud

### En Cursor / Claude Code / GitHub Copilot

```bash
git clone https://github.com/Orwel/legal-skills-colombia-juandatrifuerza.git
```

Copia las carpetas de skills al directorio de skills de tu herramienta. El formato `SKILL.md` es compatible con el estándar Agent Skills — funciona en Claude Code, Cursor, Copilot, OpenAI Codex y más.

### Descargar sin Git

1. Botón verde **Code** → **Download ZIP**
2. Descomprime en tu computador
3. Sigue las instrucciones de instalación según tu herramienta

---

## Uso

Una vez instalados, los skills se activan automáticamente. Solo escribe tu solicitud en lenguaje natural:

> *"Necesito una tutela para una paciente a quien la EPS le lleva 4 meses negando una cirugía ordenada por su médico."*

> *"Analiza este contrato de arrendamiento y dime los riesgos para el arrendatario."*

> *"Me notificaron el auto admisorio el 3 de junio. ¿Cuándo vence el término para contestar en proceso verbal?"*

> *"¿Cuál es la línea de la Corte Constitucional sobre el derecho al mínimo vital?"*

---

## Estructura del repositorio

```
legal-skills-colombia/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CHANGELOG.md
├── .cursorrules
├── templates/
│   └── SKILL-template.md
├── system-prompts/
│   ├── litigante-civil.md
│   ├── abogado-corporativo.md
│   └── abogado-general.md
├── analisis-transversal/
│   ├── analisis-archivo-documentos/
│   ├── analisis-jurisprudencial/
│   ├── due-diligence-general/
│   └── elaboracion-concepto-juridico/
├── derecho-administrativo/
├── derecho-civil/
├── derecho-comercial/
├── derecho-constitucional/
├── derecho-disciplinario/
├── derecho-familia/
├── derecho-inmobiliario/
├── derecho-laboral/
├── derecho-penal/
└── derecho-procesal/
```

Cada carpeta de skill contiene un `SKILL.md` con frontmatter YAML y 7 secciones obligatorias.

---

## Contribuir

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para el estándar de calidad y el proceso de contribución.

1. Haz fork del repositorio
2. Crea una carpeta con el nombre del skill en el área correspondiente
3. Escribe el `SKILL.md` siguiendo la plantilla en `/templates/SKILL-template.md`
4. Abre un Pull Request con una descripción del skill y el área que cubre

Los skills contribuidos deben estar fundamentados en legislación colombiana vigente y jurisprudencia verificable.

---

## Licencia

Apache 2.0 — libre para usar, adaptar y redistribuir con atribución.

---

*"El derecho no va a automatizarse. Pero la operación del derecho — la parte repetitiva, mecánica, que consume horas sin agregar valor intelectual — sí puede y debe optimizarse."*
