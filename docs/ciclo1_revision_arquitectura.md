# Revisión de arquitectura — Ciclo 1

| Campo | Valor |
|---|---|
| Issue Jira | HUEVO-7 |
| Revisor | Anayomi Quishpe, Arquitecto y modelador |
| Fecha de revisión | 21/10/2026 |
| Documentos revisados | `diagramas/casos_uso.puml`, `diagramas/actividad_lineal.puml`, `diagramas/actividad_binaria.puml`, `diagramas/actividad_optima.puml`, `diagramas/comparacion_estrategias.puml`, `docs/ciclo1_requerimientos.md` y `docs/ciclo1_decisiones_tecnicas.md` |

## Observaciones de la revisión previa

| ID | Observación | Estado |
|---|---|---|
| ARQ-01 | N = 0 debe generar un error de validación en todo el sistema | **Verificado** |
| ARQ-02 | Verificar `<<include>>` de "Ingresar H y N" en "Comparar" y "Simular" | **Verificado** |

**ARQ-01 — Verificado.** La especificación establece H ≥ 1 y N ≥ 1 en RF-01; RF-09 requiere validar entradas inválidas; y la sección 9 exige error para H ≥ 1 con N = 0 y para H = 0 con N ≥ 1. En las actividades actuales, `actividad_lineal.puml` verifica `N ≥ 1`, mientras que `actividad_binaria.puml` y `actividad_optima.puml` verifican `H ≥ 1 y N ≥ 1`; todas muestran un error y detienen el flujo si la condición falla. No se pudo verificar la ejecución del sistema: `src/` y `app/` solo contienen `.gitkeep`.

**ARQ-02 — Verificado.** `casos_uso.puml` incluye `UC07 ..> UC01 : <<include>>` y `UC08 ..> UC01 : <<include>>`. UC-01 es "Ingresar huevos (H) y pisos (N)", así que los casos Comparar (UC-07) y Simular (UC-08) reutilizan ese ingreso.

## Relación RF → diagrama

La siguiente relación contrasta los RF de la sección 6 de `ciclo1_requerimientos.md` con los artefactos que sí están disponibles y fueron revisados:

| RF | Representación encontrada | Resultado |
|---|---|---|
| RF-01 | UC-01 en `casos_uso.puml`; entradas y validaciones en `actividad_lineal.puml`, `actividad_binaria.puml` y `actividad_optima.puml`. | Representado en los diagramas revisados. |
| RF-02 | UC-03 y flujo piso por piso en `actividad_lineal.puml`. | Representado. |
| RF-03 | UC-04 y búsqueda binaria con límite de huevos en `actividad_binaria.puml`; incluye la transición a búsqueda lineal cuando queda un huevo. | Representado. |
| RF-04 | UC-05 y planificación del número T de lanzamientos en `actividad_optima.puml`. | Representado como propuesta pendiente de validar; se mantiene como hipótesis en Ciclo 1. |
| RF-05 | UC-06 y planificación/ejecución con reporte de secuencia en `actividad_optima.puml`. | Representado como propuesta pendiente de validar. |
| RF-06 | UC-07 en `casos_uso.puml`. La matriz de trazabilidad de requisitos menciona `componentes.puml`; el diagrama de comparación solicitado no está disponible. | Caso de uso representado; la comparación visual entre estrategias no pudo comprobarse en el artefacto ausente. |
| RF-07 | UC-08 en `casos_uso.puml`. | Representado como caso de uso; el detalle paso a paso se indica para el Ciclo 4. |
| RF-08 | UC-09 en `casos_uso.puml`; la matriz de requisitos deja pendiente definir un diagrama. | Representado como caso de uso; el gráfico aún no está detallado en los diagramas revisados. |
| RF-09 | UC-02 incluido por UC-01 y guardias de validación en las tres actividades revisadas. | Representado en el diseño revisado. El código ejecutable no pudo inspeccionarse. |
| RF-10 | UC-10 en `casos_uso.puml`; la matriz de requisitos deja pendiente definir el diagrama. | Representado como caso de uso; la explicación se detallará posteriormente. |

Los casos de uso referencian los diez RF. La cobertura del caso de uso no significa que exista ya un diagrama de actividad o una implementación para cada función.

## Comprobación de los diagramas y documentos

### `diagramas/casos_uso.puml`

- UC-01 a UC-10 hacen referencia respectivamente a RF-01 a RF-10.
- El actor Usuario se conecta con UC-01, UC-07, UC-08, UC-09 y UC-10. UC-01 incluye UC-02; UC-07 incluye UC-01, UC-03, UC-04 y UC-05; UC-06 extiende UC-07. Estas relaciones concuerdan con las funciones descritas.
- Los `<<include>>` requeridos para Comparar y Simular están presentes (ARQ-02).
- La referencia de trazabilidad del encabezado apunta correctamente a `docs/ciclo1_requerimientos.md`.

### `diagramas/actividad_lineal.puml`

- Valida `N ≥ 1` antes de iniciar y muestra error con `stop` si la condición no se cumple.
- Inicializa el piso y el contador, incrementa los lanzamientos después de cada prueba, reporta k cuando el huevo se rompe y avanza un piso cuando no se rompe.
- Si no hay rotura dentro del edificio, reporta k = N + 1. Esto representa el caso en que el huevo no se rompe en ningún piso.

### `diagramas/actividad_binaria.puml`

- Valida H y N antes de iniciar.
- En la búsqueda binaria, cada lanzamiento incrementa el contador y actualiza el límite inferior o superior según el resultado.
- Cuando queda un huevo, recorre linealmente desde `bajo`, incrementa el contador en cada lanzamiento, reporta k ante una rotura y, si se agota el intervalo, reporta k = bajo. Esto cumple la transición a búsqueda lineal y representa las decisiones y el conteo de esa rama.

### `diagramas/actividad_optima.puml`

- Se identifica como hipótesis en el comentario de cabecera y en el título; además, deja pendiente su validación frente a las otras estrategias y la demostración de optimalidad en ciclos posteriores.
- Comprueba H ≥ 1 y N ≥ 1, planifica T mediante la recurrencia indicada y modela la ejecución y el reporte de k, T y la secuencia.
- Los valores y la secuencia mostrados en la leyenda coinciden con los criterios de referencia indicados en la sección 9 de requerimientos para los casos enumerados.

### `diagramas/comparacion_estrategias.puml`

- Compara las estrategias para H = 2 y N = 100, con los valores y la secuencia que coinciden con los criterios de referencia de la sección 9 de requerimientos.
- La candidata aparece rotulada como "Candidata (DP, hipótesis)" y la transición hacia ella como "hipótesis por validar"; esto es coherente con el estado de hipótesis que declara `actividad_optima.puml` y con la nota de UC-05 en `casos_uso.puml`.
- Los delimitadores `@startuml`/`@enduml` están emparejados; el archivo no contiene bloques de control `if`, `while` ni `repeat`, por lo que no aplica la comprobación de esos pares.

### `docs/ciclo1_requerimientos.md`

- La sección 6 define RF-01 a RF-10; RF-01 exige H ≥ 1 y N ≥ 1, y RF-09 incluye ceros, negativos y entradas no numéricas entre los valores que se deben validar.
- La sección 9 exige error de validación para N = 0 y H = 0.
- La matriz de trazabilidad de la sección 11 asigna `componentes.puml` a RF-06 y deja pendiente el diagrama para RF-08. Esa matriz es orientativa por ciclo; la representación de RF-06 en el Ciclo 1 queda cubierta por UC-07 y por `comparacion_estrategias.puml`.

### `docs/ciclo1_decisiones_tecnicas.md`

| Decisión | Evidencia comprobada | Resultado |
|---|---|---|
| Python como lenguaje | ADR-001 compara Python con Java, JavaScript/TypeScript y C++, presenta criterios puntuados y selecciona Python 3.11+. Justifica claridad para el algoritmo, productividad e integración con Streamlit. | Justificada en el documento. |
| Streamlit para la interfaz | ADR-002 compara Streamlit con Flask + HTML, Gradio y Tkinter; fundamenta su elección en componentes nativos y menor esfuerzo de interfaz. | Justificada en el documento. |
| Arquitectura de dos capas | ADR-003 separa `app/` (presentación) de `src/` (dominio), relacionándolo con RNF-04 y la facilidad para probar lógica sin abrir la UI. | Justificada en el documento. |
| No usar Java | ADR-001 explica que una interfaz web en Java añade servidor y tecnologías como JSF/Spring y HTML, incrementando el esfuerzo de una parte que no es el foco. | Justificado en el documento. |
| No implementar una API con Uvicorn | ADR-003 expone que hay un solo cliente, sin persistencia ni integración externa; una API sumaría proceso, contratos HTTP y despliegue. ADR-002 indica que Streamlit incluye servidor. | Justificado en el documento. |
| Regla ADR-003 | Establece que `src/` no importa Streamlit, que `app/` no contiene fórmulas y que las funciones de dominio son puras. | Regla documentada; no se puede verificar su cumplimiento en código porque `src/` y `app/` solo contienen `.gitkeep`. |

## Observaciones nuevas

| ID | Documento | Observación | Acción |
|---|---|---|---|
| ARQ-03 | `docs/ciclo1_decisiones_tecnicas.md` | La tabla inicial "Relacionado con" cita `docs/requerimientos.md`, pero el documento de requisitos presente y revisado es `docs/ciclo1_requerimientos.md`. | Corregir la referencia de trazabilidad para usar la ruta real: `docs/ciclo1_requerimientos.md`. |

**Corrección concreta de ARQ-03**

Fragmento actual:

```markdown
| Relacionado con | `docs/requerimientos.md` v0.2, `diagramas/*.puml` |
```

Fragmento recomendado:

```markdown
| Relacionado con | `docs/ciclo1_requerimientos.md` v0.2, `diagramas/*.puml` |
```

La modificación alinea el enlace con el nombre real del documento de requisitos y evita una referencia inexistente.

## Verificación de sintaxis PlantUML

Se ejecutó el parser local de PlantUML (`-checkonly`) en los cinco diagramas fuente revisados: `casos_uso.puml`, `actividad_lineal.puml`, `actividad_binaria.puml`, `actividad_optima.puml` y `comparacion_estrategias.puml`. La ejecución terminó con código de salida 0. También están emparejados sus delimitadores `@startuml`/`@enduml` y, en las actividades, los bloques de control correspondientes.
## Conclusión

**¿El diseño del Ciclo 1 está listo para pasar al prototipo del Ciclo 2? Sí, con una corrección menor pendiente.**

Los cinco diagramas están trazados: los casos de uso cubren RF-01 a RF-10, las actividades lineal, binaria y óptima validan las entradas y modelan sus flujos, y comparacion de estrategias cubre RF-06 con la candidata rotulada como hipótesis. ARQ-01 y ARQ-02 quedan verificados. El ADR justifica Python, Streamlit, las dos capas y el descarte de Java y de una API con Uvicorn.

Queda pendiente ARQ-03 (ruta a `docs/requerimientos.md` en el ADR); al corregirla, la revisión puede cerrarse. El cumplimiento de ADR-003 en código se verificará en el Ciclo 2, cuando `src/` y `app/` tengan módulos inspeccionables.
