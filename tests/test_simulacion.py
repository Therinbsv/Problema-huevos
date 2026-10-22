import pytest
from src.simulacion import (
    ESTRATEGIAS,
    Paso,
    describir_rango,
    pasos_desde_lanzamientos,
    piso_critico,
    simular,
    simular_todas,
)
from src.validacion import EntradaInvalida


# 1 a 6: Simulación paso a paso para las tres estrategias en dos pisos clave
@pytest.mark.parametrize("estrategia", ["lineal", "binaria", "optima"])
@pytest.mark.parametrize("k", [1, 50])
def test_simular_estrategias_clave(estrategia, k):
    pasos = simular(estrategia, 2, 100, k)
    assert len(pasos) > 0
    assert all(isinstance(p, Paso) for p in pasos)
    assert piso_critico(pasos, 100) == k


# 7 a 9: Caso borde donde el huevo no se rompe en ningún piso (k = N + 1 = 101)
@pytest.mark.parametrize("estrategia", ["lineal", "binaria", "optima"])
def test_simular_caso_no_se_rompe(estrategia):
    pasos = simular(estrategia, 2, 100, 101)
    assert piso_critico(pasos, 100) == 101


# 10 a 14: Simular todas las estrategias simultáneamente para comparar
@pytest.mark.parametrize("k", [1, 14, 50, 99, 100])
def test_simular_todas_consistencia(k):
    resultados = simular_todas(2, 100, k)
    assert set(resultados.keys()) == set(ESTRATEGIAS)
    for est in ESTRATEGIAS:
        assert piso_critico(resultados[est], 100) == k


# 15 a 18: Función describir_rango en distintos estados de la búsqueda
def test_describir_rango_encontrado():
    texto = describir_rango(14, 14, 100)
    assert "El piso crítico es el 14." in texto


def test_describir_rango_no_se_rompe():
    texto = describir_rango(101, 101, 100)
    assert "El huevo no se rompe en ningún piso." in texto


def test_describir_rango_limite_superior():
    texto = describir_rango(100, 101, 100)
    assert "El piso crítico es el 100, o el huevo no se rompe en ningún piso." in texto


def test_describir_rango_intermedio():
    texto = describir_rango(10, 50, 100)
    assert "El piso crítico está entre 10 y 50." in texto


# 19 a 22: Validación de excepciones ante entradas inválidas
@pytest.mark.parametrize("h,n", [(0, 100), (-1, 50), (2, 0), (2, -5)])
def test_simular_entradas_invalidas(h, n):
    with pytest.raises((ValueError, EntradaInvalida)):
        simular("optima", h, n, 1)


# 23: Estrategia desconocida debe lanzar ValueError
def test_simular_estrategia_invalida():
    with pytest.raises(ValueError, match="Estrategia desconocida"):
        simular("magica", 2, 100, 10)


# 24: piso_critico con lista de pasos vacía debe fallar
def test_piso_critico_lista_vacia():
    with pytest.raises(ValueError, match="La simulación no tiene pasos."):
        piso_critico([], 100)


# 25: piso_critico si la simulación no converge (bajo != alto)
def test_piso_critico_inconcluso():
    paso_inconcluso = Paso(1, 14, False, 2, 15, 101, "texto")
    with pytest.raises(ValueError, match="sin determinar"):
        piso_critico([paso_inconcluso], 100)


# 26 a 28: Propiedades de la estructura Paso y lanzamientos directos
def test_pasos_desde_lanzamientos_decremento_huevos():
    lanzamientos = [(14, True)]
    pasos = pasos_desde_lanzamientos(lanzamientos, 2, 100)
    assert pasos[0].huevos_restantes == 1
    assert pasos[0].se_rompio is True


def test_pasos_desde_lanzamientos_sin_romper():
    lanzamientos = [(14, False)]
    pasos = pasos_desde_lanzamientos(lanzamientos, 2, 100)
    assert pasos[0].huevos_restantes == 2
    assert pasos[0].bajo == 15


def test_paso_es_inmutable():
    paso = Paso(1, 10, False, 2, 11, 101, "texto")
    with pytest.raises(Exception):
        paso.piso = 20


# 29: Consistencia de peor caso en la estrategia óptima simulada
def test_simular_optima_respeta_cota_14():
    pasos = simular("optima", 2, 100, 100)
    assert len(pasos) <= 14