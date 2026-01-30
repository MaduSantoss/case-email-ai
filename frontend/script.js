function showToast(message, type = 'error') {
    const container = document.getElementById('toast-container');
    const styles = {
        error: { bg: 'bg-slate-800', border: 'border-rose-500', icon: '✕' },
        warning: { bg: 'bg-slate-800', border: 'border-yellow-500', icon: '⚠' },
        success: { bg: 'bg-slate-800', border: 'border-emerald-500', icon: '✓' }
    };
    const style = styles[type] || styles.error;
    
    const toast = document.createElement('div');
    toast.className = `${style.bg} ${style.border} border-l-4 text-white px-4 py-3 rounded shadow-2xl flex items-center gap-3 min-w-[300px] toast-enter pointer-events-auto`;
    toast.innerHTML = `<span class="text-xl font-bold">${style.icon}</span> <span class="text-sm font-medium">${message}</span>`;

    container.appendChild(toast);
    setTimeout(() => {
        toast.classList.remove('toast-enter');
        toast.classList.add('toast-exit');
        toast.addEventListener('animationend', () => toast.remove());
    }, 4000);
}

const dropZone = document.getElementById('viewFile');
const dragOverlay = document.getElementById('dragOverlay');
let dragCounter = 0;
window.addEventListener('dragover', e => e.preventDefault(), false);
window.addEventListener('drop', e => e.preventDefault(), false);

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

dropZone.addEventListener('dragenter', (e) => {
    dragCounter++;
    dragOverlay.classList.remove('hidden');
});

dropZone.addEventListener('dragleave', (e) => {
    dragCounter--;
    if (dragCounter === 0) dragOverlay.classList.add('hidden');
});

dropZone.addEventListener('drop', (e) => {
    dragCounter = 0;
    dragOverlay.classList.add('hidden');
    const dt = e.dataTransfer;
    if (dt.files.length > 0) uploadFile(dt.files[0]);
});

const fileInput = document.getElementById('fileInput');
fileInput.addEventListener('change', (e) => {
    if (e.target.files[0]) uploadFile(e.target.files[0]);
});

function updateDropZone(file) {
    const label = document.querySelector('label[for="fileInput"]');
    const icon = document.querySelector('#viewFile .text-4xl');
    const container = document.getElementById('viewFile');
    container.classList.add('border-emerald-500/50', 'bg-emerald-500/5');
    container.classList.remove('border-white/10');
    
    icon.innerHTML = '✅'; 
    label.innerText = `Arquivo recebido:\n${file.name}`;
    label.classList.add('text-emerald-400');
}

async function uploadFile(file) {
    updateDropZone(file);
    toggleLoading(true);
    
    const fd = new FormData();
    fd.append('file', file);
    
    try {
        const res = await fetch('/api/classificar-arquivo', { method: 'POST', body: fd });
        if (!res.ok) throw new Error("Falha na conexão");
        const data = await res.json();
        render(data);
        showToast("Análise concluída!", "success");
    } catch (err) { 
        console.error(err);
        showToast("Erro ao processar arquivo.", "error"); 
    } finally { toggleLoading(false); }
}

async function copyResult() {
    const textElement = document.getElementById('textoSugestao');
    if (!textElement) return;
    try {
        await navigator.clipboard.writeText(textElement.innerText);
        showToast("Copiado com sucesso!", "success");
    } catch (err) { showToast("Erro ao copiar.", "error"); }
}

function switchTab(mode) {
    const viewFile = document.getElementById('viewFile');
    const viewText = document.getElementById('viewText');
    const tabFile = document.getElementById('tabFile');
    const tabText = document.getElementById('tabText');

    if (mode === 'file') {
        viewFile.classList.remove('hidden');
        viewText.classList.add('hidden');
        tabFile.classList.add('bg-blue-600', 'text-white');
        tabFile.classList.remove('text-slate-400');
        tabText.classList.remove('bg-blue-600', 'text-white');
        tabText.classList.add('text-slate-400');
    } else {
        viewFile.classList.add('hidden');
        viewText.classList.remove('hidden');
        tabText.classList.add('bg-blue-600', 'text-white');
        tabText.classList.remove('text-slate-400');
        tabFile.classList.remove('bg-blue-600', 'text-white');
        tabFile.classList.add('text-slate-400');
    }
}

async function handleTextUpload() {
    const text = document.getElementById('emailText').value;
    if (!text.trim()) return showToast("Digite o e-mail primeiro.", "warning");
    
    toggleLoading(true);
    try {
        const res = await fetch('/api/classificar-texto', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text })
        });
        if (!res.ok) throw new Error("Conexão falhou");
        const data = await res.json();
        render(data);
        showToast("Texto analisado!", "success");
    } catch (err) {
        showToast("Erro no servidor.", "error");
    } finally { toggleLoading(false); }
}

function toggleLoading(show) {
    const loading = document.getElementById('loading');
    if (show) loading.classList.remove('hidden');
    else loading.classList.add('hidden');
}

window.onload = () => {
    try {
        const salvo = localStorage.getItem('ultimo_resultado');
        if (salvo) render(JSON.parse(salvo));
    } catch (e) { localStorage.clear(); }
};

function render(data) {
    localStorage.setItem('ultimo_resultado', JSON.stringify(data));
    const placeholder = document.getElementById('placeholder');
    const resultadoArea = document.getElementById('resultadoArea');
    const isProd = data.categoria === 'PRODUTIVO';
    
    if (placeholder) placeholder.classList.add('hidden');

    resultadoArea.innerHTML = `
        <div class="bento-card p-8 space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500 border-t-4 ${isProd ? 'border-t-emerald-500' : 'border-t-slate-500'}">
            <div class="flex justify-between items-start">
                <div class="space-y-1">
                    <span class="label-micro">Categoria</span>
                    <div class="text-sm font-bold ${isProd ? 'text-emerald-400' : 'text-slate-400'} uppercase tracking-wider bg-white/5 px-3 py-1 rounded w-fit">${data.categoria}</div>
                </div>
                <div class="text-right space-y-1">
                    <span class="label-micro">Prioridade</span>
                    <div class="text-sm font-bold text-rose-500 uppercase tracking-wider">${data.prioridade}</div>
                </div>
            </div>
            <div>
                <span class="label-micro">Resumo</span>
                <h2 class="text-xl font-bold text-white mt-2 leading-snug">${data.resumo}</h2>
            </div>
            <div class="bg-black/20 rounded-2xl p-6 border border-white/5 relative group">
                <div class="flex justify-between items-center mb-3">
                    <span class="label-micro text-blue-400">Sugestão de Resposta</span>
                    <button id="btnCopy" onclick="copyResult()" class="text-[10px] font-bold uppercase tracking-widest text-blue-400 hover:text-white transition-colors flex items-center gap-1 cursor-pointer py-1 px-2 rounded hover:bg-white/5">
                        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg> Copiar
                    </button>
                </div>
                <p id="textoSugestao" class="text-slate-300 leading-relaxed italic text-sm border-l-2 border-blue-500/30 pl-4">"${data.resposta_sugerida}"</p>
            </div>
            <button onclick="localStorage.clear(); location.reload()" class="w-full py-4 text-xs font-bold text-slate-500 hover:text-white transition-colors uppercase tracking-widest border-t border-white/5 mt-4">Nova Análise</button>
        </div>
    `;
}