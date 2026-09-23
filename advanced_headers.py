import urllib.request
import urllib.error

base_url = "http://localhost:8080"

# Cabeceras avanzadas que imitan a un navegador real (Chrome en Windows) + un token de prueba
headers_avanzadas = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
    'X-Security-Token': 'TokenSecretoDePrueba123'
}

print(f"[*] Preparando petición camuflada hacia: {base_url}\n")
print("[*] Cabeceras que se enviarán:")
for key, value in headers_avanzadas.items():
    print(f"    - {key}: {value}")
print("-" * 50)

try:
    # Creamos la petición empaquetando nuestras cabeceras personalizadas
    req = urllib.request.Request(base_url, headers=headers_avanzadas)
    
    # Ejecutamos la petición
    response = urllib.request.urlopen(req)
    
    print(f"\n[+] ¡Petición enviada con éxito!")
    print(f"[+] Código de estado HTTP recibido: {response.getcode()}")
    print(f"[+] Tamaño de la respuesta: len({len(response.read())} bytes)")

except urllib.error.HTTPError as e:
    print(f"[!] El servidor rechazó la petición con código: {e.code}")
except urllib.error.URLError as e:
    print(f"[-] Error de conexión: {e.reason}")