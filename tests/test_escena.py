"""Prueba de humo de la escena (solo presentación). Trazabilidad: RF-07 | R-02"""

from PIL import Image

from app.escena import ANCHO, ALTO, ESCALA, dibujar_escena


def test_escena_devuelve_imagen_del_tamano_esperado():
    imagen = dibujar_escena(100, {14: "ok", 50: "roto"}, marcador=28, rotos=1)
    assert isinstance(imagen, Image.Image)
    assert imagen.size == (ANCHO * ESCALA, ALTO * ESCALA)


def test_escena_cambia_cuando_cambia_el_estado():
    vacia = dibujar_escena(100, {})
    con_lanzamiento = dibujar_escena(100, {50: "roto"})
    assert vacia.tobytes() != con_lanzamiento.tobytes()


def test_escena_con_marcador_piso_critico_y_huevos_rotos():
    imagen = dibujar_escena(100, {27: "ok", 28: "roto"}, marcador=28, rotos=2, piso_critico=28)
    assert imagen.size == (ANCHO * ESCALA, ALTO * ESCALA)
