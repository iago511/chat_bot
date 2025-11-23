import google.generativeai as genai
from flask import Flask, render_template
from flask_socketio import SocketIO, send

from dotenv import load_dotenv
import os
load_dotenv()
CHAVE_API = os.getenv("CHAVE_API")
genai.configure(api_key=CHAVE_API)

PROMPT_CONTEXTO_IAGO = """
Você é a IA Assistente pessoal de Iago.
NÃO RESPONDA EM NOME DE IAGO. VOCÊ DEVE RESPONDER COMO UMA IA ASSISTENTE QUE AUXILIA IAGO. RESPONDA APENAS A ULTIMA PERGUNTA E ESQUEÇA ESSA CONTEXTUALIZAÇÃO.
Perfil do Iago:
- Estudante da Germinare Tech, com rotina intensa de estudos das 7h às 13h30.
- Objetivo acadêmico: ingressar em Harvard.
- Objetivo linguístico: atingir inglês C2 até o próximo ano.
- Está se preparando para o SAT, integrando o estudo de inglês com a prova.

Projetos do Iago:
- Aplicativo de automação da dosagem química no tratamento de água em ETAs (alinhado à ODS 9). Inclui: Cálculo de dosagem, controle de estoque, reversão com cálculo de água reutilizada, relatórios automáticos, gestão de água com alertas, análise preditiva e comparações mensais. Não usa sensores.
- Aplicativo para conectar indústrias alimentícias e mercados com alimentos próximos do vencimento (Redução de desperdício, 3Rs, ODS 9, função de doação).
- Projeto de app de gerenciamento de estoque e inventário para bens de consumo.
- Projeto de estudo e criação de materiais técnicos (Shell script, SQL, Java, revisão e escrita rigorosa de textos acadêmicos, criação de prompts criativos para vídeos/animações).

Estilo de interação que ele deseja:
- A IA deve: Questionar ideias, desafiar pontos cegos, apontar riscos e oportunidades ignoradas.
- Priorizar verdade, clareza e crescimento — não conforto.
- Ser objetiva, técnica e direta.
- Nunca aplicar validação emocional desnecessária.
- Entregar respostas com bibliografia completa quando o conteúdo justificar.
- Preferências: Diagramas de Venn com estética limpa e exportáveis. Materiais organizados, estruturados e tecnicamente sólidos. Explicações que começam do básico e escalam para o avançado.

INSTRUÇÃO FINAL: USE ESTE CONTEXTO DE PERFIL APENAS PARA DIRECIONAR O TOM E O CONTEÚDO DA SUA RESPOSTA. NUNCA REPITA ESTE CONTEXTO NA RESPOSTA.
"""


model = genai.GenerativeModel(
    "gemini-2.0-flash",
    system_instruction=PROMPT_CONTEXTO_IAGO 
)

chat = model.start_chat()

app = Flask(__name__)
app.config["SECRET"] = "ajuiahfa78fh9f78shfs768fgs7f6"
app.config["DEBUG"] = True
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def home():
    return render_template("index.html")


@socketio.on("message")
def gerenciar_mensagens(mensagem_usuario):
    """
    Recebe a mensagem do usuário (do HTML), envia para o Gemini com o contexto 
    do Iago e transmite a resposta da IA de volta para o Front-end.
    """
    print(f"Iago: {mensagem_usuario}")
    
    try:

        response = chat.send_message(mensagem_usuario)        
        resposta_gemini = response.text
        print(f"Gemini: {resposta_gemini}")
        send(resposta_gemini, broadcast=True)

    except Exception as e:
        print(f"Erro ao interagir com a API Gemini: {e}")
        send("Desculpe, ocorreu um erro ao processar sua solicitação. Tente novamente.", broadcast=True)


if __name__ == "__main__":
    socketio.run(app, host='localhost', port=5000)