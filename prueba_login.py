#!/usr/bin/env python3
"""
Laboratorio local de login con HTTP + requests.

TODO corre en tu propia maquina (localhost). Sos duenio del servidor Y del
cliente, y los datos son inventados. No apunta a ningun sitio externo: es una
prueba para aprender como viaja un login por la red.

Uso:
    python prueba_login.py            # arranca el server y corre la prueba (todo junto)
    python prueba_login.py server     # solo el servidor (dejalo corriendo en una terminal)
    python prueba_login.py cliente    # solo el cliente (contra un server ya arriba)

Para probar contra la IP de tu compu en vez de localhost, cambia HOST abajo
(ej: "192.168.0.15") y corre el server en una terminal y el cliente en otra.
"""

import sys
import json
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

import requests  # si no lo tenes: pip install requests

# ----- Config (cambia esto cuando quieras) -----
HOST = "127.0.0.1"   # tu propia compu. Luego podes poner la IP local, ej "192.168.0.15"
PORT = 8000

# Credenciales "correctas" de la demo. Son datos FALSOS, no son nada real.
USUARIO_VALIDO = "51066056"
PASSWORD_VALIDO = "demo1234"


# ====================== SERVIDOR ======================
class LoginHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/login":
            self.send_response(404)
            self.end_headers()
            return

        # leer el cuerpo del POST (lo que manda el cliente)
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode()
        datos = parse_qs(body)            # "u=51066056&password=1234" -> dict
        u = datos.get("u", [""])[0]
        p = datos.get("password", [""])[0]

        # decidir la respuesta segun las credenciales
        if u == USUARIO_VALIDO and p == PASSWORD_VALIDO:
            self._responder(200, {"ok": True, "msg": "login correcto"})
        else:
            self._responder(401, {"ok": False, "msg": "credenciales invalidas"})

    def _responder(self, codigo, payload):
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

    def log_message(self, *args):
        pass  # silenciar los logs internos del server


def arrancar_server():
    servidor = HTTPServer((HOST, PORT), LoginHandler)
    print(f"[server] escuchando en http://{HOST}:{PORT}/login")
    servidor.serve_forever()


# ====================== CLIENTE ======================
def probar_login(usuario, password):
    """Manda un POST de login y muestra la respuesta HTTP."""
    url = f"http://{HOST}:{PORT}/login"
    datos = {"u": usuario, "password": password}
    r = requests.post(url, data=datos, timeout=5)
    print(f"[cliente] u={usuario}  pass={password!r}  ->  {r.status_code}  {r.json()}")
    return r.status_code == 200


def correr_cliente():
    # Lista de prueba con contrasenas inventadas. Como el server es TUYO, esto
    # solo sirve para ver la diferencia entre una respuesta 200 (OK) y 401 (mal).
    candidatos = ["1234", "admin", "password", "demo1234"]
    for pw in candidatos:
        if probar_login(USUARIO_VALIDO, pw):
            print(f"[cliente] >>> entro con la contrasena: {pw}")
            break
    else:
        print("[cliente] ninguna de la lista funciono")


# ====================== MAIN ======================
if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else "todo"

    if modo == "server":
        arrancar_server()
    elif modo == "cliente":
        correr_cliente()
    else:
        # arranca el server en segundo plano y corre el cliente contra el
        threading.Thread(target=arrancar_server, daemon=True).start()
        time.sleep(0.5)  # darle un instante al server para levantar
        correr_cliente()
