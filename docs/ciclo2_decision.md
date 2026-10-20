# Ciclo 2 — Evaluación de estrategias simples (hito LCA)

| Campo | Valor |
|---|---|
| Ciclo | 2 — Prototipo de estrategias simples |
| Release | `v0.2-ciclo2` |
| Responsable del documento | Gestor de configuración y documentación |
| Decisión | Líder de proyecto |
| Issues Jira | RK-02 (riesgo), decisión de ciclo |

## C1 — Objetivos

Evaluar las candidatas A (lineal) y B (binaria) con un prototipo funcional y decidir si alguna sirve como solución general.

## C2 — Análisis de riesgos

| Riesgo | Estado anterior | Estado actual | Evidencia |
|---|---|---|---|
| RK-02 Elegir una estrategia subóptima | Abierto (probabilidad alta) | **Confirmado y mitigado** | `tests/test_estrategias.py::test_rk02_binaria_falla_con_2_huevos` |

## C3 — Desarrollo y pruebas

Entregado en la rama `ciclo-2`:

- `src/validacion.py`: validación de H y N (RF-01, RF-09).
- `src/estrategias.py`: simulación y peor caso de las búsquedas lineal y binaria (RF-02, RF-03).
- `tests/`: pruebas automáticas, ejecutadas por GitHub Actions en cada PR.
- `app/main.py`: prototipo en Streamlit con la comparación.

**Resultados (N = 100):**

| Huevos (H) | Lineal | Binaria | Referencia óptima (requerimientos §9) |
|---|---|---|---|
| 1 | 100 | 100 | 100 |
| 2 | 100 | **50** | **14** |
| 3 | 100 | **26** | **9** |
| 10 | 100 | 7 | 7 |

**Hallazgo:** con 2 huevos la binaria necesita 50 lanzamientos, frente a 14 del valor de referencia. Si el primer huevo se rompe en el piso 50, el segundo tiene que revisar los pisos 1 a 49 uno por uno. La binaria solo es buena cuando sobran huevos.

## C4 — Planificación y decisión

| Opción | Decisión |
|---|---|
| Continuar con la binaria como solución general | ❌ Descartada (evidencia RK-02) |
| Continuar con la lineal | ❌ Descartada (100 lanzamientos; no aprovecha huevos extra) |
| **Avanzar con la candidata C** (`actividad_optima.puml`) | ✅ **Aprobada para el Ciclo 3** |

**Por qué esta decisión justifica la espiral:** el riesgo se detectó con un prototipo barato antes de comprometer la solución. En cascada, la binaria se habría diseñado como solución y el error aparecería recién en las pruebas finales.

## Aprobación

| Rol | Nombre | Decisión | Fecha |
|---|---|---|---|
| QA y validación | | Pruebas aprobadas | |
| Analista de requisitos y riesgos | | RK-02 confirmado | |
| Líder de proyecto | | Continuar al Ciclo 3 | |
