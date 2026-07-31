import subprocess

CANALES = {
    "América TV Perú": "https://tvgo.americatv.com.pe/",
    "France 24 Español": "https://static.france24.com/live/F24_ES_LO_HLS/live_web.m3u8",
    "DW Español": "https://dwamdstream102.akamaized.net/hls/live/2015525/dwstream102/index.m3u8"
}

def obtener_m3u8(url):
    if ".m3u8" in url:
        return url

    comando = [
        "yt-dlp",
        "--no-warnings",
        "--format", "best",
        "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "-g",
        url
    ]
    
    try:
        resultado = subprocess.check_output(comando, text=True, stderr=subprocess.DEVNULL).strip()
        if resultado:
            return resultado.split('\n')[0]
    except Exception as e:
        print(f"Error procesando {url}: {e}")
        
    return None

def main():
    m3u_content = "#EXTM3U\n"
    
    for nombre, url_web in CANALES.items():
        print(f"Obteniendo enlace para: {nombre}...")
        link_directo = obtener_m3u8(url_web)
        
        if link_directo:
            m3u_content += f'#EXTINF:-1 group-title="Canales" tvg-name="{nombre}", {nombre}\n{link_directo}\n'
            print(f"✔ Éxito al agregar {nombre}")
        else:
            print(f"✖ No se pudo obtener {nombre}")

    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)

if __name__ == "__main__":
    main()
