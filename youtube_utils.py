import yt_dlp
import os

def download_yt_audio(youtube_url, output_dir):
    """
    Baixa o áudio de um vídeo do YouTube usando yt-dlp.

    :param youtube_url: URL do vídeo do YouTube.
    :param output_dir: Diretório onde o áudio será salvo.
    :return: Caminho do arquivo de áudio baixado ou None em caso de falha.
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        output_template = os.path.join(output_dir, "%(title)s.%(ext)s")
        
        ydl_opts = {
            'format': 'bestaudio/best',  # Melhor formato de áudio disponível
            'outtmpl': output_template,  # Nome do arquivo de saída
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'nocheckcertificate': True,  # Ignora certificados HTTPS inválidos
            'quiet': False,              # Mostra logs no terminal (para debug)
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
            return filename if os.path.exists(filename) else None
    except Exception as e:
        print(f"Erro ao baixar áudio: {e}")
        return None