
# Plan de Pruebas - Proyecto Problema de los Huevos

## 1. Criterios de Aceptación (Sección 9 de Requerimientos) y Verificación

| Criterio / Parámetros                        | Valor Esperado                       | Método de Verificación   |
| :-------------------------------------------- | :----------------------------------- | :------------------------- |
| Entrada válida ($H=2, N=100$)              | Algoritmo óptimo: 14 lanzamientos   | Automática con pytest     |
| Búsqueda lineal ($N=100$)                  | Peor caso: 100 lanzamientos          | Automática con pytest     |
| Búsqueda lineal ($N=1$)                    | Peor caso: 1 lanzamiento             | Automática con pytest     |
| Búsqueda binaria ($H=1, N=100$)            | Equivale a lineal: 100 lanzamientos  | Automática con pytest     |
| Búsqueda binaria ($H=10, N=100$)           | Logarítmica pura: 7 lanzamientos    | Automática con pytest     |
| Validación de errores ($H \le 0, N \le 0$) | Lanza excepción `EntradaInvalida` | Automática con pytest     |
| Rendimiento (RNF-02)                          | Ejecución en menos de 1 segundo     | Prueba de tiempo en pytest |

## 2. Cobertura de Riesgos Técnicos

| Riesgo          | Descripción                           | Evidencia y Cómo se Verifica                                                                                                           |
| :-------------- | :------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| **RK-01** | Malinterpretar el problema             | Revisión cruzada de casos de uso y requerimientos                                                                                      |
| **RK-02** | Elegir estrategia subóptima (Binaria) | Prueba automatizada (`test_rk02_binaria_falla_con_2_huevos`): demuestra que con 2 huevos requiere 50 intentos frente a 14 del óptimo |
| **RK-03** | Casos borde no contemplados            | Pruebas parametrizadas en `tests/test_validacion.py` (0 pisos, entradas negativas, tipos inválidos)                                  |
| **RK-04** | La app no se entiende sin explicación | Prueba de usabilidad con 3 usuarios externos en el Ciclo 4                                                                              |

## 3. Criterio de Aprobación de Ciclo (QA)

- 100% de las pruebas unitarias y de integración pasando en verde (local y GitHub Actions).
- Trazabilidad directa de cada prueba con su respectivo requerimiento (RF) o riesgo (RK).
