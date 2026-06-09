# legal-skills-colombia

**Skills jurídicos para derecho colombiano — compatibles con Claude, Cursor, GitHub Copilot, OpenAI Codex y cualquier herramienta que soporte el estándar Agent Skills.**

Proyecto abierto de la comunidad jurídica colombiana. **Cualquier abogado, estudiante de derecho o persona interesada puede aportar, corregir y proponer mejoras** — ver [Contribuir](#contribuir).

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

### ¿Por qué no sirven los skills legales en inglés?

Existen repositorios de skills legales en inglés — para derecho holandés, para startups de Delaware, para contratos de M&A anglosajones. Son buenos. Pero no sirven para ti.

No conocen el **CGP**. No citan el **Código Civil colombiano** ni el **Código de Comercio**. No saben qué es una **tutela**, una **acción popular**, un **derecho de petición**, una **nulidad y restablecimiento del derecho**, una **acción de cumplimiento** o un **Habeas Data**. No entienden la diferencia entre el **proceso ordinario**, el **proceso verbal sumario**, el **proceso ejecutivo** ni el **proceso declarativo**. No calculan términos en **días hábiles** con vacancia judicial. No conocen el **CPACA**, la **contratación estatal**, ni los recursos de **reposición y apelación**.

No saben qué es una **SAS**, cómo funciona la **tradición** en un inmueble, ni qué diferencia un **contrato de prestación de servicios** de un **contrato de trabajo** con subordinación. No liquidan **cesantías, prima ni vacaciones**. No aplican la **Ley 820** al arrendamiento de vivienda urbana. No revisan cláusulas bajo el **Estatuto del Consumidor**.

No conocen la jurisprudencia de la **Corte Constitucional**, la **Corte Suprema** ni el **Consejo de Estado** — ni la diferencia entre una **SU de unificación** y un precedente común. Y lo peor: a veces responden con derecho **mexicano, español o estadounidense** disfrazado de análisis local.

**legal-skills-colombia** sí. Skills construidos sobre legislación colombiana vigente, con artículos específicos, jurisprudencia verificable y la lógica procesal que usas todos los días — en tutelas, demandas, contratos, liquidaciones, due diligence y cálculo de términos. Se activan solos. Tú escribes el caso; el sistema aplica el derecho correcto.

No reemplazan tu criterio. Liberan las horas que no lo requieren: redactar la primera versión de una tutela, revisar un contrato cláusula por cláusula, calcular un término, armar un concepto con la estructura correcta. El abogado decide; la IA opera con la lógica del derecho colombiano.

---

## Áreas cubiertas

| Área | Skills disponibles |
|---|---|
| Análisis transversal | Análisis de archivos · Análisis jurisprudencial · Due diligence general · Elaboración de concepto jurídico · Investigación jurídica |
| Derecho administrativo | Derecho de petición · Nulidad y restablecimiento · Recursos de reposición y apelación |
| Derecho civil | Análisis de riesgo contractual · Creación de contratos |
| Derecho comercial | Análisis de sociedades · Due diligence de empresa · Títulos valores |
| Derecho constitucional | Redacción de tutela |
| Derecho disciplinario | Queja disciplinaria |
| Derecho de familia | Custodia y alimentos · Divorcio · Sucesiones |
| Derecho inmobiliario | Contrato de arrendamiento · Promesa de compraventa |
| Derecho laboral | Análisis de contrato de trabajo |
| Derecho penal | Análisis de tipicidad |
| Derecho procesal | Cálculo de términos CGP · Redacción de demanda |
| *Próximamente* | Derecho ambiental · Tributario · Propiedad intelectual |

**Total: 24 skills · 10 áreas**

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

> *"Necesito investigar la jurisprudencia y normativa sobre responsabilidad del Estado por falla del servicio en contratación. Arma el plan de investigación."*

> *"Redacta un contrato de prestación de servicios de desarrollo de software entre dos SAS, con cláusulas de confidencialidad y propiedad intelectual."*

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
│   ├── elaboracion-concepto-juridico/
│   └── investigacion-juridica/
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

Este es un proyecto de la comunidad. No lo construye una sola persona ni una sola firma: lo construyen los abogados que lo usan, lo prueban y lo corrigen.

**¿Quién puede aportar?**

- Abogados en ejercicio de cualquier área
- Estudiantes de derecho
- Profesionales de legaltech
- Cualquier persona con interés en mejorar cómo la IA entiende el derecho colombiano

**No necesitas saber programar.** Los skills son archivos de texto (`SKILL.md`) con instrucciones jurídicas. Si sabes redactar un concepto, revisar un contrato o estructurar una tutela, ya tienes lo necesario para contribuir.

### Formas de participar

| Si quieres… | Cómo hacerlo |
|---|---|
| Reportar un error en un skill | Abre un [Issue](https://github.com/Orwel/legal-skills-colombia-juandatrifuerza/issues) describiendo el skill, el error y la norma o sentencia correcta |
| Proponer un cambio o mejora | Abre un Issue con tu propuesta, o un Pull Request si ya tienes el texto corregido |
| Agregar un skill nuevo | Sigue la plantilla en `/templates/SKILL-template.md` y abre un PR |
| Sugerir un área que falta | Abre un Issue con el nombre del skill que te gustaría ver (ej. tributario, ambiental, Habeas Data) |
| Revisar la calidad jurídica | Comenta en un PR o Issue — tu revisión como abogado del área es tan valiosa como escribir el skill |

### Proceso para contribuir un skill

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para el estándar de calidad completo.

1. Haz fork del repositorio
2. Crea una carpeta con el nombre del skill en el área correspondiente
3. Escribe el `SKILL.md` siguiendo la plantilla en `/templates/SKILL-template.md`
4. Abre un Pull Request con una descripción del skill y el área que cubre

Los skills contribuidos deben estar fundamentados en legislación colombiana vigente y jurisprudencia verificable — con artículos específicos y sentencias con corporación, número y año.

### Áreas donde más se necesita ayuda

- Derecho tributario
- Derecho ambiental
- Propiedad intelectual
- Derecho migratorio
- Protección de datos (Habeas Data)
- Derecho del consumidor (SIC)

Si no sabes por dónde empezar, abre un Issue con la pregunta *"¿Cómo puedo ayudar en [tu área]?"* y te orientamos.

---

## Licencia

Apache 2.0 — libre para usar, adaptar y redistribuir con atribución.

---

*"El derecho no va a automatizarse. Pero la operación del derecho — la parte repetitiva, mecánica, que consume horas sin agregar valor intelectual — sí puede y debe optimizarse."*
