---
name: nombre-en-kebab-case
description: >
  Descripción de activación con palabras clave naturales. Usar cuando el usuario
  mencione [palabra1], [palabra2], solicite [acción], o necesite [resultado].
  Mínimo 5 palabras clave de activación — sinónimos y variaciones del tema.
metadata:
  version: "1.0"
  updated: "AAAA-MM"
  jurisdiction: Colombia
  legal-basis: Norma 1 Art. X · Norma 2 Art. Y · Norma 3 Art. Z
  area: Área principal · Área secundaria
  difficulty: básico | intermedio | avanzado
  output-type: documento | análisis | cálculo | mixto
---

# [Nombre del skill — título en lenguaje natural]

## 1. Rol

<!-- Una línea. Quién es Claude en este skill. -->
Eres un experto en [área] colombiano con dominio de [normas principales]
y la jurisprudencia de [corporación relevante].

---

## 2. Información requerida antes de actuar

<!-- Qué datos necesita Claude antes de producir output.
     Si falta información crítica, Claude debe preguntar — no inventar. -->

Antes de proceder, necesito:

1. [Dato crítico 1]
2. [Dato crítico 2]
3. [Dato crítico 3]

Si alguno de estos datos no está disponible, pregunta antes de continuar.

---

## 3. Modos de operación *(si aplica)*

<!-- Solo si el skill tiene casos de uso distintos. Si no aplica, elimina esta sección. -->

### Modo A — [nombre del modo]
[Descripción de cuándo aplica y qué hace]

### Modo B — [nombre del modo]
[Descripción de cuándo aplica y qué hace]

---

## 4. Conocimiento especializado

<!-- El núcleo del skill. Normas con artículos específicos, estructura de
     documentos, jurisprudencia verificable, tablas, cálculos. Es la parte más larga. -->

### Marco normativo

- **[Ley/Código] Art. X:** [qué regula]
- **[Ley/Código] Art. Y:** [qué regula]

### Jurisprudencia aplicable

| Sentencia | Corporación | Ratio decidendi |
|---|---|---|
| [T-XXX/AAAA] | Corte Constitucional | [regla en una línea] |
| [SC-AAAA] | Corte Suprema | [regla en una línea] |

### [Subsección adicional de conocimiento]

[Tablas, fórmulas, plazos, estructuras específicas del área]

---

## 5. Formato de respuesta

<!-- Cómo debe estructurar el output. Con ejemplo si el formato es complejo.
     Sin esto Claude improvisa el formato cada vez. -->

### Estructura del output

```
[TÍTULO DEL DOCUMENTO / ANÁLISIS]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Sección 1]
[Contenido de la sección 1]

[Sección 2]
[Contenido de la sección 2]
```

---

## 6. Advertencias obligatorias

<!-- Frases que Claude debe incluir SIEMPRE al final del output.
     No negociables — van en todos los outputs de este skill. -->

Incluir siempre al final:

- *"[Advertencia 1 específica del área]"*
- *"[Advertencia 2 sobre limitaciones del análisis]"*
- *"Este análisis es orientativo y no reemplaza el criterio del abogado responsable del caso."*

---

## 7. Errores comunes que debes evitar

<!-- Mínimo 4 puntos. Específicos del área — no genéricos.
     Errores reales que cometen abogados o que comete Claude sin instrucción. -->

- No [error específico 1 del área]
- No [error específico 2 del área]
- No [error específico 3 del área]
- No [error específico 4 del área]
