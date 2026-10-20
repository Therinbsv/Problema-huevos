"""Validación de entradas.

Trazabilidad: RF-01, RF-09 | Riesgo: RK-03
"""

MAX_HUEVOS = 10
MAX_PISOS = 1000


class EntradaInvalida(ValueError):
    """Se lanza cuando H o N no cumplen las reglas de RF-01 / RF-09."""


def _es_entero(valor) -> bool:
    # bool es subclase de int en Python; True no debe aceptarse como 1 huevo.
    return isinstance(valor, int) and not isinstance(valor, bool)


def validar_pisos(n) -> int:
    """Valida el número de pisos N (1 ≤ N ≤ MAX_PISOS)."""
    if not _es_entero(n):
        raise EntradaInvalida("El número de pisos debe ser un número entero.")
    if n < 1:
        raise EntradaInvalida("El edificio debe tener al menos 1 piso.")
    if n > MAX_PISOS:
        raise EntradaInvalida(f"El número de pisos no puede superar {MAX_PISOS}.")
    return n


def validar_huevos(h) -> int:
    """Valida el número de huevos H (1 ≤ H ≤ MAX_HUEVOS)."""
    if not _es_entero(h):
        raise EntradaInvalida("El número de huevos debe ser un número entero.")
    if h < 1:
        raise EntradaInvalida("Se necesita al menos 1 huevo.")
    if h > MAX_HUEVOS:
        raise EntradaInvalida(f"El número de huevos no puede superar {MAX_HUEVOS}.")
    return h


def validar_entrada(h, n) -> tuple[int, int]:
    """Valida H y N juntos. Devuelve (h, n) si son válidos."""
    return validar_huevos(h), validar_pisos(n)
