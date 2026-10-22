"""Juego interactivo: la persona busca el piso crítico lanzando huevos.

El sistema esconde un piso crítico k y la persona decide desde qué piso lanza
cada huevo. Solo se entera de si el huevo se rompió o no, igual que las
estrategias de estrategias.py. Esta capa NO conoce la interfaz (ADR-003).

Reglas (requerimientos, sección 5):
- S2: un huevo que sobrevive se reutiliza; solo se gasta cuando se rompe.
- S3: un huevo roto se pierde.
- S4: si se rompe desde el piso p, se rompe desde cualquier piso superior.
- S5: k = N + 1 significa que el huevo no se rompe en ningún piso.

Estado de la búsqueda: el piso crítico está siempre entre `bajo` y `alto`
(mismo criterio que simulacion.py). La persona gana cuando bajo == alto y
pierde si se queda sin huevos con el piso crítico todavía sin determinar.

Trazabilidad: RF-07 (simulación), RF-08 (resultado comprensible) | Riesgo: RK-04
"""

import random
from dataclasses import dataclass, replace
from typing import Optional

from src.estrategias import Lanzamiento, min_lanzamientos, simular_optima
from src.validacion import validar_entrada

PISOS_JUEGO = 100  # el problema clásico: el edificio siempre tiene 100 pisos

JUGANDO = "jugando"
GANADO = "ganado"
PERDIDO = "perdido"


@dataclass(frozen=True)
class Juego:
    """Estado inmutable de una partida."""

    huevos_iniciales: int
    pisos: int
    piso_critico: int  # oculto para la persona; N+1 = no se rompe en ningún piso
    huevos: int
    bajo: int
    alto: int
    lanzamientos: tuple[Lanzamiento, ...] = ()

    @property
    def estado(self) -> str:
        if self.bajo == self.alto:
            return GANADO
        if self.huevos == 0:
            return PERDIDO
        return JUGANDO

    @property
    def huevos_rotos(self) -> int:
        return self.huevos_iniciales - self.huevos


@dataclass(frozen=True)
class Resultado:
    """Comparación de una partida terminada con la estrategia óptima."""

    estado: str
    piso_critico: int
    lanzamientos_usuario: int
    lanzamientos_optimos: int  # la óptima para ESTE piso crítico
    lanzamientos_garantizados: int  # máximo que la óptima garantiza con H huevos
    huevos_rotos: int


def sortear_piso_critico(pisos: int = PISOS_JUEGO, azar: Optional[random.Random] = None) -> int:
    """Sortea el piso crítico entre 1 y N+1 (N+1 = el huevo no se rompe)."""
    return (azar or random).randint(1, pisos + 1)


def nuevo_juego(huevos: int, pisos: int, piso_critico: int) -> Juego:
    """Empieza una partida con el piso crítico dado (la interfaz lo sortea)."""
    validar_entrada(huevos, pisos)
    if not (1 <= piso_critico <= pisos + 1):
        raise ValueError(f"El piso crítico debe estar entre 1 y {pisos + 1}.")
    return Juego(huevos, pisos, piso_critico, huevos, bajo=1, alto=pisos + 1)


def rango_valido(juego: Juego) -> Optional[tuple[int, int]]:
    """Pisos desde los que tiene sentido lanzar: (mínimo, máximo), o None si terminó.

    Por debajo de `bajo` ya se sabe que el huevo sobrevive y desde `alto` o más
    ya se sabe que se rompe: lanzar ahí solo gastaría un huevo sin aprender nada.
    """
    if juego.estado != JUGANDO:
        return None
    return juego.bajo, juego.alto - 1


def lanzar(juego: Juego, piso: int) -> Juego:
    """Lanza un huevo desde `piso` y devuelve el nuevo estado de la partida."""
    if juego.estado != JUGANDO:
        raise ValueError("La partida ya terminó.")
    minimo, maximo = juego.bajo, juego.alto - 1
    if not (minimo <= piso <= maximo):
        raise ValueError(f"Solo conviene lanzar entre los pisos {minimo} y {maximo}.")

    rompio = piso >= juego.piso_critico  # monotonía (S4)
    lanzamientos = juego.lanzamientos + ((piso, rompio),)
    if rompio:
        return replace(juego, huevos=juego.huevos - 1, alto=piso, lanzamientos=lanzamientos)
    return replace(juego, bajo=piso + 1, lanzamientos=lanzamientos)


def evaluar(juego: Juego) -> Resultado:
    """Compara una partida terminada con la estrategia óptima (mismo piso crítico)."""
    if juego.estado == JUGANDO:
        raise ValueError("La partida todavía no termina.")
    optima = simular_optima(juego.huevos_iniciales, juego.pisos, juego.piso_critico)
    return Resultado(
        estado=juego.estado,
        piso_critico=juego.piso_critico,
        lanzamientos_usuario=len(juego.lanzamientos),
        lanzamientos_optimos=len(optima),
        lanzamientos_garantizados=min_lanzamientos(juego.huevos_iniciales, juego.pisos),
        huevos_rotos=juego.huevos_rotos,
    )


def estados_por_piso(juego: Juego) -> dict[int, str]:
    """Resultado de cada piso lanzado: {piso: "ok" | "roto"} (para dibujar el edificio)."""
    return {piso: ("roto" if rompio else "ok") for piso, rompio in juego.lanzamientos}
