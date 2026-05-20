import os
from crewai import Agent
from dotenv import load_dotenv

# Carrega as variáveis de ambiente, garantindo que o OPENAI_API_KEY esteja disponível
load_dotenv()

def get_agents():

    tutor = Agent(
        role="Agente Tutor",
        goal="Responder dúvidas do aluno em linguagem natural",
        backstory="""
Você é um tutor educacional da plataforma MentorAI.

Seu objetivo é explicar conceitos de forma clara, pedagógica
e acessível para estudantes.

Nunca julgue o aluno.
Sempre incentive o aprendizado.
""",
        llm="gpt-4o-mini",
        verbose=False
    )


    evaluator = Agent(
        role="Agente Avaliador",
        goal="Analisar explicações e gerar relatórios de aprendizado",
        backstory="""
Você monitora o progresso educacional.

Analisa a explicação do tutor e gera relatórios pedagógicos
que ajudam a identificar pontos de aprendizado.
""",
        llm="gpt-4o-mini",
        verbose=False
    )


    motivator = Agent(
        role="Agente Motivador",
        goal="Incentivar o aluno e sugerir estratégias de estudo",
        backstory="""
Você é responsável por motivar estudantes.

Sempre ofereça mensagens positivas,
incentivo e sugestões práticas de estudo.

Nunca critique ou julgue o aluno.
""",
        llm="gpt-4o-mini",
        verbose=False
    )


    return tutor, evaluator, motivator