# **Transcrição de Áudio 🎧**

Este projeto é um **WebApp desenvolvido com Streamlit** que permite a **transcrição de áudios** a partir de vídeos do YouTube ou arquivos de áudio próprios. A transcrição é realizada utilizando o modelo **Whisper**, da OpenAI.

---

## **Funcionalidades**

- ✅ Transcrição de vídeos do **YouTube** (somente áudio).
- ✅ Transcrição de arquivos de áudio próprios (`.mp3`, `.wav`, `.m4a`).
- ✅ Geração de transcrição com **prompt contextual**, otimizando resultados para:
   - Entrevistas
   - Músicas
   - Aulas ou palestras
- ✅ Cálculo automático da **duração do áudio**.
- ✅ Baixar a transcrição em formato **.txt**.
- ✅ Reset automático dos campos após o download.
- ✅ Feedback visual durante as etapas de download e transcrição.
- ✅ Rolagem automática para o topo após o download do arquivo.

---

## **Tecnologias Utilizadas**

- [Streamlit](https://streamlit.io) - Framework para aplicações Web em Python.
- [Whisper](https://openai.com/whisper) - Modelo da OpenAI para transcrição de áudio.
- [Librosa](https://librosa.org) - Biblioteca para análise de áudio.
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Para download de áudios do YouTube.

---

## **Instalação e Execução**

### **Pré-requisitos**

- Python 3.8 ou superior.
- **Pip** instalado no ambiente.

### **1. Clone o repositório**

```
bash
git clone https://github.com/seu-usuario/nome-do-repositorio.git
cd nome-do-repositorio
```

### **2. Crie um ambiente virtual e ative**

```
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### **3. Instale as dependências**

```
pip install -r requirements.txt
```

### **4. Execute o Webapp**
```
streamlit run main.py
```

## **Como Usar**

1. **Escolha a origem do áudio**:
   - **YouTube**: Cole a URL do vídeo.
   - **Arquivo próprio**: Faça o upload do arquivo de áudio.

2. **Forneça detalhes contextuais (opcional)**, como:
   - Tipo do áudio (Entrevista, Música, Aula, etc.).
   - Descrição adicional para melhorar a precisão da transcrição.

3. **Clique em Transcrever** e aguarde o processamento.

4. **Baixe a transcrição em .txt**.

---

## **Contribuições**

Contribuições são bem-vindas! Se você tiver ideias, sugestões ou melhorias, sinta-se à vontade para abrir uma **Issue** ou enviar um **Pull Request**.

---

## **Desenvolvido por**

[Leo Laerda](https://leolacerda.com.br)

