import whisper
import os
import re

def transcribe_audio(audio_path, model_size="base", prompt=None):
    """
    Transcreve um arquivo de áudio usando o modelo Whisper.

    :param audio_path: Caminho para o arquivo de áudio.
    :param model_size: Tamanho do modelo Whisper a ser usado.
    :param prompt: Informações adicionais para guiar a transcrição.
    :return: Texto transcrito formatado.
    """
    if not os.path.exists(audio_path):
        return "Erro: Arquivo de áudio não encontrado."

    try:
        model = whisper.load_model(model_size)
        result = model.transcribe(audio_path, prompt=prompt)  # Usa "prompt" aqui
        formatted_text = format_transcription(result["text"])
        return formatted_text
    except Exception as e:
        return f"Erro na transcrição: {e}"

def format_transcription(text):
    """
    Formata o texto inserindo quebras de linha ao final de cada frase.

    :param text: Texto original da transcrição.
    :return: Texto formatado com quebras de linha.
    """
    # Adiciona uma quebra de linha após ".", "?" e "!" seguidos de espaço ou fim de texto
    formatted_text = re.sub(r'([.?!])(\s|$)', r'\1\n', text)
    return formatted_text.strip()