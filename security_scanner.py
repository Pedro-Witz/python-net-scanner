import urllib.request
import urllib.error
import urllib.parse
import os
import time
import random
import argparse
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

def banner():
    print("""
    ==================================================
        [+] NEXUSPROBE - Auditoría HTTP, Fuzzing & Red
    ==================================================
    """)

def realizar_peticion(url, headers, stealth, delay_min, delay_max):
    try:
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        
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

def escanear_puerto(target_host, port):
    try:
        ip_objetivo = socket.gethostbyname(target_host)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        result = s.connect_ex((ip_objetivo, port))
        if result == 0:
            print(f"[+] [PUERTO ABIERTO] {target_host}:{port}")
        s.close()
    except Exception:
        pass

def main():
    parser = argparse.ArgumentParser(description="NexusProbe: Escáner HTTP modular, fuzzing y escaneo de puertos en Python.")
    parser.add_argument("-u", "--url", help="URL u host objetivo (ej. http://localhost:8080 o 127.0.0.1)")
    parser.add_argument("-w", "--wordlist", help="Ruta al archivo de diccionario para fuzzing de rutas")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Número de hilos concurrentes (por defecto: 10)")
    parser.add_argument("-s", "--stealth", action="store_true", help="Activar modo sigiloso con retardos aleatorios")
    parser.add_argument("--load-test", type=int, help="Realizar una prueba de carga lanzando N peticiones a la URL base")
    parser.add_argument("--port-scan", action="store_true", help="Ejecutar escaneo de puertos TCP comunes en el objetivo")

    args = parser.parse_args()
    banner()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'X-Security-Token': 'TokenSecretoDePrueba123'
    }

    if not args.url:
        print("[!] Error: Debes especificar un objetivo usando -u o --url. Usa -h para ayuda.")
        return

    # === MODO ESCANEO DE PUERTOS ===
    if args.port_scan:
        parsed_url = urllib.parse.urlparse(args.url)
        target_host = parsed_url.hostname if parsed_url.hostname else args.url.replace("http://", "").replace("https://", "").split("/")[0]
        
        ports = [21, 22, 23, 25, 53, 80, 110, 443, 445, 3306, 3389, 8080]
        print(f"[*] Iniciando escaneo de puertos TCP en: {target_host}")
        print(f"[*] Verificando {len(ports)} puertos comunes con {args.threads} hilos...\n")
        
        inicio = time.time()
        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            for port in ports:
                executor.submit(escanear_puerto, target_host, port)
                
        print(f"\n[*] Escaneo de puertos completado en {time.time() - inicio:.4f} segundos.")
        return

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
        print("[!] Especifica una acción válida (-w para fuzzing, --load-test para carga, o --port-scan para puertos). Usa -h para ayuda.")

if __name__ == "__main__":
    main()