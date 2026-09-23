import urllib.request
import urllib.error
import os
import time
import random
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

def banner():
    print(r"""
   ___                  _              _                               
  / __| ___  ___ _   _ _| |___ __ _  __| |  ___ __ __ _ _ _  _ _ ___ _ _ 
 | (_ |/ -_)/ _ \ || | ' \/ -_) _` |/ _` | (_-<\ V  V | ' \| '_/ -_) '_|
  \___|\___|\___/\_,_|_||_\___\__,_|\__,_| /__/ \_/\_/|_||_|_| \___|_|  
    [ Herramienta Modular de Auditoría HTTP & Fuzzing - Laboratorio Local ]
    """)

def realizar_peticion(url, headers, stealth, delay_min, delay_max):
    try:
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        
        # Si aplica modo sigiloso, aplicamos la pausa en el hilo
        if stealth:
            pausa = random.uniform(delay_min, delay_max)
            time.sleep(pausa)
            
        return True, response.getcode(), url, None
    except urllib.error.HTTPError as e:
        if stealth:
            time.sleep(random.uniform(delay_min, delay_max))
        return False, e.code, url, "HTTPError"
    except urllib.error.URLError as e:
        return False, "Error de red", url, str(e.reason)

def main():
    parser = argparse.ArgumentParser(description="Escáner HTTP modular y herramienta de pruebas de carga en Python.")
    parser.add_argument("-u", "--url", required=True, help="URL objetivo (ej. http://localhost:8080)")
    parser.add_argument("-w", "--wordlist", help="Ruta al archivo de diccionario para fuzzing de rutas")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Número de hilos concurrentes (por defecto: 10)")
    parser.add_argument("-s", "--stealth", action="store_true", help="Activar modo sigiloso con retardos aleatorios")
    parser.add_argument("--load-test", type=int, help="Realizar una prueba de carga lanzando N peticiones a la URL base")

    args = parser.parse_args()
    banner()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'X-Security-Token': 'TokenSecretoDePrueba123'
    }

    # === MODO PRUEBA DE CARGA ===
    if args.load_test:
        print(f"[*] Iniciando prueba de carga sobre: {args.url}")
        print(f"[*] Lanzando {args.load_test} peticiones con {args.threads} hilos concurrentes...\n")
        
        exitosas, fallidas = 0, 0
        inicio = time.time()
        
        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            futures = [executor.submit(realizar_peticion, args.url, headers, False, 0, 0) for _ in range(args.load_test)]
            for future in as_completed(futures):
                exito, codigo, _, _ = future.result()
                if exito: exitosas += 1
                else: fallidas += 1
                
        duracion = time.time() - inicio
        print(f"\n[+] Carga finalizada en {duracion:.4f}s | Exitosas: {exitosas} | Fallidas: {fallidas}")
        return

    # === MODO FUZZING DE DIRECTORIOS ===
    if args.wordlist:
        if not os.path.exists(args.wordlist):
            print(f"[!] Error: No se encontró el archivo de diccionario '{args.wordlist}'.")
            return

        with open(args.wordlist, "r") as f:
            rutas = [line.strip() for line in f if line.strip()]

        print(f"[*] Cargadas {len(rutas)} rutas desde {args.wordlist}")
        print(f"[*] Iniciando fuzzing sobre {args.url} con {args.threads} hilos (Sigilo: {args.stealth})\n")

        urls_a_probar = [f"{args.url.rstrip('/')}/{r.lstrip('/')}" for r in rutas]
        
        inicio = time.time()
        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            futures = {executor.submit(realizar_peticion, u, headers, args.stealth, 1.0, 2.0): u for u in urls_a_probar}
            
            for future in as_completed(futures):
                exito, codigo, url_actual, tipo_err = future.result()
                if exito:
                    print(f"[+] [EXISTE] {url_actual} --> Código: {codigo}")
                elif codigo == 404:
                    print(f"[-] [No encontrado] {url_actual} (404)")
                else:
                    print(f"[!] [INTERESANTE] {url_actual} --> Código/Error: {codigo}")
                    
        print(f"\n[*] Fuzzing completado en {time.time() - inicio:.4f} segundos.")
    else:
        print("[!] Especifica un diccionario con -w o una prueba de carga con --load-test. Usa -h para ayuda.")

if __name__ == "__main__":
    main()