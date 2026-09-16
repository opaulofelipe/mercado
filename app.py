import streamlit as st

st.set_page_config(
    page_title="Mercado",
    page_icon="🛒",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
      .stApp { background:#080808; }
      .block-container { max-width:760px; padding:0.35rem 0.35rem 2rem; }
      header[data-testid="stHeader"] { background:transparent; }
      #MainMenu, footer { visibility:hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

APP_HTML = r'''
<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<style>
:root{
  --green:#9EE493;
  --mint:#DAF7DC;
  --sage:#ABC8C0;
  --mauve:#70566D;
  --plum:#42273B;
  --bg:#080808;
  --surface:#1A191C;
  --surface-2:#211F23;
  --text:#F4F2F5;
  --muted:#A49FA7;
  --line:rgba(255,255,255,.06);
  --shadow:0 10px 30px rgba(0,0,0,.18);
}
*{box-sizing:border-box}
html{background:var(--bg);color-scheme:dark}
body{
  margin:0;
  background:var(--bg);
  color:var(--text);
  font-family:"Segoe UI",-apple-system,BlinkMacSystemFont,"Helvetica Neue",Arial,sans-serif;
  -webkit-font-smoothing:antialiased;
  overscroll-behavior-y:contain;
}
button,input,select{font:inherit}
button{-webkit-tap-highlight-color:transparent}
.app{max-width:720px;margin:0 auto;padding:18px 14px max(32px,env(safe-area-inset-bottom))}
.header{padding:4px 4px 14px}
.kicker{color:var(--green);font-size:13px;font-weight:700;margin-bottom:3px}
h1{font-size:clamp(31px,8vw,43px);line-height:1.02;letter-spacing:-.035em;margin:0;font-weight:760}
.meta{font-size:14px;color:var(--muted);margin-top:7px}
.section-title{display:inline-flex;align-items:center;gap:7px;color:var(--green);font-size:14px;font-weight:700;margin:12px 4px 8px}
.section-title.done-title{color:var(--sage);margin-top:18px}
.count{opacity:.65;font-weight:600}
.list{display:flex;flex-direction:column;gap:7px}
.task{display:grid;grid-template-columns:48px minmax(0,1fr) 0px;align-items:center;min-height:70px;background:linear-gradient(180deg,var(--surface-2),var(--surface));border:1px solid var(--line);border-radius:19px;box-shadow:var(--shadow);overflow:hidden;transition:grid-template-columns .18s ease,border-color .18s ease,transform .12s ease}
.task.delete-armed{grid-template-columns:48px minmax(0,1fr) 58px;border-color:rgba(112,86,109,.55)}
.check-wrap{height:100%;display:flex;align-items:center;justify-content:center;padding-left:4px}
.check{width:30px;height:30px;border-radius:999px;border:2px solid var(--sage);background:transparent;color:#111;display:grid;place-items:center;padding:0;cursor:pointer;transition:.15s ease}
.check:hover{border-color:var(--green)}
.task.completed .check{background:var(--green);border-color:var(--green)}
.check svg{width:17px;height:17px;opacity:0;transform:scale(.7);transition:.15s ease;stroke:#1B2A1D;stroke-width:3;fill:none}
.task.completed .check svg{opacity:1;transform:scale(1)}
.task-content{min-width:0;padding:14px 8px 14px 2px;cursor:default;user-select:none;-webkit-user-select:none;touch-action:pan-y}
.task-name{font-size:17px;line-height:1.22;font-weight:520;white-space:normal;overflow-wrap:anywhere;transition:.15s ease}
.task-sub{margin-top:4px;font-size:12.5px;color:#8F8992;line-height:1.25}
.task.completed .task-name{color:#8F8B91;text-decoration:line-through;text-decoration-thickness:1.5px;text-decoration-color:#8F8B91}
.task.completed .task-sub{color:#706C73}
.trash{align-self:stretch;width:58px;border:0;background:rgba(112,86,109,.30);color:var(--mint);display:grid;place-items:center;cursor:pointer;opacity:0;pointer-events:none;transform:translateX(12px);transition:.18s ease}
.task.delete-armed .trash{opacity:1;pointer-events:auto;transform:translateX(0)}
.trash:active{background:rgba(112,86,109,.55)}
.trash svg{width:21px;height:21px;stroke:currentColor;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.completed-block{margin-top:4px}
.empty{color:var(--muted);text-align:center;background:var(--surface);border:1px dashed rgba(171,200,192,.18);padding:22px 14px;border-radius:18px;font-size:14px}
.composer{margin-top:18px;padding-top:8px}
.composer-card{background:var(--surface);border:1px solid var(--line);border-radius:20px;padding:9px;box-shadow:var(--shadow)}
.add-row{display:grid;grid-template-columns:minmax(0,1fr) 48px;gap:8px}
.add-input{width:100%;height:49px;border-radius:15px;border:1px solid transparent;background:#242227;color:var(--text);padding:0 14px;outline:none;font-size:16px}
.add-input::placeholder{color:#7E7881}
.add-input:focus{border-color:rgba(158,228,147,.45);box-shadow:0 0 0 3px rgba(158,228,147,.08)}
.add-btn{height:49px;width:48px;border:0;border-radius:15px;background:rgba(158,228,147,.16);color:var(--green);font-size:26px;display:grid;place-items:center;cursor:pointer}
.add-btn:active{transform:scale(.97)}
.details-toggle{margin-top:6px;border:0;background:transparent;color:var(--sage);font-size:12.5px;padding:7px 6px;cursor:pointer}
.details{display:none;grid-template-columns:1fr 1fr 1.6fr;gap:8px;padding-top:5px}
.details.open{display:grid}
.field{display:flex;flex-direction:column;gap:5px}
.field label{font-size:11px;color:var(--muted);padding-left:2px}
.field input,.field select{height:42px;min-width:0;border-radius:13px;border:1px solid var(--line);background:#242227;color:var(--text);padding:0 10px;outline:none}
.hint{font-size:11.5px;color:#726D75;margin:8px 5px 0;line-height:1.35}
.toast{position:fixed;left:50%;bottom:max(20px,env(safe-area-inset-bottom));transform:translate(-50%,18px);background:#2A272D;border:1px solid rgba(255,255,255,.08);color:var(--text);padding:10px 14px;border-radius:13px;font-size:13px;opacity:0;pointer-events:none;transition:.2s ease;z-index:50;box-shadow:0 10px 30px rgba(0,0,0,.35)}
.toast.show{opacity:1;transform:translate(-50%,0)}
.toast button{margin-left:12px;background:transparent;border:0;color:var(--green);font-weight:700;cursor:pointer}
@media(max-width:560px){
  .app{padding:12px 9px max(28px,env(safe-area-inset-bottom))}
  .header{padding:5px 4px 11px}
  h1{font-size:34px}
  .task{min-height:68px;border-radius:18px;grid-template-columns:46px minmax(0,1fr) 0px}
  .task.delete-armed{grid-template-columns:46px minmax(0,1fr) 56px}
  .check{width:29px;height:29px}
  .task-name{font-size:16.5px}
  .task-content{padding-top:13px;padding-bottom:13px}
  .details{grid-template-columns:1fr 1fr}
  .field.category{grid-column:1/-1}
}
@media(max-width:360px){
  .app{padding-left:7px;padding-right:7px}
  .details{grid-template-columns:1fr}
  .field.category{grid-column:auto}
}
</style>
</head>
<body>
<div class="app">
  <header class="header">
    <div class="kicker">Mercado</div>
    <h1>Minha lista</h1>
    <div class="meta" id="meta">0 pendentes · 0 concluídos</div>
  </header>

  <section>
    <div class="section-title">Pendentes <span class="count" id="pendingCount">0</span></div>
    <div class="list" id="pendingList"></div>
  </section>

  <section class="completed-block" id="completedSection">
    <div class="section-title done-title">✓ Concluídos <span class="count" id="doneCount">0</span></div>
    <div class="list" id="doneList"></div>
  </section>

  <section class="composer">
    <div class="composer-card">
      <div class="add-row">
        <input id="newName" class="add-input" maxlength="80" autocomplete="off" placeholder="Adicionar uma tarefa" aria-label="Novo item" />
        <button id="addBtn" class="add-btn" aria-label="Adicionar item">＋</button>
      </div>
      <button id="detailsToggle" class="details-toggle" type="button">Quantidade e categoria</button>
      <div id="details" class="details">
        <div class="field">
          <label for="qty">Quantidade</label>
          <input id="qty" type="number" inputmode="decimal" min="0.1" step="0.1" value="1" />
        </div>
        <div class="field">
          <label for="unit">Unidade</label>
          <select id="unit">
            <option>un</option><option>kg</option><option>g</option><option>L</option><option>mL</option><option>pct</option><option>cx</option><option>dz</option>
          </select>
        </div>
        <div class="field category">
          <label for="category">Categoria</label>
          <select id="category">
            <option>Hortifruti</option><option>Padaria</option><option>Açougue</option><option>Frios e laticínios</option><option>Mercearia</option><option>Bebidas</option><option>Congelados</option><option>Higiene</option><option>Limpeza</option><option>Pet</option><option selected>Outros</option>
          </select>
        </div>
      </div>
    </div>
    <div class="hint">Toque no círculo para concluir ou reabrir. Segure um item para mostrar a lixeira.</div>
  </section>
</div>
<div id="toast" class="toast"><span id="toastText"></span><button id="undoBtn" hidden>Desfazer</button></div>

<script>
(() => {
  const STORAGE_KEY = 'mercado_items_v1';
  const $ = (s) => document.querySelector(s);
  const pendingList = $('#pendingList');
  const doneList = $('#doneList');
  const pendingCount = $('#pendingCount');
  const doneCount = $('#doneCount');
  const meta = $('#meta');
  const completedSection = $('#completedSection');
  const newName = $('#newName');
  const qty = $('#qty');
  const unit = $('#unit');
  const category = $('#category');
  const toast = $('#toast');
  const toastText = $('#toastText');
  const undoBtn = $('#undoBtn');

  let items = loadItems();
  let lastDeleted = null;
  let toastTimer = null;

  function uid(){
    return (crypto && crypto.randomUUID) ? crypto.randomUUID() : `${Date.now()}-${Math.random().toString(16).slice(2)}`;
  }

  function normalize(raw){
    if(!Array.isArray(raw)) return [];
    return raw.filter(x => x && typeof x === 'object' && String(x.name || '').trim()).map(x => ({
      id:String(x.id || uid()),
      name:String(x.name || '').trim(),
      quantity:Number(x.quantity || 1),
      unit:String(x.unit || 'un'),
      category:String(x.category || 'Outros'),
      completed:Boolean(x.completed),
      favorite:Boolean(x.favorite),
      created_at:String(x.created_at || new Date().toISOString()),
      updated_at:String(x.updated_at || new Date().toISOString())
    }));
  }

  function loadItems(){
    try{return normalize(JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'));}
    catch(_){return [];}
  }

  function save(){
    localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
  }

  function formatQty(value){
    const n = Number(value || 1);
    return Number.isInteger(n) ? String(n) : String(n).replace('.', ',');
  }

  function showToast(text, undo=false){
    clearTimeout(toastTimer);
    toastText.textContent = text;
    undoBtn.hidden = !undo;
    toast.classList.add('show');
    toastTimer = setTimeout(() => toast.classList.remove('show'), 3200);
  }

  function disarmAll(except=null){
    document.querySelectorAll('.task.delete-armed').forEach(el => {
      if(el !== except) el.classList.remove('delete-armed');
    });
  }

  function makeTask(item){
    const row = document.createElement('article');
    row.className = 'task' + (item.completed ? ' completed' : '');
    row.dataset.id = item.id;

    const checkWrap = document.createElement('div');
    checkWrap.className = 'check-wrap';
    const check = document.createElement('button');
    check.className = 'check';
    check.type = 'button';
    check.setAttribute('aria-label', item.completed ? 'Voltar para pendente' : 'Marcar como concluído');
    check.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.2 4.2L19 7"/></svg>';
    check.addEventListener('click', (ev) => {
      ev.stopPropagation();
      item.completed = !item.completed;
      item.updated_at = new Date().toISOString();
      save();
      render();
    });
    checkWrap.appendChild(check);

    const content = document.createElement('div');
    content.className = 'task-content';
    const title = document.createElement('div');
    title.className = 'task-name';
    title.textContent = item.name;
    const sub = document.createElement('div');
    sub.className = 'task-sub';
    sub.textContent = `${formatQty(item.quantity)} ${item.unit} · ${item.category}`;
    content.append(title, sub);

    const trash = document.createElement('button');
    trash.className = 'trash';
    trash.type = 'button';
    trash.setAttribute('aria-label', `Excluir ${item.name}`);
    trash.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6h18"/><path d="M8 6V4h8v2"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v5M14 11v5"/></svg>';
    trash.addEventListener('click', (ev) => {
      ev.stopPropagation();
      const index = items.findIndex(x => x.id === item.id);
      if(index < 0) return;
      lastDeleted = {item:items[index], index};
      items.splice(index,1);
      save();
      render();
      showToast('Item excluído', true);
    });

    let timer = null;
    let startX = 0, startY = 0;
    const cancelHold = () => { if(timer){clearTimeout(timer); timer=null;} };
    content.addEventListener('pointerdown', (ev) => {
      if(ev.pointerType === 'mouse' && ev.button !== 0) return;
      startX = ev.clientX; startY = ev.clientY;
      cancelHold();
      timer = setTimeout(() => {
        disarmAll(row);
        row.classList.add('delete-armed');
        if(navigator.vibrate) navigator.vibrate(30);
        timer = null;
      }, 560);
    });
    content.addEventListener('pointermove', (ev) => {
      if(Math.hypot(ev.clientX-startX, ev.clientY-startY) > 11) cancelHold();
    });
    content.addEventListener('pointerup', cancelHold);
    content.addEventListener('pointercancel', cancelHold);
    content.addEventListener('pointerleave', cancelHold);
    content.addEventListener('contextmenu', (ev) => { ev.preventDefault(); disarmAll(row); row.classList.add('delete-armed'); });
    content.addEventListener('click', () => {
      if(row.classList.contains('delete-armed')) row.classList.remove('delete-armed');
    });

    row.append(checkWrap, content, trash);
    return row;
  }

  function render(){
    pendingList.replaceChildren();
    doneList.replaceChildren();
    const pending = items.filter(x => !x.completed);
    const done = items.filter(x => x.completed);

    pendingCount.textContent = pending.length;
    doneCount.textContent = done.length;
    meta.textContent = `${pending.length} pendente${pending.length===1?'':'s'} · ${done.length} concluído${done.length===1?'':'s'}`;

    if(pending.length === 0){
      const empty = document.createElement('div');
      empty.className='empty';
      empty.textContent='Nenhum item pendente.';
      pendingList.appendChild(empty);
    } else {
      pending.forEach(item => pendingList.appendChild(makeTask(item)));
    }

    completedSection.style.display = done.length ? '' : 'none';
    done.forEach(item => doneList.appendChild(makeTask(item)));
  }

  function addItem(){
    const name = newName.value.trim();
    if(!name){ newName.focus(); return; }
    const now = new Date().toISOString();
    items.unshift({
      id:uid(), name,
      quantity:Math.max(.1, Number(qty.value || 1)),
      unit:unit.value, category:category.value,
      completed:false, favorite:false,
      created_at:now, updated_at:now
    });
    save();
    newName.value=''; qty.value='1'; unit.value='un'; category.value='Outros';
    render();
    newName.focus();
  }

  $('#addBtn').addEventListener('click', addItem);
  newName.addEventListener('keydown', (ev) => { if(ev.key === 'Enter'){ ev.preventDefault(); addItem(); } });
  $('#detailsToggle').addEventListener('click', () => $('#details').classList.toggle('open'));
  undoBtn.addEventListener('click', () => {
    if(!lastDeleted) return;
    items.splice(Math.min(lastDeleted.index, items.length),0,lastDeleted.item);
    lastDeleted=null; save(); render(); toast.classList.remove('show');
  });
  document.addEventListener('pointerdown', (ev) => {
    if(!ev.target.closest('.task')) disarmAll();
  });
  window.addEventListener('storage', (ev) => {
    if(ev.key === STORAGE_KEY){ items = loadItems(); render(); }
  });

  render();
})();
</script>
</body>
</html>
'''

# HTML/JS roda dentro de um iframe do próprio app. O código continua sendo
# entregue pelo Streamlit/Python, mas a lista é persistida diretamente no
# localStorage do navegador e as interações não dependem de reruns do servidor.
st.iframe(APP_HTML, width="stretch", height="content")
