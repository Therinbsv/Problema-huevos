import pytest
from src.validacion import EntradaInvalida
from src.estrategias import (
    min_lanzamientos,
    secuencia_pisos,
    simular_optima,
    peor_caso_optima,
)


# 1 a 5: Valores óptimos de referencia (2 huevos en 100 pisos = 14)
@pytest.mark.parametrize(
    "huevos,pisos,esperado",
    [
        (2, 100, 14),
        (3, 100, 9),
        (7, 100, 7),
        (1, 10, 10),
        (2, 10, 4),
    ],
)
def test_min_lanzamientos_valores_clave(huevos, pisos, esperado):
    assert min_lanzamientos(huevos, pisos) == esperado


# 6 y 7: Propiedades de la secuencia de pisos para 2 huevos y 100 pisos
def test_secuencia_pisos_limites():
    secuencia = secuencia_pisos(2, 100)
    assert secuencia[0] == 14
    assert secuencia[-1] == 100


def test_secuencia_pisos_es_estrictamente_creciente():
    secuencia = secuencia_pisos(2, 100)
    assert all(x < y for x, y in zip(secuencia, secuencia[1:]))


# 8 a 17: Simulación en pisos críticos: nunca debe superar el peor caso (14)
@pytest.mark.parametrize("piso_critico", [1, 14, 15, 27, 39, 50, 75, 99, 100])
def test_simular_optima_pisos_clave(piso_critico):
    pasos = simular_optima(2, 100, piso_critico)
    assert isinstance(pasos, list)
    assert len(pasos) <= 14


# 17: Caso borde donde ningún piso rompe el huevo (k = N + 1 = 101)
def test_simular_optima_no_se_rompe():
    pasos = simular_optima(2, 100, 101)
    assert isinstance(pasos, list)
    assert len(pasos) <= 14


# 18 a 23: Consistencia de peor_caso_optima respecto a min_lanzamientos
@pytest.mark.parametrize(
    "huevos,pisos",
    [
        (1, 20),
        (2, 15),
        (2, 36),
        (2, 100),
        (3, 50),
        (4, 100),
    ],
)
def test_peor_caso_consistencia(huevos, pisos):
    assert peor_caso_optima(huevos, pisos) == min_lanzamientos(huevos, pisos)


# 24 a 28: Validaciones de entradas inválidas para min_lanzamientos
@pytest.mark.parametrize(
    "huevos,pisos",
    [
        (0, 100),
        (-1, 50),
        (2, -10),
        (2, 0),
    ],
)
def test_min_lanzamientos_entradas_invalidas(huevos, pisos):
    with pytest.raises((ValueError, EntradaInvalida, AssertionError)):
        min_lanzamientos(huevos, pisos)


# 29: Caso borde con 1 solo piso
def test_min_lanzamientos_un_solo_piso():
    assert min_lanzamientos(2, 1) == 1


# 30: Validación de error si k está fuera del rango permitido en simular_optima
def test_simular_optima_k_invalido():
    with pytest.raises(ValueError):
        simular_optima(2, 100, 0)

def test_simular_optima_piso_critico_maximo():
    pasos = simular_optima(2, 100, 100)
    assert isinstance(pasos, list)
    assert len(pasos) <= 14