import yt_dlp
import os

def download_yt_audio(youtube_url, output_dir):
    """
    Baixa o áudio de um vídeo do YouTube usando yt-dlp.

    :param youtube_url: URL do vídeo do YouTube.
    :param output_dir: Diretório onde o áudio será salvo.
    :return: Caminho do arquivo de áudio baixado.
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        output_template = os.path.join(output_dir, "%(title)s.%(ext)s")
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_template,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            filename = os.path.join(output_dir, f"{info['title']}.mp3")
            return filename if os.path.exists(filename) else None
    except Exception as e:
        print(f"Erro ao baixar áudio: {e}")
        return None