import streamlit as st
import tempfile
import os
import time
from transcriber import transcribe_audio
from youtube_utils import download_yt_audio

# Configuração da página
st.set_page_config(page_title="Transcrição de Áudio", page_icon="🎧")
st.title('Transcrição de Áudio')
st.write('Pesquisadores: aqui vocês podem transcrever (gratuitamente) áudios de vídeos do YouTube ou de arquivos de áudio próprios de entrevistas')
st.info('Web app criado no [**Streamlit**](https://streamlit.io) por [**Leo Lacerda**](https://linkedin.com/in/leolacerda)', icon="🤓")

# Inicialização do estado da sessão
if "transcription" not in st.session_state:
    st.session_state["transcription"] = None
if "audio_name" not in st.session_state:
    st.session_state["audio_name"] = None
if "youtube_url" not in st.session_state:
    st.session_state["youtube_url"] = ""

# Seção: Informações sobre o áudio
st.write("### Sobre o áudio")
audio_context_type = st.selectbox(
    "Qual o tipo de áudio?",
    ["Geral", "Entrevista", "Aula ou palestra"],
    key="audio_context_type",
    help="Selecione o tipo do áudio para fornecer ao sistema mais contexto."
)

context_description = st.text_area(
    "Descreva o contexto do áudio (opcional):",
    height=80,
    key="context_description",
    help="Forneça mais detalhes, como nomes de pessoas ou temas, para ajudar a melhorar a transcrição."
)

# Língua do áudio
language = st.selectbox(
    "Língua do áudio:",
    ["Português (BR)", "Português (PT)", "Inglês",
     "Espanhol", "Francês", "Alemão"],
    help="Selecione a língua predominante no áudio para melhorar a transcrição."
)

# Prompt inicial
default_prompts = {
    "Geral": "Este é um áudio geral.",
    "Entrevista": "Este é um áudio de uma entrevista entre duas ou mais pessoas.",
    "Aula ou palestra": "Este é um áudio de uma aula ou palestra.",
}
initial_prompt = f"{default_prompts[audio_context_type]} Língua selecionada: {language}."
if context_description:
    initial_prompt += f" {context_description}"

# Escolha da origem do áudio
st.write("### Escolha a origem do áudio")
audio_source = st.radio("", ["YouTube", "Arquivo Próprio"])

# Transcrição de arquivos próprios
if audio_source == "Arquivo Próprio":
    audio_file = st.file_uploader("Faça o upload do arquivo", type=["mp3", "wav", "m4a"])
    st.warning(
        "⚠️ A qualidade do áudio influencia a precisão da transcrição. Áudios de baixa qualidade podem ter erros."
    )
    if audio_file:
        temp_dir = tempfile.gettempdir()
        st.session_state["audio_name"] = os.path.splitext(audio_file.name)[0]
        audio_path = os.path.join(temp_dir, audio_file.name)

        with open(audio_path, "wb") as f:
            f.write(audio_file.read())
        st.success(f"Arquivo {audio_file.name} carregado com sucesso!")

        if st.button("Transcrever"):
            start_time = time.time()
            with st.spinner("Transcrevendo... Isso pode levar alguns minutos."):
                st.session_state["transcription"] = transcribe_audio(audio_path, prompt=initial_prompt)
            end_time = time.time()

            st.success(f"Transcrição finalizada em {int((end_time - start_time) // 60)} minutos e {int((end_time - start_time) % 60)} segundos!")
            os.remove(audio_path)

# Transcrição de vídeos do YouTube
if audio_source == "YouTube":
    youtube_url = st.text_input("Cole a URL do vídeo do YouTube:")
    st.warning(
        "⚠️ Alguns vídeos do YouTube não permitem download e transcrição devido a restrições de direitos autorais."
    )
    if st.button("Baixar e Transcrever"):
        if youtube_url:
            temp_dir = tempfile.gettempdir()
            st.info("Fazendo o download do áudio do YouTube...")
            audio_path = download_yt_audio(youtube_url, temp_dir)

            if audio_path and os.path.exists(audio_path):
                st.success("Download do áudio finalizado!")
                start_time = time.time()
                with st.spinner("Transcrevendo... Isso pode levar alguns minutos."):
                    st.session_state["transcription"] = transcribe_audio(audio_path, prompt=initial_prompt)
                end_time = time.time()

                st.session_state["audio_name"] = os.path.splitext(os.path.basename(audio_path))[0]
                st.success(f"Transcrição finalizada em {int((end_time - start_time) // 60)} minutos e {int((end_time - start_time) % 60)} segundos!")
                os.remove(audio_path)
            else:
                st.error("Falha no download do áudio. Verifique a URL.")
        else:
            st.error("Por favor, forneça uma URL válida do YouTube.")

# Exibição da transcrição e botão de download
if st.session_state["transcription"] and st.session_state["audio_name"]:
    st.text_area("Transcrição", st.session_state["transcription"], height=300)
    txt_filename = f"{st.session_state['audio_name']}.txt"
    if st.download_button(
        "Baixar Transcrição",
        st.session_state["transcription"],
        file_name=txt_filename,
        mime="text/plain"
    ):
        # Recarrega a página (reseta todos os inputs)
        st.markdown(
            '<meta http-equiv="refresh" content="0;URL=https://transcricaodeaudio.streamlit.app/">',
            unsafe_allow_html=True
        )