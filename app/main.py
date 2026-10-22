"""Prototipo del Ciclo 3 — Estrategia óptima.

Capa de presentación: solo lee entradas, llama a src/ y muestra resultados.
No contiene fórmulas de cálculo (RNF-04, ADR-003): el dibujo del edificio solo
ordena y pinta los pisos que devuelve secuencia_pisos().

Ejecutar desde la raíz del repositorio:
    python -m streamlit run app/main.py

Trazabilidad: RF-01 a RF-05, RF-09 | Riesgos: RK-02, RK-03 | Issue: HUEVO-24
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.estrategias import (  # noqa: E402
    min_lanzamientos,
    peor_caso_binaria,
    peor_caso_lineal,
    secuencia_pisos,
)
from src.validacion import MAX_HUEVOS, MAX_PISOS, EntradaInvalida, validar_entrada  # noqa: E402

PISOS_POR_FILA = 10
MAX_PISOS_DIBUJO = 300  # más pisos se muestran solo como texto
MAX_PISOS_EN_TEXTO = 30

st.set_page_config(page_title="Problema de los huevos — Ciclo 3", page_icon="🥚", layout="wide")


@st.cache_data
def tabla_por_huevos(n: int) -> dict[str, list[int]]:
    huevos = list(range(1, MAX_HUEVOS + 1))
    return {
        "Huevos": huevos,
        "Lineal": [peor_caso_lineal(n)] * len(huevos),
        "Binaria": [peor_caso_binaria(h, n) for h in huevos],
        "Óptima": [min_lanzamientos(h, n) for h in huevos],
    }


def html_resultado(lanzamientos: int, h: int, n: int) -> str:
    """Tarjeta grande con el resultado de la estrategia óptima."""
    return f"""
    <div style="border:2px solid #f59f00;border-radius:12px;padding:18px 22px;
                background:rgba(245,159,0,0.12);margin:6px 0 10px 0;">
      <div style="font-size:0.8rem;letter-spacing:0.08em;opacity:0.75;">ESTRATEGIA ÓPTIMA</div>
      <div style="font-size:3rem;font-weight:800;line-height:1.1;">{lanzamientos}
        <span style="font-size:1.2rem;font-weight:600;">lanzamientos garantizados</span></div>
      <div style="opacity:0.8;">Con {h} huevo(s) y {n} pisos.</div>
    </div>
    """


def html_edificio(n: int, pisos_de_lanzamiento: list[int]) -> str:
    """Cuadrícula de pisos: el piso 1 abajo y los pisos de la secuencia resaltados."""
    ordenados = {piso: orden for orden, piso in enumerate(pisos_de_lanzamiento, start=1)}
    filas = -(-n // PISOS_POR_FILA)  # techo de n / 10
    celdas = []
    for fila in range(filas - 1, -1, -1):  # la fila de arriba primero
        for col in range(PISOS_POR_FILA):
            piso = fila * PISOS_POR_FILA + col + 1
            if piso > n:
                celdas.append("<div></div>")
            elif piso in ordenados:
                celdas.append(
                    f'<div title="Lanzamiento {ordenados[piso]} del primer huevo: piso {piso}" '
                    'style="background:#f59f00;color:#1b1b1b;font-weight:800;border-radius:4px;'
                    f'padding:7px 0;text-align:center;font-size:0.85rem;">{piso}</div>'
                )
            else:
                celdas.append(
                    '<div style="background:rgba(128,128,128,0.16);opacity:0.6;border-radius:4px;'
                    f'padding:7px 0;text-align:center;font-size:0.75rem;">{piso}</div>'
                )
    return f"""
    <div style="max-width:520px;">
      <div style="text-align:center;font-size:0.8rem;opacity:0.7;margin-bottom:4px;">
        ▲ Piso {n}</div>
      <div style="display:grid;grid-template-columns:repeat({PISOS_POR_FILA},1fr);gap:4px;
                  border:2px solid rgba(128,128,128,0.5);border-radius:8px;padding:8px;">
        {"".join(celdas)}
      </div>
      <div style="text-align:center;font-size:0.8rem;opacity:0.7;margin-top:4px;">
        ▼ Piso 1 (planta baja)</div>
    </div>
    """


def texto_secuencia(secuencia: list[int]) -> str:
    if len(secuencia) <= MAX_PISOS_EN_TEXTO:
        return ", ".join(str(piso) for piso in secuencia)
    inicio = ", ".join(str(piso) for piso in secuencia[:MAX_PISOS_EN_TEXTO])
    return f"{inicio}, … ({len(secuencia)} lanzamientos en total)"


# ---------------------------------------------------------------- Encabezado
st.title("🥚 Problema de los huevos")
st.caption("Prototipo del Ciclo 3 · Estrategia óptima")
st.markdown(
    "Encuentra el piso más bajo desde el que un huevo se rompe, "
    "con el **menor número de lanzamientos en el peor caso**."
)

izquierda, derecha = st.columns([5, 6], gap="large")

# ---------------------------------------------------------------- Columna izquierda
with izquierda:
    st.info(
        "**¿Qué es el peor caso?** No sabemos desde qué piso se rompe el huevo. "
        "El peor caso es la cantidad de lanzamientos que necesitas si ese piso está en el "
        "lugar más difícil para tu estrategia: es lo que la estrategia **garantiza**."
    )

    h = st.slider("Huevos (H)", min_value=1, max_value=MAX_HUEVOS, value=2)  # RF-01

    with st.expander("Opciones avanzadas"):
        n = st.number_input(  # RF-01
            "Pisos (N)", min_value=1, max_value=MAX_PISOS, value=100, step=1,
            help="El problema clásico usa 100 pisos.",
        )

    try:
        h, n = validar_entrada(int(h), int(n))  # RF-09
    except EntradaInvalida as error:
        st.error(str(error))
        st.stop()

    lineal = peor_caso_lineal(n)  # RF-02
    binaria = peor_caso_binaria(h, n)  # RF-03
    optima = min_lanzamientos(h, n)  # RF-04
    secuencia = secuencia_pisos(h, n)  # RF-05

    st.html(html_resultado(optima, h, n))

    st.markdown("**Frente a las otras estrategias** (evidencia del Ciclo 2)")
    c1, c2, c3 = st.columns(3)
    c1.metric("Lineal", lineal)
    c2.metric("Binaria", binaria)
    c3.metric("Óptima", optima)

    if optima < binaria:
        st.success(
            f"Con {h} huevo(s), la óptima garantiza **{optima}** lanzamientos, "
            f"frente a **{binaria}** de la binaria."
        )
    else:
        st.info(f"Con {h} huevo(s) la binaria ya alcanza el mínimo ({binaria} lanzamientos).")

# ---------------------------------------------------------------- Columna derecha
with derecha:
    st.subheader("El edificio")
    st.markdown(
        "Los pisos **resaltados** son los que usa la estrategia óptima para lanzar el primer huevo. "
        "Mientras no se rompa, sube al siguiente resaltado; cuando se rompe, los huevos que quedan "
        "revisan los pisos intermedios."
    )
    if n <= MAX_PISOS_DIBUJO:
        st.html(html_edificio(n, secuencia))
    else:
        st.info(f"Con {n} pisos el edificio es demasiado grande para dibujarlo; se muestra solo la secuencia.")
    st.markdown("**Secuencia de pisos:**")
    st.markdown(texto_secuencia(secuencia))

# ---------------------------------------------------------------- Gráfico comparativo
st.divider()
st.subheader("¿Cómo cambia con el número de huevos?")
datos = tabla_por_huevos(n)
st.line_chart(datos, x="Huevos", y=["Lineal", "Binaria", "Óptima"], y_label="Lanzamientos (peor caso)")
with st.expander("Ver tabla"):
    st.table(datos)

st.caption(
    "Ciclo 3: la estrategia óptima se valida con los valores de referencia y con una búsqueda por "
    "fuerza bruta (tests/test_optima.py). El Ciclo 4 agrega el simulador y la explicación."
)