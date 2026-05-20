

# 🎓 MentorAI — Plataforma de Tutoria Inteligente

MentorAI é uma plataforma de tutoria educacional com IA que responde dúvidas de alunos com base em materiais didáticos enviados em PDF. Utiliza agentes especializados com CrewAI para explicar, avaliar e motivar o aprendizado.

## ✨ Funcionalidades

- 📄 **Upload de PDF educacional** — o aluno envia o material e o sistema aprende com ele
- 🤖 **3 agentes de IA colaborando:**
  - **Tutor** — explica conceitos de forma didática baseado no material
  - **Avaliador** — analisa a qualidade da explicação e gera relatório pedagógico
  - **Motivador** — adiciona incentivo e estratégias de estudo
- 🔍 **RAG (Retrieval-Augmented Generation)** — respostas baseadas no conteúdo real do PDF
- 📊 **Dashboard de progresso** — acompanha perguntas feitas, tópicos estudados e dificuldades
- 🛡️ **Guardrails** — filtra perguntas fora do contexto educacional

## 🛠️ Tecnologias

- [Streamlit](https://streamlit.io/) — interface web
- [CrewAI](https://crewai.com/) — orquestração de agentes
- [LangChain](https://langchain.com/) — pipeline de RAG e embeddings
- [FAISS](https://github.com/facebookresearch/faiss) — busca vetorial
- [OpenAI GPT-4o-mini](https://openai.com/) — modelo de linguagem
- [PyPDF](https://pypdf.readthedocs.io/) — leitura de PDFs

## 🚀 Como rodar localmente

**1. Clone o repositório**
```bash
git clone https://github.com/daniellwendyson/studymate-ai.git
cd studymate-ai
```

**2. Crie e ative o ambiente virtual**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

**3. Instale as dependências**
```bash
pip install -r requirements.txt
```

**4. Configure as variáveis de ambiente**
```bash
cp .env.example .env
# Abra o arquivo .env e preencha com sua chave da OpenAI
```

**5. Rode a aplicação**
```bash
streamlit run app.py
```

## 📁 Estrutura do projeto

```
studymate-ai/
├── app.py            # Interface Streamlit e fluxo principal
├── agents.py         # Definição dos agentes CrewAI
├── rag.py            # Processamento de PDF e busca vetorial
├── guardrails.py     # Filtros de segurança
├── data/             # PDFs carregados (gerado automaticamente)
├── requirements.txt
├── .env.example
└── .gitignore
```

## ⚙️ Variáveis de ambiente

Veja o arquivo `.env.example` para as variáveis necessárias.

