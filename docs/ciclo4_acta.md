# Ciclo 4 — Producto y cierre (hito IOC)

| Campo | Valor |
|---|---|
| Ciclo | 4 — Producto y cierre |
| Release | `v1.0` |
| Épica Jira | HUEVO-17 |
| Responsable del documento | Gestor de configuración y documentación |
| Decisión | Líder de proyecto |
| Fecha de la reunión de cierre | 21/10/2026 |
| Asistentes | Josselyn Pozo, Josue Quintana, Anayomi Quishpe, Matthew Redín, Jorge Revelo, Katherine Sánchez |

## Qué heredamos y qué aprendimos

Lo que cada ciclo anterior aportó al producto final:

| Ciclo | Qué heredamos | Dónde se usa en el producto |
|---|---|---|
| 1 — Concepto | Supuestos S1 a S8, medir el **peor caso**, restricciones (R-02: Streamlit sin HTML, CSS ni JS propios), arquitectura de dos capas (ADR-003) | Reglas del juego, comparación contra el máximo garantizado, interfaz como imagen, separación `src/` y `app/` |
| 2 — Estrategias simples | La búsqueda binaria no sirve con pocos huevos (50 lanzamientos con 2 huevos, RK-02 confirmado) y la validación de entradas | Pestaña Comparar, y la razón de ser del juego |
| 3 — Modelo óptimo | La recurrencia f(h,t) y la estrategia óptima con valores de referencia 14, 9 y 7 | Pestaña Cómo funciona (RF-10) y la estrategia contra la que el juego mide al jugador |

Lo que aprendimos al revisar el prototipo del Ciclo 3:

- Los pisos resaltados del edificio **no se entendían sin explicación**: era RK-04 materializándose, detectado antes de la prueba formal.
- Esa versión usaba `st.html` con CSS propio, lo que **incumplía R-02**. Se detectó al contrastar la interfaz con las restricciones.
- Respuesta del Ciclo 4: rediseñar la interfaz como juego (el usuario busca el piso crítico) con una imagen dibujada con Pillow, que cumple R-02. Decisión registrada en `docs/adr-006_modo_juego.md`.

## C1 — Objetivos

Entregar un simulador comparativo que el docente pueda usar sin explicación, con todas las funciones de los requerimientos.

| Issue | Entregable | Rol |
|---|---|---|
| HUEVO-26 | Simulación paso a paso y lógica del juego de búsqueda del piso crítico (RF-07) | Desarrollador backend |
| HUEVO-27 | App final: juego, comparador, gráfico y explicación (RF-06, RF-07, RF-08, RF-10) | Desarrollador frontend |
| HUEVO-28 | Pruebas del simulador y del juego | QA |
| HUEVO-29 | Prueba de usabilidad con usuarios externos (RK-04, RNF-03) | QA |
| HUEVO-30 | Revisión final de diagramas | Arquitecto |
| HUEVO-31 | Publicación en Streamlit Community Cloud | Gestor |
| HUEVO-32 | Informe final y release `v1.0` | Gestor |

## C2 — Análisis de riesgos

| Riesgo | Estado anterior | Estado actual | Evidencia |
|---|---|---|---|
| RK-04 La demo no se entiende sin explicación (HUEVO-19) | Abierto; el prototipo del Ciclo 3 ya mostró el problema | En curso: se evalúan las refactorizaciones | `docs/ciclo4_usabilidad.md` |
| Incumplimiento de R-02 en el prototipo del Ciclo 3 (`st.html` con CSS propio) | Detectado en la revisión | Corregido: la interfaz usa solo componentes nativos y una imagen de Pillow | Búsqueda de `st.html` y `unsafe_allow_html` en `app/` sin resultados |
| El modo juego crece sin respaldo (alcance) | Posible | Controlado: alcance congelado y decisión documentada | `docs/adr-006_modo_juego.md` |

## C3 — Desarrollo y pruebas

Entregado en la rama `ciclo-4`:

- `src/simulacion.py`: convierte los lanzamientos de cualquier estrategia en pasos explicados (RF-07).
- `src/juego.py`: lógica pura del juego (estado, lanzamiento, ganar o perder, comparación con la óptima).
- `app/main.py` y `app/escena.py`: app final con 4 pestañas y el edificio dibujado con Pillow.
    - **Simular:** el juego. El sistema esconde el piso crítico; el usuario elige cuántos huevos usar y desde qué piso lanzar. Al terminar compara sus lanzamientos con la óptima y con el máximo garantizado (RF-07).
    - **Comparar:** las 3 estrategias y la secuencia de pisos (RF-02 a RF-06).
    - **Gráfico:** lanzamientos según el número de huevos (RF-08).
    - **Cómo funciona:** el modelo matemático y la simulación paso a paso con el piso crítico elegido por el usuario (RF-07, RF-10).
- `tests/`: 42 pruebas nuevas (simulación, juego y escena). El total sube a **170 pruebas**, todas en verde.
- `docs/ciclo4_usabilidad.md`, `docs/informe_final.md` y `docs/adr-006_modo_juego.md`.

### Cobertura de requerimientos

| Requerimiento | Dónde se cumple | Verificado por |
|---|---|---|
| RF-01, RF-09 | Control de huevos con límites; validación en `src/validacion.py`. En la interfaz el edificio es de 100 pisos (el problema clásico); el backend acepta cualquier N | test_validacion |
| RF-02, RF-03 | Pestaña Comparar | test_estrategias |
| RF-04, RF-05 | Pestaña Comparar y Cómo funciona | test_optima |
| RF-06 | Pestaña Comparar | revisión y prueba de usabilidad (T2) |
| RF-07 | Cómo funciona (piso elegido por el usuario) y Simular (juego con piso sorteado) | test_simulacion, test_juego y prueba de usabilidad (T3, T4) |
| RF-08 | Pestaña Gráfico | revisión |
| RF-10 | Pestaña Cómo funciona (recurrencia f(h,t)) | revisión |
| RNF-01 | — | 100 % de las pruebas de referencia pasan |
| RNF-02 | — | test_rendimiento_*; medido: menos de 0,3 s para N = 1000 y H = 10 |
| RNF-03 | — | prueba de usabilidad |
| RNF-04 | `app/` sin fórmulas del problema, `src/` sin Streamlit | componentes.puml y revisión de código |
| RNF-05 | GitHub Actions en cada PR | historial de PR |
| RNF-06 | Python 3.11+ y `requirements.txt` | ejecución en las máquinas del equipo |
| RNF-07 | Cada commit con `HUEVO-n` | pestaña *Desarrollo* de Jira |
| R-02 | Sin `st.html`, CSS ni JS propios | búsqueda en `app/` |

## C4 — Cierre (hito IOC)

| Opción | Decisión |
|---|---|
| Entregar `v1.0` | Listo para entregar |
| Ajustar antes de entregar | No se requieren ajustes |

**Enlace de la app publicada:** https://problema-huevos-zspdjxago5b32tv4mgwbw9.streamlit.app

## Aprobación

| Rol | Nombre | Decisión | Fecha |
|---|---|---|---|
| QA y validación | Josselyn Pozo| Pruebas y usabilidad aprobadas |21/10/2026 |
| Arquitecto y modelador | Anayomi Quishpe| Diseño final revisado |21/10/2026 |
| Analista de requisitos y riesgos |Josué Quintana | RK-04 cerrado |21/10/2026 |
| Gestor de configuración y documentación |Katherine Sánchez | Informe y release `v1.0` |21/10/2026 |
| Líder de proyecto | Jorge Revelo| Proyecto entregado | 21/10/2026|
