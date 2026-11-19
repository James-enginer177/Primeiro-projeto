<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Jogo da Cobrinha</title>
<style>
  :root { --bg:#0f172a; --card:#1e293b; --text:#e2e8f0; --accent:#22c55e; --food:#ef4444; }
  * { box-sizing:border-box; }
  body { margin:0; min-height:100vh; display:flex; align-items:center; justify-content:center;
         background:var(--bg); color:var(--text); font-family:system-ui,sans-serif; }
  .wrap { width:min(92vw,480px); text-align:center; }
  h1 { margin:0 0 8px; font-size:1.5rem; }
  .bar { display:flex; justify-content:space-between; margin-bottom:8px; font-weight:600; }
  .box { position:relative; }
  canvas { width:100%; aspect-ratio:1; background:var(--card); border-radius:12px; display:block; touch-action:none; }
  .overlay { position:absolute; inset:0; display:flex; flex-direction:column; align-items:center;
             justify-content:center; background:rgba(15,23,42,.8); border-radius:12px; gap:10px; }
  .overlay.hide { display:none; }
  button { background:var(--accent); color:#052e16; border:0; padding:10px 22px; border-radius:8px;
           font-size:1rem; font-weight:700; cursor:pointer; }
  p.dica { opacity:.7; font-size:.85rem; margin:10px 0 0; }
</style>
</head>
<body>
<div class="wrap">
  <h1>🐍 Jogo da Cobrinha</h1>
  <div class="bar"><span>Pontos: <b id="pts">0</b></span><span>Recorde: <b id="rec">0</b></span></div>
  <div class="box">
    <canvas id="c" width="480" height="480"></canvas>
    <div class="overlay" id="ov">
      <div id="msg" style="font-size:1.3rem;font-weight:700">Pronto para jogar?</div>
      <button id="btn">Jogar</button>
    </div>
  </div>
  <p class="dica">Setas ou WASD para mover • Espaço para pausar • No celular, deslize o dedo</p>
</div>
<script>
const cv = document.getElementById('c'), ctx = cv.getContext('2d');
const N = 20, S = cv.width / N;
const ptsEl = document.getElementById('pts'), recEl = document.getElementById('rec');
const ov = document.getElementById('ov'), msg = document.getElementById('msg'), btn = document.getElementById('btn');

let snake, dir, nextDir, food, pts, rec = 0, timer, rodando = false, pausado = false, delay;

try { rec = +localStorage.getItem('cobrinha-recorde') || 0; } catch (e) {}
recEl.textContent = rec;

function iniciar() {
  snake = [{x:10,y:10},{x:9,y:10},{x:8,y:10}];
  dir = nextDir = {x:1,y:0};
  pts = 0; delay = 130; ptsEl.textContent = 0;
  novaComida();
  rodando = true; pausado = false;
  ov.classList.add('hide');
  clearInterval(timer); timer = setInterval(passo, delay);
}

function novaComida() {
  do { food = {x:Math.floor(Math.random()*N), y:Math.floor(Math.random()*N)}; }
  while (snake.some(s => s.x === food.x && s.y === food.y));
}

function passo() {
  dir = nextDir;
  const h = {x:snake[0].x + dir.x, y:snake[0].y + dir.y};
  if (h.x < 0 || h.y < 0 || h.x >= N || h.y >= N || snake.some(s => s.x === h.x && s.y === h.y)) return fim();
  snake.unshift(h);
  if (h.x === food.x && h.y === food.y) {
    pts++; ptsEl.textContent = pts; novaComida();
    if (delay > 60) { delay -= 3; clearInterval(timer); timer = setInterval(passo, delay); }
  } else snake.pop();
  desenhar();
}

function fim() {
  clearInterval(timer); rodando = false;
  if (pts > rec) {
    rec = pts; recEl.textContent = rec;
    try { localStorage.setItem('cobrinha-recorde', rec); } catch (e) {}
  }
  msg.textContent = 'Fim de jogo! ' + pts + ' pontos';
  btn.textContent = 'Jogar de novo';
  ov.classList.remove('hide');
}

function desenhar() {
  ctx.clearRect(0, 0, cv.width, cv.height);
  ctx.fillStyle = '#ef4444';
  ctx.beginPath(); ctx.arc(food.x*S+S/2, food.y*S+S/2, S/2-3, 0, 7); ctx.fill();
  snake.forEach((s, i) => {
    ctx.fillStyle = i === 0 ? '#4ade80' : '#22c55e';
    ctx.beginPath(); ctx.roundRect(s.x*S+1, s.y*S+1, S-2, S-2, 6); ctx.fill();
  });
  const h = snake[0]; ctx.fillStyle = '#052e16';
  ctx.beginPath(); ctx.arc(h.x*S+S/2 + dir.x*4 - dir.y*5, h.y*S+S/2 + dir.y*4 + dir.x*5, 2.5, 0, 7); ctx.arc(h.x*S+S/2 + dir.x*4 + dir.y*5, h.y*S+S/2 + dir.y*4 - dir.x*5, 2.5, 0, 7); ctx.fill();
}

function mudar(x, y) {
  if (x === -dir.x && y === -dir.y) return; // não deixa voltar para trás
  nextDir = {x, y};
}

function pausar() {
  if (!rodando) return;
  pausado = !pausado;
  if (pausado) { clearInterval(timer); msg.textContent = 'Pausado'; btn.textContent = 'Continuar'; ov.classList.remove('hide'); }
  else { ov.classList.add('hide'); timer = setInterval(passo, delay); }
}

btn.onclick = () => pausado ? pausar() : iniciar();

document.addEventListener('keydown', e => {
  const k = e.key.toLowerCase();
  const m = {arrowup:[0,-1], w:[0,-1], arrowdown:[0,1], s:[0,1], arrowleft:[-1,0], a:[-1,0], arrowright:[1,0], d:[1,0]}[k];
  if (m) { e.preventDefault(); if (rodando && !pausado) mudar(...m); }
  else if (k === ' ') { e.preventDefault(); rodando ? pausar() : iniciar(); }
});

let t0;
cv.addEventListener('touchstart', e => { t0 = e.touches[0]; }, {passive:true});
cv.addEventListener('touchend', e => {
  if (!t0 || !rodando || pausado) return;
  const dx = e.changedTouches[0].clientX - t0.clientX, dy = e.changedTouches[0].clientY - t0.clientY;
  if (Math.max(Math.abs(dx), Math.abs(dy)) < 20) return;
  Math.abs(dx) > Math.abs(dy) ? mudar(dx > 0 ? 1 : -1, 0) : mudar(0, dy > 0 ? 1 : -1);
});
</script>
</body>
</html>