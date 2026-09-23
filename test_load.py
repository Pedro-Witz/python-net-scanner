import urllib.request
import urllib.error
import time

base_url = "http://localhost:8080/"
total_peticiones = 50  # Lanzaremos 50 peticiones seguidas sin pausas

print(f"[*] Iniciando prueba de carga masiva sobre: {base_url}")
print(f"[*] Lanzando {total_peticiones} peticiones a máxima velocidad...\n")

inicio_tiempo = time.time()
exitosas = 0
fallidas = 0

for i in range(1, total_peticiones + 1):
    try:
        # Petición limpia a máxima velocidad
        response = urllib.request.urlopen(base_url)
        exitosas += 1
        print(f"[+] Petición #{i} enviada con éxito -> Código: {response.getcode()}")
    except urllib.error.HTTPError as e:
        fallidas += 1
        print(f"[!] Petición #{i} rechazada -> Código: {e.code}")
    except urllib.error.URLError as e:
        fallidas += 1
        print(f"[-] Petición #{i} fallida -> Error de conexión")

fin_tiempo = time.time()
tiempo_total = fin_tiempo - inicio_tiempo

print("\n" + "="*40)
print(f"[*] Prueba de carga finalizada.")
print(f"[*] Peticiones exitosas: {exitosas}")
print(f"[*] Peticiones fallidas: {fallidas}")
print(f"[*] Tiempo total transcurrido: {tiempo_total:.4f} segundos")
print("="*40)