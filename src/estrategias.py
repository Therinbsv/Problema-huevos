"""Estrategias del problema de los huevos: lineal, binaria (Ciclo 2) y óptima (Ciclo 3).

Cada estrategia tiene dos funciones:
- simular_*(..., k): ejecuta la búsqueda para un piso crítico k concreto y
  devuelve la lista de lanzamientos [(piso, se_rompio), ...].
- peor_caso_*(...): número de lanzamientos en el peor caso, calculado
  recorriendo TODOS los pisos críticos posibles (k = 1 … N+1).

Calcular el peor caso por simulación exhaustiva es intencional: no depende de
ninguna fórmula, así que sirve como evidencia objetiva para el riesgo RK-02.

Supuestos (requerimientos, sección 5): S2 huevo intacto se reutiliza,
S3 huevo roto se pierde, S4 monotonía, S5 puede no romperse nunca (k = N+1).

Trazabilidad: RF-02 (lineal), RF-03 (binaria), RF-04 y RF-05 (óptima) | Riesgos: RK-01, RK-02
Diagramas: diagramas/actividad_lineal.puml, diagramas/actividad_binaria.puml,
           diagramas/actividad_optima.puml
"""

from src.validacion import validar_entrada, validar_pisos

Lanzamiento = tuple[int, bool]  # (piso, se_rompio)


def _se_rompe(piso: int, k: int) -> bool:
    """Monotonía (S4): el huevo se rompe en el piso k y en todos los superiores."""
    return piso >= k


def _validar_k(k: int, n: int) -> None:
    if not (1 <= k <= n + 1):
        raise ValueError(f"El piso crítico debe estar entre 1 y {n + 1} (N+1 = no se rompe).")


# ---------------------------------------------------------------- Lineal (RF-02)

def simular_lineal(n: int, k: int) -> list[Lanzamiento]:
    """Lanza desde el piso 1 hacia arriba hasta que el huevo se rompa."""
    validar_pisos(n)
    _validar_k(k, n)
    lanzamientos: list[Lanzamiento] = []
    for piso in range(1, n + 1):
        rompio = _se_rompe(piso, k)
        lanzamientos.append((piso, rompio))
        if rompio:
            break
    return lanzamientos


def peor_caso_lineal(n: int) -> int:
    """Lanzamientos en el peor caso de la búsqueda lineal (no depende de H)."""
    validar_pisos(n)
    return max(len(simular_lineal(n, k)) for k in range(1, n + 2))


# ---------------------------------------------------------------- Binaria (RF-03)

def simular_binaria(h: int, n: int, k: int) -> list[Lanzamiento]:
    """Búsqueda binaria limitada por H huevos.

    Mientras quede más de un huevo, lanza desde el piso medio del intervalo.
    Si queda un solo huevo, ya no puede arriesgarlo y recorre el intervalo
    restante de forma lineal (ver actividad_binaria.puml).
    """
    validar_entrada(h, n)
    _validar_k(k, n)
    bajo, alto, huevos = 1, n, h
    lanzamientos: list[Lanzamiento] = []

    while bajo <= alto:
        if huevos == 1:
            for piso in range(bajo, alto + 1):
                rompio = _se_rompe(piso, k)
                lanzamientos.append((piso, rompio))
                if rompio:
                    return lanzamientos
            return lanzamientos

        medio = (bajo + alto) // 2
        rompio = _se_rompe(medio, k)
        lanzamientos.append((medio, rompio))
        if rompio:
            huevos -= 1
            alto = medio - 1
        else:
            bajo = medio + 1

    return lanzamientos


def peor_caso_binaria(h: int, n: int) -> int:
    """Lanzamientos en el peor caso de la búsqueda binaria con H huevos."""
    validar_entrada(h, n)
    return max(len(simular_binaria(h, n, k)) for k in range(1, n + 2))


def piso_encontrado(lanzamientos: list[Lanzamiento], n: int) -> int:
    """Deduce el piso crítico a partir de los lanzamientos realizados.

    Es el piso más bajo donde el huevo se rompió; si nunca se rompió, N+1.
    Se usa en las pruebas para comprobar que cada estrategia encuentra el k correcto.
    """
    rotos = [piso for piso, rompio in lanzamientos if rompio]
    return min(rotos) if rotos else n + 1


# ---------------------------------------------------------------- Óptima (RF-04, RF-05)
#
# Idea: en vez de preguntar "¿cuántos lanzamientos necesito para N pisos?",
# se pregunta al revés: "con h huevos y t lanzamientos, ¿cuántos pisos puedo resolver?".
#
#   f(h, t) = f(h-1, t-1) + f(h, t-1) + 1
#             ^ se rompe:   ^ no se rompe:  ^ el piso
#               pisos de      pisos de        del lanzamiento
#               abajo         arriba
#
# Casos base: sin huevos o sin lanzamientos no se resuelve ningún piso (f = 0).
# El mínimo de lanzamientos es el menor t tal que f(h, t) >= N.

def pisos_cubiertos(h: int, t: int) -> int:
    """f(h, t): máximo de pisos que se resuelven con h huevos y t lanzamientos."""
    if h <= 0 or t <= 0:
        return 0
    # f[i] = pisos cubiertos con i huevos y los lanzamientos considerados hasta ahora.
    f = [0] * (h + 1)
    for _ in range(t):
        # De mayor a menor para usar el valor de la vuelta anterior (t-1) en f[i-1].
        for i in range(h, 0, -1):
            f[i] = f[i - 1] + f[i] + 1
    return f[h]


def min_lanzamientos(h: int, n: int) -> int:
    """RF-04: número mínimo de lanzamientos en el peor caso con h huevos y n pisos."""
    validar_entrada(h, n)
    t = 0
    while pisos_cubiertos(h, t) < n:
        t += 1
    return t


def siguiente_piso(huevos: int, restantes: int, bajo: int, alto: int) -> int:
    """RF-05: piso desde el que conviene lanzar ahora.

    Se lanza justo encima de los pisos que se podrían revisar con un huevo y un
    lanzamiento menos: si se rompe, el resto del trabajo cabe exactamente en
    los lanzamientos que quedan. Nunca pasa del último piso posible (alto).
    """
    return min(bajo + pisos_cubiertos(huevos - 1, restantes - 1), alto)


def secuencia_pisos(h: int, n: int) -> list[int]:
    """RF-05: secuencia inicial de pisos mientras el primer huevo no se rompa.

    Con h = 2 y n = 100: 14, 27, 39, 50, 60, 69, 77, 84, 90, 95, 99, 100.
    """
    validar_entrada(h, n)
    restantes = min_lanzamientos(h, n)
    bajo, pisos = 1, []
    while bajo <= n:
        piso = siguiente_piso(h, restantes, bajo, n)
        pisos.append(piso)
        bajo = piso + 1
        restantes -= 1
    return pisos


def simular_optima(h: int, n: int, k: int) -> list[Lanzamiento]:
    """Ejecuta la estrategia óptima para un piso crítico k concreto.

    Después de cada lanzamiento ajusta el intervalo y los huevos según el
    resultado, y elige el siguiente piso con siguiente_piso (RF-05).
    Con un solo huevo, siguiente_piso devuelve 'bajo': la búsqueda pasa a ser lineal.
    """
    validar_entrada(h, n)
    _validar_k(k, n)
    bajo, alto, huevos = 1, n, h
    restantes = min_lanzamientos(h, n)
    lanzamientos: list[Lanzamiento] = []

    while bajo <= alto:
        piso = siguiente_piso(huevos, restantes, bajo, alto)
        rompio = _se_rompe(piso, k)
        lanzamientos.append((piso, rompio))
        restantes -= 1
        if rompio:
            huevos -= 1
            alto = piso - 1
        else:
            bajo = piso + 1

    return lanzamientos


def peor_caso_optima(h: int, n: int) -> int:
    """Peor caso medido de la estrategia óptima, recorriendo todos los k.

    Debe coincidir con min_lanzamientos: así se valida la hipótesis del Ciclo 1
    con la misma evidencia medida que se usó para descartar la binaria.
    """
    validar_entrada(h, n)
    return max(len(simular_optima(h, n, k)) for k in range(1, n + 2))
