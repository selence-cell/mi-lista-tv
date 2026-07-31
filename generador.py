import urllib.request
import re

def obtener_america_tv():
    url_web = "https://tvgo.americatv.com.pe/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        req = urllib.request.Request(url_web, headers=headers)
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            # Busca la URL m3u8 que contiene el access_token activo en el código fuente de la página
            match = re.search(r'https://[^\s"\']+\.mdstrm\.com/live-stream-secure/[^\s"\']+\.m3u8[^\s"\']*', html)
            if match:
                return match.group(0)
    except Exception as e:
        print(f"Error: {e}")
    return None

CANALES_ESTABLES = {
    "America": "https://live-evg1.tv360.bitel.com.pe/bitel/americatv/playlist.m3u8",
    "DW Español": "https://dwamdstream102.akamaized.net/hls/live/2015525/dwstream102/index.m3u8",
    "France 24 Español": "https://static.france24.com/live/F24_ES_LO_HLS/live_web.m3u8"
}

def main():
    m3u_content = "#EXTM3U\n"
    
    # 1. Intentar obtener América TV con token
    link_america = obtener_america_tv()
    if link_america:
        m3u_content += f'#EXTINF:-1 group-title="Canales" tvg-name="América TV Perú", América TV Perú\n{link_america}\n'
        print("✔ América TV agregado con token.")
    else:
        print("✖ No se pudo pescar el token de América TV.")

    # 2. Agregar el resto de canales
    for nombre, url in CANALES_ESTABLES.items():
        m3u_content += f'#EXTINF:-1 group-title="Canales" tvg-name="{nombre}", {nombre}\n{url}\n'

    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)

if __name__ == "__main__":
    main()
