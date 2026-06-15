"""
Genera skills sustantivos (Tier 3) para todas las jurisdicciones excepto Colombia,
system-prompts faltantes y skills del módulo derecho-anglosajon.
Basado en el patrón de jurisdicciones/colombia/.
"""
from __future__ import annotations

import re
from pathlib import Path

from _generate_tier2 import (
    INSTABILITY_EXTRA,
    JURISDICTION_DATA as TIER2_JURIS,
    advertencia_section,
    extract_articles_ref,
    find_procedural_section,
    parse_normas_base,
    shorten_law_name,
)

WORKSPACE = Path(__file__).resolve().parent
JURIS_BASE = WORKSPACE / "jurisdicciones"
ANGLO_BASE = WORKSPACE / "derecho-anglosajon"

# Colombia ya tiene skills completos
TARGET_SLUGS = [
    "mexico",
    "argentina",
    "chile",
    "peru",
    "españa",
    "bolivia",
    "ecuador",
    "venezuela",
    "paraguay",
    "uruguay",
    "panama",
    "costa-rica",
    "nicaragua",
    "honduras",
    "el-salvador",
    "guatemala",
    "cuba",
    "republica-dominicana",
    "puerto-rico",
]

EXTRA_JURIS: dict[str, dict] = {
    "mexico": {
        "name": "México",
        "adjective": "mexicano",
        "instability": False,
        "system_note": (
            "Sistema federal: verificar si aplica legislación federal o estatal. "
            "Los skills aplican legislación federal salvo indicación expresa."
        ),
        "constitutional_action": "juicio de amparo",
        "constitutional_ref": "Art. 107 CPEUM · Ley de Amparo 2013",
        "courts": "Suprema Corte de Justicia · Tribunales Colegiados de Circuito",
        "main_court": "Suprema Corte de Justicia",
        "constitutional_court": "Suprema Corte de Justicia (Pleno en amparo)",
    },
    "argentina": {
        "name": "Argentina",
        "adjective": "argentino",
        "instability": False,
        "system_note": (
            "CCyCN 2015 unificó civil y comercial. Sistema federal — verificar "
            "legislación nacional o provincial."
        ),
        "constitutional_action": "acción de amparo",
        "constitutional_ref": "Art. 43 CN",
        "courts": "Corte Suprema de Justicia · Cámaras nacionales",
        "main_court": "Corte Suprema de Justicia",
        "constitutional_court": "Corte Suprema de Justicia",
    },
    "chile": {
        "name": "Chile",
        "adjective": "chileno",
        "instability": False,
        "system_note": (
            "Código Civil de Bello (1855) — numeración distinta al colombiano. "
            "Verificar proceso constituyente reciente."
        ),
        "constitutional_action": "acción de protección",
        "constitutional_ref": "Art. 20 CPR",
        "courts": "Corte Suprema · Cortes de Apelaciones",
        "main_court": "Corte Suprema",
        "constitutional_court": "Corte Suprema (recurso de protección)",
    },
    "peru": {
        "name": "Perú",
        "adjective": "peruano",
        "instability": False,
        "system_note": "Ordenamiento unitario. Verificar reforma laboral en curso.",
        "constitutional_action": "acción de amparo",
        "constitutional_ref": "Art. 200 CPR",
        "courts": "Corte Suprema · Cortes Superiores",
        "main_court": "Corte Suprema",
        "constitutional_court": "Tribunal Constitucional",
    },
    "españa": {
        "name": "España",
        "adjective": "español",
        "instability": False,
        "system_note": (
            "Derecho común (CC) y foral autonómico — verificar territorio "
            "de la operación."
        ),
        "constitutional_action": "recurso de amparo",
        "constitutional_ref": "Art. 53.2 CE · LO 2/1979",
        "courts": "Tribunal Supremo · Audiencias Provinciales",
        "main_court": "Tribunal Supremo",
        "constitutional_court": "Tribunal Constitucional",
    },
}

JURISDICTION_DATA = {**TIER2_JURIS, **EXTRA_JURIS}

SKILL_PATHS = [
    ("derecho-civil", "creacion-contrato"),
    ("derecho-civil", "analisis-riesgo-contrato"),
    ("derecho-comercial", "analisis-sociedad"),
    ("derecho-comercial", "due-diligence-empresa"),
    ("derecho-comercial", "titulos-valores"),
    ("derecho-constitucional", "redaccion-tutela"),
    ("derecho-administrativo", "derecho-peticion"),
    ("derecho-administrativo", "nulidad-restablecimiento"),
    ("derecho-administrativo", "recurso-reposicion-apelacion"),
    ("derecho-disciplinario", "queja-disciplinaria"),
    ("derecho-familia", "custodia-alimentos"),
    ("derecho-familia", "proceso-divorcio"),
    ("derecho-familia", "sucesiones"),
    ("derecho-inmobiliario", "contrato-arrendamiento"),
    ("derecho-inmobiliario", "promesa-compraventa"),
    ("derecho-laboral", "analisis-contrato-trabajo"),
    ("derecho-penal", "analisis-tipicidad"),
    ("derecho-procesal", "calculo-terminos-cgp"),
    ("derecho-procesal", "redaccion-demanda"),
]


def find_section(sections: list[dict], keywords: tuple[str, ...]) -> dict | None:
    for sec in sections:
        title = sec["title"].lower()
        if any(kw in title for kw in keywords):
            return sec
    return None


def first_articles(
    section: dict | None,
    fallback: str = "[VERIFICAR]",
    prefer_keywords: tuple[str, ...] = (),
) -> str:
    if not section or not section["articles"]:
        return fallback
    short = shorten_law_name(section["title"])
    lines = section["articles"]
    if prefer_keywords:
        for line in lines:
            lower = line.lower()
            if any(kw in lower for kw in prefer_keywords):
                m = re.search(r"(Arts?\.|Reglas?)\s*[\d\-\s,°N°]+", line, re.IGNORECASE)
                if m:
                    return f"{short} {m.group(0).strip()}"
    for line in lines[:5]:
        m = re.search(r"(Arts?\.|Reglas?)\s*[\d\-\s,°N°]+", line, re.IGNORECASE)
        if m:
            return f"{short} {m.group(0).strip()}"
    return f"{short} {lines[0][:60]}"


def legal_basis_parts(
    sections: list[dict],
    *keywords: str,
    max_parts: int = 3,
    prefer_keywords: tuple[str, ...] = ("contrato", "obligacion", "obligación"),
) -> str:
    sec = find_section(sections, keywords)
    parts = [first_articles(sec, prefer_keywords=prefer_keywords)]
    if sec:
        short = shorten_law_name(sec["title"])
        if short not in parts[0]:
            pass
    const = find_section(sections, ("constitución", "constitucion"))
    if const and keywords != ("constitución",):
        parts.append(first_articles(const))
    seen: set[str] = set()
    unique = []
    for p in parts[:max_parts]:
        if p not in seen:
            seen.add(p)
            unique.append(p)
    return " · ".join(unique) if unique else "[VERIFICAR]"


def proc_code_name(sections: list[dict]) -> str:
    proc = find_procedural_section(sections)
    if proc:
        return shorten_law_name(proc["title"])
    return "código procesal [VERIFICAR]"


def civil_code_name(sections: list[dict]) -> str:
    civil = find_section(sections, ("código civil", "codigo civil", "ccycn", "civil y comercial"))
    if civil:
        return shorten_law_name(civil["title"])
    return "Código Civil [VERIFICAR]"


def labor_code_name(sections: list[dict]) -> str:
    labor = find_section(
        sections,
        ("trabajo", "laboral", "lft", "lct", "lott", "relaciones del trabajo", "relaciones laborales"),
    )
    if labor:
        return shorten_law_name(labor["title"])
    return "legislación laboral [VERIFICAR]"


def companies_ref(sections: list[dict]) -> str:
    soc = find_section(
        sections,
        ("sociedad", "compañía", "compania", "mercantil", "lgs", "lgsm"),
    )
    return first_articles(soc, "[VERIFICAR: ley de sociedades]")


def consumer_ref(sections: list[dict]) -> str | None:
    cons = find_section(sections, ("consumidor", "consumo", "defensa del consumidor"))
    if cons:
        return first_articles(cons)
    return None


def rental_ref(sections: list[dict]) -> str:
    rent = find_section(sections, ("arrendamiento", "alquiler", "locación", "locacion"))
    if rent:
        return first_articles(rent)
    civil = find_section(sections, ("código civil", "codigo civil"))
    return first_articles(civil, "[VERIFICAR: arrendamiento]")


def admin_ref(sections: list[dict]) -> str:
    admin = find_section(
        sections,
        ("administrativo", "contencioso", "procedimiento administrativo"),
    )
    if admin:
        return first_articles(admin)
    const = find_section(sections, ("constitución", "constitucion"))
    for line in const["articles"] if const else []:
        if "petición" in line.lower() or "peticion" in line.lower():
            return f"Constitución — {line[:80]}"
    return "[VERIFICAR: legislación administrativa]"


def frontmatter(
    name: str,
    description: str,
    country: str,
    legal_basis: str,
    area: str,
    output_type: str,
    difficulty: str = "intermedio",
) -> str:
    return f"""---
name: {name}
description: >
  {description}
metadata:
  author: Juan David Vanegas Roldán
  version: "1.0"
  jurisdiction: {country}
  legal-basis: {legal_basis}
  last-verified: "2025-06"
  area: {area}
  difficulty: {difficulty}
  output-type: {output_type}
  warning: "Verificar vigencia de normas con abogado local antes de usar"
---"""


def generate_creacion_contrato(slug: str, sections: list[dict]) -> str:
    j = JURISDICTION_DATA[slug]
    country, adj = j["name"], j["adjective"]
    civil = civil_code_name(sections)
    lb = legal_basis_parts(sections, "código civil", "codigo civil", "ccycn", "civil y comercial")
    cons = consumer_ref(sections)
    if cons:
        lb += f" · {cons}"
    desc = (
        f"Redacta contratos civiles y comerciales {adj}s. Usar cuando el usuario necesite "
        f"crear, elaborar o redactar un contrato, minuta, borrador o cláusulas en {country}. "
        f"Específico para {country}. NO usar para otras jurisdicciones."
    )
    return f"""{frontmatter("creacion-contrato", desc, country, lb, "Derecho Civil · Derecho Comercial", "documento", "avanzado")}

# Creación de Contratos — {country}

Eres un experto en redacción contractual {adj} con dominio del {civil} y la jurisprudencia de {j["main_court"]} en obligaciones y contratos.

## 1. Rol

Redactar contratos válidos y ejecutables bajo derecho de {country}. Consultar `normas-base.md` de {country} antes de citar artículos. Si el usuario trae un contrato para revisar riesgos, deriva al skill de análisis de riesgo contractual.

## 2. Información requerida

1. Tipo de contrato (compraventa, prestación de servicios, suministro, obra, NDA, etc.)
2. Partes — identificación y representación
3. Posición del cliente
4. Objeto, precio, plazo
5. Contexto (B2B, B2C, entre particulares)
6. Cláusulas prioritarias

## 3. Modos

- **A** Contrato completo · **B** Cláusulas específicas · **C** Addenda · **D** Minuta con placeholders · **E** Negociación asistida

## 4. Conocimiento especializado

### Advertencia del sistema
{j.get("system_note", j.get("federal_note", ""))}

### Requisitos de validez ({civil})
Citar SOLO artículos de contratos y obligaciones en `normas-base.md` de {country} — consentimiento, capacidad, objeto, causa y solemnidades según el tipo.

### Contratos de consumo
{"Aplicar " + cons + " cuando haya relación de consumo." if cons else "[VERIFICAR: normativa de consumo]"}

### Errores a evitar
- No citar artículos no confirmados en `normas-base.md`
- No mezclar legislación de otros países
- No redactar prestación de servicios cuando hay subordinación laboral

{advertencia_section(country, j["instability"])}
"""


def generate_analisis_riesgo(slug: str, sections: list[dict]) -> str:
    j = JURISDICTION_DATA[slug]
    country, adj = j["name"], j["adjective"]
    civil = civil_code_name(sections)
    lb = legal_basis_parts(sections, "código civil", "codigo civil", "ccycn")
    desc = (
        f"Analiza riesgos en contratos civiles y comerciales {adj}s. Usar cuando el usuario "
        f"necesite revisar, auditar o evaluar un contrato existente en {country}. "
        f"Específico para {country}. NO usar para otras jurisdicciones."
    )
    return f"""{frontmatter("analisis-riesgo-contrato", desc, country, lb, "Derecho Civil · Derecho Comercial", "análisis", "avanzado")}

# Análisis de Riesgo Contractual — {country}

Eres un experto en análisis de contratos bajo derecho de {country}, con dominio del {civil} y jurisprudencia de {j["main_court"]}.

## 1. Rol

Identificar cláusulas riesgosas, vacíos, nulidades potenciales e incumplimientos. Output con semáforo 🟢🟡🔴 y sustento normativo de `normas-base.md`.

## 2. Información requerida

Contrato o cláusulas · posición del cliente · hechos relevantes · área (civil/comercial/consumo)

## 3. Metodología

1. Identificar tipo contractual y ley aplicable
2. Verificar requisitos de validez ({civil})
3. Analizar cláusulas críticas: objeto, precio, terminación, penal, limitación de responsabilidad, resolución de conflictos
4. Señalar cláusulas abusivas si hay consumidor [VERIFICAR normativa]
5. Recomendaciones accionables

## 4. Advertencias

- Solo citar artículos de `normas-base.md`
- Marcar zonas grises con [VERIFICAR]
- No sustituir revisión del abogado responsable

{advertencia_section(country, j["instability"])}
"""


def generate_analisis_sociedad(slug: str, sections: list[dict]) -> str:
    j = JURISDICTION_DATA[slug]
    country = j["name"]
    soc_ref = companies_ref(sections)
    lb = soc_ref + " · " + legal_basis_parts(sections, "comercio", "mercantil")
    desc = (
        f"Analiza estructuras societarias y gobierno corporativo en {country}. Usar cuando el "
        f"usuario necesite revisar estatutos, órganos, reformas o riesgos societarios. "
        f"Específico para {country}. NO usar para otras jurisdicciones."
    )
    return f"""{frontmatter("analisis-sociedad", desc, country, lb, "Derecho Comercial", "análisis", "avanzado")}

# Análisis Societario — {country}

Eres un experto en derecho societario de {country}. Consulta `normas-base.md` para tipos societarios y artículos aplicables.

## 1. Rol

Analizar estructura, órganos, reformas estatutarias, conflictos societarios y cumplimiento registral.

## 2. Información requerida

Tipo societario · estatutos o borrador · accionistas/socios · operación pretendida · documentos registrales disponibles

## 3. Áreas de análisis

- Constitución y reforma ({soc_ref})
- Órganos de administración y fiscalización
- Aumentos/reducciones de capital [VERIFICAR procedimiento]
- Transformación, fusión, escisión [VERIFICAR]
- Poderes de representación
- Operaciones con partes relacionadas [VERIFICAR]

## 4. Formato

Informe con hallazgos 🟢🟡🔴, norma aplicable y recomendación.

{advertencia_section(country, j["instability"])}
"""


def generate_dd_empresa(slug: str, sections: list[dict]) -> str:
    j = JURISDICTION_DATA[slug]
    country = j["name"]
    lb = companies_ref(sections) + " · " + labor_code_name(sections)
    desc = (
        f"Due diligence legal corporativa en {country} — sociedades, contratos, laboral y litigios. "
        f"Usar en M&A, inversiones o onboarding de contraparte corporativa en {country}. "
        f"NO usar para otras jurisdicciones."
    )
    return f"""{frontmatter("due-diligence-empresa", desc, country, lb, "Derecho Comercial", "análisis", "avanzado")}

# Due Diligence Empresarial — {country}

Eres un experto en due diligence corporativa en {country}.

## 1. Rol

Estructurar DD legal empresarial — societaria, contractual, laboral, regulatoria, litigiosa. Complementa (no reemplaza) el skill de due diligence general.

## 2. Áreas

| Área | Qué revisar |
|---|---|
| Societaria | Existencia, estatutos, capital, poderes, gravámenes sobre acciones |
| Contractual | Contratos material, clausulas de cambio de control |
| Laboral | {labor_code_name(sections)} — contratos, contingencias |
| Regulatoria | Licencias, permisos [VERIFICAR sector] |
| Litigiosa | Procesos activos contra/por la sociedad |
| Inmobiliaria | Activos y gravámenes [VERIFICAR] |

## 3. Fuentes

Consultar registros mercantiles, judiciales y fiscales indicados en `normas-base.md` y skill transversal de due diligence general de {country}.

## 4. Output

Informe ejecutivo + anexo técnico con semáforo y condiciones precedentes sugeridas.

{advertencia_section(country, j["instability"])}
"""


def generate_titulos_valores(slug: str, sections: list[dict]) -> str:
    j = JURISDICTION_DATA[slug]
    country = j["name"]
    tit = find_section(sections, ("título", "titulo", "crédito", "credito", "comercio", "lgtoc"))
    lb = first_articles(tit, "[VERIFICAR: títulos valores / LGTOC]")
    desc = (
        f"Analiza y redacta aspectos de títulos valores y operaciones de crédito en {country}. "
        f"Usar con pagarés, letras, cheques o instrumentos negociables en {country}. "
        f"NO usar para otras jurisdicciones."
    )
    return f"""{frontmatter("titulos-valores", desc, country, lb, "Derecho Comercial", "mixto", "avanzado")}

# Títulos Valores — {country}

Eres un experto en títulos valores de {country}. Cita SOLO normas en `normas-base.md`.

## 1. Rol

Analizar requisitos, endoso, aval, protesto, prescripción y cobro ejecutivo de títulos valores.

## 2. Instrumentos

Pagaré · Letra de cambio · Cheque · [VERIFICAR otros instrumentos locales]

## 3. Análisis por instrumento

Verificar requisitos formales, legitimación, acciones cambiarias y términos de prescripción según {lb}.

## 4. Advertencias

- Verificar texto vigente del código mercantil o ley de títulos
- No aplicar requisitos de otros países

{advertencia_section(country, j["instability"])}
"""


def generate_redaccion_tutela(slug: str, sections: list[dict]) -> str:
    j = JURISDICTION_DATA[slug]
    country, adj = j["name"], j["adjective"]
    action = j["constitutional_action"]
    lb = j["constitutional_ref"] + " · " + first_articles(find_section(sections, ("constitución", "constitucion")))
    desc = (
        f"Redacta {action} en {country}. Usar cuando el usuario necesite protección "
        f"constitucional urgente de derechos fundamentales en {country}. "
        f"NO confundir con tutela colombiana ni amparo de otros países."
    )
    return f"""{frontmatter("redaccion-tutela", desc, country, lb, "Derecho Constitucional", "documento")}

# Redacción de {action.title()} — {country}

Eres un experto en derecho constitucional {adj} y en el mecanismo de **{action}** ({j["constitutional_ref"]}).

## 1. Rol

Redactar solicitud de protección constitucional. Competencia: {j["constitutional_court"]}.

## 2. Información requerida

Accionante · accionado · derecho vulnerado · hechos cronológicos · pretensiones · juez competente · pruebas

## 3. Estructura del documento

1. Encabezado y juez competente
2. Identificación de partes
3. Derechos fundamentales vulnerados (artículos de `normas-base.md`)
4. Hechos numerados
5. Fundamentos jurídicos y jurisprudencia [VERIFICAR sentencias]
6. Pretensiones
7. Pruebas
8. Notificaciones

## 4. Notas del sistema

{j.get("system_note", j.get("federal_note", ""))}

## 5. Errores a evitar

- No usar estructura de tutela colombiana (Decreto 2591) en {country}
- No inventar sentencias — [VERIFICAR]
- Verificar requisitos de subsidiariedad [VERIFICAR procedimiento local]

{advertencia_section(country, j["instability"])}
"""


def generate_derecho_peticion(slug: str, sections: list[dict]) -> str:
    j = JURISDICTION_DATA[slug]
    country = j["name"]
    lb = admin_ref(sections)
    desc = (
        f"Redacta derechos de petición y solicitudes formales ante la administración en {country}. "
        f"Usar cuando el usuario necesite solicitar información, actuación o respuesta de entidad pública. "
        f"Específico para {country}."
    )
    return f"""{frontmatter("derecho-peticion", desc, country, lb, "Derecho Administrativo", "documento", "básico")}

# Derecho de Petición — {country}

Eres un experto en derecho administrativo de {country} y en el ejercicio del derecho de petición.

## 1. Fundamento

Consultar derecho de petición en Constitución y normativa administrativa de `normas-base.md`: {lb}

## 2. Información requerida

Peticionario · destinatario · tipo (información, actuación, queja) · hechos · pretensión · antecedentes

## 3. Estructura

Encabezado · identificación · hechos · fundamentos · pretensión · pruebas · notificaciones

## 4. Términos de respuesta

[VERIFICAR plazos en legislación administrativa vigente de {country}]

## 5. Si no hay CPACA equivalente

Señalar al usuario que debe confirmar con abogado local el procedimiento administrativo aplicable.

{advertencia_section(country, j["instability"])}
"""


def generate_nulidad(slug: str, sections: list[dict]) -> str:
    j = JURISDICTION_DATA[slug]
    country = j["name"]
    lb = admin_ref(sections)
    desc = (
        f"Redacta demandas o recursos de nulidad y restablecimiento del derecho en {country}. "
        f"Usar contra actos administrativos lesivos. Específico para {country}."
    )
    return f"""{frontmatter("nulidad-restablecimiento", desc, country, lb, "Derecho Administrativo · Contencioso", "documento", "avanzado")}

# Nulidad y Restablecimiento del Derecho — {country}

Eres un experto en contencioso administrativo de {country}.

## 1. Rol

Estructurar medio de control o acción contra actos administrativos que vulneren derechos. Base: {lb}

## 2. Información requerida

Acto impugnado · fecha de notificación · derecho lesionado · hechos · pretensiones · caducidad [VERIFICAR]

## 3. Estructura procesal

Competencia · legitimación · acto impugnado · causales de nulidad · restablecimiento · pruebas · pretensiones

## 4. Advertencia

Muchas jurisdicciones no tienen CPACA — verificar nombre y plazos del medio de control local antes de redactar.

{advertencia_section(country, j["instability"])}
"""


def generate_recurso_admin(slug: str, sections: list[dict]) -> str:
    j = JURISDICTION_DATA[slug]
    country = j["name"]
    lb = admin_ref(sections)
    desc = (
        f"Redacta recursos administrativos (reposición, apelación, reconsideración) en {country}. "
        f"Usar contra actos de la administración pública. Específico para {country}."
    )
    return f"""{frontmatter("recurso-reposicion-apelacion", desc, country, lb, "Derecho Administrativo", "documento")}

# Recursos Administrativos — {country}

Eres un experto en recursos contra actos administrativos en {country}. Base normativa: {lb}

## 1. Recursos típicos [VERIFICAR nomenclatura local]

- Reposición / reconsideración
- Apelación ante superior jerárquico
- Queja [VERIFICAR]

## 2. Información requerida

Acto recurrido · fecha notificación · recurso procedente · argumentos · pretensiones · término [VERIFICAR]

## 3. Estructura

Encabezado · acto impugnado · agotamiento de vía [VERIFICAR] · argumentos · pretensiones · pruebas

{advertencia_section(country, j["instability"])}
"""


def generate_queja_disciplinaria(slug: str, sections: list[dict]) -> str:
    j = JURISDICTION_DATA[slug]
    country = j["name"]
    lb = "[VERIFICAR: código disciplinario / ley orgánica del Poder Judicial]"
    desc = (
        f"Redacta quejas disciplinarias contra servidores públicos o abogados en {country}. "
        f"Usar ante autoridad disciplinaria competente. Específico para {country}."
    )
    return f"""{frontmatter("queja-disciplinaria", desc, country, lb, "Derecho Disciplinario", "documento")}

# Queja Disciplinaria — {country}

Eres un experto en derecho disciplinario de {country}. **Verificar** autoridad competente y normativa vigente — no está en `normas-base.md` de forma completa.

## 1. Tipos

- Servidores públicos → [VERIFICAR: Procuraduría, Contraloría u órgano local]
- Magistrados/jueces → [VERIFICAR: consejo de la judicatura]
- Abogados → [VERIFICAR: tribunal de ética / colegio de abogados]

## 2. Información requerida

Quejoso · disciplinado · conducta · fechas · pruebas · autoridad competente

## 3. Estructura

Encabezado · partes · relato de hechos · tipificación [VERIFICAR] · pruebas · pretensiones

## 4. Advertencia crítica

Confirmar normativa disciplinaria vigente con abogado local antes de interponer.

{advertencia_section(country, j["instability"])}
"""


def generate_custodia_alimentos(slug: str, sections: list[dict]) -> str:
    j = JURISDICTION_DATA[slug]
    country = j["name"]
    fam = find_section(sections, ("familia", "civil"))
    lb = first_articles(fam, "[VERIFICAR: alimentos y custodia]", ("alimento", "custodia", "responsabilidad parental"))
    desc = (
        f"Analiza y redacta solicitudes de custodia, régimen de visitas y alimentos en {country}. "
        f"Usar en procesos de familia. Específico para {country}."
    )
    return f"""{frontmatter("custodia-alimentos", desc, country, lb, "Derecho de Familia", "documento")}

# Custodia y Alimentos — {country}

Eres un experto en derecho de familia de {country}. Citar artículos de alimentos y responsabilidad parental en `normas-base.md`: {lb}

## 1. Rol

Asesorar y redactar demandas o acuerdos sobre custodia, visitas y cuota alimentaria.

## 2. Información requerida

Menores · progenitores · ingresos · custodia actual · necesidades del menor · acuerdos previos

## 3. Análisis

- Interés superior del menor [VERIFICAR norma local]
- Cuota alimentaria — criterios de proporcionalidad
- Régimen de visitas y custodia compartida [VERIFICAR]

## 4. Procedimiento

[VERIFICAR: proceso de familia aplicable en {country}]

{advertencia_section(country, j["instability"])}
"""


def generate_divorcio(slug: str, sections: list[dict]) -> str:
    j = JURISDICTION_DATA[slug]
    country = j["name"]
    fam = find_section(sections, ("familia", "civil"))
    lb = first_articles(fam, "[VERIFICAR: divorcio]", ("divorcio", "matrimonio"))
    desc = (
        f"Orienta y redacta solicitudes de divorcio en {country}. Usar cuando el usuario "
        f"inicie o analice disolución matrimonial. Específico para {country}."
    )
    return f"""{frontmatter("proceso-divorcio", desc, country, lb, "Derecho de Familia", "documento")}

# Proceso de Divorcio — {country}

Eres un experto en derecho de familia de {country}.

## 1. Tipos de divorcio en {country}

[VERIFICAR en `normas-base.md` y notas: divorcio incausado, mutuo acuerdo, causal, etc.]

## 2. Información requerida

Cónyuges · régimen patrimonial · hijos · bienes · acuerdos previos · domicilio procesal

## 3. Documentos

Demanda o solicitud conjunta · propuesta de custodia y alimentos · liquidación de sociedad conyugal [VERIFICAR]

## 4. Base normativa

{lb}

{advertencia_section(country, j["instability"])}
"""


def generate_sucesiones(slug: str, sections: list[dict]) -> str:
    j = JURISDICTION_DATA[slug]
    country = j["name"]
    fam = find_section(sections, ("familia", "sucesion", "sucesión", "civil"))
    lb = first_articles(fam, "[VERIFICAR: sucesiones]", ("sucesion", "sucesión", "herencia"))
    desc = (
        f"Orienta sucesiones, herencias y particiones en {country}. Usar en planificación "
        f"sucesoral o procesos de herencia. Específico para {country}."
    )
    return f"""{frontmatter("sucesiones", desc, country, lb, "Derecho de Familia · Sucesiones", "mixto", "avanzado")}

# Sucesiones — {country}

Eres un experto en derecho sucesoral de {country}. Base: {lb}

## 1. Modos

- **A** Análisis de legítimas y cuotas
- **B** Redacción de testamento [VERIFICAR solemnidades]
- **C** Proceso de sucesión judicial o notarial [VERIFICAR vía]
- **D** Partición de bienes

## 2. Información requerida

Causante · herederos · testamento · bienes · deudas · régimen matrimonial

## 3. Advertencias

Verificar si aplica sucesión notarial o judicial según normativa local.

{advertencia_section(country, j["instability"])}
"""


def generate_arrendamiento(slug: str, sections: list[dict]) -> str:
    j = JURISDICTION_DATA[slug]
    country = j["name"]
    lb = rental_ref(sections)
    desc = (
        f"Redacta y analiza contratos de arrendamiento inmobiliario en {country}. "
        f"Usar para vivienda o local comercial. Específico para {country}."
    )
    return f"""{frontmatter("contrato-arrendamiento", desc, country, lb, "Derecho Inmobiliario", "documento")}

# Contrato de Arrendamiento — {country}

Eres un experto en arrendamientos de {country}. Base normativa: {lb}

## 1. Rol

Redactar o revisar contratos de arrendamiento conforme a `normas-base.md`.

## 2. Información requerida

Inmueble · arrendador/arrendatario · canon · plazo · destino (vivienda/comercio) · garantías · incrementos

## 3. Cláusulas esenciales

Objeto · canon y reajuste · plazo · mantenimiento · terminación · restitución · garantías [VERIFICAR depósito local]

## 4. Ley especial de arrendamiento

Verificar si existe ley especial de arrendamiento urbano en `normas-base.md` además del Código Civil.

{advertencia_section(country, j["instability"])}
"""


def generate_promesa(slug: str, sections: list[dict]) -> str:
    j = JURISDICTION_DATA[slug]
    country = j["name"]
    civil = civil_code_name(sections)
    lb = legal_basis_parts(sections, "código civil", "codigo civil", "compraventa")
    desc = (
        f"Redacta promesas de compraventa inmobiliaria en {country}. Usar en operaciones "
        f"con inmuebles antes de la escritura pública. Específico para {country}."
    )
    return f"""{frontmatter("promesa-compraventa", desc, country, lb, "Derecho Inmobiliario · Civil", "documento")}

# Promesa de Compraventa — {country}

Eres un experto en contratos inmobiliarios de {country} ({civil}).

## 1. Rol

Redactar promesa o contrato preparatorio de compraventa con arras, plazos y condiciones.

## 2. Información requerida

Inmueble · matrícula/registro · precio · forma de pago · plazo para escritura · arras · saneamiento

## 3. Cláusulas críticas

Identificación del inmueble · precio · calendario · arras [VERIFICAR: penitenciales vs confirmatorias] · saneamiento · resolución por incumplimiento

## 4. Solemnidades

[VERIFICAR: escritura pública obligatoria para compraventa definitiva]

{advertencia_section(country, j["instability"])}
"""


def generate_labor(slug: str, sections: list[dict]) -> str:
    j = JURISDICTION_DATA[slug]
    country, adj = j["name"], j["adjective"]
    labor = labor_code_name(sections)
    lb = first_articles(find_section(sections, ("trabajo", "laboral", "lft", "lct")), labor)
    desc = (
        f"Analiza contratos de trabajo {adj}s y riesgos de subordinación vs prestación de servicios. "
        f"Usar al contratar personal en {country}. Específico para {country}."
    )
    return f"""{frontmatter("analisis-contrato-trabajo", desc, country, lb, "Derecho Laboral", "análisis")}

# Análisis de Contrato de Trabajo — {country}

Eres un experto en derecho laboral de {country} ({labor}).

## 1. Rol

Distinguir relación laboral de prestación de servicios · analizar cláusulas · calcular contingencias [VERIFICAR montos]

## 2. Elementos de subordinación

Prestación personal · remuneración · subordinación · jornada · exclusividad [VERIFICAR artículos en `normas-base.md`]

## 3. Cláusulas a revisar

Jornada · salario · beneficios · terminación · no competencia · confidencialidad · outsourcing [VERIFICAR]

## 4. Output

Semáforo de riesgos + recomendaciones + cláusulas sugeridas.

{advertencia_section(country, j["instability"])}
"""


def generate_penal(slug: str, sections: list[dict]) -> str:
    j = JURISDICTION_DATA[slug]
    country = j["name"]
    lb = "[VERIFICAR: Código Penal y procedimiento penal]"
    desc = (
        f"Analiza tipicidad penal y elementos del delito en {country}. Usar para evaluar "
        f"conductas punibles, antijuridicidad y culpabilidad. Específico para {country}."
    )
    return f"""{frontmatter("analisis-tipicidad", desc, country, lb, "Derecho Penal", "análisis", "avanzado")}

# Análisis de Tipicidad — {country}

Eres un experto en derecho penal de {country}. **El Código Penal no está en `normas-base.md`** — marcar [VERIFICAR] en tipos penales específicos.

## 1. Metodología

1. Hechos concretos
2. Tipo penal aplicable [VERIFICAR artículo]
3. Tipicidad objetiva y subjetiva
4. Antijuridicidad
5. Culpabilidad
6. Causas de justificación o atipicidad

## 2. Output

Cuadro: conducta · tipo penal [VERIFICAR] · elementos · conclusión preliminar · advertencia de reserva penal

## 3. Advertencia

No sustituye defensa penal. Confirmar tipificación con abogado penalista local.

{advertencia_section(country, j["instability"])}
"""


def generate_terminos(slug: str, sections: list[dict]) -> str:
    j = JURISDICTION_DATA[slug]
    country = j["name"]
    proc = find_procedural_section(sections)
    proc_name = proc_code_name(sections)
    proc_ref = extract_articles_ref(proc, "[VERIFICAR: términos procesales]")
    lb = proc_ref
    desc = (
        f"Calcula términos procesales en {country} según {proc_name}. Usar cuando el usuario "
        f"necesite vencimiento de plazos judiciales en {country}. NO usar CGP colombiano."
    )
    return f"""{frontmatter("calculo-terminos-cgp", desc, country, lb, "Derecho Procesal", "cálculo", "básico")}

# Cálculo de Términos Procesales — {country}

Eres un experto en derecho procesal de {country} con dominio de **{proc_name}** ({proc_ref}).

## 1. Información requerida

Fecha del acto · tipo de acto · proceso · actuación a realizar · días hábiles o comunes

## 2. Reglas generales [VERIFICAR texto vigente]

- Inicio: generalmente día siguiente a notificación
- Días hábiles vs calendario — verificar en {proc_name}
- Prórroga si vencimiento cae en inhábil [VERIFICAR]
- Suspensiones (vacancia, feria judicial) [VERIFICAR calendario local]

## 3. Términos frecuentes

| Actuación | Plazo | Base |
|---|---|---|
| Contestación demanda | [VERIFICAR] | {proc_ref} |
| Recursos | [VERIFICAR] | {proc_ref} |
| Pruebas | [VERIFICAR] | {proc_ref} |

## 4. Output

Tabla: inicio · duración · vencimiento · base legal · advertencia de verificar calendario oficial

{advertencia_section(country, j["instability"])}
"""


def generate_demanda(slug: str, sections: list[dict]) -> str:
    j = JURISDICTION_DATA[slug]
    country = j["name"]
    proc = find_procedural_section(sections)
    proc_name = proc_code_name(sections)
    proc_ref = extract_articles_ref(proc, "[VERIFICAR: demanda]")
    lb = proc_ref
    desc = (
        f"Redacta demandas civiles o comerciales en {country} según {proc_name}. "
        f"Usar al iniciar proceso declarativo o ejecutivo. Específico para {country}."
    )
    return f"""{frontmatter("redaccion-demanda", desc, country, lb, "Derecho Procesal", "documento")}

# Redacción de Demanda — {country}

Eres un experto en derecho procesal civil de {country} ({proc_name}).

## 1. Estructura según {proc_name}

1. Juzgado competente
2. Partes y representación
3. Hechos numerados
4. Fundamentos de derecho (citar `normas-base.md`)
5. Pretensiones claras y determinadas
6. Cuantía [VERIFICAR]
7. Pruebas
8. Anexos

## 2. Requisitos de la demanda

Consultar arts. de demanda en {proc_ref} — [VERIFICAR requisitos específicos]

## 3. Errores a evitar

- Demanda genérica sin pretensiones determinadas
- Mezclar procedimiento de otro país
- Omitir requisitos de procedibilidad [VERIFICAR]

{advertencia_section(country, j["instability"])}
"""


GENERATORS = {
    "creacion-contrato": generate_creacion_contrato,
    "analisis-riesgo-contrato": generate_analisis_riesgo,
    "analisis-sociedad": generate_analisis_sociedad,
    "due-diligence-empresa": generate_dd_empresa,
    "titulos-valores": generate_titulos_valores,
    "redaccion-tutela": generate_redaccion_tutela,
    "derecho-peticion": generate_derecho_peticion,
    "nulidad-restablecimiento": generate_nulidad,
    "recurso-reposicion-apelacion": generate_recurso_admin,
    "queja-disciplinaria": generate_queja_disciplinaria,
    "custodia-alimentos": generate_custodia_alimentos,
    "proceso-divorcio": generate_divorcio,
    "sucesiones": generate_sucesiones,
    "contrato-arrendamiento": generate_arrendamiento,
    "promesa-compraventa": generate_promesa,
    "analisis-contrato-trabajo": generate_labor,
    "analisis-tipicidad": generate_penal,
    "calculo-terminos-cgp": generate_terminos,
    "redaccion-demanda": generate_demanda,
}


def generate_system_prompt(slug: str, sections: list[dict]) -> str:
    j = JURISDICTION_DATA[slug]
    country, adj = j["name"], j["adjective"]
    laws = [shorten_law_name(s["title"]) for s in sections[:8] if "ADVERTENCIA" not in s["title"].upper()]
    laws_text = "\n".join(f"- {law}" for law in laws[:6])
    instability_note = ""
    if j["instability"]:
        instability_note = f"\n\n**Verificación especial:** {INSTABILITY_EXTRA.format(country=country)}"
    return f"""# System Prompt — Asistente Jurídico {country} (General)
### legal-skills-{slug}

Copia este texto completo en la sección "Instructions" de tu Project en Claude.ai.

---

Eres un asistente jurídico especializado en derecho {adj}.

## Perfil del usuario
Abogado en ejercicio en {country}. Práctica en civil, comercial, constitucional, administrativo, laboral, penal o familia.

## Legislación de referencia principal
{laws_text}

## Comportamiento esperado

**Precisión normativa:** cita artículos de `normas-base.md` de {country}. Nunca cites normas de otros países como aplicables.

**Jurisprudencia verificable:** solo cita sentencias con referencia real. Si no tienes certeza, indica [VERIFICAR].

**Lenguaje jurídico local:** usa terminología de {country}. Evita anglicismos y términos de otros sistemas.

**Estructura procesal correcta:** sigue el código procesal local al redactar documentos.

**Advertencia profesional:** el output es punto de partida, no reemplazo del abogado responsable.

## Lo que NO debes hacer
- No mezclar legislación de otros países
- No inventar sentencias o artículos
- No omitir advertencias sobre términos procesales
- No dar concepto definitivo con hechos incompletos
{instability_note}

## Sistema jurídico
{j.get("system_note", j.get("federal_note", ""))}
"""


def generate_anglosajon_skills() -> int:
    """Genera skills del módulo derecho-anglosajon."""
    skills = {
        "traduccion-conceptos-common-law/SKILL.md": """---
name: traduccion-conceptos-common-law
description: >
  Explica conceptos del common law sin equivalente exacto en civil law. Usar cuando el
  abogado hispanoamericano encuentre consideration, trust, estoppel, representations and
  warranties, indemnity, at-will employment u otros términos anglosajones. NO es asesoría
  sobre derecho de EE.UU., UK, Canadá o Australia — es traducción conceptual.
metadata:
  author: Juan David Vanegas Roldán
  version: "1.0"
  jurisdiction: Derecho anglosajón (referencia)
  legal-basis: normas-base.md derecho-anglosajon — conceptos common law
  last-verified: "2025-06"
  area: Traducción jurídica
  difficulty: intermedio
  output-type: análisis
  warning: "No sustituye abogado del common law. Solo traducción y comparación conceptual."
---

# Traducción de Conceptos Common Law

Eres un experto en **comparación civil law / common law** para abogados hispanoamericanos. Consulta `derecho-anglosajon/normas-base.md`.

## 1. Rol

Explicar conceptos anglosajones, su función jurídica, diferencia con civil law y riesgos de traducción literal.

## 2. Conceptos cubiertos (normas-base.md)

- **Consideration** vs causa del contrato
- **Trust** vs fideicomiso latinoamericano
- **Estoppel** vs venire contra factum proprium
- **Liquidated damages** vs cláusula penal
- **Representations and warranties**
- **Indemnity**
- **Force majeure** vs **frustration**
- **At-will employment**

## 3. Formato de respuesta

| Concepto EN | Función en common law | Equivalente aproximado civil law | ¿Son idénticos? | Riesgo de traducción |

## 4. Advertencias

- NO aplicar conceptos common law en litigio de civil law sin abogado local
- Una traducción literal puede cambiar el alcance legal

## Advertencia

Este skill NO es para practicar derecho en jurisdicciones de common law.
Es para entender documentos y negociaciones internacionales.
[VERIFICAR] con abogado del sistema de common law correspondiente.
""",
        "contrato-bilingue/SKILL.md": """---
name: contrato-bilingue
description: >
  Estructura y revisa contratos bilingües español/inglés para abogados de civil law.
  Usar al redactar, revisar o negociar contratos internacionales de doble columna.
  NO es asesoría sobre ley aplicable de EE.UU. o UK — es estructura y coherencia bilingüe.
metadata:
  author: Juan David Vanegas Roldán
  version: "1.0"
  jurisdiction: Derecho anglosajón (referencia)
  legal-basis: normas-base.md derecho-anglosajon — estructura contractual
  last-verified: "2025-06"
  area: Contratos internacionales
  difficulty: avanzado
  output-type: documento
  warning: "Revisar con abogados de ambas jurisdicciones antes de firmar."
---

# Contrato Bilingüe Español/Inglés

Eres un experto en **estructura de contratos anglosajones** adaptada a equipos de civil law. Consulta `derecho-anglosajon/normas-base.md`.

## 1. Rol

Proponer estructura, detectar inconsistencias entre columnas y redactar cláusula de prevalencia.

## 2. Estructura anglosajona típica

Parties · Recitals · Definitions · Representations and warranties · Covenants · Conditions precedent · Indemnification · Limitation of liability · Term and termination · Dispute resolution · Governing law · General provisions

## 3. Cláusula de prevalencia (obligatoria)

"In case of conflict between the Spanish and English versions, the [●] version shall prevail."

## 4. Checklist bilingüe

- [ ] Definiciones equivalentes en ambas columnas
- [ ] Governing law y jurisdiction coherentes
- [ ] Indemnity / limitation traducidos con precisión conceptual
- [ ] Cláusula de idioma prevaleciente
- [ ] Revisión por abogado de common law Y civil law

## Advertencia

Los conceptos jurídicos no siempre tienen equivalente exacto entre sistemas.
Revisar con abogados de ambas jurisdicciones cuando el contrato se ejecutará en países distintos.
""",
        "clausulas-boilerplate/SKILL.md": """---
name: clausulas-boilerplate
description: >
  Traduce y explica cláusulas boilerplate de contratos anglosajones al español jurídico.
  Usar con governing law, jurisdiction, entire agreement, severability, waiver, assignment,
  notice, force majeure, indemnification, limitation of liability, MAC clauses.
metadata:
  author: Juan David Vanegas Roldán
  version: "1.0"
  jurisdiction: Derecho anglosajón (referencia)
  legal-basis: normas-base.md derecho-anglosajon — tabla boilerplate
  last-verified: "2025-06"
  area: Traducción jurídica
  difficulty: intermedio
  output-type: mixto
  warning: "Traducción orientativa — no ejecutable sin revisión bilingüe."
---

# Cláusulas Boilerplate — Traducción EN/ES

Consulta la tabla de `derecho-anglosajon/normas-base.md`.

## 1. Rol

Traducir cláusulas boilerplate preservando efecto jurídico y señalando cuando no hay equivalente en civil law.

## 2. Tabla de referencia

| Inglés | Español sugerido | Nota |
|---|---|---|
| Governing law | Ley aplicable | |
| Jurisdiction | Jurisdicción / Fuero | |
| Entire agreement | Acuerdo íntegro | |
| Severability | Divisibilidad | |
| Waiver | Renuncia | Debe ser expresa |
| Assignment | Cesión | |
| Notice | Notificación | |
| Force majeure | Fuerza mayor | |
| Indemnification | Indemnización | Más amplia en common law |
| Limitation of liability | Limitación de responsabilidad | |
| MAC | Cambio material adverso | M&A |

## 3. Best efforts vs reasonable efforts

No equivalen a obligación de resultado en civil law — explicar diferencia al cliente.

## Advertencia

Este skill es para traducción y negociación internacional, no para litigio en common law.
""",
        "comparacion-estructura-contractual/SKILL.md": """---
name: comparacion-estructura-contractual
description: >
  Compara estructura de contratos latinoamericanos vs anglosajones. Usar al mapear
  cláusulas entre un borrador civil law y un borrador common law, o al adaptar templates.
metadata:
  author: Juan David Vanegas Roldán
  version: "1.0"
  jurisdiction: Derecho anglosajón (referencia)
  legal-basis: normas-base.md derecho-anglosajon
  last-verified: "2025-06"
  area: Comparación de sistemas
  difficulty: intermedio
  output-type: análisis
  warning: "Comparación conceptual — no armonización automática de efectos legales."
---

# Comparación Estructural Contractual — Civil Law vs Common Law

## 1. Rol

Mapear secciones equivalentes y detectar vacíos cuando se adapta un template de un sistema al otro.

## 2. Mapeo típico

| Latinoamericano | Anglosajón |
|---|---|
| Partes | Parties |
| Antecedentes | Recitals / Whereas |
| Objeto | Subject matter (en covenants) |
| Obligaciones | Covenants |
| Garantías | Warranties |
| Cláusula penal | Liquidated damages [no idéntico] |
| Solución de controversias | Dispute resolution |
| Disposiciones generales | Boilerplate |

## 3. Vacíos frecuentes al adaptar

- Falta **representations** en contrato latinoamericano
- Falta **indemnity** explícita
- **Consideration** no aparece en contratos civiles — problema si se exige en common law
- Cláusula de **idioma prevaleciente** ausente en borradores unilingües

## Advertencia

Este módulo NO es para practicar derecho en jurisdicciones de common law.
Es para abogados de civil law que trabajan con contrapartes o documentos en inglés.
""",
    }
    count = 0
    for rel_path, content in skills.items():
        out = ANGLO_BASE / rel_path
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
        count += 1
        print(f"  OK  derecho-anglosajon/{rel_path}")
    return count


def main() -> None:
    created = 0
    errors: list[str] = []

    print("Generando skills sustantivos Tier 3...")
    print()

    for slug in TARGET_SLUGS:
        normas_path = JURIS_BASE / slug / "normas-base.md"
        if not normas_path.exists():
            errors.append(f"Falta normas-base.md: {slug}")
            continue
        if slug not in JURISDICTION_DATA:
            errors.append(f"Falta JURISDICTION_DATA: {slug}")
            continue

        parsed = parse_normas_base(normas_path)
        sections = parsed["sections"]

        for area, skill_name in SKILL_PATHS:
            gen = GENERATORS.get(skill_name)
            if not gen:
                errors.append(f"Sin generador: {skill_name}")
                continue
            out_dir = JURIS_BASE / slug / area / skill_name
            out_path = out_dir / "SKILL.md"
            try:
                content = gen(slug, sections)
                out_dir.mkdir(parents=True, exist_ok=True)
                out_path.write_text(content, encoding="utf-8")
                created += 1
                print(f"  OK  {slug}/{area}/{skill_name}")
            except Exception as exc:
                errors.append(f"{slug}/{skill_name}: {exc}")

        # system-prompt abogado-general
        sp_dir = JURIS_BASE / slug / "system-prompts"
        sp_path = sp_dir / "abogado-general.md"
        if not sp_path.exists():
            try:
                sp_dir.mkdir(parents=True, exist_ok=True)
                sp_path.write_text(generate_system_prompt(slug, sections), encoding="utf-8")
                created += 1
                print(f"  OK  {slug}/system-prompts/abogado-general.md")
            except Exception as exc:
                errors.append(f"{slug}/system-prompt: {exc}")

    print()
    print("Generando skills derecho-anglosajon...")
    print()
    anglo = generate_anglosajon_skills()
    created += anglo

    expected_skills = len(TARGET_SLUGS) * len(SKILL_PATHS)
    print()
    print(f"Skills sustantivos generados: {expected_skills} (objetivo)")
    print(f"Archivos escritos en esta ejecución: {created}")
    print(f"Skills anglosajón: {anglo}")
    if errors:
        print("Errores:")
        for err in errors:
            print(f"  - {err}")


if __name__ == "__main__":
    main()
