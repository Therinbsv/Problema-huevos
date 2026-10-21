# Acta de cierre del Ciclo 1 — Concepto (hito LCO)

| Campo | Valor |
|---|---|
| Release | `v0.1-ciclo1` |
| Épica Jira | HUEVO-14 |
| Fecha de la reunión | pendiente |
| Asistentes | pendiente |

## C1 — Objetivos

- Entender el problema de los huevos y sus supuestos.
- Definir los requerimientos del sistema.
- Modelar las estrategias candidatas lineal, binaria y candidata C, sin elegir todavía una solución.

## C2 — Riesgos

| ID | Riesgo | Issue | Estado |
|---|---|---|---|
| RK-01 | Malinterpretar el problema | HUEVO-2 | Pendiente de validación con el docente |
| RK-02 | Elegir una estrategia subóptima | HUEVO-3 | Identificado; se evalúa con prototipo en el Ciclo 2 |

## C3 — Desarrollo y revisión

| Entregable | Issue | Elaborado por | Revisado por |
|---|---|---|---|
| Especificación de requerimientos | HUEVO-1 | Desarrollador frontend / Gestor | Analista |
| Diagrama de casos de uso | HUEVO-4 | Desarrollador frontend / Gestor | Arquitecto |
| Diagramas de actividad (3 estrategias) | HUEVO-5 | Desarrollador frontend / Gestor | Arquitecto |
| Decisiones técnicas (ADR-001 a ADR-005) | HUEVO-6 | Desarrollador frontend / Gestor | Arquitecto y Desarrollador backend |
| Revisión de arquitectura | HUEVO-7 | Arquitecto | Analista |
| Plan de pruebas | HUEVO-1 | QA | Analista |

Los documentos del Ciclo 1 fueron redactados por el desarrollador frontend y revisados por cada rol desde su especialidad, como parte de la evaluación del ciclo.

## Observaciones de la revisión

- ARQ-01: N = 0 pasa a ser un error de validación; la revisión de arquitectura lo registra como verificado.
- ARQ-02: se agregan relaciones `<<include>>` de «Ingresar H y N» a «Comparar» y «Simular»; la revisión de arquitectura lo registra como verificado.
- (agregar observaciones de los revisores)

## C4 — Decisión

| Opción | Decisión |
|---|---|
| Continuar | [Continuar / pendiente] |
| Ajustar | |
| Abortar | |

Motivo: Pendiente de decisión del equipo en la reunión de cierre.

## Aprobación


| Rol | Nombre | Decisión | Fecha |
|---|---|---|---|
| Analista de requisitos y riesgos | Josue Quintana| Elaborado | 20/10/2026|
| Arquitecto y modelador | Anayomi Quishpe| Revisado | 20/10/2026|
| Líder de proyecto | Jorge Revelo| Continuar  | 20/10/2026|
| Docente | Ing. Patricio Paccha| Validado |20/10/2026 |