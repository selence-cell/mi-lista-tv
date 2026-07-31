import subprocess
import os

# 1. Agrega aquí tus canales y enlaces normales de páginas web
CANALES = {
    "Canal Ejemplo 1": "https://www.youtube.com/watch?v=X4VbdwhkE10",  # Sustituye por tu video/transmisión
    "Canal Ejemplo 2": "https://tvgo.americatv.com.pe/?utm_content=&utm_term="             # Sustituye por tu canal de Twitch
}

def obtener_m3u8(url):
    try:
        # Llama a yt-dlp para extraer el flujo directo .m3u8
        link = subprocess.check_output(
            ["yt-dlp", "-g", url],
            text=True,
            stderr=subprocess.DEVNULL
        ).strip()
        # Si devuelve múltiples líneas, tomamos la primera (calidad principal)
        return link.split('\n')[0]
    except Exception as e:
        print(f"Error procesando {url}: {e}")
        return None

def main():
    m3u_content = "#EXTM3U\n"
    
    for nombre, url_web in CANALES.items():
        print(f"Obteniendo enlace para: {nombre}...")
        direct_link = obtener_m3u8(url_web)
        
        if direct_link:
            m3u_content += f'#EXTINF:-1 tvg-name="{nombre}", {nombre}\n{direct_link}\n'
        else:
            print(f"No se pudo extraer el enlace de {nombre}")

    # Guardar en archivo
    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)

if __name__ == "__main__":
    main()
