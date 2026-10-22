# Informe final — Problema de los huevos con el modelo en espiral

| Campo | Valor |
|---|---|
| Asignatura | Metodologías Ágiles — Escuela Politécnica Nacional |
| Equipo | 6 integrantes (ver sección 3) |
| Repositorio | https://github.com/grupo5-espiral/Problema-huevos |
| App publicada | *COMPLETAR: enlace de Streamlit Cloud* |
| Release final | `v1.0` |
| Responsable del informe | Gestor de configuración y documentación |

## 1. Resumen

El equipo resolvió el problema de los huevos aplicando el modelo en espiral de Boehm en 4 ciclos. Cada ciclo redujo un riesgo antes de construir el siguiente. El hallazgo central llegó en el Ciclo 2: la búsqueda binaria, que parecía la solución natural, necesita **50 lanzamientos** con 2 huevos y 100 pisos, mientras que la estrategia óptima necesita **14**. Ese riesgo se detectó con un prototipo barato, y el rumbo se corrigió antes de invertir en la solución final.

El producto es una aplicación web en Streamlit con un juego en el que el usuario busca el piso crítico y compara su resultado con la estrategia óptima, además de un comparador de estrategias, un gráfico y la explicación del modelo. Tiene 171 pruebas automáticas que se ejecutan en cada Pull Request.

## 2. El problema

En un edificio de N pisos se dispone de H huevos idénticos. Existe un piso crítico k: desde el piso k o superior el huevo se rompe, y desde uno inferior no. El objetivo es encontrar k con el **menor número de lanzamientos en el peor caso**. Los supuestos (huevo reutilizable si no se rompe, monotonía, peor caso) están en `docs/ciclo1_requerimientos.md`, sección 5.

## 3. Equipo y roles

| Rol | Integrante | Herramienta que lidera | Aporte principal |
|---|---|---|---|
| Líder de proyecto | Jorge Revelo | Jira | Decisiones de cada ciclo y comunicación con el docente |
| Analista de requisitos y riesgos | Josue Quintana | Jira (riesgos) | Requerimientos y registro de riesgos RK-01 a RK-04 |
| Arquitecto y modelador | Anayomi Quishpe | PlantUML | Diagramas y decisiones técnicas (ADR) |
| Desarrollador backend y gestor (repositorio, ramas y releases) | Matthew Redín | VS Code + GitHub | Implementación de `src/`, ramas y releases |
| Desarrollador frontend y gestor (actas, README, informe y publicación) | *COMPLETAR: verificar con la tabla Equipo del README* | VS Code + Streamlit | Implementación de `app/`, actas, informe y publicación |
| QA y validación | Josselin Pozo | GitHub (PR y pruebas) | Pruebas automáticas y prueba de usabilidad |

## 4. Herramientas

| Herramienta | Uso | Justificación |
|---|---|---|
| Jira | Épicas por ciclo, historias, tareas y riesgos con probabilidad, impacto y mitigación | Hace visible el análisis de riesgos, que es lo que distingue a la espiral |
| PlantUML | Diagramas como texto dentro del repositorio | El historial muestra cómo evolucionó el diseño |
| VS Code | Entorno único para código, diagramas y Git | Todos trabajan con el mismo entorno |
| GitHub | Ramas por ciclo, PR revisados, Actions y releases | Cada ciclo queda congelado y verificable |
| Streamlit | Interfaz web solo con Python | Cada ciclo termina con un prototipo evaluable sin invertir en frontend |

Las alternativas descartadas (Java, JavaScript, pandas, Plotly, FastAPI + Uvicorn) y sus razones están en `docs/ciclo1_decisiones_tecnicas.md`.

## 5. Los 4 ciclos

| Ciclo | Objetivo (C1) | Riesgo (C2) | Resultado (C3) | Decisión (C4) | Release |
|---|---|---|---|---|---|
| 1 — Concepto (LCO) | Entender el problema y modelar las alternativas | RK-01 Malinterpretar el problema | Requerimientos, ADR y 4 diagramas; 3 estrategias candidatas | Avanzar a prototipos | `v0.1-ciclo1` |
| 2 — Estrategias simples (LCA) | Probar lineal y binaria | RK-02 Estrategia subóptima | Binaria: 50 lanzamientos con 2 huevos frente a 14 de referencia | Descartar la binaria y avanzar con la estrategia óptima | `v0.2-ciclo2` |
| 3 — Modelo óptimo | Implementar y demostrar la óptima | RK-03 Casos borde | 14, 9 y 7 lanzamientos con 2, 3 y 7 huevos; el peor caso medido por simulación exhaustiva coincide con el cálculo. Al revisar la interfaz se detectó que los pisos resaltados no se entendían y que usaba CSS propio (incumplía R-02) | Avanzar al producto rediseñando la interfaz | `v0.3-ciclo3` |
| 4 — Producto (IOC) | Interfaz comprensible y completa | RK-04 Usabilidad | App con juego, comparador, gráfico y explicación; 171 pruebas; prueba con usuarios externos | *COMPLETAR en la reunión de cierre* | `v1.0` |

El detalle de cada ciclo está en su acta: `docs/ciclo2_decision.md`, `docs/ciclo3_acta.md` y `docs/ciclo4_acta.md`.

## 6. Modelo matemático

La estrategia óptima responde la pregunta inversa: con h huevos y t lanzamientos, ¿cuántos pisos se resuelven con certeza?

```
f(h, t) = f(h-1, t-1) + f(h, t-1) + 1        con f(0, t) = f(h, 0) = 0
```

El mínimo de lanzamientos es el menor t con f(H, t) ≥ N. Con 2 huevos, f(2, 13) = 91 y f(2, 14) = 105, por lo que hacen falta 14 lanzamientos para 100 pisos. La secuencia de pisos del primer huevo es 14, 27, 39, 50, 60, 69, 77, 84, 90, 95, 99 y 100.

| Huevos (N = 100) | Lineal | Binaria | Óptima |
|---|---|---|---|
| 1 | 100 | 100 | 100 |
| 2 | 100 | 50 | 14 |
| 3 | 100 | 26 | 9 |
| 4 | 100 | 14 | 8 |
| 7 | 100 | 7 | 7 |

Con 7 huevos o más ya no se mejora: 7 es el mínimo posible para 100 pisos.

## 7. El producto

La aplicación tiene cuatro pestañas:

- **Simular:** un juego. El sistema esconde el piso crítico; el usuario elige cuántos huevos usar y desde qué piso lanzar. Un huevo se gasta solo si se rompe. Se gana al determinar el piso crítico y se pierde si se acaban los huevos. Al terminar se compara con la estrategia óptima y con el máximo garantizado. La idea que transmite es la del problema: no gana la suerte, gana la estrategia que garantiza el peor caso.
- **Comparar:** lineal, binaria y óptima en una vista, con la secuencia de pisos.
- **Gráfico:** lanzamientos según el número de huevos.
- **Cómo funciona:** el modelo matemático y la simulación paso a paso con el piso crítico que elige el usuario.

La decisión de agregar el modo juego está justificada en `docs/adr-006_modo_juego.md`: reduce RK-04 y define la tarea de la prueba de usabilidad (RNF-03). No agregó dependencias ni requerimientos nuevos.

## 8. Arquitectura y calidad

- **Dos capas** (`diagramas/componentes.puml`): `src/` contiene la lógica pura y `app/` solo la presentación. El edificio se dibuja con Pillow y se muestra como imagen, sin HTML, CSS ni JavaScript propios (R-02).
- **171 pruebas automáticas** con pytest, ejecutadas por GitHub Actions en cada Pull Request:
    - valores de referencia;
    - simulación de todos los pisos críticos posibles;
    - reglas del juego (huevos, ganar y perder, rango válido);
    - casos borde y rendimiento (menos de 0,3 s con N = 1000 y H = 10).
- **Revisión obligatoria:** ningún cambio entra a `main` sin un PR aprobado por otro integrante.

## 9. Trazabilidad

Cada requerimiento se puede seguir hasta su prueba y su release, y cada commit hasta su issue de Jira:

```
Requerimiento (RF/RNF) → Riesgo (RK) → Issue (HUEVO-n) → Commit → Prueba → Release
```

Ejemplos:

- **RF-03** (búsqueda binaria) → **RK-02** → **HUEVO-10** → `test_rk02_binaria_falla_con_2_huevos` → `v0.2-ciclo2`.
- **RF-07** (simulación) → **RK-04** → **HUEVO-26, 27 y 28** → `test_juego` y `test_simulacion` → `v1.0`.

La matriz completa de requerimientos está en `docs/ciclo4_acta.md`, sección "Cobertura de requerimientos".

## 10. Prueba de usabilidad

*COMPLETAR con los resultados reales de `docs/ciclo4_usabilidad.md`: número de usuarios, cuántos completaron las cuatro tareas sin ayuda, problemas encontrados y cambios aplicados.*

## 11. Lecciones aprendidas

*COMPLETAR en la reunión de cierre. Preguntas guía:*

- ¿Qué habría pasado si hubiéramos usado cascada y diseñado la binaria como solución desde el inicio?
- ¿Qué riesgo nos costó más identificar?
- ¿Qué haríamos distinto en la organización del equipo?
- Del Ciclo 3 al 4: ¿qué cambió al detectar que la interfaz no se entendía y que incumplía R-02?

## 12. Conclusión

El modelo en espiral fue adecuado para este problema porque su mayor riesgo, elegir una estrategia que parece correcta pero no lo es, se podía detectar barato y temprano. El Ciclo 2 lo demostró: un prototipo de pocas horas descartó la binaria antes de comprometer el diseño final. El Ciclo 3 volvió a mostrar su valor: al revisar el prototipo aparecieron dos problemas (la interfaz no se entendía y no cumplía una restricción), y el Ciclo 4 los corrigió antes de entregar. El resultado es un producto correcto y verificado, con cada decisión documentada y rastreable.
