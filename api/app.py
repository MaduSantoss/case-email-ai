import os
import re
import json
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import fitz 
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Servidor funcionando!"}

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

STOP_WORDS = {
    "de", "a", "o", "que", "e", "do", "da", "em", "um", "para", "com", "não", "uma", "os", "no", "se", "na", "por", "mais", "as", "dos", "como", "mas", "ao", "ele", "das", "à", "seu", "sua", "ou", "quando", "muito", "nos", "já", "eu", "também", "só", "pelo", "pela", "até", "isso", "ela", "entre", "depois", "sem", "mesmo", "aos", "seus", "quem", "nas", "me", "esse", "eles", "você", "essa", "num", "nem", "suas", "meu", "às", "minha", "numa", "pelos", "elas", "qual", "nós", "lhe", "deles", "essas", "esses", "pelas", "este", "dele", "tu", "te", "vocês", "vos", "lhes", "meus", "minhas", "teu", "tua", "teus", "tuas", "nosso", "nossa", "nossos", "nossas", "dela", "delas", "esta", "estes", "estas", "aquele", "aquela", "aqueles", "aquelas", "isto", "aquilo", "estou", "está", "estamos", "estão", "estive", "esteve", "estivemos", "estiveram", "estava", "estavam", "estivera", "estiveram", "haja", "hajamos", "hajam", "houve", "houvemos", "houveram", "houvera", "houveram", "haja", "hajamos", "hajam", "houvesse", "houvéssemos", "houvessem", "tiver", "tivermos", "tiverem", "hei", "há", "havemos", "hão", "houve", "houvemos", "houveram", "houvera", "houveram", "houve", "houvemos", "houveram", "houvesse", "houvéssemos", "houvessem", "tiver", "tivermos", "tiverem", "terei", "terá", "teremos", "terão", "teria", "teríamos", "teriam", "tinha", "tínhamos", "tinham", "tivera", "tiveram", "tivesse", "tivéssemos", "tivessem", "tiver", "tivermos", "tiverem", "ser", "sou", "somos", "são", "era", "éramos", "eram", "fui", "foi", "fomos", "foram", "fora", "foram", "seja", "sejamos", "sejam", "fosse", "fôssemos", "fossem", "for", "formos", "forem", "serei", "será", "seremos", "serão", "seria", "seríamos", "seriam", "tenho", "tem", "temos", "tém", "tinha", "tínhamos", "tinham", "tive", "teve", "tivemos", "tiveram", "tivera", "tiveram", "tenha", "tenhamos", "tenham", "tivesse", "tivéssemos", "tivessem", "tiver", "tivermos", "tiverem"
}

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    words = text.split()
    filtered_words = [word for word in words if word not in STOP_WORDS]
    text = " ".join(filtered_words)
    return text

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
        return {"categoria": "ERRO", "resumo": "Falha ao processar resposta da IA", "prioridade": "N/A", "resposta_sugerida": "Verifique o log do servidor."}

def analyze_email(content):
    cleaned_content = clean_text(content)
    
    prompt = f"""
    Analise este e-mail financeiro:
    "{cleaned_content}"

    Classifique como "PRODUTIVO" ou "IMPRODUTIVO".
    Retorne APENAS um JSON puro, sem markdown, sem crases, neste formato:
    {{
        "categoria": "PRODUTIVO",
        "resumo": "Resumo curto",
        "prioridade": "ALTA",
        "resposta_sugerida": "Sugestão de resposta."
    }}
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.1 
        )
        raw_response = chat_completion.choices[0].message.content
        return extract_json_from_ai(raw_response)
    except Exception as e:
        print(f"Erro na API Groq: {e}")
        return {"categoria": "ERRO API", "resumo": str(e), "prioridade": "CRITICA", "resposta_sugerida": "Erro de conexão."}

# Endpoint para Arquivos
@app.post("/classificar-arquivo")
async def classify_file(file: UploadFile = File(...)):
    try:
        content = ""
        if file.filename.endswith(".pdf"):
            content = await file.read()
            content = fitz.open(stream=content, filetype="pdf")
            text = ""
            for page in content:
                text += page.get_text()
            content = text
        elif file.filename.endswith(".txt"):
            content = (await file.read()).decode("utf-8")
        
        return analyze_email(content)
    except Exception as e:
        print(f"Erro no upload: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para Texto
class EmailText(BaseModel):
    text: str

@app.post("/classificar-texto")
async def classify_text(email: EmailText):
    return analyze_email(email.text)