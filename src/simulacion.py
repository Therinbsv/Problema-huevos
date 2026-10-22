"""Simulación paso a paso de la búsqueda del piso crítico.

Convierte los lanzamientos de cualquier estrategia (lineal, binaria u óptima)
en pasos que una persona puede seguir: desde qué piso se lanzó, si el huevo se
rompió, cuántos huevos quedan y entre qué pisos puede estar todavía el piso crítico.

El programa NO usa el piso crítico k para decidir dónde lanzar: cada estrategia
solo ve si el huevo se rompió o no. k representa la realidad que el usuario elige
para ver la búsqueda en acción.

Rango del piso crítico: empieza en [1, N+1]. N+1 significa que el huevo no se
rompe en ningún piso (supuesto S5).
- Si el huevo se rompe en el piso p, el piso crítico es p o uno más bajo: alto = p.
- Si no se rompe, el piso crítico está más arriba: bajo = p + 1.
La búsqueda termina cuando bajo == alto: ese es el piso crítico.

Trazabilidad: RF-07 | Riesgo: RK-04 (la demo debe entenderse sin explicación)
"""

from dataclasses import dataclass

from src.estrategias import (
    Lanzamiento,
    simular_binaria,
    simular_lineal,
    simular_optima,
)
from src.validacion import validar_entrada

ESTRATEGIAS = ("lineal", "binaria", "optima")


@dataclass(frozen=True)
class Paso:
    """Un lanzamiento explicado."""

    numero: int            # 1, 2, 3, ...
    piso: int              # piso desde el que se lanzó
    se_rompio: bool
    huevos_restantes: int  # huevos que quedan después de este lanzamiento
    bajo: int              # el piso crítico está entre bajo ...
    alto: int              # ... y alto (N+1 = no se rompe en ningún piso)
    texto: str             # explicación para mostrar en la app


def describir_rango(bajo: int, alto: int, n: int) -> str:
    """Explica en palabras dónde puede estar el piso crítico."""
    if bajo == alto:
        if bajo == n + 1:
            return "El huevo no se rompe en ningún piso."
        return f"El piso crítico es el {bajo}."
    if alto == n + 1:
        if bajo == n:
            return f"El piso crítico es el {n}, o el huevo no se rompe en ningún piso."
        return f"El piso crítico está entre {bajo} y {n}, o el huevo no se rompe en ningún piso."
    return f"El piso crítico está entre {bajo} y {alto}."


def _texto_huevos(huevos: int) -> str:
    if huevos == 0:
        return "no quedan huevos"
    return "queda 1 huevo" if huevos == 1 else f"quedan {huevos} huevos"


def pasos_desde_lanzamientos(lanzamientos: list[Lanzamiento], h: int, n: int) -> list[Paso]:
    """Convierte la lista [(piso, se_rompio), ...] de una estrategia en pasos explicados."""
    validar_entrada(h, n)
    bajo, alto, huevos = 1, n + 1, h
    pasos: list[Paso] = []

    for numero, (piso, rompio) in enumerate(lanzamientos, start=1):
        if rompio:
            huevos -= 1
            alto = piso
            resultado = "se rompe"
        else:
            bajo = piso + 1
            resultado = "no se rompe"
        texto = (
            f"Lanzo desde el piso {piso}: {resultado} ({_texto_huevos(huevos)}). "
            f"{describir_rango(bajo, alto, n)}"
        )
        pasos.append(Paso(numero, piso, rompio, huevos, bajo, alto, texto))

    return pasos


def simular(estrategia: str, h: int, n: int, k: int) -> list[Paso]:
    """RF-07: simula la búsqueda paso a paso con la estrategia elegida.

    estrategia: "lineal", "binaria" u "optima".
    k: piso crítico elegido por el usuario (1 … N+1; N+1 = no se rompe).
    """
    if estrategia == "lineal":
        validar_entrada(h, n)
        lanzamientos = simular_lineal(n, k)
    elif estrategia == "binaria":
        lanzamientos = simular_binaria(h, n, k)
    elif estrategia == "optima":
        lanzamientos = simular_optima(h, n, k)
    else:
        raise ValueError(f"Estrategia desconocida: {estrategia!r}. Usa una de {ESTRATEGIAS}.")
    return pasos_desde_lanzamientos(lanzamientos, h, n)


def simular_todas(h: int, n: int, k: int) -> dict[str, list[Paso]]:
    """Simula las tres estrategias con el mismo piso crítico, para compararlas."""
    return {estrategia: simular(estrategia, h, n, k) for estrategia in ESTRATEGIAS}


def piso_critico(pasos: list[Paso], n: int) -> int:
    """Piso crítico encontrado al final de la simulación (N+1 = no se rompe)."""
    if not pasos:
        raise ValueError("La simulación no tiene pasos.")
    ultimo = pasos[-1]
    if ultimo.bajo != ultimo.alto:
        raise ValueError("La simulación terminó sin determinar el piso crítico.")
    return ultimo.bajo
