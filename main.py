import streamlit as st
import tempfile
import librosa
import os
from transcriber import transcribe_audio
from youtube_utils import download_yt_audio
import time

# Configuração inicial da página
st.set_page_config(
    page_title="Transcrição de Áudio",
    page_icon="🎧",
    layout="centered"
)

# Inicialização do estado da sessão
if "transcription" not in st.session_state:
    st.session_state["transcription"] = None
if "audio_name" not in st.session_state:
    st.session_state["audio_name"] = None
if "youtube_url" not in st.session_state:
    st.session_state["youtube_url"] = ""
if "audio_context_type" not in st.session_state:
    st.session_state["audio_context_type"] = "Geral"
if "context_description" not in st.session_state:
    st.session_state["context_description"] = ""
if "download_status" not in st.session_state:
    st.session_state["download_status"] = ""
if "reset_trigger" not in st.session_state:
    st.session_state["reset_trigger"] = False

# Título e Introdução
st.title('Transcrição de Áudio')
st.write('Transcreva áudios de vídeos do YouTube ou de arquivos de áudio próprios')
st.info('Web app criado no [**Streamlit**](https://streamlit.io) por [**Leo Lacerda**](https://leolacerda.com.br)', icon="🤓")

# Modelo único definido
whisper_model = "base"

# Reset dos inputs caso seja necessário
if st.session_state.get("reset_trigger", False):
    st.session_state["audio_context_type"] = "Geral"
    st.session_state["context_description"] = ""

# Seleção do tipo de áudio
st.write("#### Sobre o áudio")
audio_context_type = st.selectbox(
    "Qual o tipo de áudio?",
    ["Geral", "Entrevista", "Aula ou palestra"],
    index=["Geral", "Entrevista", "Aula ou palestra"].index(st.session_state.get("audio_context_type", "Geral")),
    key="audio_context_type",
    help="Selecione o tipo do áudio para fornecer ao sistema mais contexto, o que pode melhorar a precisão da transcrição."
)

# Entrada para descrição opcional do contexto
context_description = st.text_area(
    "Descreva o contexto do áudio (opcional):",
    value=st.session_state.get("context_description", ""),
    height=80,
    key="context_description",
    help="Se possível, forneça mais detalhes sobre o áudio. Isso pode ajudar o sistema a gerar uma transcrição mais precisa."
)

# Gera o prompt final
default_prompts = {
    "Geral": "Este é um áudio geral.",
    "Entrevista": "Este é um áudio de uma entrevista entre duas ou mais pessoas.",
    "Aula ou palestra": "Este é um áudio de uma aula ou palestra.",
}
initial_prompt = default_prompts.get(audio_context_type, "Este é um áudio geral.")  # Evita KeyError
if context_description:
    initial_prompt += f" {context_description}"

# Origem do áudio
st.write("#### Escolha a origem do áudio")
audio_source = st.radio("", ["YouTube", "Arquivo Próprio"])

audio_path = None

# Função para obter a duração do áudio
def get_audio_duration(file_path):
    try:
        duration = librosa.get_duration(path=file_path)
        minutes = int(duration // 60)
        seconds = int(duration % 60)
        return minutes, seconds
    except Exception as e:
        st.error(f"Erro ao calcular a duração do áudio: {e}")
        return 0, 0

# Upload do arquivo próprio
if audio_source == "Arquivo Próprio":
    audio_file = st.file_uploader("Faça o upload do arquivo", type=["mp3", "wav", "m4a"])
    if audio_file:
        temp_dir = tempfile.gettempdir()
        st.session_state["audio_name"] = os.path.splitext(audio_file.name)[0]
        audio_path = os.path.join(temp_dir, audio_file.name)

        with open(audio_path, "wb") as f:
            f.write(audio_file.read())
        st.success("Arquivo carregado!")

        # Exibe a duração do áudio
        minutes, seconds = get_audio_duration(audio_path)
        st.info(f"Duração do áudio: {minutes} minutos e {seconds} segundos.")

        if st.button("Transcrever"):
            start_time = time.time()
            with st.spinner("Transcrevendo... Isso pode levar alguns minutos."):
                st.session_state["transcription"] = transcribe_audio(audio_path, whisper_model, prompt=initial_prompt)
            end_time = time.time()

            total_time = end_time - start_time
            st.success(f"Transcrição finalizada em {int(total_time // 60)} minutos e {int(total_time % 60)} segundos!")
            os.remove(audio_path)

# Baixar e transcrever do YouTube
if audio_source == "YouTube":
    st.session_state["youtube_url"] = st.text_input(
        "Cole a URL do vídeo do YouTube:",
        value=st.session_state["youtube_url"]
    )

    if st.button("Baixar e Transcrever"):
        temp_dir = tempfile.gettempdir()
        st.session_state["download_status"] = "Fazendo o download do áudio..."  # Mensagem inicial
        st.info(st.session_state["download_status"])

        # Download do áudio
        with st.spinner("Baixando o áudio do YouTube... Aguarde."):
            audio_path = download_yt_audio(st.session_state["youtube_url"], temp_dir)

        if audio_path and os.path.exists(audio_path):
            st.session_state["audio_name"] = os.path.splitext(os.path.basename(audio_path))[0]
            st.session_state["download_status"] = "Download do áudio finalizado!"  # Mensagem final
            st.success(st.session_state["download_status"])

            # Exibe a duração do áudio
            minutes, seconds = get_audio_duration(audio_path)
            st.info(f"Duração do áudio: {minutes} minutos e {seconds} segundos.")

            # Transcrição
            start_time = time.time()
            with st.spinner("Transcrevendo... Isso pode levar alguns minutos."):
                st.session_state["transcription"] = transcribe_audio(audio_path, whisper_model, prompt=initial_prompt)
            end_time = time.time()

            st.success(f"Transcrição finalizada em {int((end_time - start_time) // 60)} minutos e {int((end_time - start_time) % 60)} segundos!")
            os.remove(audio_path)
        else:
            st.session_state["download_status"] = "Falha no download do áudio. Verifique a URL."
            st.error(st.session_state["download_status"])

# Mostrar transcrição e botão de download
if st.session_state["transcription"] and st.session_state["audio_name"]:
    st.text_area("Transcrição", st.session_state["transcription"], height=300)
    txt_filename = f"{st.session_state['audio_name']}.txt"
    if st.download_button(
        "Baixar Transcrição",
        st.session_state["transcription"],
        file_name=txt_filename,
        mime="text/plain"
    ):
        # Limpa os estados após o download
        st.session_state["transcription"] = None
        st.session_state["audio_name"] = None
        st.session_state["youtube_url"] = ""
        st.session_state["reset_trigger"] = True

        # Adiciona JavaScript para rolar ao topo
        st.markdown(
            "<script>window.scrollTo(0, 0);</script>",
            unsafe_allow_html=True
        )
        st.rerun()