"""Pruebas de validación de entradas. Trazabilidad: RF-01, RF-09 | Riesgo: RK-03"""

import pytest

from src.validacion import EntradaInvalida, validar_entrada


@pytest.mark.parametrize("h, n", [(1, 1), (2, 100), (10, 1000)])
def test_entradas_validas(h, n):
    assert validar_entrada(h, n) == (h, n)


@pytest.mark.parametrize(
    "h, n",
    [
        (0, 100),    # sin huevos (sección 9 de requerimientos)
        (2, 0),      # sin pisos (sección 9, corrección ARQ-01)
        (-1, 100),   # negativo
        (2, -5),     # negativo
        (11, 100),   # supera el máximo de huevos
        (2, 1001),   # supera el máximo de pisos
        (2.5, 100),  # no entero
        ("2", 100),  # texto
        (True, 100), # bool no cuenta como entero
    ],
)
def test_entradas_invalidas(h, n):
    with pytest.raises(EntradaInvalida):
        validar_entrada(h, n)
