import argparse
import subprocess
from pathlib import Path

def ejecutar(comando):
    resultado = subprocess.run(comando)
    if resultado.returncode != 0:
        raise SystemExit("Hubo un error al procesar el video.")

def main():
    parser = argparse.ArgumentParser(
        description="BRO CLIPPER AI - clips verticales de 45 segundos"
    )
    parser.add_argument("url", help="URL del video")
    args = parser.parse_args()

    carpeta = Path("clips")
    carpeta.mkdir(exist_ok=True)

    print("Descargando video...")
    ejecutar([
        "yt-dlp",
        "-f", "best[ext=mp4]/best",
        "-o", "source.%(ext)s",
        args.url
    ])

    videos = list(Path(".").glob("source.*"))
    if not videos:
        raise SystemExit("No se encontró el video descargado.")

    video = videos[0]
    print("Creando clips verticales de 45 segundos...")

    ejecutar([
        "ffmpeg", "-y",
        "-i", str(video),
        "-vf",
        "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-crf", "23",
        "-c:a", "aac",
        "-f", "segment",
        "-segment_time", "45",
        "-reset_timestamps", "1",
        str(carpeta / "clip_%03d.mp4")
    ])

    print("¡Listo! Tus clips están en la carpeta clips.")

if __name__ == "__main__":
    main()
