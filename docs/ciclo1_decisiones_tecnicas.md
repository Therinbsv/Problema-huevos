# Decisiones técnicas y de arquitectura — Problema de los huevos

| Campo | Valor |
|---|---|
| Documento | Registro de decisiones de arquitectura (ADR) |
| Versión | 0.2 — Ciclo 1 (Concepto, hito LCO) — pila reducida a las 5 herramientas acordadas por el equipo |
| Responsable | Arquitecto y modelador |
| Revisión | Líder de proyecto, Desarrollador |
| Issue Jira | HUEVO-6 |
| Relacionado con | `docs/requerimientos.md` v0.2, `diagramas/*.puml` |

---

## 1. Propósito

Dejar escrito **qué tecnologías se usan, por qué se eligieron y qué alternativas se descartaron**. Cada decisión responde a requerimientos y riesgos concretos, para que cualquier integrante o el docente pueda entender el porqué sin preguntar.

Formato: cada decisión es un ADR (*Architecture Decision Record*) con contexto, opciones evaluadas, decisión y consecuencias. Un ADR aceptado no se borra; si cambia, se crea uno nuevo que lo reemplaza.

## 2. Qué exige el problema a la tecnología

Antes de elegir, se identificó qué necesita realmente el sistema:

| Necesidad | Origen | Implicación técnica |
|---|---|---|
| Cálculo numérico pequeño (N ≤ 1000, H ≤ 10) | RNF-02 | El rendimiento del lenguaje **no es un factor decisivo**; cualquier lenguaje responde en milisegundos |
| Interfaz web evaluable por el docente | RF-06, RF-07, RF-08 | Se necesita una UI con controles, tablas y gráficos |
| Foco en metodología, no en código | Documento de metodología | Minimizar el esfuerzo en frontend e infraestructura |
| Un solo desarrollador | Roles del equipo | La pila debe ser pequeña y fácil de aprender |
| Pruebas automáticas en cada PR | RNF-05 | Framework de pruebas simple e integrable con GitHub Actions |
| Lógica separada de la interfaz | RNF-04 | Arquitectura en capas aunque el sistema sea pequeño |

**Conclusión del análisis:** el criterio dominante es la **productividad y simplicidad**, no el rendimiento.

---

## ADR-001 — Lenguaje de implementación

**Estado:** Aceptado · **Ciclo:** 1

**Contexto:** el núcleo del sistema es un algoritmo de cálculo (recurrencia sobre huevos y lanzamientos) más una interfaz de demostración. El equipo tiene experiencia académica en Java y conocimientos de Python y JavaScript.

**Opciones evaluadas** (1 = peor, 5 = mejor):

| Criterio | Python | Java | JavaScript / TypeScript | C++ |
|---|---|---|---|---|
| Claridad para expresar el algoritmo | 5 | 3 | 4 | 3 |
| Esfuerzo para construir la interfaz web | 5 (Streamlit) | 2 (JSF/Spring + HTML) | 3 (React + HTML/CSS) | 1 |
| Gráficos y tablas | 5 (integrados en Streamlit) | 2 | 4 (Chart.js) | 1 |
| Pruebas automáticas | 5 (pytest) | 4 (JUnit) | 4 (Jest/Vitest) | 3 |
| Rendimiento | 3 | 4 | 3 | 5 |
| Curva de aprendizaje para el equipo | 5 | 4 | 3 | 2 |
| Notebooks para demostrar el modelo | 5 (Jupyter) | 1 | 2 | 1 |
| **Total** | **33** | **20** | **23** | **16** |

**Decisión:** **Python 3.11+**.

**Por qué:**
- El algoritmo se escribe casi igual que la fórmula matemática, lo que facilita demostrar que el código implementa el modelo.
- Permite construir la interfaz con Streamlit sin HTML, CSS ni JavaScript (ver ADR-002).
- Su única desventaja relevante, el rendimiento, no aplica: con N = 100 el cálculo es instantáneo.

**Alternativas descartadas:**
- **Java:** el equipo lo conoce, pero una interfaz web requiere servidor de aplicaciones, JSF o Spring y plantillas HTML. Multiplica el esfuerzo en una parte que no se evalúa.
- **JavaScript/TypeScript:** buena opción para web pura, pero obliga a diseñar HTML/CSS y a separar manualmente cálculo e interfaz.
- **C++:** su ventaja (velocidad) es irrelevante para este tamaño de problema y no tiene una vía simple hacia una interfaz web.

**Consecuencias:** se requiere `requirements.txt` con versiones fijadas para garantizar portabilidad (RNF-06).

---

## ADR-002 — Interfaz de usuario

**Estado:** Aceptado · **Ciclo:** 1

**Contexto:** cada ciclo debe terminar con un prototipo que el docente pueda evaluar. Un script de consola no sirve para comparar estrategias ni simular paso a paso.

**Opciones evaluadas:** Streamlit, Flask + HTML, Gradio, aplicación de escritorio (Tkinter).

| Opción | Ventaja | Desventaja |
|---|---|---|
| **Streamlit** | UI completa solo con Python; sliders, tablas y gráficos integrados; despliegue gratuito | Personalización visual limitada |
| Flask + HTML | Control total del diseño | Requiere HTML, CSS y JavaScript |
| Gradio | Muy rápido para demos de entrada/salida | Pensado para modelos de ML; peor para vistas comparativas y simulaciones paso a paso |
| Tkinter | No necesita navegador | Aspecto anticuado; no se puede compartir por enlace |

**Decisión:** **Streamlit**.

**Consecuencias:**
- La personalización visual limitada se acepta, porque la estética no es un criterio de evaluación.
- Tablas y gráficos se hacen con los componentes nativos de Streamlit (`st.table`, `st.dataframe`, `st.line_chart`, `st.bar_chart`, `st.metric`). **No se agregan librerías de datos o gráficos** (pandas, Plotly, Matplotlib): los datos del problema son listas de pocos números y no justifican una dependencia más.
- Streamlit incluye su propio servidor web (`streamlit run app/main.py`). **No se necesita Uvicorn, Gunicorn ni otro servidor.**
- La app puede publicarse gratis en **Streamlit Community Cloud**, de modo que el docente la abra desde un enlace sin instalar nada.

---

## ADR-003 — Arquitectura del sistema

**Estado:** Aceptado · **Ciclo:** 1

**Contexto:** RNF-04 exige separar la lógica de la interfaz. Aunque el sistema es pequeño, esa separación permite probar el cálculo sin abrir la interfaz y cambiar la UI sin tocar el algoritmo.

**Decisión:** arquitectura en **dos capas**, sin base de datos ni API.

```
app/            ← Capa de presentación (Streamlit)
  main.py         Solo lee entradas, llama a src/ y muestra resultados
src/            ← Capa de dominio (lógica pura, sin dependencias de UI)
  validacion.py   Valida H y N (RF-01, RF-09)
  estrategias.py  Lineal, binaria y óptima (RF-02 a RF-05)
  simulacion.py   Búsqueda paso a paso (RF-07)
tests/          ← Pruebas de la capa de dominio
```

**Reglas:**
- `src/` **nunca** importa `streamlit`.
- `app/` **nunca** contiene fórmulas de cálculo.
- Todas las funciones de `src/` son puras: misma entrada, misma salida, sin estado global.

**Por qué no una API REST (FastAPI + Uvicorn) con frontend separado:** Uvicorn es el servidor que ejecuta una API en Python; solo tendría sentido si el sistema expusiera servicios a otros clientes (una app móvil, otro sistema). Aquí hay un único cliente, sin persistencia ni integración externa. Agregarlo implicaría un segundo proceso, contratos HTTP y doble despliegue sin ningún requerimiento que lo pida. En la capa de presentación, `app/main.py` importa directamente las funciones de `src/`, que cumple RNF-04 con mucha menos complejidad.

**Consecuencias:** el diagrama `componentes.puml` se elaborará en el Ciclo 3 reflejando esta estructura.

---

## ADR-004 — Calidad y pruebas

**Estado:** Aceptado · **Ciclo:** 1

**Decisión:**

| Herramienta | Uso |
|---|---|
| **pytest** | Pruebas unitarias con los valores de referencia de la sección 9 de requerimientos |
| **GitHub Actions** | Ejecuta pytest en cada Pull Request; un PR con pruebas fallidas no se integra |

pytest no es una herramienta adicional de la pila: es la librería de pruebas estándar de Python y se ejecuta **dentro de GitHub** mediante Actions, cubriendo el rol que el documento de metodología asigna a GitHub ("Actions para pruebas").

**Por qué:** pytest permite escribir los criterios de aceptación casi tal como están en la tabla de requerimientos, lo que hace visible la trazabilidad requerimiento → prueba.

---

## ADR-005 — Herramientas de gestión y diseño

**Estado:** Aceptado · **Ciclo:** 1

Estas decisiones ya están justificadas en el documento de metodología; aquí se registran para mantener todas las decisiones en un solo lugar.

| Herramienta | Decisión | Justificación resumida |
|---|---|---|
| Jira | Gestión, riesgos y trazabilidad | Tipos de issue propios (Riesgo), Epics por ciclo, integración con GitHub |
| GitHub | Versiones, revisión y releases por ciclo | PRs con revisión obligatoria, tags `v0.x-cicloN` |
| PlantUML | Diagramas como texto | Versionables; el diff muestra cómo evolucionó el diseño |
| VS Code | Entorno unificado | Python, Jupyter, PlantUML y Git en un solo editor |

**Extensiones de VS Code acordadas:** Python, Jupyter, PlantUML (jebbs) y GitLens. La extensión de PlantUML requiere Java instalado; la vista previa se abre con `Alt + D`.

---

## 3. Pila tecnológica resumida

| Capa | Tecnología |
|---|---|
| Lenguaje | Python 3.11+ |
| Interfaz, tablas y gráficos | Streamlit (componentes nativos) |
| Pruebas | pytest ejecutado con GitHub Actions |
| Diagramas | PlantUML |
| Despliegue | Streamlit Community Cloud |
| Gestión | Jira + GitHub |

### Dependencias del proyecto (`requirements.txt`)

```
streamlit
pytest
```

Solo dos dependencias directas, cada una justificada por un requerimiento: Streamlit por RF-06/07/08 y pytest por RNF-05.

## 4. Riesgos técnicos asociados

| ID | Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|---|
| RK-05 | Diferencias de entorno entre integrantes (versiones de Python o librerías) | Media | Medio | `requirements.txt` con versiones fijadas y entorno virtual (`venv`) |
| RK-06 | Algún integrante no conoce Streamlit | Media | Bajo | Solo el desarrollador lo usa; tutorial oficial de 1 hora |
| RK-07 | La extensión de PlantUML no renderiza por falta de Java | Media | Bajo | Instalar Java 17+ o usar el servidor web de PlantUML como alternativa |

## 5. Aprobación

| Rol | Nombre | Decisión | Fecha |
|---|---|---|---|
| Arquitecto y modelador | | Elaborado | |
| Desarrollador backend | Matthew Redín | Revisado (viable, con observaciones DEV-01 a DEV-03) | 21/10/2026 |
| Líder de proyecto | | Aprobado / Ajustar | |

### Observaciones de la revisión técnica (Desarrollador backend, HUEVO-6)

Verificación realizada: con Python 3.11+, `streamlit` y `pytest` instalados en un entorno virtual, la pila funciona y las pruebas de la rama `ciclo-2` pasan (66 passed). La separación `src/` y `app/` es viable: `src/` no importa `streamlit`.

| ID | Observación | Propuesta |
|---|---|---|
| DEV-01 | La tabla inicial cita `docs/requerimientos.md`, pero el archivo se llama `docs/ciclo1_requerimientos.md`. | Corregir la referencia para no romper la trazabilidad. |
| DEV-02 | La sección 3 lista `streamlit` y `pytest` sin versión, pero ADR-001 y RK-05 exigen versiones fijadas. | Usar rangos: `streamlit>=1.40,<2` y `pytest>=8,<9`. |
| DEV-03 | La sección 2 dice "Un solo desarrollador", pero el equipo tiene backend y frontend. | Actualizar el texto; ADR-003 favorece esto, porque cada desarrollador trabaja en su capa (`src/` o `app/`) sin conflictos. |
