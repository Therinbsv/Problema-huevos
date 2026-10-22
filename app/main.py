"""Aplicación final — Problema de los huevos (Ciclo 4).

Capa de presentación: solo lee entradas, llama a src/ y muestra resultados.
No contiene fórmulas de cálculo (RNF-04, ADR-003). El edificio es una imagen
dibujada con Pillow (app/escena.py), sin HTML, CSS ni JS propios (R-02).

Pestañas:
- Simular:       el juego. El sistema esconde un piso crítico y tú lo buscas.
- Comparar:      peor caso de las tres estrategias según el número de huevos.
- Gráfico:       cómo cambia el peor caso al agregar huevos.
- Cómo funciona: explicación y ejemplo paso a paso de cada estrategia.

Ejecutar desde la raíz del repositorio:
    python -m streamlit run app/main.py

Trazabilidad: RF-01 a RF-10 | Riesgos: RK-02, RK-03, RK-04 | Issues: HUEVO-27, HUEVO-29
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.escena import dibujar_escena  # noqa: E402
from src.estrategias import (  # noqa: E402
    min_lanzamientos,
    peor_caso_binaria,
    peor_caso_lineal,
    secuencia_pisos,
)
from src.juego import (  # noqa: E402
    GANADO,
    JUGANDO,
    PISOS_JUEGO,
    estados_por_piso,
    evaluar,
    lanzar,
    nuevo_juego,
    rango_valido,
    sortear_piso_critico,
)
from src.simulacion import ESTRATEGIAS, describir_rango, piso_critico, simular  # noqa: E402
from src.validacion import MAX_HUEVOS  # noqa: E402

N = PISOS_JUEGO
NOMBRES = {"lineal": "Lineal", "binaria": "Binaria", "optima": "Óptima"}

st.set_page_config(page_title="Problema de los huevos", page_icon="🥚", layout="wide")


@st.cache_data
def tabla_por_huevos(pisos: int) -> dict[str, list[int]]:
    huevos = list(range(1, MAX_HUEVOS + 1))
    return {
        "Huevos": huevos,
        "Lineal": [peor_caso_lineal(pisos)] * len(huevos),
        "Binaria": [peor_caso_binaria(h, pisos) for h in huevos],
        "Óptima": [min_lanzamientos(h, pisos) for h in huevos],
    }


@st.cache_data
def imagen_escena(estados: tuple, marcador, rotos: int, critico) -> object:
    return dibujar_escena(N, dict(estados), marcador=marcador, rotos=rotos, piso_critico=critico)


# ---------------------------------------------------------------- Estado de la partida

def empezar_partida() -> None:
    """Nueva partida con los huevos que muestra el control y un piso crítico sorteado."""
    huevos = st.session_state.get("huevos_sel", 2)
    st.session_state.juego = nuevo_juego(huevos, N, sortear_piso_critico(N))
    st.session_state.mensaje = None


def accion_lanzar() -> None:
    """Callback del botón: lanza desde el piso escrito y guarda el mensaje."""
    juego = st.session_state.juego
    piso = int(st.session_state[f"piso_{len(juego.lanzamientos)}"])
    nuevo = lanzar(juego, piso)
    st.session_state.juego = nuevo
    se_rompio = nuevo.lanzamientos[-1][1]
    if se_rompio:
        quedan = nuevo.huevos
        resto = "no te quedan huevos" if quedan == 0 else f"te quedan {quedan}"
        st.session_state.mensaje = ("roto", f"💥 **Se rompió** desde el piso {piso}; {resto}.")
    else:
        st.session_state.mensaje = ("ok", f"✅ **Sobrevivió** en el piso {piso}. El huevo sigue intacto.")


if "juego" not in st.session_state:
    empezar_partida()

st.title("🥚 Problema de los huevos")
st.caption("Encuentra el piso más bajo desde el que un huevo se rompe, con pocos lanzamientos.")

tab_simular, tab_comparar, tab_grafico, tab_explicacion = st.tabs(
    ["🎯 Simular", "📊 Comparar", "📈 Gráfico", "💡 Cómo funciona"]
)

# ================================================================ Simular
with tab_simular:
    izquierda, derecha = st.columns([5, 4], gap="large")
    juego = st.session_state.juego

    with izquierda:
        st.markdown(
            f"El edificio tiene **{N} pisos**. Hay un piso crítico escondido: desde ahí (y desde "
            "cualquier piso más alto) el huevo se rompe. Elige cuántos huevos usar y desde qué "
            "piso lanzar. **Un huevo solo se gasta si se rompe.**"
        )
        st.slider(
            "Cantidad de huevos", 1, MAX_HUEVOS, value=2, key="huevos_sel",
            on_change=empezar_partida,
            help="Cambiarla empieza una partida nueva.",
        )

        c1, c2 = st.columns(2)
        c1.metric("Lanzamientos", len(juego.lanzamientos))
        huevos_vivos = "🥚" * juego.huevos + "💥" * juego.huevos_rotos
        c2.metric("Huevos", f"{juego.huevos} de {juego.huevos_iniciales}")
        c2.caption(huevos_vivos)

        elegido = None
        if juego.estado == JUGANDO:
            minimo, maximo = rango_valido(juego)
            elegido = st.number_input(
                "Piso desde el que lanzas", min_value=minimo, max_value=maximo,
                value=(minimo + maximo) // 2, step=1,
                key=f"piso_{len(juego.lanzamientos)}",
            )
            st.button("🥚 Lanzar", type="primary", on_click=accion_lanzar)
            st.caption("Pista: " + describir_rango(juego.bajo, juego.alto, N))

        mensaje = st.session_state.get("mensaje")
        if mensaje and juego.estado == JUGANDO:
            (st.error if mensaje[0] == "roto" else st.success)(mensaje[1])

        if juego.estado != JUGANDO:
            r = evaluar(juego)
            donde = (
                "El huevo no se rompe en ningún piso." if r.piso_critico == N + 1
                else f"El piso crítico era el **{r.piso_critico}**."
            )
            if juego.estado == GANADO:
                st.success(
                    f"🏆 **¡Lo encontraste!** {donde} Lo lograste en **{r.lanzamientos_usuario}** "
                    f"lanzamientos y rompiste {r.huevos_rotos} huevo(s)."
                )
            else:
                st.error(
                    f"😵 **Te quedaste sin huevos.** {donde} Con {r.huevos_rotos} huevos rotos no "
                    "alcanzó para descartar todos los pisos."
                )
            m1, m2, m3 = st.columns(3)
            m1.metric("Tus lanzamientos", r.lanzamientos_usuario)
            m2.metric("Óptima en este piso", r.lanzamientos_optimos,
                      help="Lanzamientos que habría usado la estrategia óptima con este mismo piso crítico.")
            m3.metric("Garantizado", r.lanzamientos_garantizados,
                      help=f"Máximo de lanzamientos que la óptima asegura con {juego.huevos_iniciales} huevo(s), pase lo que pase.")
            st.caption(
                f"Con {juego.huevos_iniciales} huevo(s), la estrategia óptima garantiza encontrar el piso "
                f"en **{r.lanzamientos_garantizados}** lanzamientos como máximo."
            )

        st.button("🔄 Nueva partida", on_click=empezar_partida)

        if juego.lanzamientos:
            with st.expander("Historial de lanzamientos"):
                st.table(
                    {
                        "N.º": list(range(1, len(juego.lanzamientos) + 1)),
                        "Piso": [p for p, _ in juego.lanzamientos],
                        "Resultado": ["💥 se rompió" if r_ else "✅ sobrevivió" for _, r_ in juego.lanzamientos],
                    }
                )

    with derecha:
        terminado = juego.estado != JUGANDO
        st.image(
            imagen_escena(
                tuple(sorted(estados_por_piso(juego).items())),
                int(elegido) if elegido is not None else None,
                juego.huevos_rotos,
                juego.piso_critico if terminado and juego.piso_critico <= N else None,
            ),
            width=400,
        )

# ================================================================ Comparar
with tab_comparar:
    h_cmp = st.slider("Huevos", 1, MAX_HUEVOS, value=2, key="huevos_cmp")
    lineal, binaria, optima = peor_caso_lineal(N), peor_caso_binaria(h_cmp, N), min_lanzamientos(h_cmp, N)
    st.caption(f"Lanzamientos necesarios en el peor caso, con {N} pisos.")
    c1, c2, c3 = st.columns(3)
    c1.metric("Lineal", lineal)
    c2.metric("Binaria", binaria)
    c3.metric("Óptima", optima)
    if optima < binaria:
        st.success(f"Con {h_cmp} huevo(s), la óptima garantiza **{optima}** lanzamientos, frente a **{binaria}** de la binaria.")
    else:
        st.info(f"Con {h_cmp} huevo(s) la binaria ya alcanza el mínimo ({binaria} lanzamientos).")
    st.markdown("**Pisos que usa la óptima mientras el primer huevo no se rompe:**")
    st.write(", ".join(str(p) for p in secuencia_pisos(h_cmp, N)))
    with st.expander("Ver tabla para todos los huevos"):
        st.table(tabla_por_huevos(N))

# ================================================================ Gráfico
with tab_grafico:
    st.subheader("¿Cómo cambia con el número de huevos?")
    st.line_chart(tabla_por_huevos(N), x="Huevos", y=["Lineal", "Binaria", "Óptima"],
                  y_label="Lanzamientos (peor caso)")
    st.caption("Con 1 huevo las tres estrategias coinciden. Desde 7 huevos ya no se mejora: es el mínimo para 100 pisos.")

# ================================================================ Cómo funciona
with tab_explicacion:
    st.markdown(
        """
**¿Qué es el peor caso?** No sabemos desde qué piso se rompe el huevo. El peor caso es la cantidad
de lanzamientos que necesitas si ese piso está donde más le cuesta a tu estrategia. Es lo que la
estrategia **garantiza**.

- **Lineal:** sube piso por piso. Usa un solo huevo, pero puede necesitar 100 lanzamientos.
- **Binaria:** lanza desde la mitad. Es rápida con muchos huevos, pero con pocos se arriesga demasiado.
- **Óptima:** reparte los saltos para que, se rompa donde se rompa el huevo, el trabajo restante
  quepa justo en los lanzamientos que quedan.
"""
    )
    st.subheader("Mira cómo lo resolvería cada estrategia")
    e1, e2, e3 = st.columns(3)
    estrategia = e1.selectbox("Estrategia", ESTRATEGIAS, index=2, format_func=NOMBRES.get)
    h_ej = e2.slider("Huevos", 1, MAX_HUEVOS, value=2, key="huevos_ej")
    k_ej = e3.number_input("Piso crítico (N+1 = no se rompe)", min_value=1, max_value=N + 1, value=28, step=1)
    pasos = simular(estrategia, h_ej, N, int(k_ej))
    for paso in pasos:
        st.markdown(f"{paso.numero}. {paso.texto}")
    st.success(f"Encontró el piso crítico ({piso_critico(pasos, N)}) en **{len(pasos)}** lanzamientos.")
