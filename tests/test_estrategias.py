"""Pruebas de las estrategias del Ciclo 2.

Trazabilidad: RF-02, RF-03 | Riesgo: RK-02
La prueba `test_rk02_binaria_falla_con_2_huevos` es la evidencia del Ciclo 2:
demuestra que la búsqueda binaria NO es óptima con pocos huevos.
"""

import pytest

from src.estrategias import (
    peor_caso_binaria,
    peor_caso_lineal,
    piso_encontrado,
    simular_binaria,
    simular_lineal,
)

N = 100
OPTIMO_2_HUEVOS = 14  # valor de referencia, requerimientos sección 9


# ------------------------------------------------------------- Lineal (RF-02)

def test_lineal_peor_caso_100_pisos():
    assert peor_caso_lineal(N) == 100


def test_lineal_un_piso():
    assert peor_caso_lineal(1) == 1


@pytest.mark.parametrize("k", [1, 37, 100, 101])
def test_lineal_encuentra_el_piso_correcto(k):
    assert piso_encontrado(simular_lineal(N, k), N) == k


def test_lineal_se_detiene_al_romperse():
    lanzamientos = simular_lineal(N, 5)
    assert lanzamientos[-1] == (5, True)
    assert len(lanzamientos) == 5


# ------------------------------------------------------------- Binaria (RF-03)

@pytest.mark.parametrize("h", [1, 2, 3, 7, 10])
@pytest.mark.parametrize("k", [1, 2, 49, 50, 51, 99, 100, 101])
def test_binaria_encuentra_el_piso_correcto(h, k):
    """Sea cual sea k, la binaria siempre encuentra el piso crítico."""
    assert piso_encontrado(simular_binaria(h, N, k), N) == k


def test_binaria_nunca_usa_mas_huevos_de_los_disponibles():
    for h in (1, 2, 3):
        for k in range(1, N + 2):
            rotos = sum(rompio for _, rompio in simular_binaria(h, N, k))
            assert rotos <= h


def test_binaria_con_1_huevo_es_lineal():
    assert peor_caso_binaria(1, N) == peor_caso_lineal(N) == 100


def test_binaria_con_muchos_huevos_es_logaritmica():
    # Con huevos suficientes se comporta como binaria pura: ⌈log2(101)⌉ = 7
    assert peor_caso_binaria(10, N) == 7


# ------------------------------------------------------------- Evidencia RK-02

def test_rk02_binaria_falla_con_2_huevos():
    """RK-02 confirmado: con 2 huevos la binaria necesita 50 lanzamientos.

    El primer huevo se rompe en el piso 50 y el segundo debe recorrer 1…49.
    El valor de referencia de requerimientos (sección 9) es 14, así que la
    binaria NO puede ser la solución general.
    """
    peor = peor_caso_binaria(2, N)
    assert peor == 50
    assert peor > OPTIMO_2_HUEVOS


def test_rk02_peor_caso_se_da_debajo_del_primer_lanzamiento():
    lanzamientos = simular_binaria(2, N, 50)
    assert lanzamientos[0] == (50, True)  # primer huevo roto en el piso medio
    assert len(lanzamientos) == 50        # 1 + 49 lanzamientos lineales


def test_binaria_mejora_al_agregar_huevos():
    """La binaria depende fuertemente de H: peor caso no creciente al agregar huevos."""
    peores = [peor_caso_binaria(h, N) for h in range(1, 11)]
    assert peores == sorted(peores, reverse=True)
    assert peores[0] == 100 and peores[-1] == 7


# ------------------------------------------------------------- Rendimiento (RNF-02)

def test_rendimiento_dentro_de_un_segundo():
    import time

    inicio = time.perf_counter()
    peor_caso_binaria(10, 1000)
    peor_caso_lineal(1000)
    assert time.perf_counter() - inicio < 1.0
