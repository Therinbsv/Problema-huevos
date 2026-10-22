"""Dibujo del edificio nocturno (solo presentación, sin lógica del problema).

Genera una imagen con Pillow y la interfaz la muestra con st.image: así se
cumple la restricción R-02 (sin HTML, CSS ni JS propios). La imagen es
estática: se vuelve a dibujar cada vez que cambia el estado de la partida.

Cada piso es una fila de 8 ventanas:
- verde: se lanzó un huevo desde ese piso y sobrevivió
- roja:  se lanzó un huevo desde ese piso y se rompió
- dorada con borde blanco: el piso crítico (solo se revela al terminar)
- el resto: ventanas encendidas o apagadas al azar (decoración fija)

Trazabilidad: RF-06, RF-07, RF-08 | Riesgo: RK-04 | Issue: HUEVO-27
"""

import random
from typing import Optional

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ESCALA = 2  # se dibuja al doble de tamaño para que los bordes salgan suaves
ANCHO, ALTO = 480, 700

# Torre
TORRE_X0, TORRE_X1 = 120, 330
COLUMNAS = 8
CALLE_Y = 640
TECHO_Y = 92
BASE_Y = 636       # parte baja del piso 1

VERDE = (70, 205, 120)
ROJO = (240, 80, 80)
CRITICO = (255, 236, 150)
ENCENDIDA = (255, 214, 120)
APAGADA = (38, 46, 78)


def _fuente(tamano: int, negrita: bool = False) -> ImageFont.ImageFont:
    nombre = "DejaVuSans-Bold.ttf" if negrita else "DejaVuSans.ttf"
    try:
        return ImageFont.truetype(nombre, tamano * ESCALA)
    except OSError:
        return ImageFont.load_default()


def _e(valor: float) -> int:
    return int(round(valor * ESCALA))


def _fila_y(piso: int, pisos: int) -> tuple[float, float]:
    """Borde superior e inferior (en píxeles lógicos) de la fila del piso."""
    alto_piso = (BASE_Y - TECHO_Y - 8) / pisos
    inferior = BASE_Y - (piso - 1) * alto_piso
    return inferior - alto_piso, inferior


def _cielo(lienzo: Image.Image) -> None:
    dibujo = ImageDraw.Draw(lienzo)
    alto = lienzo.height
    for y in range(alto):
        t = y / alto
        color = (int(8 + 52 * t), int(8 + 18 * t), int(26 + 56 * t))
        dibujo.line([(0, y), (lienzo.width, y)], fill=color)


def _estrellas(lienzo: Image.Image, azar: random.Random) -> None:
    dibujo = ImageDraw.Draw(lienzo)
    for _ in range(70):
        x, y = azar.randint(0, ANCHO), azar.randint(0, 400)
        brillo = azar.randint(120, 230)
        r = azar.choice((0.5, 0.5, 0.8, 1.1))
        dibujo.ellipse([_e(x - r), _e(y - r), _e(x + r), _e(y + r)], fill=(brillo, brillo, min(255, brillo + 20)))


def _luna(lienzo: Image.Image) -> Image.Image:
    cx, cy, r = 408, 62, 20
    halo = Image.new("RGBA", lienzo.size, (0, 0, 0, 0))
    ImageDraw.Draw(halo).ellipse(
        [_e(cx - 54), _e(cy - 54), _e(cx + 54), _e(cy + 54)], fill=(255, 240, 190, 70)
    )
    halo = halo.filter(ImageFilter.GaussianBlur(_e(18)))
    lienzo = Image.alpha_composite(lienzo.convert("RGBA"), halo)
    dibujo = ImageDraw.Draw(lienzo)
    dibujo.ellipse([_e(cx - r), _e(cy - r), _e(cx + r), _e(cy + r)], fill=(250, 240, 200))
    for dx, dy, rr in ((-6, -4, 3.5), (5, 5, 2.5), (-2, 8, 2)):
        dibujo.ellipse(
            [_e(cx + dx - rr), _e(cy + dy - rr), _e(cx + dx + rr), _e(cy + dy + rr)],
            fill=(226, 214, 168),
        )
    return lienzo


def _edificios_de_fondo(lienzo: Image.Image, azar: random.Random) -> None:
    dibujo = ImageDraw.Draw(lienzo)
    bloques = [(0, 62, 250), (62, 112, 170), (338, 392, 190), (392, 440, 280), (440, 480, 200)]
    for x0, x1, alto in bloques:
        tope = CALLE_Y - alto
        dibujo.rectangle([_e(x0), _e(tope), _e(x1), _e(CALLE_Y)], fill=(14, 14, 32))
        y = tope + 8
        while y < CALLE_Y - 8:
            x = x0 + 5
            while x + 6 < x1 - 3:
                if azar.random() < 0.42:
                    dibujo.rectangle([_e(x), _e(y), _e(x + 5), _e(y + 4)], fill=(255, 205, 110))
                x += 10
            y += 12


def _torre(lienzo: Image.Image, azar: random.Random, pisos: int,
           estados: dict[int, str], piso_critico: Optional[int]) -> None:
    dibujo = ImageDraw.Draw(lienzo)
    # antena, remate y cuerpo
    dibujo.line([_e(225), _e(60), _e(225), _e(TECHO_Y)], fill=(70, 70, 100), width=_e(1.5))
    dibujo.ellipse([_e(223), _e(57), _e(227), _e(61)], fill=(240, 70, 70))
    dibujo.rectangle([_e(TORRE_X0 + 20), _e(TECHO_Y - 8), _e(TORRE_X1 - 20), _e(TECHO_Y)], fill=(22, 26, 52))
    dibujo.rectangle([_e(TORRE_X0), _e(TECHO_Y), _e(TORRE_X1), _e(CALLE_Y)], fill=(18, 22, 46),
                     outline=(52, 60, 100), width=_e(1))

    ancho_col = (TORRE_X1 - TORRE_X0 - 10) / COLUMNAS
    for piso in range(1, pisos + 1):
        arriba, abajo = _fila_y(piso, pisos)
        alto_ventana = max(2.0, (abajo - arriba) - 2.0)
        estado = estados.get(piso)
        if estado in ("ok", "roto") and piso != piso_critico:  # franja tenue para que se note más
            tinte = (24, 70, 48) if estado == "ok" else (86, 30, 36)
            dibujo.rectangle([_e(TORRE_X0 + 1), _e(arriba), _e(TORRE_X1 - 1), _e(abajo)], fill=tinte)
        for col in range(COLUMNAS):
            x = TORRE_X0 + 5 + col * ancho_col + 2.5
            if piso == piso_critico:
                color = CRITICO
            elif estado == "ok":
                color = VERDE
            elif estado == "roto":
                color = ROJO
            else:
                color = ENCENDIDA if azar.random() < 0.55 else APAGADA
            caja = [_e(x), _e(abajo - alto_ventana - 1), _e(x + ancho_col - 5), _e(abajo - 1)]
            dibujo.rectangle(caja, fill=color)
        if piso == piso_critico:  # borde blanco para que se note al revelarlo
            dibujo.rectangle(
                [_e(TORRE_X0 + 3), _e(arriba), _e(TORRE_X1 - 3), _e(abajo)],
                outline=(255, 255, 255), width=_e(1),
            )


def _escala(lienzo: Image.Image, pisos: int) -> None:
    dibujo = ImageDraw.Draw(lienzo)
    fuente = _fuente(9)
    for piso in [1] + list(range(10, pisos + 1, 10)):
        arriba, abajo = _fila_y(piso, pisos)
        y = (arriba + abajo) / 2
        texto = str(piso)
        ancho = dibujo.textlength(texto, font=fuente) / ESCALA
        dibujo.rectangle([_e(TORRE_X0 - 36), _e(y - 6), _e(TORRE_X0 - 8), _e(y + 6)], fill=(10, 10, 24))
        dibujo.text((_e(TORRE_X0 - 12 - ancho), _e(y - 6)), texto, font=fuente, fill=(200, 205, 230))
        dibujo.line([_e(TORRE_X0 - 6), _e(y), _e(TORRE_X0), _e(y)], fill=(120, 130, 170), width=_e(1))


def _marcador(lienzo: Image.Image, piso: int, pisos: int) -> None:
    """Huevo con flecha a la derecha de la torre, a la altura del piso elegido."""
    dibujo = ImageDraw.Draw(lienzo)
    arriba, abajo = _fila_y(piso, pisos)
    y = (arriba + abajo) / 2
    dibujo.line([_e(TORRE_X1), _e(y), _e(TORRE_X1 + 24), _e(y)], fill=(255, 220, 150), width=_e(1.2))
    dibujo.ellipse([_e(TORRE_X1 + 22), _e(y - 7), _e(TORRE_X1 + 36), _e(y + 7)],
                   fill=(255, 246, 225), outline=(210, 170, 110), width=_e(1))
    texto = f"← piso {piso}"
    fuente = _fuente(10, negrita=True)
    ancho = dibujo.textlength(texto, font=fuente) / ESCALA
    dibujo.rectangle([_e(TORRE_X1 + 40), _e(y - 8), _e(TORRE_X1 + 46 + ancho), _e(y + 8)], fill=(10, 10, 24))
    dibujo.text((_e(TORRE_X1 + 43), _e(y - 7)), texto, font=fuente, fill=(255, 224, 160))


def _calle(lienzo: Image.Image, rotos: int) -> Image.Image:
    dibujo = ImageDraw.Draw(lienzo)
    for y in range(CALLE_Y, ALTO):
        t = (y - CALLE_Y) / (ALTO - CALLE_Y)
        dibujo.line([(0, _e(y)), (lienzo.width, _e(y))], fill=(int(24 - 10 * t), int(22 - 8 * t), int(40 - 14 * t)))
    # farolas con luz
    luces = Image.new("RGBA", lienzo.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(luces)
    farolas = (60, 400)
    for x in farolas:
        ld.ellipse([_e(x - 34), _e(CALLE_Y - 40), _e(x + 34), _e(CALLE_Y + 28)], fill=(255, 200, 110, 110))
    luces = luces.filter(ImageFilter.GaussianBlur(_e(12)))
    lienzo = Image.alpha_composite(lienzo.convert("RGBA"), luces)
    dibujo = ImageDraw.Draw(lienzo)
    for x in farolas:
        dibujo.line([_e(x), _e(CALLE_Y - 30), _e(x), _e(CALLE_Y + 6)], fill=(50, 50, 70), width=_e(1.5))
        dibujo.ellipse([_e(x - 4), _e(CALLE_Y - 34), _e(x + 4), _e(CALLE_Y - 27)], fill=(255, 236, 170))
    # huevos rotos al pie del edificio
    for i in range(rotos):
        x = TORRE_X0 + 12 + (i * 37) % (TORRE_X1 - TORRE_X0 - 30)
        y = CALLE_Y + 14 + (i % 3) * 11
        dibujo.ellipse([_e(x - 10), _e(y - 4), _e(x + 10), _e(y + 4)], fill=(250, 244, 226))
        dibujo.ellipse([_e(x - 3), _e(y - 2), _e(x + 3), _e(y + 2)], fill=(250, 190, 40))
    return lienzo


def dibujar_escena(
    pisos: int,
    estados: dict[int, str],
    marcador: Optional[int] = None,
    rotos: int = 0,
    piso_critico: Optional[int] = None,
) -> Image.Image:
    """Dibuja el edificio.

    estados: {piso: "ok" | "roto"} de los pisos desde los que ya se lanzó.
    marcador: piso elegido para el próximo lanzamiento (None = sin marcador).
    rotos: huevos rotos hasta ahora (aparecen en la calle).
    piso_critico: solo se pasa al terminar la partida, para revelarlo.
    """
    azar = random.Random(11)  # decoración fija: el edificio no "parpadea" entre lanzamientos
    lienzo = Image.new("RGB", (_e(ANCHO), _e(ALTO)))
    _cielo(lienzo)
    _estrellas(lienzo, azar)
    lienzo = _luna(lienzo)
    _edificios_de_fondo(lienzo, azar)
    _torre(lienzo, azar, pisos, estados, piso_critico)
    _escala(lienzo, pisos)
    lienzo = _calle(lienzo, rotos)
    if marcador is not None and 1 <= marcador <= pisos:
        _marcador(lienzo, marcador, pisos)
    return lienzo.convert("RGB")
