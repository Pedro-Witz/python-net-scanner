import urllib.request
import urllib.error

# Objetivo de nuestro laboratorio
base_url = "http://localhost:8080"

# Diccionario simulado de rutas comunes que busca un atacante o auditor
rutas_a_probar = [
    "/",
    "/admin",
    "/login",
    "/config.json",
    "/dashboard",
    "/secret",
    "/robots.txt"
]

print(f"[*] Iniciando fuzzing web sobre: {base_url}\n")

for ruta in rutas_a_probar:
    url_completa = base_url + ruta
    try:
        # Intentamos hacer la petición
        req = urllib.request.Request(url_completa, headers={'User-Agent': 'SecurityAuditorBot/1.0'})
        response = urllib.request.urlopen(req)
        print(f"[+] [EXISTE] {url_completa} --> Código: {response.getcode()}")
    except urllib.error.HTTPError as e:
        # Capturamos errores HTTP controlados (ej. 404 No encontrado, 403 Prohibido)
        if e.code == 404:
            print(f"[-] [No encontrado] {url_completa} (404)")
        else:
            print(f"[!] [INTERESANTE] {url_completa} --> Código HTTP: {e.code}")
    except urllib.error.URLError as e:
        print(f"[-] Error de conexión con {url_completa}: {e.reason}")

print("\n[*] Fuzzing finalizado con éxito.")