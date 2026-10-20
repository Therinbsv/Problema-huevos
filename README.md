# Problema de los huevos — Modelo en espiral

Proyecto académico: encontrar el piso crítico en un edificio de N pisos con H huevos, minimizando los lanzamientos en el peor caso, aplicando el modelo en espiral de Boehm.

## Estado

| Ciclo | Contenido | Release |
|---|---|---|
| 1 — Concepto (LCO) | Requerimientos, decisiones técnicas, diagramas | `v0.1-ciclo1` |
| 2 — Estrategias simples (LCA) | Lineal y binaria, pruebas, prototipo | `v0.2-ciclo2` |
| 3 — Modelo óptimo | Pendiente | |
| 4 — Producto (IOC) | Pendiente | |

## Estructura

```
app/        Interfaz (Streamlit)
src/        Lógica del problema, sin dependencias de interfaz
tests/      Pruebas (pytest)
docs/       Requerimientos, decisiones técnicas, actas por ciclo
diagramas/  PlantUML
```

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
