# Problema de los huevos — Modelo en espiral

[![Pruebas](https://github.com/grupo5-espiral/Problema-huevos/actions/workflows/pruebas.yml/badge.svg)](https://github.com/grupo5-espiral/Problema-huevos/actions/workflows/pruebas.yml)

Proyecto académico: encontrar el piso crítico en un edificio de N pisos con H huevos, minimizando los lanzamientos en el peor caso, aplicando el modelo en espiral de Boehm.

## Equipo

| Rol | Nombre |
|---|---|
| Líder de proyecto | Jorge Revelo |
| Analista de requisitos y riesgos | Josue Quintana |
| Arquitecto y modelador | Anayomi Quishpe |
| Desarrollador backend y Gestor (repositorio, ramas y releases) | Matthew Redín |
| Desarrollador frontend y Gestor (actas, README, informe y publicación) | Katherine Sánchez |
| QA y validación | Josselin Pozo |

## Estado

| Ciclo | Contenido | Release |
|---|---|---|
| 1 — Concepto (LCO) | Requerimientos, decisiones técnicas, diagramas | `v0.1-ciclo1` |
| 2 — Estrategias simples (LCA) | Lineal y binaria, pruebas, prototipo | `v0.2-ciclo2` |
| 3 — Modelo óptimo | 🔄 en revisión | `v0.3-ciclo3` |
| 4 — Producto (IOC) | Pendiente | |

Ciclo 3 pasará a ✅ cuando se fusione el Pull Request.

## Estructura

```
app/        Interfaz (Streamlit)
src/        Lógica del problema, sin dependencias de interfaz
            estrategias.py: estrategias lineal, binaria y óptima (RF-04, RF-05)
tests/      Pruebas (pytest)
docs/       Requerimientos, decisiones técnicas, actas por ciclo
            ciclo3_acta.md: acta del ciclo 3 — Modelo óptimo
diagramas/  PlantUML
```

## Documentación

| Archivo | Contenido |
|---|---|
| `docs/ciclo3_acta.md` | Objetivos, riesgos, resultados, trazabilidad y decisión del Ciclo 3 |
| `src/estrategias.py` | Estrategias lineal y binaria; estrategia óptima (RF-04, RF-05) |

## Cómo ejecutarlo

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt

pytest -v                  # pruebas
streamlit run app/main.py  # prototipo en http://localhost:8501
```

## Convenciones

- Una rama por ciclo (`ciclo-1`, `ciclo-2`, …) integrada a `main` con Pull Request revisado.
- Cada commit incluye la clave del issue de Jira: `HUEVO-12: descripción`.
- GitHub Actions ejecuta las pruebas en cada PR; no se integra un PR con pruebas fallidas.
