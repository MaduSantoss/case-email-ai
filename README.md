# 🚀 MailFlow - Automação de Triagem de E-mails

![Project Status](https://img.shields.io/badge/Status-Concluído-success)
![Python](https://img.shields.io/badge/Backend-FastAPI-blue)
![AI](https://img.shields.io/badge/AI-Llama3-purple)
![Deploy](https://img.shields.io/badge/Deploy-Vercel-black)

## 📋 Sobre o Projeto
O **MailFlow** é uma solução Full-Stack desenvolvida para otimizar a rotina de departamentos financeiros. O sistema utiliza Inteligência Artificial Generativa para ler, interpretar e classificar e-mails e anexos (faturas, comprovantes, dúvidas), gerando minutas de respostas automáticas.

O objetivo é reduzir o tempo gasto em triagem manual e aumentar a produtividade da equipe.

### 🔴 Teste Ao Vivo 
👉 **Acesse o projeto rodando na nuvem:** https://case-email-ai.vercel.app/

---

## 🛠️ Tecnologias Utilizadas

### Backend & AI
* **Python 3.12+**
* **FastAPI:** Framework moderno e assíncrono para construção da API.
* **Groq Cloud (Llama 3.3):** LLM de altíssima velocidade para inferência e análise de contexto.
* **Pypdf:** Processamento robusto de arquivos PDF para extração de texto.
* **Regex & NLP:** Pré-processamento de texto para limpeza de dados e economia de tokens.

### Frontend
* **HTML5 & Vanilla JavaScript:** Foco em performance e leveza.
* **TailwindCSS:** Estilização responsiva e moderna.

### Infraestrutura
* **Vercel:** Deploy serverless com integração CI/CD automática via GitHub.

---

## ⚙️ Funcionalidades

1.  **Upload de Arquivos (PDF/TXT):** Extração automática de conteúdo de anexos financeiros.
2.  **Análise de Contexto:** A IA identifica se o e-mail é "Produtivo" (faturas, boletos) ou "Improdutivo" (spam, phishing).
3.  **Classificação de Prioridade:** Define se a demanda é ALTA, MÉDIA ou BAIXA.
4.  **Geração de Resposta:** Cria um rascunho de e-mail formal pronto para ser enviado.

---

## 🚀 Como Rodar Localmente

Se quiser rodar o projeto na sua máquina:

### 1. Clone o repositório
```bash
git clone https://github.com/MaduSantoss/case-email-ai
cd case-email-ai

```

### 2. Configure as Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto e adicione sua chave da Groq:

```env
GROQ_API_KEY=_sua_chave_aqui

```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt

```

### 4. Execute o Servidor

```bash
python -m uvicorn api.index:app --reload

```

Acesse em: `http://127.0.0.1:8000`

---

## 📂 Estrutura do Projeto

```
/
├── api/                 # Backend (Python/FastAPI)
│   └── index.py         # Lógica principal e rotas
├── frontend/            # Frontend (HTML/JS/CSS)
├── requirements.txt     # Dependências do projeto
├── vercel.json          # Configuração de Deploy
└── README.md            # Documentação

```

---

## 📞 Contato

Desenvolvido por **Maria Eduarda Santos Silva**.
