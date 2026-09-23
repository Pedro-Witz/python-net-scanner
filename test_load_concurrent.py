import urllib.request
import urllib.error
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

base_url = "http://localhost:8080/"
total_peticiones = 100  # Subimos la apuesta a 100 peticiones
hilos_maximos = 20      # 20 peticiones simultáneas al mismo tiempo

print(f"[*] Iniciando prueba de carga concurrente sobre: {base_url}")
print(f"[*] Lanzando {total_peticiones} peticiones usando {hilos_maximos} hilos en paralelo...\n")

exitosas = 0
fallidas = 0

def hacer_peticion(i):
    try:
        response = urllib.request.urlopen(base_url)
        return True, response.getcode(), i
    except urllib.error.HTTPError as e:
        return False, e.code, i
    except urllib.error.URLError:
        return False, "Error de red", i

inicio_tiempo = time.time()

# ThreadPoolExecutor maneja las conexiones concurrentes en paralelo
with ThreadPoolExecutor(max_workers=hilos_maximos) as executor:
    # Disparamos todas las tareas y guardamos las referencias
    futures = [executor.submit(hacer_peticion, i) for i in range(1, total_peticiones + 1)]
    
    # A medida que van respondiendo, las procesamos
    for future in as_completed(futures):
        exito, codigo, i = future.result()
        if exito:
            exitosas += 1
            print(f"[+] Petición #{i} completada -> Código: {codigo}")
        else:
            fallidas += 1
            print(f"[!] Petición #{i} falló -> Código/Error: {codigo}")

fin_tiempo = time.time()
tiempo_total = fin_tiempo - inicio_tiempo

print("\n" + "="*45)
print(f"[*] Prueba de carga concurrente finalizada.")
print(f"[*] Peticiones exitosas: {exitosas}")
print(f"[*] Peticiones fallidas: {fallidas}")
print(f"[*] Tiempo total transcurrido: {tiempo_total:.4f} segundos")
print("="*45)