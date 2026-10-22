"""Pruebas del juego interactivo. Trazabilidad: RF-07, RF-08 | Riesgo: RK-04"""

import random

import pytest

from src.estrategias import min_lanzamientos, simular_optima
from src.juego import (
    GANADO,
    JUGANDO,
    PERDIDO,
    PISOS_JUEGO,
    estados_por_piso,
    evaluar,
    lanzar,
    nuevo_juego,
    rango_valido,
    sortear_piso_critico,
)
from src.validacion import EntradaInvalida

N = PISOS_JUEGO


# ------------------------------------------------------------- Inicio de partida

def test_nuevo_juego_estado_inicial():
    juego = nuevo_juego(2, N, 28)
    assert juego.estado == JUGANDO
    assert (juego.huevos, juego.huevos_iniciales, juego.huevos_rotos) == (2, 2, 0)
    assert (juego.bajo, juego.alto) == (1, N + 1)
    assert juego.lanzamientos == ()


@pytest.mark.parametrize("h, n", [(0, 100), (11, 100), (2, 0), (2, 1001), (True, 100)])
def test_nuevo_juego_valida_entradas(h, n):
    with pytest.raises(EntradaInvalida):
        nuevo_juego(h, n, 10)


@pytest.mark.parametrize("k", [0, N + 2, -1])
def test_nuevo_juego_valida_piso_critico(k):
    with pytest.raises(ValueError):
        nuevo_juego(2, N, k)


def test_sortear_piso_critico_cubre_todo_el_rango():
    azar = random.Random(7)
    sorteados = {sortear_piso_critico(N, azar) for _ in range(5000)}
    assert min(sorteados) == 1
    assert max(sorteados) == N + 1  # "no se rompe" también puede salir


# ------------------------------------------------------------- Reglas de un lanzamiento

def test_huevo_que_sobrevive_no_se_gasta():
    juego = lanzar(nuevo_juego(2, N, 28), 27)
    assert juego.huevos == 2
    assert (juego.bajo, juego.alto) == (28, N + 1)
    assert juego.lanzamientos == ((27, False),)


def test_huevo_que_se_rompe_se_gasta():
    juego = lanzar(nuevo_juego(2, N, 28), 50)
    assert juego.huevos == 1
    assert (juego.bajo, juego.alto) == (1, 50)
    assert juego.lanzamientos == ((50, True),)


def test_el_piso_critico_se_rompe_y_el_anterior_no():
    assert lanzar(nuevo_juego(2, N, 28), 28).lanzamientos[-1] == (28, True)
    assert lanzar(nuevo_juego(2, N, 28), 27).lanzamientos[-1] == (27, False)


def test_juego_es_inmutable():
    inicial = nuevo_juego(2, N, 28)
    lanzar(inicial, 50)
    assert inicial.lanzamientos == () and inicial.huevos == 2


# ------------------------------------------------------------- Pisos permitidos

def test_rango_valido_al_inicio_y_despues_de_lanzar():
    juego = nuevo_juego(2, N, 28)
    assert rango_valido(juego) == (1, N)
    assert rango_valido(lanzar(juego, 50)) == (1, 49)
    assert rango_valido(lanzar(juego, 20)) == (21, N)


@pytest.mark.parametrize("piso", [0, N + 1, -3])
def test_lanzar_fuera_del_edificio(piso):
    with pytest.raises(ValueError):
        lanzar(nuevo_juego(2, N, 28), piso)


def test_lanzar_desde_un_piso_ya_descartado():
    juego = lanzar(nuevo_juego(2, N, 28), 50)  # se rompió: del 50 para arriba ya se sabe
    with pytest.raises(ValueError):
        lanzar(juego, 60)
    juego = lanzar(nuevo_juego(2, N, 28), 20)  # sobrevivió: del 20 para abajo ya se sabe
    with pytest.raises(ValueError):
        lanzar(juego, 10)


# ------------------------------------------------------------- Ganar y perder

def test_gana_al_determinar_el_piso_critico():
    juego = nuevo_juego(2, N, 28)
    for piso in (27, 28):
        juego = lanzar(juego, piso)
    assert juego.estado == GANADO
    assert rango_valido(juego) is None


def test_gana_cuando_el_huevo_no_se_rompe_nunca():
    juego = nuevo_juego(2, N, N + 1)
    juego = lanzar(juego, N)
    assert juego.estado == GANADO
    assert (juego.bajo, juego.alto) == (N + 1, N + 1)


def test_gana_si_se_rompe_en_el_piso_1():
    juego = lanzar(nuevo_juego(1, N, 1), 1)
    assert juego.estado == GANADO
    assert juego.huevos == 0  # se gastó el último huevo, pero ya sabe la respuesta


def test_pierde_si_se_queda_sin_huevos():
    juego = nuevo_juego(2, N, 28)
    juego = lanzar(juego, 50)  # se rompe: queda 1
    juego = lanzar(juego, 40)  # se rompe: quedan 0, el piso crítico está entre 1 y 40
    assert juego.estado == PERDIDO
    assert juego.huevos == 0
    assert rango_valido(juego) is None


def test_con_un_huevo_hay_que_subir_piso_por_piso():
    juego = nuevo_juego(1, N, 5)
    juego = lanzar(juego, 50)  # se arriesga y pierde
    assert juego.estado == PERDIDO


def test_no_se_puede_lanzar_con_la_partida_terminada():
    juego = nuevo_juego(1, N, 1)
    juego = lanzar(juego, 1)
    with pytest.raises(ValueError):
        lanzar(juego, 1)


# ------------------------------------------------------------- Evaluación contra la óptima

def test_evaluar_exige_partida_terminada():
    with pytest.raises(ValueError):
        evaluar(nuevo_juego(2, N, 28))


def test_evaluar_ejemplo_k28_con_2_huevos():
    juego = nuevo_juego(2, N, 28)
    for piso in (14, 27, 28):
        juego = lanzar(juego, piso)
    resultado = evaluar(juego)
    assert resultado.estado == GANADO
    assert resultado.piso_critico == 28
    assert resultado.lanzamientos_usuario == 3
    assert resultado.lanzamientos_garantizados == 14
    assert resultado.huevos_rotos == 1
    # La óptima para k = 28 usa 4 lanzamientos: (14,F) (27,F) (39,T) (28,T)
    assert resultado.lanzamientos_optimos == 4


def test_evaluar_partida_perdida():
    juego = lanzar(lanzar(nuevo_juego(2, N, 28), 50), 40)
    resultado = evaluar(juego)
    assert resultado.estado == PERDIDO
    assert resultado.huevos_rotos == 2


def test_estados_por_piso():
    juego = lanzar(lanzar(nuevo_juego(2, N, 28), 27), 50)
    assert estados_por_piso(juego) == {27: "ok", 50: "roto"}


# ------------------------------------------------------------- Propiedades (todas las partidas posibles)

@pytest.mark.parametrize("h", [1, 2, 3, 4, 7, 10])
def test_seguir_la_estrategia_optima_siempre_gana_dentro_de_la_garantia(h):
    """Con cualquier piso crítico, jugar los pisos de simular_optima gana en ≤ garantizado."""
    for k in range(1, N + 2):
        juego = nuevo_juego(h, N, k)
        for piso, _ in simular_optima(h, N, k):
            juego = lanzar(juego, piso)
        assert juego.estado == GANADO
        assert len(juego.lanzamientos) <= min_lanzamientos(h, N)
        assert evaluar(juego).lanzamientos_usuario == evaluar(juego).lanzamientos_optimos


@pytest.mark.parametrize("h", [1, 2, 3])
def test_jugador_al_azar_nunca_rompe_las_reglas(h):
    """Un jugador que lanza donde quiere (dentro del rango) siempre termina, y bien."""
    azar = random.Random(2026)
    for _ in range(300):
        k = azar.randint(1, N + 1)
        juego = nuevo_juego(h, N, k)
        while juego.estado == JUGANDO:
            minimo, maximo = rango_valido(juego)
            juego = lanzar(juego, azar.randint(minimo, maximo))
            assert 0 <= juego.huevos <= h
            assert juego.bajo <= juego.alto
            assert juego.bajo <= k <= juego.alto  # el piso crítico nunca se pierde de vista
        if juego.estado == GANADO:
            assert juego.bajo == juego.alto == k
        else:
            assert juego.huevos == 0 and juego.bajo < juego.alto
