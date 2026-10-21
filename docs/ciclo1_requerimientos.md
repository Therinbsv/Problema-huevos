# Especificación de Requerimientos — Problema de los huevos

| Campo | Valor |
|---|---|
| Proyecto | Problema de los huevos (modelo en espiral) |
| Documento | Especificación de requerimientos |
| Versión | 0.2 — Ciclo 1 (Concepto, hito LCO) — corrige observación ARQ-01 de la revisión de arquitectura |
| Responsable | Analista de requisitos y riesgos |
| Revisión | Líder de proyecto, Arquitecto y modelador |
| Estado | Borrador para validación con el docente |
| Issue Jira | HUEVO-1 |

---

## 1. Propósito

Definir qué debe hacer el sistema para resolver el problema de los huevos, bajo qué supuestos y con qué criterios se aceptará. Este documento es la base del Ciclo 1. Su objetivo es asegurar que el equipo entiende correctamente el problema antes de diseñar o programar cualquier solución.

## 2. Descripción del problema

En un edificio de **N pisos** (por defecto, 100) se dispone de **H huevos** idénticos. Existe un piso crítico desconocido **k**: un huevo lanzado desde el piso k o superior se rompe, y desde un piso inferior no se rompe.

El objetivo es **encontrar k con el menor número de lanzamientos posible en el peor caso**.

> El problema no consiste en adivinar el piso con suerte. Se busca la estrategia que garantice encontrarlo con el mínimo de lanzamientos sin importar dónde esté k.

## 3. Alcance

**Incluye:**
- Cálculo del número mínimo de lanzamientos en el peor caso para H huevos y N pisos.
- Comparación de las estrategias de búsqueda candidatas (lineal, binaria y otras que surjan del análisis).
- Generación de la secuencia de pisos de la estrategia óptima.
- Simulación de la búsqueda para un piso crítico dado.
- Interfaz web para que el docente evalúe los resultados.

**No incluye:**
- Simulación física (velocidad, resistencia del huevo, altura real).
- Persistencia de datos, usuarios o autenticación.
- Huevos con resistencias distintas entre sí.

## 4. Interesados

| Interesado | Interés |
|---|---|
| Docente | Evaluar la aplicación de la metodología y la justificación de las decisiones |
| Equipo (6 integrantes) | Entregar un producto correcto con trazabilidad completa |
| Usuario de la demo | Entender el problema y la comparación sin explicación previa |

## 5. Supuestos y reglas del problema

| ID | Supuesto |
|---|---|
| S1 | Todos los huevos son idénticos y tienen el mismo piso crítico. |
| S2 | Un huevo que no se rompe queda intacto y puede reutilizarse sin desgaste. |
| S3 | Un huevo roto no puede volver a usarse. |
| S4 | **Monotonía:** si un huevo se rompe en el piso k, se rompe en cualquier piso mayor que k; si no se rompe en k, no se rompe en ningún piso menor. |
| S5 | Es posible que el huevo no se rompa en ningún piso (k > N). |
| S6 | Un lanzamiento es cualquier tiro de un huevo, se rompa o no. |
| S7 | Se mide el **peor caso**, no el promedio ni el mejor caso. |
| S8 | El piso crítico k puede tomar valores entre 1 y N+1. Si k = 1, el huevo se rompe desde el primer piso; si k = N+1, no se rompe en ningún piso del edificio. |

## 6. Requerimientos funcionales

Prioridad según MoSCoW: **M** = Must (obligatorio), **S** = Should (debería), **C** = Could (deseable).

| ID | Requerimiento | Prioridad | Ciclo |
|---|---|---|---|
| RF-01 | El sistema debe permitir ingresar el número de huevos H (H ≥ 1) y de pisos N (N ≥ 1). | M | 2 |
| RF-02 | El sistema debe calcular el número de lanzamientos en el peor caso de la búsqueda **lineal**. | M | 2 |
| RF-03 | El sistema debe calcular el número de lanzamientos en el peor caso de la búsqueda **binaria**, respetando el límite de H huevos. | M | 2 |
| RF-04 | El sistema debe calcular el **número mínimo** de lanzamientos en el peor caso para cualquier H y N. | M | 3 |
| RF-05 | El sistema debe generar la secuencia inicial de pisos de lanzamiento de la estrategia óptima y permitir determinar los lanzamientos siguientes según los resultados anteriores, respetando la cantidad de huevos disponibles. | M | 3 |
| RF-06 | El sistema debe **comparar** en una misma vista los resultados de todas las estrategias para los valores ingresados. | M | 4 |
| RF-07 | El sistema debe **simular** la búsqueda paso a paso para un piso crítico elegido por el usuario, mostrando cada lanzamiento y su resultado. | S | 4 |
| RF-08 | El sistema debe mostrar un **gráfico** de lanzamientos según el número de huevos. | S | 4 |
| RF-09 | El sistema debe validar las entradas y mostrar un mensaje claro ante valores inválidos (H = 0, N = 0, valores negativos o no numéricos). | M | 3 |
| RF-10 | El sistema podría mostrar una explicación breve del modelo matemático usado. | C | 4 |

## 7. Requerimientos no funcionales

| ID | Categoría | Requerimiento | Criterio de medición |
|---|---|---|---|
| RNF-01 | Corrección | Los resultados deben coincidir con los valores de referencia de la sección 9. | 100 % de las pruebas de referencia pasan |
| RNF-02 | Rendimiento | El cálculo debe responder rápido para tamaños razonables. | < 1 s para N ≤ 1000 y H ≤ 10 |
| RNF-03 | Usabilidad | Un usuario externo al equipo debe entender la demo sin explicación. | 2 de 3 usuarios completan la tarea de prueba sin ayuda (Ciclo 4) |
| RNF-04 | Mantenibilidad | La lógica de cálculo debe estar separada de la interfaz. | Backend en `src/`, frontend en `app/`, sin lógica de cálculo en la interfaz |
| RNF-05 | Verificabilidad | Toda función de cálculo debe tener pruebas automáticas. | Pruebas con `pytest` ejecutadas en GitHub Actions en cada PR |
| RNF-06 | Portabilidad | El sistema debe ejecutarse en Windows, macOS y Linux. | Ejecución con Python 3.11+ y `requirements.txt` |
| RNF-07 | Trazabilidad | Cada cambio debe vincularse a un issue. | Todo commit incluye una clave `HUEVO-n` |

## 8. Restricciones

| ID | Restricción |
|---|---|
| R-01 | Lenguaje: Python 3.11 o superior. |
| R-02 | Interfaz: Streamlit (sin HTML, CSS ni JavaScript propios). |
| R-03 | Diagramas: PlantUML, versionados en el repositorio. |
| R-04 | Gestión: Jira; control de versiones: GitHub. |
| R-05 | Metodología: modelo en espiral con 4 ciclos y release al final de cada uno. |

## 9. Criterios de aceptación (valores de referencia)

| Huevos (H) | Pisos (N) | Lanzamientos mínimos esperados (peor caso) |
|---|---|---|
| 1 | 100 | 100 |
| 2 | 100 | 14 |
| 3 | 100 | 9 |
| 7 | 100 | 7 |
| 1 | 1 | 1 |
| 5 | 1 | 1 |
| H ≥ 1 | 0 | Error de validación (RF-09) |
| 0 | N ≥ 1 | Error de validación (RF-09) |

**Secuencia esperada con H = 2 y N = 100 (RF-05):** 14, 27, 39, 50, 60, 69, 77, 84, 90, 95, 99, 100.

## 10. Riesgos iniciales (Ciclo 1)

| ID | Riesgo | Probabilidad | Impacto | Mitigación | Req. afectados |
|---|---|---|---|---|---|
| RK-01 | Malinterpretar el problema (por ejemplo, optimizar el promedio en lugar del peor caso) | Media | Alto | Supuestos S1–S8 explícitos y validación con el docente antes del Ciclo 2 | RF-02 a RF-05 |
| RK-02 | Elegir una estrategia subóptima como solución general | Alta | Alto | Prototipar y comparar estrategias en el Ciclo 2 antes de comprometer la solución | RF-03, RF-04 |
| RK-03 | Casos borde no contemplados (0 huevos, 1 piso, más huevos que pisos) | Media | Medio | Incluirlos en los criterios de aceptación y en las pruebas | RF-09, RNF-01 |
| RK-04 | La demo no se entiende sin explicación | Media | Medio | Prueba de usabilidad con usuarios externos en el Ciclo 4 | RF-06, RNF-03 |

## 11. Matriz de trazabilidad inicial

| Requerimiento | Riesgo | Diagrama (PlantUML) | Prueba | Ciclo |
|---|---|---|---|---|
| RF-01 | RK-03 | casos_uso.puml | test_validacion | 2 |
| RF-02 | RK-02 | actividad_lineal.puml | test_lineal | 2 |
| RF-03 | RK-02 | actividad_binaria.puml | test_binaria | 2 |
| RF-04 | RK-01, RK-02 | actividad_optima.puml | test_minimo | 3 |
| RF-05 | RK-01 | actividad_optima.puml | test_secuencia | 3 |
| RF-06 | RK-04 | componentes.puml | prueba de usabilidad | 4 |
| RF-07 | RK-04 | casos_uso.puml | test_simulacion | 4 |
| RF-08 | RK-04 | Pendiente de definir | Prueba de visualización del gráfico (planificada) | 4 |
| RF-09 | RK-03 | actividad_optima.puml | test_validacion | 3 |
| RF-10 | RK-04 | Pendiente de definir | Revisión de contenido explicativo (planificada) | 4 |

> Las columnas de diagrama y prueba se completan a medida que avanzan los ciclos. El gestor de documentación actualiza esta matriz en cada release.

## 12. Glosario

| Término | Definición |
|---|---|
| Piso crítico (k) | Piso más bajo desde el que el huevo se rompe. |
| Lanzamiento | Tirar un huevo desde un piso, se rompa o no. |
| Peor caso | Máximo número de lanzamientos que necesita una estrategia, considerando todas las posiciones posibles de k. |
| Estrategia | Regla que decide desde qué piso lanzar en cada paso según los resultados anteriores. |
| LCO | *Life Cycle Objectives*: hito de objetivos del ciclo de vida aprobados (fin del Ciclo 1). |

## 13. Aprobación (hito LCO)

| Rol | Nombre | Decisión | Fecha |
|---|---|---|---|
| Analista de requisitos y riesgos | Josue Quintana| Elaborado | 20/10/2026|
| Arquitecto y modelador | | Revisado | |
| Líder de proyecto | | Continuar / Ajustar / Abortar | |
| Docente | | Validado | |
