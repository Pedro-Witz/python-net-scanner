import urllib.request
import urllib.error

url = "http://localhost:8080"
print(f"[*] Enviando petición HTTP de prueba hacia: {url}")

try:
    response = urllib.request.urlopen(url)
    print(f"[+] Conexión exitosa. Código de Estado: {response.getcode()}")
    
    # Mostramos las cabeceras técnicas del servidor
    print("\n[+] Cabeceras HTTP (Headers) del servidor:")
    print(response.headers)

except urllib.error.URLError as e:
    print(f"[-] Error de conexión: {e.reason}. ¿Está el contenedor encendido?")