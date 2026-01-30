import os
import re
import json
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pypdf import PdfReader 
import io
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API MailFlow Online! O Frontend está rodando na rota principal."}

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

STOP_WORDS = {
    "de", "a", "o", "que", "e", "do", "da", "em", "um", "para", "com", "não", "uma", "os", "no", "se", "na", "por", "mais", "as", "dos", "como", "mas", "ao", "ele", "das", "à", "seu", "sua", "ou", "quando", "muito", "nos", "já", "eu", "também", "só", "pelo", "pela", "até", "isso", "ela", "entre", "depois", "sem", "mesmo", "aos", "seus", "quem", "nas", "me", "esse", "eles", "você", "essa", "num", "nem", "suas", "meu", "às", "minha", "numa", "pelos", "elas", "qual", "nós", "lhe", "deles", "essas", "esses", "pelas", "este", "dele", "tu", "te", "vocês", "vos", "lhes", "meus", "minhas", "teu", "tua", "teus", "tuas", "nosso", "nossa", "nossos", "nossas", "dela", "delas", "esta", "estes", "estas", "aquele", "aquela", "aqueles", "aquelas", "isto", "aquilo"
}

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    words = text.split()
    filtered_words = [word for word in words if word not in STOP_WORDS]
    return " ".join(filtered_words)

def extract_json_from_ai(ai_response):
    try:
        start = ai_response.find('{')
        end = ai_response.rfind('}') + 1
        if start != -1 and end != -1:
            json_str = ai_response[start:end]
            return json.loads(json_str)
        else:
            return {"categoria": "ERRO", "resumo": "IA não retornou JSON válido", "prioridade": "N/A", "resposta_sugerida": "Tente novamente."}
    except:
        return {"categoria": "ERRO", "resumo": "Falha ao processar resposta", "prioridade": "N/A", "resposta_sugerida": "Verifique o log."}

def analyze_email(content):
    cleaned_content = clean_text(content)
    
    prompt = f"""
    Analise este e-mail financeiro já tratado:
    "{cleaned_content}"

    Classifique como "PRODUTIVO" ou "IMPRODUTIVO".
    Retorne APENAS um JSON puro neste formato:
    {{
        "categoria": "PRODUTIVO",
        "resumo": "Resumo curto em pt-br",
        "prioridade": "ALTA",
        "resposta_sugerida": "Sugestão de resposta formal."
    }}
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.1 
        )
        return extract_json_from_ai(chat_completion.choices[0].message.content)
    except Exception as e:
        print(f"Erro na API: {e}")
        return {"categoria": "ERRO API", "resumo": str(e), "prioridade": "CRITICA", "resposta_sugerida": "Erro de conexão."}

@app.get("/api/")
def read_root():
    return {"message": "Servidor MailFlow Online 🚀"}

@app.post("/api/classificar-arquivo")
async def classify_file(file: UploadFile = File(...)):
    try:
        content = ""
        if file.filename.endswith(".pdf"):
            file_bytes = await file.read()
            pdf_reader = PdfReader(io.BytesIO(file_bytes))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
            content = text
        elif file.filename.endswith(".txt"):
            content = (await file.read()).decode("utf-8")
        
        return analyze_email(content)
    except Exception as e:
        print(f"Erro no upload: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class EmailText(BaseModel):
    text: str

@app.post("/api/classificar-texto")
async def classify_text(email: EmailText):
    return analyze_email(email.text)