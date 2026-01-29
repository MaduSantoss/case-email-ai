# MailFlow | Intelligent Financial Triaging

> Sistema de Inteligência Artificial para triagem automática, priorização e resposta de e-mails financeiros.

![Status](https://img.shields.io/badge/status-concluído-emerald)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![AI Model](https://img.shields.io/badge/LLM-Llama%203.3-violet)

## 🎯 O Problema
Equipes financeiras perdem horas preciosas lendo e-mails repetitivos, separando comprovantes de spam e redigindo respostas padrão. A sobrecarga operacional gera atrasos em demandas críticas (como estornos e pagamentos).

## 💡 A Solução: MailFlow
O **MailFlow** atua como um analista júnior digital. Ele lê anexos (PDF/TXT) ou textos copiados, entende o contexto usando **NLP (Processamento de Linguagem Natural)** e utiliza um **LLM (Llama 3.3)** para:

1.  **Classificar** a demanda (Produtivo vs Improdutivo).
2.  **Definir Prioridade** (Alta, Média, Baixa) com base no conteúdo financeiro.
3.  **Redigir a Resposta** formal, empática e pronta para envio.

### ✨ Diferenciais Técnicos (Highlights)
* **Pipeline de NLP Customizado:** Implementação de um estágio de pré-processamento que realiza limpeza de texto (Regex) e remoção de *Stop Words* (palavras irrelevantes) antes da inferência. Isso aumenta a precisão da IA e reduz o custo computacional.
* **UX/UI Profissional:** Interface "Deep Navy" focada em produtividade, com feedback visual em tempo real (Toasts), Drag & Drop intuitivo com validação visual e layout responsivo.
* **Arquitetura Resiliente:** Tratamento robusto de erros no Backend e Frontend. Se a IA falhar ou a conexão cair, o sistema degrada graciosamente com mensagens claras ao usuário, sem travar a aplicação.

---

## 🛠️ Stack Tecnológica

A arquitetura foi desenhada para ser desacoplada, escalável e de fácil manutenção.

| Camada | Tecnologia | Motivo da Escolha |
| :--- | :--- | :--- |
| **Backend** | `FastAPI` | Alta performance (ASGI), tipagem forte e validação automática de dados com Pydantic. |
| **AI Engine** | `Groq Cloud` | Uso de LPUs (Language Processing Units) para inferência em tempo real do modelo `Llama-3.3-70b`. |
| **Data Processing** | `PyMuPDF` + `Regex` | Extração precisa de dados de PDFs e higienização de strings para o pipeline de NLP. |
| **Frontend** | `Vanilla JS` + `Tailwind` | Interface leve e rápida, sem o *overhead* de frameworks complexos (React/Vue) para este escopo. |

---

## ⚡ Como Rodar Localmente

### Pré-requisitos
* Python 3.10 ou superior.
* Uma chave de API da Groq (Gratuita).

### 1. Clonar e Instalar
Clone o repositório e instale as dependências listadas:

```bash
# Clone o projeto
git clone [https://github.com/MaduSantoss/case-email-ai]

# Entre na pasta do backend
cd backend

# Instale os pacotes
pip install -r requirements.txt

```

### 2. Configurar Variáveis de Ambiente

Crie um arquivo `.env` dentro da pasta `backend` e adicione sua chave de API para habilitar a IA:

```env
GROQ_API_KEY=sua_chave_aqui_gsk_...

```

### 3. Executar a Aplicação

Inicie o servidor de desenvolvimento:

```bash
python -m uvicorn app:app --reload

```

*O servidor iniciará em `http://127.0.0.1:8000*`

### 4. Acessar

Abra o arquivo `frontend/index.html` diretamente no seu navegador ou use um servidor local (como o Live Server do VS Code).

---

## 🧠 Decisões de Design (Engenharia)

1. **Segurança e Privacidade:** O arquivo `.gitignore` foi configurado para excluir segredos (.env) e arquivos temporários, garantindo que credenciais não sejam expostas no repositório.
2. **Otimização de Tokens:** A função `clean_text` no backend remove ruídos do e-mail. Isso significa que enviamos menos dados para a API da Groq, resultando em respostas mais rápidas e menor custo por token.
3. **Usabilidade (Hick's Law):** A interface foi simplificada para reduzir a carga cognitiva do usuário. O sistema de abas separa claramente as duas formas de entrada (Arquivo vs Texto), e o feedback visual (Toasts) confirma cada ação do sistema.

---

## 📄 Licença

Desenvolvido como parte de um Case Técnico para vaga de Desenvolvimento de Software.
