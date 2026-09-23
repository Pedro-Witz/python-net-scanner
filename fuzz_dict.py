import urllib.request
import urllib.error
import os

base_url = "http://localhost:8080"
wordlist_file = "wordlist.txt"

# Verificamos que el archivo de diccionario exista
if not os.path.exists(wordlist_file):
    print(f"[!] Error: No se encontró el archivo {wordlist_file} en la carpeta.")
    exit(1)

print(f"[*] Cargando diccionario desde: {wordlist_file}")
print(f"[*] Iniciando fuzzing avanzado sobre: {base_url}\n")

# Abrimos y leemos el diccionario línea por línea
with open(wordlist_file, "r") as f:
    rutas = f.readlines()

for ruta in rutas:
    # Limpiamos espacios o saltos de línea invisibles
    ruta = ruta.strip()
    
    # Ignoramos líneas vacías
    if not ruta:
        continue
        
    url_completa = base_url + ruta
    
    try:
        # Usamos el camuflaje de navegador que aprendimos antes para evitar bloqueos
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0'
        }
        req = urllib.request.Request(url_completa, headers=headers)
        response = urllib.request.urlopen(req)
        
        print(f"[+] [EXISTE] {url_completa} --> Código HTTP: {response.getcode()}")
        
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"[-] [No encontrado] {url_completa} (404)")
        else:
            print(f"[!] [INTERESANTE] {url_completa} --> Código HTTP: {e.code}")
            
    except urllib.error.URLError as e:
        print(f"[-] Error de conexión con {url_completa}: {e.reason}")

print("\n[*] Fuzzing basado en diccionario finalizado con éxito.")