CANALES = {
    "América TV Perú": "https://pe-p4-p-e-cx1.cdn.mdstrm.com/live-stream-secure/6099b04d9418ac082441dd74/publish/playlist.m3u8",
    "DW Español": "https://dwamdstream102.akamaized.net/hls/live/2015525/dwstream102/index.m3u8",
    "France 24 Español": "https://static.france24.com/live/F24_ES_LO_HLS/live_web.m3u8"
}

def main():
    m3u_content = "#EXTM3U\n"
    
    for nombre, url in CANALES.items():
        m3u_content += f'#EXTINF:-1 group-title="Canales" tvg-name="{nombre}", {nombre}\n{url}\n'
        print(f"✔ Agregado: {nombre}")

    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)

if __name__ == "__main__":
    main()
