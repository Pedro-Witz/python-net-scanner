import urllib.request
import urllib.error
import os
import time
import random

base_url = "http://localhost:8080"
wordlist_file = "wordlist.txt"

if not os.path.exists(wordlist_file):
    print(f"[!] Error: No se encontró el archivo {wordlist_file}")
    exit(1)

print(f"[*] Cargando diccionario sigiloso desde: {wordlist_file}")
print(f"[*] Iniciando fuzzing sigiloso sobre: {base_url}\n")

with open(wordlist_file, "r") as f:
    rutas = f.readlines()

for ruta in rutas:
    ruta = ruta.strip()
    if not ruta:
        continue
        
    url_completa = base_url + ruta
    
    try:
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

    # === TÉCNICA DE SIGILO (STEALTH) ===
    # Pausa aleatoria entre 1 y 2 segundos para no saturar ni alertar al WAF
    tiempo_pausa = random.uniform(1.0, 2.0)
    print(f"    [i] Esperando {tiempo_pausa:.2f} segundos para mantener perfil bajo...")
    time.sleep(tiempo_pausa)

print("\n[*] Fuzzing sigiloso finalizado con éxito.")