"""Prototipo del Ciclo 2 — Búsqueda lineal vs. búsqueda binaria.

Capa de presentación: solo lee entradas, llama a src/ y muestra resultados.
No contiene fórmulas de cálculo (RNF-04, ADR-003).

Ejecutar desde la raíz del repositorio:
    streamlit run app/main.py

Trazabilidad: RF-01, RF-02, RF-03, RF-09 | Riesgo evaluado: RK-02
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.estrategias import (  # noqa: E402
    peor_caso_binaria,
    peor_caso_lineal,
    simular_binaria,
)
from src.validacion import MAX_HUEVOS, MAX_PISOS, EntradaInvalida, validar_entrada  # noqa: E402

st.set_page_config(page_title="Problema de los huevos — Ciclo 2", page_icon="🥚", layout="centered")


@st.cache_data
def tabla_por_huevos(n: int) -> dict[str, list[int]]:
    huevos = list(range(1, MAX_HUEVOS + 1))
    return {
        "Huevos": huevos,
        "Lineal": [peor_caso_lineal(n)] * len(huevos),
        "Binaria": [peor_caso_binaria(h, n) for h in huevos],
    }


st.title("🥚 Problema de los huevos")
st.caption("Prototipo del Ciclo 2 · Evaluación de estrategias simples (hito LCA)")

st.markdown(
    "En un edificio de **N** pisos, con **H** huevos, hay que encontrar el piso más bajo "
    "desde el que un huevo se rompe, con el **menor número de lanzamientos en el peor caso**."
)

st.info(
    "**¿Qué es el peor caso?** No sabemos desde qué piso se rompe el huevo. "
    "El peor caso es la cantidad de lanzamientos que necesitas si ese piso está en el "
    "lugar más difícil para tu estrategia: es lo que la estrategia **garantiza**. "
    "Ejemplo: con 2 huevos, la binaria puede acertar en 2 lanzamientos con suerte, "
    "pero si el piso crítico es el 49 necesita 50."
)

# ---------------------------------------------------------------- Entradas (RF-01)
col_h, col_n = st.columns(2)
h = col_h.slider("Huevos (H)", min_value=1, max_value=MAX_HUEVOS, value=2)
n = col_n.number_input("Pisos (N)", min_value=1, max_value=MAX_PISOS, value=100, step=1)

try:
    h, n = validar_entrada(int(h), int(n))
except EntradaInvalida as error:  # RF-09
    st.error(str(error))
    st.stop()

# ---------------------------------------------------------------- Resultados (RF-02, RF-03)
lineal = peor_caso_lineal(n)
binaria = peor_caso_binaria(h, n)

st.subheader("Lanzamientos en el peor caso")
m1, m2 = st.columns(2)
m1.metric("Búsqueda lineal", lineal, help="Lanza piso por piso desde el 1. Usa un solo huevo.")
m2.metric(
    "Búsqueda binaria",
    binaria,
    delta=f"{binaria - lineal} vs. lineal" if binaria < lineal else None,
    delta_color="inverse",
    help="Lanza desde el piso medio; si queda un solo huevo, recorre el resto piso por piso.",
)

if h <= 3:
    st.warning(
        f"Con {h} huevo(s), la búsqueda binaria necesita **{binaria}** lanzamientos. "
        "Cuando se rompe el primer huevo en un piso alto, el resto debe revisarse piso por piso. "
        "La binaria **no aprovecha bien pocos huevos** (riesgo RK-02)."
    )
else:
    st.info(
        f"Con {h} huevos la binaria funciona bien ({binaria} lanzamientos), "
        "pero el caso exigido por el problema es con pocos huevos."
    )

# ---------------------------------------------------------------- Comparación por huevos
st.subheader("¿Cómo cambia con el número de huevos?")
datos = tabla_por_huevos(n)
st.line_chart(datos, x="Huevos", y=["Lineal", "Binaria"], y_label="Lanzamientos (peor caso)")
with st.expander("Ver tabla"):
    st.table(datos)

# ---------------------------------------------------------------- Peor caso paso a paso
st.subheader("El peor caso de la binaria, paso a paso")
peor_k = max(range(1, n + 2), key=lambda k: len(simular_binaria(h, n, k)))
recorrido = simular_binaria(h, n, peor_k)
texto_k = f"piso {peor_k}" if peor_k <= n else "no se rompe en ningún piso"
st.markdown(f"Piso crítico que produce el peor caso: **{texto_k}** → **{len(recorrido)}** lanzamientos.")
with st.expander("Ver lanzamientos"):
    st.table(
        {
            "Lanzamiento": list(range(1, len(recorrido) + 1)),
            "Piso": [piso for piso, _ in recorrido],
            "Resultado": ["Se rompe" if rompio else "No se rompe" for _, rompio in recorrido],
        }
    )

st.divider()
st.caption(
    "Conclusión del Ciclo 2: la búsqueda lineal es segura pero lenta y la binaria degrada con pocos "
    "huevos. Ninguna de las dos es la solución general; se avanza a la candidata C en el Ciclo 3."
)
