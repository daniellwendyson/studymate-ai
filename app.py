import os
import re
import streamlit as st
from dotenv import load_dotenv

from agents import get_agents
from rag import process_pdf, search
from guardrails import check_guardrails

from crewai import Task, Crew


# ===============================
# CONFIG
# ===============================

load_dotenv()

st.set_page_config(
    page_title="MentorAI",
    layout="wide"
)

st.title("🎓 MentorAI — Plataforma de Tutoria Inteligente")


# ===============================
# EXTRAIR TÓPICO DA PERGUNTA
# ===============================

def extract_topic(question: str):

    q = question.lower()

    patterns = [
        r"explique\s+(.*)",
        r"o que são\s+(.*)",
        r"o que é\s+(.*)",
        r"defina\s+(.*)",
        r"me explique\s+(.*)"
    ]

    for pattern in patterns:

        match = re.search(pattern, q)

        if match:

            topic = match.group(1)
            topic = topic.replace("?", "").strip()

            return topic

    return question.replace("?", "").strip()


# ===============================
# MEMÓRIA DO SISTEMA
# ===============================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "questions_count" not in st.session_state:
    st.session_state.questions_count = 0

if "topics" not in st.session_state:
    st.session_state.topics = []

if "difficulty_score" not in st.session_state:
    st.session_state.difficulty_score = 0


# ===============================
# SIDEBAR
# ===============================

st.sidebar.header("📚 Material educacional")

uploaded_file = st.sidebar.file_uploader(
    "Envie um PDF educacional",
    type=["pdf"]
)

if uploaded_file:

    os.makedirs("data", exist_ok=True)

    file_path = f"data/{uploaded_file.name}"

    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    with st.spinner("Processando material..."):
        process_pdf(file_path)

    st.sidebar.success("Material carregado!")


# ===============================
# PROGRESSO DO ALUNO
# ===============================

st.sidebar.header("📊 Progresso do aluno")

st.sidebar.metric(
    "Perguntas feitas",
    st.session_state.questions_count
)

st.sidebar.metric(
    "Tópicos estudados",
    len(set(st.session_state.topics))
)

st.sidebar.metric(
    "Nível de dificuldade",
    st.session_state.difficulty_score
)


# ===============================
# CHAT
# ===============================

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])


# ===============================
# INPUT
# ===============================

user_input = st.chat_input("Faça sua pergunta sobre o conteúdo...")


if user_input:

    allowed, warning = check_guardrails(user_input)

    if not allowed:

        st.warning(warning)

    else:

        st.session_state.questions_count += 1

        topic = extract_topic(user_input)
        st.session_state.topics.append(topic)

        difficult_words = [
            "não entendi",
            "dificuldade",
            "confuso",
            "difícil"
        ]

        for word in difficult_words:
            if word in user_input.lower():
                st.session_state.difficulty_score += 1

        st.chat_message("user").markdown(user_input)

        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })


        # ===============================
        # RAG
        # ===============================

        with st.spinner("Buscando conteúdo educacional..."):
            context = search(user_input)

        context_text = "\n\n".join(context)


        # ===============================
        # AGENTES
        # ===============================

        tutor, evaluator, motivator = get_agents()


        # ===============================
        # TUTOR
        # ===============================

        task1 = Task(
            description=f"""
Use o contexto educacional abaixo para responder à pergunta do aluno.

CONTEXTO DO MATERIAL DIDÁTICO:
{context_text}

PERGUNTA DO ALUNO:
{user_input}

INSTRUÇÕES:

1. Primeiro explique o conceito usando o conteúdo do material.
2. Sempre incorpore trechos ou ideias presentes no material.
3. Depois explique de forma didática e amigável.
4. Você pode incluir incentivo ao aluno, mas nunca ignore o material.

IMPORTANTE:
Se o material definir o conceito, explique essa definição em linguagem simples.

Resposta do tutor:
""",
            expected_output="Explicação pedagógica baseada no material",
            agent=tutor
        )


        # ===============================
        # AVALIADOR
        # ===============================

        task2 = Task(
            description="""
Avalie a explicação do Tutor.

Produza um relatório contendo:

- clareza da explicação
- conceitos principais
- pontos de revisão
""",
            expected_output="Relatório educacional",
            agent=evaluator
        )


        # ===============================
        # MOTIVADOR
        # ===============================

        task3 = Task(
            description=f"""
Leia a explicação do Tutor e acrescente UMA pequena mensagem motivacional no final.

Não substitua a explicação.
Não escreva estratégias de estudo longas.
Apenas adicione 1 ou 2 frases de incentivo.

Explicação do Tutor:
{{task1.output}}
""",
            expected_output="Explicação do tutor + pequena motivação",
            agent=motivator
        )


        crew = Crew(
            agents=[tutor, evaluator, motivator],
            tasks=[task1, task2, task3],
            verbose=False,
            process="sequential"
        )


        # ===============================
        # EXECUÇÃO
        # ===============================

        with st.spinner("🤖 MentorAI analisando..."):
            crew_result = crew.kickoff()


        # ===============================
        # RESULTADO
        # ===============================

        if hasattr(crew_result, "raw"):
            final_answer = crew_result.raw
        elif hasattr(crew_result, "output"):
            final_answer = crew_result.output
        elif isinstance(crew_result, str):
            final_answer = crew_result
        else:
            final_answer = str(crew_result)

        final_answer = final_answer.strip()

        st.chat_message("assistant").markdown(final_answer)

        st.session_state.messages.append({
            "role": "assistant",
            "content": final_answer
        })


# ===============================
# PLANO DE ESTUDOS
# ===============================

if st.session_state.questions_count >= 3:

    st.divider()

    st.subheader("📚 Plano de estudos sugerido")

    topics = list(set(st.session_state.topics))[:5]

    st.write("Recomendamos revisar os seguintes conceitos:")

    for topic in topics:
        st.write(f"• **{topic.capitalize()}**")

    st.info(
        "💡 Revise esses conceitos e tente resolver exercícios sobre eles."
    )


# ===============================
# DASHBOARD PROFESSOR
# ===============================

if st.session_state.questions_count >= 5:

    st.divider()

    st.subheader("🧑‍🏫 Dashboard do professor")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Perguntas do aluno",
        st.session_state.questions_count
    )

    col2.metric(
        "Tópicos únicos",
        len(set(st.session_state.topics))
    )

    col3.metric(
        "Sinais de dificuldade",
        st.session_state.difficulty_score
    )

    if st.session_state.difficulty_score >= 2:

        st.warning(
            "⚠️ O sistema detectou possíveis dificuldades do aluno."
        )

    else:

        st.success(
            "✅ O aluno está progredindo bem."
        )