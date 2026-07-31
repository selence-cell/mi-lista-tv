import subprocess
import urllib.request
import re

CANALES_DIRECTOS = {
    "DW Español": "https://dwamdstream102.akamaized.net/hls/live/2015525/dwstream102/index.m3u8",
    "France 24 Español": "https://static.france24.com/live/F24_ES_LO_HLS/live_web.m3u8"
}

def obtener_america_tv():
    url_web = "https://tvgo.americatv.com.pe/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        req = urllib.request.Request(url_web, headers=headers)
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            
            # Buscar el enlace directo m3u8 o el iframe del reproductor Mediastream
            match = re.search(r'https://[^\s"\']+\.mdstrm\.com[^\s"\']+\.m3u8[^\s"\']*', html)
            if match:
                return match.group(0)
            
            # Buscar la ID de transmisión de Mediastream
            embed_id = re.search(r'6099b04d9418ac082441dd74', html)
            if embed_id:
                # Consultar la API pública de Mediastream para obtener el token actual
                api_url = f"https://mdstrm.com/live-stream/6099b04d9418ac082441dd74"
                req_api = urllib.request.Request(api_url, headers=headers)
                with urllib.request.urlopen(req_api) as api_res:
                    api_html = api_res.read().decode('utf-8')
                    stream_match = re.search(r'https://[^\s"\']+\.m3u8[^\s"\']*', api_html)
                    if stream_match:
                        return stream_match.group(0)
    except Exception as e:
        print(f"Error extrayendo América TV: {e}")
        
    return None

def main():
    m3u_content = "#EXTM3U\n"
    
    # 1. Procesar América TV
    print("Obteniendo enlace para: América TV Perú...")
    link_america = obtener_america_tv()
    if link_america:
        m3u_content += f'#EXTINF:-1 group-title="Canales" tvg-name="América TV Perú", América TV Perú\n{link_america}\n'
        print("✔ Éxito al agregar América TV Perú")
    else:
        print("✖ No se pudo obtener América TV Perú")

    # 2. Agregar los canales directos
    for nombre, url in CANALES_DIRECTOS.items():
        m3u_content += f'#EXTINF:-1 group-title="Canales" tvg-name="{nombre}", {nombre}\n{url}\n'
        print(f"✔ Éxito al agregar {nombre}")

    # 3. Guardar archivo M3U
    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)

if __name__ == "__main__":
    main()
