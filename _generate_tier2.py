"""
Genera skills transversales Tier 2 para jurisdicciones con solo normas-base.md.
Estructura basada en jurisdicciones/mexico/analisis-transversal/.
"""
from __future__ import annotations

import re
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent
JURIS_BASE = WORKSPACE / "jurisdicciones"

SKILLS = [
    "investigacion-juridica",
    "analisis-jurisprudencial",
    "elaboracion-concepto-juridico",
    "due-diligence-general",
    "analisis-archivo-documentos",
]

JURISDICTION_SLUGS = [
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

INSTABILITY_EXTRA = (
    "Este skill requiere verificación especial. La legislación de {country} "
    "puede haber sido modificada significativamente. Consultar con abogado "
    "local antes de cualquier aplicación práctica."
)

JURISDICTION_DATA: dict[str, dict] = {
    "bolivia": {
        "name": "Bolivia",
        "adjective": "boliviano",
        "instability": False,
        "system_note": (
            "Estado plurinacional: coexisten ordenamiento estatal y derecho "
            "indígena originario campesino (DIOC). Verificar si el caso "
            "involucra jurisdicción ordinaria o justicia indígena originaria."
        ),
        "constitutional_action": "acción de amparo constitucional",
        "constitutional_ref": "Art. 128",
        "courts": "Tribunal Constitucional Plurinacional · Corte Suprema de Justicia · tribunales superiores",
        "main_court": "Corte Suprema de Justicia",
        "constitutional_court": "Tribunal Constitucional Plurinacional",
        "precedent_mechanism": "jurisprudencia de la Corte Suprema y del Tribunal Constitucional",
        "sources": [
            ("Gaceta Oficial de Bolivia", "gaceta.gob.bo", "Vigencia de leyes y decretos"),
            ("Órgano Judicial", "organojudicial.gob.bo", "Sentencias y jurisprudencia"),
            ("Asamblea Legislativa Plurinacional", None, "Proyectos de ley y antecedentes legislativos"),
        ],
        "dd_sources": [
            ("Órgano Judicial", "Procesos judiciales", "organojudicial.gob.bo"),
            ("Fundempresa / Registro de Comercio", "Existencia y representación de sociedades", "[VERIFICAR]"),
            ("Servicio de Impuestos Nacionales (SIN)", "Situación fiscal", "[VERIFICAR]"),
            ("Derechos Reales", "Inmuebles y gravámenes", "[VERIFICAR]"),
            ("OFAC / listas internacionales", "Restricciones", "Listas de control"),
        ],
        "terminology_avoid": ["tutela", "injunction", "due process", "writ of mandamus"],
        "terminology_prefer": ["amparo constitucional", "nulidad", "resolución de contrato", "prescripción", "Ley General del Trabajo"],
    },
    "ecuador": {
        "name": "Ecuador",
        "adjective": "ecuatoriano",
        "instability": False,
        "system_note": (
            "Ordenamiento unitario. El COGEP (2015) unificó los procedimientos "
            "civiles. Ecuador usa el dólar estadounidense como moneda oficial."
        ),
        "constitutional_action": "acción de protección",
        "constitutional_ref": "Art. 88",
        "courts": "Corte Constitucional · Corte Nacional de Justicia · tribunales superiores",
        "main_court": "Corte Nacional de Justicia",
        "constitutional_court": "Corte Constitucional",
        "precedent_mechanism": "jurisprudencia vinculante de la Corte Constitucional y criterio de la Corte Nacional",
        "sources": [
            ("Registro Oficial", "registroficial.gob.ec", "Vigencia de leyes y decretos"),
            ("Función Judicial", "funcionjudicial.gob.ec", "Sentencias y jurisprudencia"),
            ("Asamblea Nacional", "asambleanacional.gob.ec", "Proyectos de ley"),
        ],
        "dd_sources": [
            ("Función Judicial", "Procesos judiciales", "funcionjudicial.gob.ec"),
            ("Superintendencia de Compañías", "Existencia y representación societaria", "[VERIFICAR: supercias.gob.ec]"),
            ("Servicio de Rentas Internas (SRI)", "Situación fiscal", "[VERIFICAR: sri.gob.ec]"),
            ("Registro de la Propiedad", "Inmuebles (por cantón)", "Verificar cantón correspondiente"),
            ("OFAC / listas internacionales", "Restricciones", "Listas de control"),
        ],
        "terminology_avoid": ["tutela", "injunction", "amparo mexicano"],
        "terminology_prefer": ["acción de protección", "COGEP", "nulidad", "resolución de contrato", "Código del Trabajo"],
    },
    "venezuela": {
        "name": "Venezuela",
        "adjective": "venezolano",
        "instability": True,
        "system_note": (
            "Inestabilidad normativa severa: verificar vigencia de TODA norma con "
            "abogado local. Muchas normas han sido modificadas por decretos de "
            "emergencia o leyes de habilitación."
        ),
        "constitutional_action": "acción de amparo",
        "constitutional_ref": "Art. 27",
        "courts": "Tribunal Supremo de Justicia (TSJ) · Sala Constitucional · tribunales superiores",
        "main_court": "Tribunal Supremo de Justicia (TSJ)",
        "constitutional_court": "Sala Constitucional del TSJ",
        "precedent_mechanism": "jurisprudencia del TSJ y de la Sala Constitucional [VERIFICAR alcance vinculante]",
        "sources": [
            ("Gaceta Oficial", "gacetaoficial.gob.ve", "Vigencia de leyes y decretos"),
            ("TSJ", "tsj.gob.ve", "Sentencias y jurisprudencia"),
            ("Asamblea Nacional", None, "Proyectos de ley [VERIFICAR acceso]"),
        ],
        "dd_sources": [
            ("TSJ / tribunales", "Procesos judiciales", "[VERIFICAR: tsj.gob.ve]"),
            ("Registro Mercantil", "Existencia y representación de sociedades", "[VERIFICAR]"),
            ("SENIAT", "Situación fiscal", "[VERIFICAR]"),
            ("Registro de Títulos", "Inmuebles", "[VERIFICAR]"),
            ("OFAC / listas internacionales", "Restricciones", "Listas de control"),
        ],
        "terminology_avoid": ["tutela", "injunction", "due process"],
        "terminology_prefer": ["amparo", "LOTTT", "nulidad", "resolución de contrato", "prescripción"],
    },
    "paraguay": {
        "name": "Paraguay",
        "adjective": "paraguayo",
        "instability": False,
        "system_note": (
            "Ordenamiento unitario y bilingüe (español y guaraní). Los documentos "
            "en guaraní tienen validez jurídica."
        ),
        "constitutional_action": "acción de amparo",
        "constitutional_ref": "Art. 134",
        "courts": "Corte Suprema de Justicia · tribunales superiores",
        "main_court": "Corte Suprema de Justicia",
        "constitutional_court": "Corte Suprema de Justicia (sala constitucional)",
        "precedent_mechanism": "jurisprudencia de la Corte Suprema de Justicia",
        "sources": [
            ("Diario Oficial", "diariooficial.gov.py", "Vigencia de leyes y decretos"),
            ("Poder Judicial", "poderjudicial.gov.py", "Sentencias y jurisprudencia"),
            ("Congreso Nacional", "congreso.gov.py", "Proyectos de ley"),
        ],
        "dd_sources": [
            ("Poder Judicial", "Procesos judiciales", "poderjudicial.gov.py"),
            ("SUACE / Registro Público", "Existencia y representación de sociedades", "[VERIFICAR]"),
            ("SET", "Situación fiscal", "[VERIFICAR]"),
            ("Registro Público de la Propiedad", "Inmuebles", "[VERIFICAR]"),
            ("OFAC / listas internacionales", "Restricciones", "Listas de control"),
        ],
        "terminology_avoid": ["tutela", "injunction", "writ of mandamus"],
        "terminology_prefer": ["amparo", "CPC", "nulidad", "resolución de contrato", "Código Laboral"],
    },
    "uruguay": {
        "name": "Uruguay",
        "adjective": "uruguayo",
        "instability": False,
        "system_note": (
            "Ordenamiento unitario con sistema de consejos de salarios por sector "
            "muy desarrollado. El BPS gestiona la seguridad social."
        ),
        "constitutional_action": "acción de amparo",
        "constitutional_ref": "Ley 16.011",
        "courts": "Suprema Corte de Justicia · tribunales superiores",
        "main_court": "Suprema Corte de Justicia",
        "constitutional_court": "Suprema Corte de Justicia",
        "precedent_mechanism": "jurisprudencia de la Suprema Corte de Justicia",
        "sources": [
            ("Diario Oficial", "impo.com.uy", "Vigencia de leyes y decretos"),
            ("Poder Judicial", "pj.gov.uy", "Sentencias y jurisprudencia"),
            ("Parlamento", "parlamento.gub.uy", "Proyectos de ley"),
        ],
        "dd_sources": [
            ("Poder Judicial", "Procesos judiciales", "pj.gov.uy"),
            ("DGI / Registro Nacional de Comercio", "Existencia y representación societaria", "[VERIFICAR]"),
            ("DGI", "Situación fiscal", "[VERIFICAR]"),
            ("Registro de la Propiedad", "Inmuebles", "[VERIFICAR]"),
            ("OFAC / listas internacionales", "Restricciones", "Listas de control"),
        ],
        "terminology_avoid": ["tutela", "injunction", "due process"],
        "terminology_prefer": ["amparo", "CGP", "nulidad", "despido abusivo", "Ley 16.060"],
    },
    "panama": {
        "name": "Panamá",
        "adjective": "panameño",
        "instability": False,
        "system_note": (
            "Influencia española y estadounidense. El balboa equivale al dólar "
            "estadounidense. Verificar normativa especial de Zona Libre de Colón "
            "y del centro financiero internacional."
        ),
        "constitutional_action": "acción de amparo de garantías",
        "constitutional_ref": "Art. 50",
        "courts": "Corte Suprema de Justicia · tribunales superiores",
        "main_court": "Corte Suprema de Justicia",
        "constitutional_court": "Corte Suprema de Justicia",
        "precedent_mechanism": "jurisprudencia de la Corte Suprema de Justicia",
        "sources": [
            ("Gaceta Oficial", "gacetaoficial.gob.pa", "Vigencia de leyes y decretos"),
            ("Órgano Judicial", "organojudicial.gob.pa", "Sentencias y jurisprudencia"),
            ("Asamblea Nacional", "asamblea.gob.pa", "Proyectos de ley"),
        ],
        "dd_sources": [
            ("Órgano Judicial", "Procesos judiciales", "organojudicial.gob.pa"),
            ("Registro Público", "Existencia y representación de sociedades (Ley 32)", "[VERIFICAR: registropublico.gob.pa]"),
            ("DGI", "Situación fiscal", "[VERIFICAR]"),
            ("Registro Público de la Propiedad", "Inmuebles", "[VERIFICAR]"),
            ("OFAC / listas internacionales", "Restricciones", "Listas de control"),
        ],
        "terminology_avoid": ["tutela", "injunction colombiano"],
        "terminology_prefer": ["amparo de garantías", "nulidad", "Ley 32", "Código de Trabajo", "prescripción"],
    },
    "costa-rica": {
        "name": "Costa Rica",
        "adjective": "costarricense",
        "instability": False,
        "system_note": (
            "Ordenamiento unitario. La Sala Constitucional (Sala IV) es "
            "especialmente activa en derechos fundamentales."
        ),
        "constitutional_action": "recurso de amparo",
        "constitutional_ref": "Art. 48",
        "courts": "Sala Constitucional (Sala IV) · Corte Suprema de Justicia · tribunales superiores",
        "main_court": "Corte Suprema de Justicia",
        "constitutional_court": "Sala Constitucional (Sala IV)",
        "precedent_mechanism": "jurisprudencia de la Sala Constitucional y de la Corte Suprema",
        "sources": [
            ("La Gaceta", "gaceta.go.cr", "Vigencia de leyes y decretos"),
            ("Poder Judicial", "poder-judicial.go.cr", "Sentencias y jurisprudencia"),
            ("Asamblea Legislativa", "asamblea.go.cr", "Proyectos de ley"),
        ],
        "dd_sources": [
            ("Poder Judicial", "Procesos judiciales", "poder-judicial.go.cr"),
            ("Registro Nacional", "Existencia y representación societaria", "[VERIFICAR: registronacional.go.cr]"),
            ("Hacienda / Tributación Directa", "Situación fiscal", "[VERIFICAR]"),
            ("Registro Nacional — Bienes Inmuebles", "Inmuebles", "[VERIFICAR]"),
            ("OFAC / listas internacionales", "Restricciones", "Listas de control"),
        ],
        "terminology_avoid": ["tutela", "injunction", "writ of mandamus"],
        "terminology_prefer": ["amparo", "Sala IV", "nulidad", "Código de Trabajo", "cesantía"],
    },
    "nicaragua": {
        "name": "Nicaragua",
        "adjective": "nicaragüense",
        "instability": True,
        "system_note": (
            "Verificar toda norma con abogado local — situación institucional "
            "compleja e inestabilidad reciente."
        ),
        "constitutional_action": "acción de amparo",
        "constitutional_ref": "Art. 188",
        "courts": "Corte Suprema de Justicia · tribunales superiores",
        "main_court": "Corte Suprema de Justicia",
        "constitutional_court": "Corte Suprema de Justicia",
        "precedent_mechanism": "jurisprudencia de la Corte Suprema de Justicia [VERIFICAR]",
        "sources": [
            ("La Gaceta", "lagaceta.gob.ni", "Vigencia de leyes y decretos"),
            ("Poder Judicial", "poderjudicial.gob.ni", "Sentencias y jurisprudencia"),
            ("Asamblea Nacional", None, "Proyectos de ley [VERIFICAR]"),
        ],
        "dd_sources": [
            ("Poder Judicial", "Procesos judiciales", "[VERIFICAR: poderjudicial.gob.ni]"),
            ("MIFIC / Registro Mercantil", "Existencia y representación de sociedades", "[VERIFICAR]"),
            ("DGI", "Situación fiscal", "[VERIFICAR]"),
            ("Registro Público", "Inmuebles", "[VERIFICAR]"),
            ("OFAC / listas internacionales", "Restricciones", "Listas de control"),
        ],
        "terminology_avoid": ["tutela", "injunction", "due process"],
        "terminology_prefer": ["amparo", "nulidad", "Código del Trabajo", "décimo tercer mes", "prescripción"],
    },
    "honduras": {
        "name": "Honduras",
        "adjective": "hondureño",
        "instability": False,
        "system_note": "Ordenamiento unitario. Verificar reformas laborales recientes (2022-2025).",
        "constitutional_action": "acción de amparo",
        "constitutional_ref": "Arts. 183-185",
        "courts": "Corte Suprema de Justicia · tribunales superiores",
        "main_court": "Corte Suprema de Justicia",
        "constitutional_court": "Corte Suprema de Justicia",
        "precedent_mechanism": "jurisprudencia de la Corte Suprema de Justicia",
        "sources": [
            ("La Gaceta", "la-gaceta.hn", "Vigencia de leyes y decretos"),
            ("Poder Judicial", "poderjudicial.gob.hn", "Sentencias y jurisprudencia"),
            ("Congreso Nacional", "congresonacional.hn", "Proyectos de ley"),
        ],
        "dd_sources": [
            ("Poder Judicial", "Procesos judiciales", "poderjudicial.gob.hn"),
            ("Registro Mercantil", "Existencia y representación de sociedades", "[VERIFICAR]"),
            ("SAR", "Situación fiscal", "[VERIFICAR]"),
            ("Instituto de la Propiedad", "Inmuebles", "[VERIFICAR]"),
            ("OFAC / listas internacionales", "Restricciones", "Listas de control"),
        ],
        "terminology_avoid": ["tutela", "injunction", "writ of mandamus"],
        "terminology_prefer": ["amparo", "nulidad", "auxilio de cesantía", "Código del Trabajo", "prescripción"],
    },
    "el-salvador": {
        "name": "El Salvador",
        "adjective": "salvadoreño",
        "instability": False,
        "system_note": (
            "Ordenamiento unitario. Usa el dólar estadounidense como moneda "
            "oficial desde 2001. Verificar implicaciones contractuales de "
            "Bitcoin como moneda de curso legal (2021)."
        ),
        "constitutional_action": "acción de amparo",
        "constitutional_ref": "Art. 247",
        "courts": "Corte Suprema de Justicia · tribunales superiores",
        "main_court": "Corte Suprema de Justicia",
        "constitutional_court": "Sala de lo Constitucional",
        "precedent_mechanism": "jurisprudencia de la Corte Suprema de Justicia",
        "sources": [
            ("Diario Oficial", "diariooficial.gob.sv", "Vigencia de leyes y decretos"),
            ("Órgano Judicial", "organojudicial.gob.sv", "Sentencias y jurisprudencia"),
            ("Asamblea Legislativa", "asamblea.gob.sv", "Proyectos de ley"),
        ],
        "dd_sources": [
            ("Órgano Judicial", "Procesos judiciales", "organojudicial.gob.sv"),
            ("CNR / Registro de Comercio", "Existencia y representación de sociedades", "[VERIFICAR]"),
            ("Ministerio de Hacienda", "Situación fiscal", "[VERIFICAR]"),
            ("Centro Nacional de Registros", "Inmuebles", "[VERIFICAR]"),
            ("OFAC / listas internacionales", "Restricciones", "Listas de control"),
        ],
        "terminology_avoid": ["tutela", "injunction", "due process"],
        "terminology_prefer": ["amparo", "nulidad", "Código de Trabajo", "aguinaldo", "prescripción"],
    },
    "guatemala": {
        "name": "Guatemala",
        "adjective": "guatemalteco",
        "instability": False,
        "system_note": (
            "Alta proporción de población indígena — en comunidades puede aplicar "
            "derecho consuetudinario maya. Verificar Ley de Amparo además de la "
            "Constitución."
        ),
        "constitutional_action": "acción de amparo",
        "constitutional_ref": "Arts. 265-272 + Ley de Amparo",
        "courts": "Corte de Constitucionalidad · Corte Suprema de Justicia · tribunales superiores",
        "main_court": "Corte Suprema de Justicia",
        "constitutional_court": "Corte de Constitucionalidad",
        "precedent_mechanism": "jurisprudencia de la Corte de Constitucionalidad y de la Corte Suprema",
        "sources": [
            ("Diario de Centro América", "diariooficial.gob.gt", "Vigencia de leyes y decretos"),
            ("Órgano Judicial", "oj.gob.gt", "Sentencias y jurisprudencia"),
            ("Congreso de la República", "congreso.gob.gt", "Proyectos de ley"),
        ],
        "dd_sources": [
            ("Órgano Judicial", "Procesos judiciales", "oj.gob.gt"),
            ("Registro Mercantil", "Existencia y representación de sociedades", "[VERIFICAR]"),
            ("SAT", "Situación fiscal", "[VERIFICAR]"),
            ("Registro General de la Propiedad", "Inmuebles", "[VERIFICAR]"),
            ("OFAC / listas internacionales", "Restricciones", "Listas de control"),
        ],
        "terminology_avoid": ["tutela", "injunction", "writ of mandamus"],
        "terminology_prefer": ["amparo", "nulidad", "Código de Trabajo", "SMO", "prescripción"],
    },
    "cuba": {
        "name": "Cuba",
        "adjective": "cubano",
        "instability": True,
        "system_note": (
            "Sistema de derecho civil con particularidades socialistas. "
            "Empresas estatales y privadas (MIPYMES, trabajo por cuenta propia) "
            "coexisten — verificar forma jurídica. Sistema en transformación acelerada."
        ),
        "constitutional_action": "recursos constitucionales [VERIFICAR mecanismo vigente]",
        "constitutional_ref": "Constitución 2019",
        "courts": "Tribunal Supremo Popular · tribunales provinciales",
        "main_court": "Tribunal Supremo Popular",
        "constitutional_court": "Tribunal Supremo Popular",
        "precedent_mechanism": "criterio del Tribunal Supremo Popular [VERIFICAR]",
        "sources": [
            ("Gaceta Oficial", "gacetaoficial.gob.cu", "Vigencia de leyes y decretos"),
            ("Tribunal Supremo Popular", None, "Sentencias y jurisprudencia [VERIFICAR]"),
            ("Asamblea Nacional", None, "Proyectos de ley [VERIFICAR]"),
        ],
        "dd_sources": [
            ("Tribunales populares", "Procesos judiciales", "[VERIFICAR]"),
            ("Registro Mercantil / ONEI", "Existencia y representación de entidades", "[VERIFICAR]"),
            ("ONAT", "Situación fiscal", "[VERIFICAR]"),
            ("Registro de la Propiedad", "Inmuebles", "[VERIFICAR]"),
            ("OFAC / listas internacionales", "Restricciones", "Listas de control"),
        ],
        "terminology_avoid": ["tutela", "injunction", "LLC offshore"],
        "terminology_prefer": ["nulidad", "Código Civil", "Código de Trabajo", "MIPYMES", "trabajo por cuenta propia"],
    },
    "republica-dominicana": {
        "name": "República Dominicana",
        "adjective": "dominicano",
        "instability": False,
        "system_note": (
            "Fuerte influencia napoleónica — el Código Civil es similar al "
            "francés de 1804. Verificar Ley 141-15 de Reestructuración Mercantil "
            "para empresas en dificultad."
        ),
        "constitutional_action": "acción de amparo",
        "constitutional_ref": "Art. 72",
        "courts": "Suprema Corte de Justicia · tribunales superiores",
        "main_court": "Suprema Corte de Justicia",
        "constitutional_court": "Suprema Corte de Justicia",
        "precedent_mechanism": "jurisprudencia de la Suprema Corte de Justicia",
        "sources": [
            ("Gaceta Oficial", "gacetaoficial.gob.do", "Vigencia de leyes y decretos"),
            ("Poder Judicial", "poderjudicial.gob.do", "Sentencias y jurisprudencia"),
            ("Congreso Nacional", "congreso.gob.do", "Proyectos de ley"),
        ],
        "dd_sources": [
            ("Poder Judicial", "Procesos judiciales", "poderjudicial.gob.do"),
            ("Cámara de Comercio / Registro Mercantil", "Existencia y representación de sociedades", "[VERIFICAR]"),
            ("DGII", "Situación fiscal", "[VERIFICAR: dgii.gov.do]"),
            ("Registro de Títulos", "Inmuebles", "[VERIFICAR]"),
            ("OFAC / listas internacionales", "Restricciones", "Listas de control"),
        ],
        "terminology_avoid": ["tutela", "injunction", "writ of mandamus"],
        "terminology_prefer": ["amparo", "nulidad", "Código de Trabajo", "regalía pascual", "cesantía"],
    },
    "puerto-rico": {
        "name": "Puerto Rico",
        "adjective": "puertorriqueño",
        "instability": False,
        "federal_note": (
            "Sistema híbrido civil/common law: derecho privado (civil, familia, "
            "contratos) sigue tradición civil española; derecho federal de EE.UU. "
            "aplica plenamente; derecho procesal mezcla ambos sistemas; derecho "
            "laboral: coexisten ley local y federal. SIEMPRE identificar si la "
            "norma aplicable es estatal (PR) o federal (EE.UU.)."
        ),
        "system_note": (
            "Territorio de EE.UU. con sistema jurídico híbrido único. Español e "
            "inglés tienen igual validez oficial. La quiebra se rige por derecho "
            "federal (Título 11 USC)."
        ),
        "constitutional_action": "recursos constitucionales estatales y federales",
        "constitutional_ref": "Constitución ELA 1952 + Constitución EE.UU.",
        "courts": "Tribunal Supremo de Puerto Rico · tribunales federales (Distrito de PR, 1er Circuito)",
        "main_court": "Tribunal Supremo de Puerto Rico",
        "constitutional_court": "Tribunal Supremo de Puerto Rico",
        "precedent_mechanism": "precedente del Tribunal Supremo de PR y precedente federal vinculante de circuito/SCOTUS",
        "sources": [
            ("Registro de Legislación de PR", "oslpr.org", "Leyes locales vigentes"),
            ("Tribunal Supremo de PR", "poderjudicial.pr", "Sentencias estatales"),
            ("PACER / tribunales federales", None, "Sentencias federales [VERIFICAR]"),
            ("Congress.gov / US Code", None, "Legislación federal aplicable"),
        ],
        "dd_sources": [
            ("Tribunales estatales y federales", "Procesos judiciales", "[VERIFICAR: poderjudicial.pr / pacer]"),
            ("Departamento de Estado — Registro de Corporaciones", "Existencia y representación societaria", "[VERIFICAR]"),
            ("Departamento de Hacienda de PR", "Situación fiscal local", "[VERIFICAR]"),
            ("Registro de la Propiedad", "Inmuebles", "[VERIFICAR]"),
            ("OFAC / listas internacionales", "Restricciones", "Listas de control"),
        ],
        "terminology_avoid": ["tutela colombiana", "amparo mexicano"],
        "terminology_prefer": ["descubrimiento de prueba", "sentencia sumaria", "Ley 80", "Código Civil de PR", "NLRA / FLSA"],
    },
}


def parse_normas_base(path: Path) -> dict:
    """Extrae secciones y artículos de normas-base.md."""
    text = path.read_text(encoding="utf-8")
    sections: list[dict] = []
    current: dict | None = None

    for line in text.splitlines():
        if line.startswith("## "):
            title = line[3:].strip()
            if any(skip in title.upper() for skip in ("ADVERTENCIA", "NOTAS IMPORTANTES")):
                current = None
                continue
            current = {"title": title, "articles": []}
            sections.append(current)
        elif current and line.strip().startswith("- "):
            current["articles"].append(line.strip()[2:])

    return {"sections": sections}


def shorten_law_name(title: str) -> str:
    """Abrevia nombres de leyes para legal-basis."""
    patterns = [
        (r"Constitución.*", lambda m: "Constitución"),
        (r"Código Civil.*", lambda m: "Código Civil"),
        (r"Código de Procedimiento Civil.*", lambda m: "CPC"),
        (r"Código Procesal Civil.*", lambda m: "CPC"),
        (r"Código Orgánico General de Procesos.*", lambda m: "COGEP"),
        (r"Código General del Proceso.*", lambda m: "CGP"),
        (r"Reglas de Procedimiento Civil.*", lambda m: "Reglas Civiles PR"),
        (r"Código Civil de Puerto Rico.*", lambda m: "CC PR 2020"),
        (r"Código de Trabajo.*", lambda m: "Código de Trabajo"),
        (r"Código del Trabajo.*", lambda m: "Código del Trabajo"),
        (r"Código Laboral.*", lambda m: "Código Laboral"),
        (r"Ley General del Trabajo.*", lambda m: "Ley General del Trabajo"),
        (r"Ley Orgánica del Trabajo.*", lambda m: "LOTTT"),
        (r"Ley de Relaciones del Trabajo.*", lambda m: "Ley 130/1945"),
        (r"Ley de Relaciones Laborales.*", lambda m: "Ley Relaciones Laborales"),
        (r"Ley de Compañías.*", lambda m: "Ley de Compañías"),
        (r"Ley de Sociedades Comerciales.*", lambda m: "Ley 16.060"),
        (r"Ley Núm\. 80.*", lambda m: "Ley 80/1976"),
        (r"Constitución de EE\.UU\..*", lambda m: "Constitución EE.UU."),
        (r"National Labor Relations Act.*", lambda m: "NLRA"),
        (r"Fair Labor Standards Act.*", lambda m: "FLSA"),
    ]
    for pattern, repl in patterns:
        if re.match(pattern, title, re.IGNORECASE):
            return repl(title)
    # fallback: primeras palabras significativas
    return title.split("—")[0].split("(")[0].strip()[:40]


def find_procedural_section(sections: list[dict]) -> dict | None:
    keywords = ("procedimiento", "procesal", "procesos", "cogep", "cgp", "reglas de procedimiento")
    for sec in sections:
        title_lower = sec["title"].lower()
        if any(kw in title_lower for kw in keywords):
            return sec
    return None


def extract_articles_ref(section: dict | None, fallback: str = "[VERIFICAR]") -> str:
    if not section:
        return fallback
    short = shorten_law_name(section["title"])
    for art_line in section["articles"]:
        if re.search(r"Arts?\.|Reglas?|Art\.", art_line, re.IGNORECASE):
            match = re.search(r"(Arts?\.|Reglas?)\s*[\d\-\s,]+", art_line, re.IGNORECASE)
            if match:
                return f"{short} {match.group(0)}"
    return short


def build_legal_basis(sections: list[dict], skill: str) -> str:
    names = [shorten_law_name(s["title"]) for s in sections]
    if not names:
        return "[VERIFICAR]"

    proc = find_procedural_section(sections)
    proc_ref = extract_articles_ref(proc)

    if skill == "investigacion-juridica":
        parts = names[:5]
    elif skill == "analisis-jurisprudencial":
        const = names[0] if names else "Constitución"
        parts = [const, proc_ref]
    elif skill == "elaboracion-concepto-juridico":
        parts = [n for n in names if n not in ("Constitución EE.UU.",)][:5]
    elif skill == "due-diligence-general":
        parts = [n for n in names if "Constitución" not in n or "EE.UU." in n][:4]
    elif skill == "analisis-archivo-documentos":
        parts = [proc_ref]
        if names[0].startswith("Constitución"):
            parts.append(names[0])
    else:
        parts = names[:4]

    # deduplicate preserving order
    seen: set[str] = set()
    unique = []
    for p in parts:
        if p not in seen:
            seen.add(p)
            unique.append(p)
    return " · ".join(unique)


def format_source_row(name: str, url: str | None, purpose: str) -> str:
    if url:
        return f"| {name} — [VERIFICAR: {url}] | {purpose} |"
    return f"| {name} — [VERIFICAR] | {purpose} |"


def format_dd_row(name: str, what: str, note: str) -> str:
    if note.startswith("[VERIFICAR"):
        return f"| {name} | {what} | {note} |"
    return f"| {name} | {what} | [VERIFICAR: {note}] |"


def advertencia_section(country: str, instability: bool) -> str:
    base = f"""## Advertencia

Este skill aplica legislación de {country}. No usar para otras jurisdicciones.
Verificar la vigencia de las normas citadas con un abogado local antes de
aplicar este skill en la práctica profesional. La legislación puede haber
sido modificada con posterioridad a la fecha de verificación indicada.
[VERIFICAR] indica normas o fuentes que requieren confirmación adicional."""
    if instability:
        base += f"\n{INSTABILITY_EXTRA.format(country=country)}"
    return base


def system_warning_block(j: dict) -> str:
    note = j.get("federal_note") or j.get("system_note", "")
    label = "Advertencia del sistema — derecho federal y estatal" if j.get("federal_note") else "Advertencia del sistema"
    return f"### {label}\n{note}"


def generate_investigacion(slug: str, j: dict, legal_basis: str) -> str:
    country = j["name"]
    adj = j["adjective"]
    sources_table = "\n".join(format_source_row(*s) for s in j["sources"])
    avoid = ", ".join(f'"{t}"' for t in j["terminology_avoid"])
    prefer = ", ".join(f'"{t}"' for t in j["terminology_prefer"])
    primary_source = j["sources"][0]
    primary_label = f"{primary_source[0]} — [VERIFICAR: {primary_source[1]}]" if primary_source[1] else f"{primary_source[0]} — [VERIFICAR]"

    return f"""---
name: investigacion-juridica
description: >
  Guía y ejecuta investigación jurídica sobre derecho {adj}. Usar cuando el usuario necesite investigar un tema legal, buscar normas vigentes, localizar jurisprudencia, armar un plan de investigación o verificar vigencia normativa en {country}. Específico para {country}. NO usar para otras jurisdicciones.
metadata:
  author: Juan David Vanegas Roldán
  version: "1.0"
  jurisdiction: {country}
  legal-basis: {legal_basis}
  last-verified: "2025-06"
  area: Análisis Transversal
  difficulty: intermedio
  output-type: mixto
  warning: "Verificar vigencia de normas con abogado local antes de usar"
---

# Investigación Jurídica — {country}

Eres un experto en metodología de investigación jurídica de {country}. Conoces las fuentes oficiales del ordenamiento, las bases de datos de las altas corporaciones y las técnicas de búsqueda jurisprudencial aplicables al sistema jurídico {adj}.

## 1. Rol

Tu función es **investigar, localizar, verificar y organizar** el material jurídico que sustenta un concepto, demanda o estrategia. Si el usuario necesita analizar una sentencia en profundidad, deriva mentalmente al skill de análisis jurisprudencial. Si necesita redactar el concepto final, deriva al skill de elaboración de concepto jurídico.

---

## 2. Información requerida antes de actuar

1. **Tema o problema jurídico**
2. **Área del derecho**
3. **Propósito** — concepto, demanda, {j["constitutional_action"]}, estrategia procesal, due diligence
4. **Profundidad** — exploratoria / estándar / exhaustiva
5. **Corporaciones de interés** (si las conoce)
6. **Restricciones temporales** (si aplica)

Si falta el tema o el propósito, pregunta antes de continuar.

---

## 3. Modos de operación

### Modo A — Plan de investigación
Hoja de ruta: qué buscar, dónde, en qué orden.

### Modo B — Investigación normativa
Localizar y verificar legislación aplicable.

### Modo C — Investigación jurisprudencial
Estrategia de búsqueda y organización de sentencias.

### Modo D — Investigación integral
Normas + jurisprudencia + doctrina + antecedentes administrativos.

### Modo E — Verificación de fuentes
Confirmar vigencia y aplicabilidad de normas o sentencias citadas.

---

## 4. Conocimiento especializado

{system_warning_block(j)}

### Jerarquía de fuentes en {country}

| Nivel | Fuente |
|---|---|
| 1 | Constitución |
| 2 | Leyes orgánicas y estatutarias [VERIFICAR por materia] |
| 3 | Leyes ordinarias y códigos |
| 4 | Reglamentos y decretos de desarrollo |
| 5 | Jurisprudencia de altas corporaciones ({j["constitutional_court"]}, tribunales superiores) |
| 6 | Doctrina administrativa de reguladores |
| 7 | Doctrina académica |

### Bases de datos y fuentes oficiales

| Fuente | Para qué sirve |
|---|---|
{sources_table}
| {j["constitutional_court"]} | {j["constitutional_action"].capitalize()} y control constitucional |

### Metodología — 6 pasos

1. **Delimitar el problema jurídico** — supuesto de hecho + tensión jurídica + pregunta de cierre
2. **Identificar marco normativo primario** — consultar {primary_label} y `normas-base.md` de {country}
3. **Rastrear normas conexas** — leyes especiales, reglamentos, tratados [VERIFICAR]
4. **Diseñar búsqueda jurisprudencial** — usar terminología de {country}, no anglosajona
5. **Complementar con doctrina y fuentes administrativas**
6. **Verificar y organizar hallazgos** — vigencia, precedentes superados, distinciones fácticas

### Terminología de búsqueda

- Evitar: {avoid}
- Preferir: {prefer}

### Verificación de vigencia

| Situación | Qué verificar |
|---|---|
| Ley modificada | Texto consolidado vigente, no el original |
| Sentencia de inconstitucionalidad | Alcance: artículo completo o aparte |
| Derogatoria | Expresa o tácita por ley posterior |
| Vacío normativo | Señalarlo — no inventar norma |

---

## 5. Formato de respuesta

Usar estructura de plan de investigación o informe según el modo, con tablas de normativa, jurisprudencia y bibliografía consultada.

---

## 6. Advertencias obligatorias

- *"Las fuentes deben verificarse directamente en las bases oficiales indicadas."*
- *"Este informe puede no reflejar normas o sentencias publicadas con posterioridad."*
- *"No constituye concepto jurídico ni asesoría vinculante."*

---

## 7. Errores comunes que debes evitar

- No citar normas sin verificar vigencia
- No usar terminología anglosajona en bases de datos locales
- No presentar jurisprudencia de instancia como precedente obligatorio nacional
- No mezclar legislación de otros países
- No inventar sentencias o artículos — usar [VERIFICAR]
- No investigar solo norma sustantiva sin la procesal aplicable

{advertencia_section(country, j["instability"])}
"""


def generate_jurisprudencial(slug: str, j: dict, legal_basis: str) -> str:
    country = j["name"]
    adj = j["adjective"]
    return f"""---
name: analisis-jurisprudencial
description: >
  Analiza sentencias de {country} y construye líneas jurisprudenciales. Usar cuando el usuario necesite entender una sentencia, extraer la ratio decidendi, identificar precedentes o evaluar aplicabilidad a un caso concreto en {country}. NO usar para otras jurisdicciones.
metadata:
  author: Juan David Vanegas Roldán
  version: "1.0"
  jurisdiction: {country}
  legal-basis: {legal_basis}
  last-verified: "2025-06"
  area: Análisis Transversal
  difficulty: avanzado
  output-type: análisis
  warning: "Verificar vigencia de normas con abogado local antes de usar"
---

# Análisis Jurisprudencial — {country}

Eres un experto en análisis jurisprudencial de {country} con dominio de {j["courts"]}. Conoces la distinción entre ratio decidendi y obiter dicta y la jerarquía del precedente en el sistema jurídico {adj}.

## 1. Rol

Analizar sentencias concretas o construir líneas jurisprudenciales sobre un tema. Identificar el modo (A: sentencia específica / B: línea jurisprudencial) según la solicitud.

---

## 2. Información requerida

- Texto o referencia de la sentencia (Modo A)
- Tema jurídico y corporación de interés (Modo B)
- Caso concreto del usuario para evaluar aplicabilidad (si aplica)

---

## 3. Modos de operación

### Modo A — Análisis de sentencia específica
Identificación, problema jurídico, ratio decidendi, obiter dicta, decisum, precedentes citados, posición en la línea, aplicabilidad al caso.

### Modo B — Construcción de línea jurisprudencial
Definición del problema, sentencias hito cronológicas, estado actual, síntesis aplicable.

---

## 4. Conocimiento especializado

{system_warning_block(j)}

### {j["constitutional_court"]}
- Competencia en materia constitucional y {j["constitutional_action"]}
- Precedente constitucional [VERIFICAR alcance vinculante]

### Tribunales superiores
{j["courts"]}

### Unificación de criterios
Mecanismo principal: **{j["precedent_mechanism"]}**

### Formulación del problema jurídico
Debe incluir: supuesto de hecho + tensión jurídica + pregunta de cierre.

### Ratio decidendi — fórmula
*"Cuando [supuesto de hecho], entonces [consecuencia jurídica], porque [fundamento normativo]."*

### Metodología de puntos nodales
1. Sentencia ancla (más reciente y relevante)
2. Nicho citacional
3. Reconstrucción hacia atrás hasta sentencia fundadora
4. Identificación de cambios e inflexiones

---

## 5. Formato de respuesta

Estructura con identificación, ratio decidendi (1-2 oraciones), obiter dicta, decisum, precedentes y aplicabilidad.

---

## 6. Advertencias obligatorias

- *"Verifique la vigencia del precedente consultando jurisprudencia reciente."*
- *"Consulte los textos completos de las sentencias citadas."*
- *"Este análisis es orientativo, no asesoría vinculante."*

---

## 7. Errores comunes que debes evitar

- No confundir obiter dicta con ratio decidendi
- No citar sentencias de instancia como precedente nacional obligatorio
- No inventar referencias — usar [VERIFICAR]
- No mezclar jurisprudencia de corporaciones distintas sin aclarar jerarquía
- No aplicar precedente sin verificar distinciones fácticas relevantes

{advertencia_section(country, j["instability"])}
"""


def generate_concepto(slug: str, j: dict, legal_basis: str) -> str:
    country = j["name"]
    adj = j["adjective"]
    sources_rows = "\n".join(
        f"| {s[0]} — [VERIFICAR: {s[1]}] | {s[2]} |" if s[1] else f"| {s[0]} — [VERIFICAR] | {s[2]} |"
        for s in j["sources"][:3]
    )
    return f"""---
name: elaboracion-concepto-juridico
description: >
  Elabora conceptos jurídicos, memos y consultas formales sobre derecho {adj}. Usar cuando el usuario solicite concepto, opinión jurídica, memo de derecho o análisis normativo en {country}. NO usar para otras jurisdicciones.
metadata:
  author: Juan David Vanegas Roldán
  version: "1.0"
  jurisdiction: {country}
  legal-basis: {legal_basis}
  last-verified: "2025-06"
  area: Análisis Transversal
  difficulty: avanzado
  output-type: documento
  warning: "Verificar vigencia de normas con abogado local antes de usar"
---

# Elaboración de Concepto Jurídico — {country}

Eres un experto en derecho de {country} capaz de elaborar conceptos técnicos con base en legislación vigente, doctrina y jurisprudencia de {j["main_court"]} y tribunales superiores.

## 1. Rol

Elaborar conceptos jurídicos rigurosos. Si falta material de investigación, sugerir usar el skill de investigación jurídica primero.

---

## 2. Información requerida

1. Tema o pregunta jurídica
2. Propósito (interno / cliente / entidad pública o privada)
3. Área del derecho
4. Contexto fáctico (si es concepto aplicado)
5. Nivel de detalle (ejecutivo / técnico / académico)

---

## 3. Modos de operación

### Modo A — Concepto normativo puro
### Modo B — Concepto con análisis jurisprudencial
### Modo C — Concepto aplicado a hechos concretos
### Modo D — Memo ejecutivo para cliente no abogado

---

## 4. Conocimiento especializado

{system_warning_block(j)}

### Estructura del concepto

1. Pregunta jurídica (supuesto + tensión + pregunta)
2. Marco normativo — artículos de `normas-base.md` de {country}
3. Posición doctrinal (si aplica)
4. Jurisprudencia — corporación + referencia + ratio decidendi
5. Análisis aplicado
6. Conclusión y recomendación

### Fuentes de consulta

| Fuente | Uso |
|---|---|
{sources_rows}
| {j["constitutional_court"]} | {j["constitutional_action"].capitalize()} y control constitucional |

### Criterios de calidad

- Citar artículos específicos de normas en `normas-base.md`
- Jurisprudencia verificable o marcada [VERIFICAR]
- Señalar vacíos normativos y zonas grises
- Distinguir posición mayoritaria de minoritaria

---

## 5. Formato de respuesta

```
CONCEPTO JURÍDICO — {country.upper()}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PARA / DE / FECHA / ASUNTO / ÁREA

I. PREGUNTA JURÍDICA
II. ANTECEDENTES (si aplica)
III. MARCO NORMATIVO
IV. JURISPRUDENCIA APLICABLE
V. ANÁLISIS
VI. CONCLUSIÓN
VII. RECOMENDACIÓN
```

---

## 6. Advertencias obligatorias

- *"Concepto orientativo, no asesoría vinculante."*
- *"Verificar vigencia de normas y jurisprudencia citadas."*
- *"No reemplaza el criterio del abogado responsable."*

---

## 7. Errores comunes que debes evitar

- No citar artículos no confirmados en `normas-base.md`
- No inventar sentencias
- No generalizar jurisprudencia constitucional sin verificar alcance
- No mezclar derecho de otros países
- No formular problemas jurídicos genéricos

{advertencia_section(country, j["instability"])}
"""


def generate_due_diligence(slug: str, j: dict, legal_basis: str) -> str:
    country = j["name"]
    adj = j["adjective"]
    dd_table = "\n".join(format_dd_row(*row) for row in j["dd_sources"])
    inmueble_note = (
        "Verificar si aplica registro estatal (PR) o consultas federales según el bien."
        if slug == "puerto-rico"
        else "La propiedad inmobiliaria se registra en el registro correspondiente — verificar jurisdicción territorial."
    )
    return f"""---
name: due-diligence-general
description: >
  Realiza due diligence legal general sobre personas, contratos, inmuebles u operaciones en {country}. Usar cuando el usuario necesite verificar antecedentes, situación judicial o riesgos legales en {country}. NO usar para otras jurisdicciones.
metadata:
  author: Juan David Vanegas Roldán
  version: "1.0"
  jurisdiction: {country}
  legal-basis: {legal_basis}
  last-verified: "2025-06"
  area: Análisis Transversal
  difficulty: intermedio
  output-type: análisis
  warning: "Verificar vigencia de normas con abogado local antes de usar"
---

# Due Diligence Legal General — {country}

Eres un experto en verificación jurídica de personas, bienes y operaciones en {country}.

## 1. Rol

Estructurar y ejecutar due diligence legal general — no sustituye due diligence corporativa especializada (M&A).

---

## 2. Tipos de due diligence

### A. Persona natural
Identidad, procesos judiciales, sanciones, inhabilidades, historial crediticio [con autorización], listas internacionales.

### B. Inmueble
Cadena registral, gravámenes, embargos, uso del suelo, paz y salvos.

### C. Operación comercial
Contraparte societaria, representación legal, contratos, procesos activos.

---

## 3. Conocimiento especializado

{system_warning_block(j)}

### Fuentes públicas de consulta en {country}

| Fuente | Qué verifica | Nota |
|---|---|---|
{dd_table}

### Inmuebles
{inmueble_note}

### Persona jurídica
Verificar existencia y representación con certificado registral vigente (preferiblemente reciente).

### Señales de alerta

**Críticas (bloquean operación):**
- Embargo vigente sobre inmueble
- Representante sin facultades para el acto
- Sociedad en liquidación [VERIFICAR registro]
- Aparición en listas de control internacional

**Relevantes (requieren atención):**
- Procesos ejecutivos activos como demandado
- Gravámenes no resueltos
- Certificados registrales desactualizados

---

## 4. Formato de respuesta

```
INFORME DE DUE DILIGENCE — {country.upper()}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OBJETO / FECHA / FUENTES CONSULTADAS

HALLAZGOS CRÍTICOS (🔴)
HALLAZGOS RELEVANTES (🟡)
SIN NOVEDAD (🟢)
INFORMACIÓN NO VERIFICADA

RECOMENDACIÓN: Proceder / Proceder con condiciones / No proceder

LIMITACIÓN: Refleja información disponible a la fecha indicada.
```

---

## 5. Advertencias obligatorias

- *"Verificar directamente en las fuentes oficiales indicadas."*
- *"No garantiza inexistencia de situaciones no registradas públicamente."*
- *"Due diligence orientativo — no reemplaza auditoría legal completa."*

---

## 6. Errores comunes que debes evitar

- No confiar solo en declaraciones de la contraparte
- No omitir consulta de procesos judiciales
- No usar certificados registrales vencidos
- No asumir representación legal sin verificar estatutos
- No mezclar procedimientos de verificación de otros países

{advertencia_section(country, j["instability"])}
"""


def generate_archivo(slug: str, j: dict, legal_basis: str, proc_ref: str) -> str:
    country = j["name"]
    adj = j["adjective"]
    return f"""---
name: analisis-archivo-documentos
description: >
  Analiza conjuntos de documentos jurídicos en {country} — expedientes, contratos, actas — para extraer información, cronologías, inconsistencias y riesgos. Específico para {country}. NO usar para otras jurisdicciones.
metadata:
  author: Juan David Vanegas Roldán
  version: "1.0"
  jurisdiction: {country}
  legal-basis: {legal_basis}
  last-verified: "2025-06"
  area: Análisis Transversal
  difficulty: intermedio
  output-type: mixto
  warning: "Verificar vigencia de normas con abogado local antes de usar"
---

# Análisis de Archivo de Documentos Jurídicos — {country}

Eres un experto en análisis documental jurídico en {country}. Procesas conjuntos de documentos de forma integrada.

## 1. Rol

Inventariar, cronologizar, mapear partes, detectar inconsistencias y riesgos. Punto de partida para estrategia — no reemplaza criterio del abogado.

---

## 2. Modos de análisis

### Modo A — Expediente judicial
### Modo B — Expediente contractual
### Modo C — Expediente corporativo
### Modo D — Análisis libre
### Modo E — Expediente con pruebas multi-tipo

---

## 3. Protocolo de análisis integrado

1. **Inventario** — tipo, fecha, partes, resumen
2. **Cronología** — eventos con fuente documental
3. **Mapa de partes** — roles y relaciones
4. **Análisis** — inconsistencias, riesgos, fortalezas, vacíos
5. **Síntesis y recomendaciones**

---

## 4. Conocimiento especializado

### Referencia procesal para pruebas
{proc_ref} — régimen probatorio aplicable [consultar texto vigente]

### Clasificación probatoria (referencia general)

| Tipo | Valor probatorio |
|---|---|
| Documentos públicos | Alta prueba de origen y contenido [VERIFICAR requisitos] |
| Documentos privados | Requieren reconocimiento o peritaje según caso |
| Mensajes de datos | Admisibles — verificar autenticidad y cadena |
| Testimonios | Según {proc_ref.split()[0] if proc_ref else 'código procesal'} [VERIFICAR] |
| Pericial | Según designación judicial o convención |

{system_warning_block(j)}

---

## 5. Formato de respuesta

Usar plantilla de expediente judicial o contractual según el modo, con semáforo 🔴🟡🟢 y vacíos documentales.

---

## 6. Advertencias obligatorias

- *"Basado exclusivamente en documentos proporcionados."*
- *"Inconsistencias requieren verificación adicional antes de uso procesal."*
- *"Punto de partida para criterio jurídico, no reemplazo."*

---

## 7. Errores comunes que debes evitar

- No concluir con documentos parciales sin señalar vacíos
- No ignorar fechas — son datos críticos
- No mezclar hechos probados con inferencias sin distinguirlos
- No omitir vacíos documentales
- No aplicar reglas probatorias de otros ordenamientos

{advertencia_section(country, j["instability"])}
"""


GENERATORS = {
    "investigacion-juridica": generate_investigacion,
    "analisis-jurisprudencial": generate_jurisprudencial,
    "elaboracion-concepto-juridico": generate_concepto,
    "due-diligence-general": generate_due_diligence,
    "analisis-archivo-documentos": generate_archivo,
}


def generate_skill(slug: str, skill: str) -> str:
    j = JURISDICTION_DATA[slug]
    normas_path = JURIS_BASE / slug / "normas-base.md"
    parsed = parse_normas_base(normas_path)
    sections = parsed["sections"]
    legal_basis = build_legal_basis(sections, skill)
    proc = find_procedural_section(sections)
    proc_ref = extract_articles_ref(proc, "código procesal [VERIFICAR]")

    gen = GENERATORS[skill]
    if skill == "analisis-archivo-documentos":
        return generate_archivo(slug, j, legal_basis, proc_ref)
    return gen(slug, j, legal_basis)


def main() -> None:
    created = 0
    skipped = 0
    errors: list[str] = []

    for slug in JURISDICTION_SLUGS:
        normas_path = JURIS_BASE / slug / "normas-base.md"
        if not normas_path.exists():
            errors.append(f"Falta normas-base.md para {slug}")
            continue

        for skill in SKILLS:
            out_dir = JURIS_BASE / slug / "analisis-transversal" / skill
            out_path = out_dir / "SKILL.md"
            try:
                content = generate_skill(slug, skill)
                out_dir.mkdir(parents=True, exist_ok=True)
                out_path.write_text(content, encoding="utf-8")
                created += 1
                print(f"  OK  {slug}/{skill}")
            except Exception as exc:
                errors.append(f"{slug}/{skill}: {exc}")

    print()
    print(f"Archivos creados: {created}")
    print(f"Esperados: {len(JURISDICTION_SLUGS) * len(SKILLS)}")
    if errors:
        print("Errores:")
        for err in errors:
            print(f"  - {err}")


if __name__ == "__main__":
    print("Generando skills transversales Tier 2...")
    print()
    main()
