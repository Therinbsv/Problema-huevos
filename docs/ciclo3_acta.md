# Ciclo 3 — Modelo óptimo

| Campo | Valor |
|---|---|
| Ciclo | 3 — Modelo óptimo |
| Release | `v0.3-ciclo3` |
| Épica Jira | HUEVO-16 |
| Responsable | Gestor |
| Decisión (Líder) | |
| Fecha de la reunión | |
| Asistentes | |

## C1 — Objetivos

Implementar y validar la estrategia óptima descrita en `diagramas/actividad_optima.puml`, y demostrar que alcanza los valores de referencia del problema. Para 2 huevos y 100 pisos, la estrategia garantiza el resultado con 14 lanzamientos en el peor caso.

| Issue | Entrega | Responsable |
|---|---|---|
| HUEVO-20 | RF-04: mínimo de lanzamientos en el peor caso | Dev backend |
| HUEVO-21 | RF-05: secuencia de pisos para la estrategia óptima | Dev backend |
| HUEVO-22 | Pruebas y casos borde de RK-03 | QA |
| HUEVO-23 | Diagrama de componentes y actividad óptima | Arquitecto |
| HUEVO-24 | Estrategia óptima en el prototipo Streamlit | Dev frontend |
| HUEVO-25 | Esta acta y el release | Gestor |

## C2 — Riesgos

| Riesgo | Estado anterior | Estado actual | Evidencia |
|---|---|---|---|
| RK-02 — Elegir una estrategia subóptima como solución general | Confirmado en el Ciclo 2 | Cerrado | `tests/test_estrategias.py::test_rk02_binaria_falla_con_2_huevos`; `tests/test_optima.py::test_peor_caso_consistencia` |
| RK-03 — Casos borde no contemplados (HUEVO-18) |  | Mitigado | `tests/test_validacion.py::test_entradas_invalidas`; `tests/test_optima.py::test_min_lanzamientos_un_solo_piso`; `tests/test_optima.py::test_simular_optima_no_se_rompe` |
| RK-01 — Malinterpretar el problema (HUEVO-2) |  | Reforzado | `tests/test_optima.py::test_min_lanzamientos_valores_clave`; `tests/test_optima.py::test_simular_optima_pisos_clave` |

## C3 — Desarrollo y pruebas

Entregado en este ciclo:

- `src/estrategias.py`: `pisos_cubiertos`, `min_lanzamientos`, `siguiente_piso`, `secuencia_pisos`, `simular_optima` y `peor_caso_optima` para RF-04 y RF-05.
- `tests/test_optima.py`: pruebas de valores de referencia, secuencia, simulación, consistencia del peor caso y validaciones.
- Suite de pruebas: **100 passed** (`python -m pytest` desde el entorno virtual del proyecto).
- Diagramas: `diagramas/actividad_optima.puml`, `diagramas/componentes.puml` y `diagramas/comparacion_estrategias.puml`.
- `app/main.py`: prototipo que presenta las tres estrategias, dibuja el edificio con los pisos de lanzamiento resaltados, muestra la secuencia y ofrece el gráfico comparativo.

La recurrencia de cobertura es:

**f(h,t) = f(h-1,t-1) + f(h,t-1) + 1**

El primer término representa los pisos que se pueden revisar si el huevo se rompe; el segundo, los pisos que se pueden revisar si no se rompe; el `1` corresponde al piso del lanzamiento actual. El mínimo de lanzamientos es el menor `t` para el que `f(h,t) ≥ N`. Con 2 huevos, `f(2,13) = 91`, insuficiente para cubrir 100 pisos; `f(2,14) = 105`, por lo que 14 lanzamientos sí bastan.

**Resultados calculados con las funciones de `src/estrategias.py` para N = 100:**

| Huevos (H) | Peor caso lineal | Peor caso binario | Mínimo óptimo | Secuencia de pisos si el primer huevo no se rompe |
|---:|---:|---:|---:|---|
| 1 | 100 | 100 | 100 | 1, 2, 3, …, 100 |
| 2 | 100 | 50 | 14 | 14, 27, 39, 50, 60, 69, 77, 84, 90, 95, 99, 100 |
| 3 | 100 | 26 | 9 | 37, 66, 88, 100 |
| 4 | 100 | 14 | 8 | 64, 100 |
| 7 | 100 | 7 | 7 | 64, 96, 100 |

La secuencia con 2 huevos y 100 pisos es: **14, 27, 39, 50, 60, 69, 77, 84, 90, 95, 99, 100**.

### Matriz de trazabilidad

| Requerimiento | Riesgo | Diagrama (PlantUML) | Prueba | Ciclo |
|---|---|---|---|---:|
| RF-01 | RK-03 | `diagramas/casos_uso.puml` | `tests/test_validacion.py::test_entradas_validas` | 2 |
| RF-02 | RK-02 | `diagramas/actividad_lineal.puml` | `tests/test_estrategias.py::test_lineal_peor_caso_100_pisos` | 2 |
| RF-03 | RK-02 | `diagramas/actividad_binaria.puml` | `tests/test_estrategias.py::test_binaria_encuentra_el_piso_correcto` | 2 |
| RF-04 | RK-01, RK-02 | `diagramas/actividad_optima.puml` | `tests/test_optima.py::test_min_lanzamientos_valores_clave` | 3 |
| RF-05 | RK-01 | `diagramas/actividad_optima.puml` | `tests/test_optima.py::test_secuencia_pisos_limites` | 3 |
| RF-09 | RK-03 | `diagramas/actividad_optima.puml` | `tests/test_optima.py::test_min_lanzamientos_entradas_invalidas` | 3 |

## C4 — Planificación y decisión
| Rol | Nombre | Decisión | Fecha |
|---|---|---|---|
| QA y validación | Josselyn Pozo | Pruebas aprobadas (100 passed) | 21/10/2026 |
| Analista de requisitos y riesgos | Josue Quintana | RK-02 cerrado, RK-03 mitigado, RK-01 reforzado | 21/10/2026 |
| Arquitecto y modelador | Anayomi Quishpe | Diagramas coherentes con el código | 21/10/2026 |
| Líder de proyecto | Jorge Revelo | Continuar al Ciclo 4 | 21/10/2026 |

**Decisión del líder: Continuar al Ciclo 4**  

**Siguiente ciclo — Producto (Ciclo 4):** completar el simulador, el comparador, el gráfico y la explicación; realizar una prueba de usabilidad con usuarios externos.
