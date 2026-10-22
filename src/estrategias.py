"""Estrategias candidatas del Ciclo 2: búsqueda lineal y búsqueda binaria.

Cada estrategia tiene dos funciones:
- simular_*(..., k): ejecuta la búsqueda para un piso crítico k concreto y
  devuelve la lista de lanzamientos [(piso, se_rompio), ...].
- peor_caso_*(...): número de lanzamientos en el peor caso, calculado
  recorriendo TODOS los pisos críticos posibles (k = 1 … N+1).

Calcular el peor caso por simulación exhaustiva es intencional: no depende de
ninguna fórmula, así que sirve como evidencia objetiva para el riesgo RK-02.

Supuestos (requerimientos, sección 5): S2 huevo intacto se reutiliza,
S3 huevo roto se pierde, S4 monotonía, S5 puede no romperse nunca (k = N+1).

Trazabilidad: RF-02 (lineal), RF-03 (binaria) | Riesgo: RK-02
Diagramas: diagramas/actividad_lineal.puml, diagramas/actividad_binaria.puml
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
