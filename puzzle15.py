import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="15Puzzle", layout="centered")

# Streamlitのヘッダー・フッター・余白を非表示にしてゲームを最大化
st.markdown("""
<style>
header[data-testid="stHeader"] { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
#MainMenu { display: none !important; }
footer { display: none !important; }
.block-container {
    padding-top: 0.2rem !important;
    padding-bottom: 0 !important;
    padding-left: 0.5rem !important;
    padding-right: 0.5rem !important;
}
.stMainBlockContainer { padding-top: 0.2rem !important; }
</style>
""", unsafe_allow_html=True)

components.html("""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  * { box-sizing: border-box; }
  body { margin: 0; background: #f0f0f0; display: flex; justify-content: center; }
  #app { font-family: Arial, sans-serif; text-align: center; padding: 2px 4px; width: 100%; max-width: 480px; }
  #title { font-size: clamp(16px, 4.6vw, 22px); font-weight: bold; margin: 0 0 2px; }
  #info { font-size: clamp(12px, 3.5vw, 17px); margin: 2px 0; font-weight: bold; }
  #board {
    position: relative;
    width: min(86vw, 400px);
    height: min(86vw, 400px);
    background: #8ab4d4;
    border-radius: 12px;
    display: inline-block;
    touch-action: none;
  }
  .tile {
    position: absolute;
    background: #ffffff;
    border-radius: 10px;
    border: 1px solid #c8d4e0;
    font-weight: 900;
    font-family: 'Georgia', serif;
    cursor: grab;
    display: flex; align-items: center; justify-content: center;
    user-select: none;
    transition: left 0.15s ease, top 0.15s ease;
    letter-spacing: -1px;
  }
  .tile::after {
    content: '';
    position: absolute;
    inset: 3px;
    border-radius: 7px;
    border: 1px solid rgba(200,210,220,0.6);
    pointer-events: none;
  }
  @keyframes hint-pulse {
    0%,100% { background: #ffffff; border-color: #c8d4e0; }
    50%      { background: #fff8e1; border-color: #f90;
               box-shadow: 0 0 14px 4px rgba(255,160,0,0.7); }
  }
  .tile.hint { animation: hint-pulse 0.6s ease-in-out 3; }
  .btns { margin: 4px 0; }
  button {
    font-size: clamp(11px, 3vw, 14px);
    padding: clamp(5px,1.5vw,7px) clamp(10px,3.5vw,18px);
    margin: 2px;
    border-radius: 8px; border: none; cursor: pointer;
    background: #4a90d9; color: white; font-weight: bold;
  }
  button:hover { background: #2a70b9; }
  #soundBtn { background: #5cb85c; }
  #soundBtn:hover { background: #3d8b3d; }
  #soundBtn.muted { background: #aaa; }
  #soundBtn.muted:hover { background: #888; }
  #msg { font-size: clamp(14px, 4vw, 20px); color: #c00; font-weight: bold; min-height: 22px; margin: 4px 0 6px; }
  .info-links {
    display: flex;
    justify-content: center;
    gap: 14px;
    margin: 2px 0 6px;
    font-size: clamp(11px, 3vw, 13px);
  }
  .info-link {
    padding: 2px 0;
    color: #2f6fa8;
    background: transparent;
    border: none;
    font: inherit;
    font-weight: bold;
    text-decoration: underline;
    cursor: pointer;
  }
  .info-link:hover { color: #174e7b; background: transparent; }
  #info-modal {
    display: none;
    position: fixed;
    inset: 0;
    align-items: center;
    justify-content: center;
    padding: 16px;
    background: rgba(0,0,0,0.42);
    z-index: 11000;
  }
  #info-modal.show { display: flex; }
  .modal-panel {
    width: min(92vw, 440px);
    max-height: min(82vh, 620px);
    overflow-y: auto;
    background: #ffffff;
    border: 3px solid #4a90d9;
    border-radius: 8px;
    box-shadow: 0 14px 32px rgba(0,0,0,0.28);
    text-align: left;
  }
  .modal-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    padding: 12px 14px 8px;
    border-bottom: 1px solid #d7e3ee;
  }
  #modal-title {
    margin: 0;
    color: #174e7b;
    font-size: clamp(18px, 5vw, 22px);
    line-height: 1.25;
  }
  .modal-close {
    width: 34px;
    height: 34px;
    flex: 0 0 auto;
    padding: 0;
    margin: 0;
    border-radius: 50%;
    background: #e8eef5;
    color: #174e7b;
    font-size: 22px;
    line-height: 1;
  }
  .modal-close:hover { background: #d4e2f0; color: #0f3858; }
  #modal-body {
    padding: 12px 16px 16px;
    color: #222;
    font-size: clamp(14px, 3.8vw, 16px);
    line-height: 1.7;
  }
  #modal-body p { margin: 0 0 10px; }
  #modal-body ol { margin: 0; padding-left: 1.35em; }
  #modal-body li { margin: 0 0 8px; }
  @media (max-width: 600px) {
    #app {
      padding-top: clamp(48px, 9vh, 78px);
    }
  }
  #confetti-canvas {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none;
    z-index: 9999;
  }
  #congrats-overlay {
    display: none;
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    justify-content: center;
    align-items: center;
    padding: 0 4vw;
    pointer-events: none;
    z-index: 10000;
  }
  #congrats-overlay.show { display: flex; }
  #congrats-text {
    font-family: 'Georgia', serif;
    position: relative;
    top: -3vh;
    width: 100%;
    text-align: center;
    font-size: clamp(32px, 10vw, 120px);
    line-height: 1.08;
    font-weight: 900;
    letter-spacing: 2px;
    color: #ffffff;
    -webkit-text-stroke: clamp(1px, 0.42vw, 4px) #ef3f3b;
    paint-order: stroke fill;
    text-shadow:
      3px 0 0 #ef3f3b,
      -3px 0 0 #ef3f3b,
      0 3px 0 #ef3f3b,
      0 -3px 0 #ef3f3b,
      2px 2px 0 #ef3f3b,
      -2px 2px 0 #ef3f3b,
      2px -2px 0 #ef3f3b,
      -2px -2px 0 #ef3f3b,
      5px 0 0 #f54c48,
      -5px 0 0 #f54c48,
      0 5px 0 #f54c48,
      0 -5px 0 #f54c48,
      4px 4px 0 #f54c48,
      -4px 4px 0 #f54c48,
      4px -4px 0 #f54c48,
      -4px -4px 0 #f54c48,
      0 8px 0 rgba(177,33,31,0.5);
    animation: congrats-pop 0.6s cubic-bezier(0.175,0.885,0.32,1.275) both,
               congrats-shine 2s 0.6s ease-in-out infinite alternate;
    filter: drop-shadow(0 5px 0 rgba(177,33,31,0.45));
  }
  @keyframes congrats-pop {
    0%   { transform: scale(0) rotate(-10deg); opacity: 0; }
    70%  { transform: scale(1.15) rotate(3deg); opacity: 1; }
    100% { transform: scale(1) rotate(0deg); opacity: 1; }
  }
  @keyframes congrats-shine {
    0%   { filter: drop-shadow(0 5px 0 rgba(177,33,31,0.45)); }
    100% { filter: drop-shadow(0 7px 0 rgba(177,33,31,0.6)); }
  }
  .congrats-icon {
    display: block;
    font-size: 1.15em;
    line-height: 1;
    margin-bottom: 0.34em;
  }
  .congrats-label {
    display: block;
  }
  @keyframes congrats-fade-out {
    0%   { opacity: 1; transform: scale(1); }
    100% { opacity: 0; transform: scale(0.8) translateY(-30px); }
  }
</style>
</head>
<body>
<div id="app">
  <div id="title">🔢15Puzzle</div>
  <div id="info">移動回数: 0</div>
  <div id="board"></div>
  <div class="btns">
    <button onclick="shuffleBoard()">🔀 シャッフル</button>
    <button onclick="resetBoard()">🔄 リセット</button>
    <button onclick="showHint()" id="hintBtn">💡 ヒント</button>
    <button onclick="toggleSound()" id="soundBtn">🔊 音ON</button>
  </div>
  <div id="msg"></div>
  <div class="info-links">
    <button class="info-link" onclick="openInfoModal('howto')">遊び方</button>
    <button class="info-link" onclick="openInfoModal('history')">15パズルの歴史的背景</button>
  </div>
</div>
<canvas id="confetti-canvas"></canvas>
<div id="congrats-overlay">
  <span id="congrats-text"><span class="congrats-icon">🎊</span><span class="congrats-label">クリアおめでとう</span></span>
</div>
<div id="info-modal" onclick="closeInfoModal(event)">
  <div class="modal-panel" role="dialog" aria-modal="true" aria-labelledby="modal-title" onclick="event.stopPropagation()">
    <div class="modal-head">
      <h2 id="modal-title"></h2>
      <button class="modal-close" onclick="closeInfoModal()" aria-label="閉じる">×</button>
    </div>
    <div id="modal-body"></div>
  </div>
</div>

<script>
const SIZE = 4;
const COLORS = {
  1:"#1356b4",2:"#1356b4",3:"#1356b4",4:"#1356b4",
  5:"#9c2fa0",6:"#9c2fa0",7:"#9c2fa0",8:"#9c2fa0",
  9:"#1a7a3c",10:"#1a7a3c",11:"#1a7a3c",12:"#1a7a3c",
  13:"#b71c1c",14:"#b71c1c",15:"#b71c1c"
};
const INFO_CONTENT = {
  howto: {
    title: '遊び方',
    body: `
      <ol>
        <li>「シャッフル」ボタンで盤面を混ぜます。</li>
        <li>空きマスに隣り合うタイルをタップ、クリック、またはスワイプして動かします。</li>
        <li>数字を1から15まで順番に並べ、空きマスを右下に戻すとクリアです。</li>
        <li>困ったときは「ヒント」ボタンで、次に動かすタイルを確認できます。</li>
      </ol>
    `
  },
  history: {
    title: '15パズルの歴史的背景',
    body: `
      <p>15パズルは、19世紀後半に広まった古典的なスライディングパズルです。4x4の盤面でタイルを動かし、1から15までを順番にそろえる遊びとして知られています。</p>
      <p>一般にはアメリカのパズル作家サム・ロイドの名前と結びつけられることがありますが、現在ではニューヨーク州カナストータの郵便局長だったノイズ・パーマー・チャップマンが初期の考案者として知られています。</p>
      <p>1880年ごろにはアメリカやヨーロッパで大流行しました。14と15のタイルだけを入れ替えた配置を解けるかどうかという話題も有名ですが、この配置は通常のルールでは解けません。そのため、15パズルは遊びとしてだけでなく、置換や偶奇性といった数学的な性質を考える題材にもなっています。</p>
    `
  }
};

let board = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0];
let moves = 0;
const tileEls = new Map();

function openInfoModal(type) {
  const content = INFO_CONTENT[type];
  if (!content) return;
  document.getElementById('modal-title').textContent = content.title;
  document.getElementById('modal-body').innerHTML = content.body;
  document.getElementById('info-modal').classList.add('show');
}

function closeInfoModal(event) {
  if (event && event.target && event.target.id !== 'info-modal') return;
  document.getElementById('info-modal').classList.remove('show');
}

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeInfoModal();
});

function getMetrics() {
  const boardEl = document.getElementById('board');
  const boardSize = boardEl.offsetWidth || 380;
  const PAD = Math.max(2, Math.round(boardSize * 0.007));
  const GAP = Math.max(1, Math.round(boardSize * 0.005));
  const TILE = Math.floor((boardSize - 2 * PAD - 3 * GAP) / 4);
  return { TILE, GAP, PAD };
}

function posToXY(pos) {
  const { TILE, GAP, PAD } = getMetrics();
  const r = Math.floor(pos / SIZE), c = pos % SIZE;
  return { left: PAD + c * (TILE + GAP), top: PAD + r * (TILE + GAP) };
}

function getNeighbors(pos) {
  const r = Math.floor(pos / SIZE), c = pos % SIZE, res = [];
  if (r > 0)      res.push(pos - SIZE);
  if (r < SIZE-1) res.push(pos + SIZE);
  if (c > 0)      res.push(pos - 1);
  if (c < SIZE-1) res.push(pos + 1);
  return res;
}

function applyTileSize(el) {
  const { TILE } = getMetrics();
  el.style.width  = TILE + 'px';
  el.style.height = TILE + 'px';
  el.style.fontSize = Math.round(TILE * 0.40) + 'px';
}

function initTiles() {
  const boardEl = document.getElementById('board');
  boardEl.innerHTML = '';
  tileEls.clear();
  board.forEach((val, pos) => {
    if (val === 0) return;
    const div = document.createElement('div');
    div.className = 'tile';
    div.textContent = val;
    div.style.color = COLORS[val];
    div.dataset.val = val;
    applyTileSize(div);
    const {left, top} = posToXY(pos);
    div.style.left = left + 'px';
    div.style.top  = top  + 'px';
    div.addEventListener('mousedown',  onPointerDown);
    div.addEventListener('touchstart', onPointerDown, {passive: false});
    boardEl.appendChild(div);
    tileEls.set(val, div);
  });
}

function updatePositions(animate = true) {
  if (!animate) tileEls.forEach(el => el.style.transition = 'none');
  board.forEach((val, pos) => {
    if (val === 0) return;
    const el = tileEls.get(val);
    const {left, top} = posToXY(pos);
    el.style.left = left + 'px';
    el.style.top  = top  + 'px';
  });
  if (!animate) {
    setTimeout(() => tileEls.forEach(el => el.style.transition = ''), 50);
  }
}

function refreshLayout() {
  tileEls.forEach(el => applyTileSize(el));
  updatePositions(false);
}

window.addEventListener('resize', refreshLayout);

let dragVal = null, dragStartX = 0, dragStartY = 0;

function onPointerDown(e) {
  e.preventDefault();
  const t = e.touches ? e.touches[0] : e;
  dragVal = parseInt(e.currentTarget.dataset.val);
  dragStartX = t.clientX;
  dragStartY = t.clientY;
}

function onPointerUp(e) {
  if (dragVal === null) return;
  const t = e.changedTouches ? e.changedTouches[0] : e;
  const dx = t.clientX - dragStartX;
  const dy = t.clientY - dragStartY;
  const pos   = board.indexOf(dragVal);
  const blank = board.indexOf(0);
  const tr = Math.floor(pos / SIZE),   tc = pos % SIZE;
  const br = Math.floor(blank / SIZE), bc = blank % SIZE;
  const rd = br - tr, cd = bc - tc;

  if (Math.abs(rd) + Math.abs(cd) === 1) {
    const th = 15;
    let go = (Math.abs(dx) < th && Math.abs(dy) < th);
    if (!go && Math.abs(dx) >= Math.abs(dy)) {
      if (cd ===  1 && dx >  th) go = true;
      if (cd === -1 && dx < -th) go = true;
    } else if (!go) {
      if (rd ===  1 && dy >  th) go = true;
      if (rd === -1 && dy < -th) go = true;
    }
    if (go) doMove(pos);
  }
  dragVal = null;
}

function doMove(pos) {
  const blank = board.indexOf(0);
  if (!getNeighbors(blank).includes(pos)) return;
  board[blank] = board[pos];
  board[pos] = 0;
  moves++;
  document.getElementById('info').textContent = `移動回数: ${moves}`;
  document.getElementById('msg').textContent = '';
  updatePositions(true);

  setTimeout(() => playClick(), 150);

  if (board.join(',') === '1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0') {
    setTimeout(() => {
      document.getElementById('msg').textContent = `🎉 クリア！ ${moves} 手で完成！`;
      launchConfetti();
    }, 1200);
  }
}

document.addEventListener('mouseup',     onPointerUp);
document.addEventListener('touchend',    onPointerUp, {passive: false});
document.addEventListener('touchcancel', () => { dragVal = null; });

function shuffleBoard() {
  board = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0];
  let blank = 15;
  for (let i = 0; i < 1000; i++) {
    const nb = getNeighbors(blank);
    const t = nb[Math.floor(Math.random() * nb.length)];
    [board[blank], board[t]] = [board[t], board[blank]];
    blank = t;
  }
  moves = 0;
  document.getElementById('info').textContent = '移動回数: 0';
  document.getElementById('msg').textContent = '';
  updatePositions(false);
}

function resetBoard() {
  board = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0];
  moves = 0;
  document.getElementById('info').textContent = '移動回数: 0';
  document.getElementById('msg').textContent = '';
  updatePositions(false);
}

function manhattan(b) {
  let d = 0;
  for (let i = 0; i < 16; i++) {
    const v = b[i];
    if (v === 0) continue;
    d += Math.abs(Math.floor(i/4) - Math.floor((v-1)/4))
       + Math.abs(i%4 - (v-1)%4);
  }
  return d;
}

function linearConflict(b) {
  let lc = 0;
  for (let r = 0; r < 4; r++) {
    for (let c1 = 0; c1 < 4; c1++) {
      const v1 = b[r*4+c1];
      if (v1 === 0 || Math.floor((v1-1)/4) !== r) continue;
      for (let c2 = c1+1; c2 < 4; c2++) {
        const v2 = b[r*4+c2];
        if (v2 === 0 || Math.floor((v2-1)/4) !== r) continue;
        if ((v1-1)%4 > (v2-1)%4) lc += 2;
      }
    }
  }
  for (let c = 0; c < 4; c++) {
    for (let r1 = 0; r1 < 4; r1++) {
      const v1 = b[r1*4+c];
      if (v1 === 0 || (v1-1)%4 !== c) continue;
      for (let r2 = r1+1; r2 < 4; r2++) {
        const v2 = b[r2*4+c];
        if (v2 === 0 || (v2-1)%4 !== c) continue;
        if (Math.floor((v1-1)/4) > Math.floor((v2-1)/4)) lc += 2;
      }
    }
  }
  return lc;
}

function heuristic(b) { return manhattan(b) + linearConflict(b); }

function solveHint() {
  if (heuristic(board) === 0) return { status: 'solved', tile: null };
  let nodeCount = 0;
  const MAX_NODES = 2000000;
  let firstTile = null;

  function search(b, blank, g, bound, prevBlank) {
    const h = heuristic(b);
    const f = g + h;
    if (f > bound) return f;
    if (h === 0) return -1;
    if (nodeCount++ > MAX_NODES) return Infinity;
    let min = Infinity;
    for (const next of getNeighbors(blank)) {
      if (next === prevBlank) continue;
      const tileVal = b[next];
      b[blank] = tileVal; b[next] = 0;
      const t = search(b, next, g + 1, bound, blank);
      b[next] = tileVal; b[blank] = 0;
      if (t === -1) {
        if (g === 0) firstTile = tileVal;
        return -1;
      }
      if (t < min) min = t;
    }
    return min;
  }

  let bound = heuristic(board);
  const b = board.slice();
  for (let iter = 0; iter < 100; iter++) {
    firstTile = null;
    nodeCount = 0;
    const t = search(b, b.indexOf(0), 0, bound, -1);
    if (t === -1) return { status: 'found', tile: firstTile };
    if (t === Infinity) return { status: 'timeout', tile: null };
    bound = t;
  }
  return { status: 'timeout', tile: null };
}

function showHint() {
  const btn = document.getElementById('hintBtn');
  btn.disabled = true;
  btn.textContent = '🔍 計算中...';
  document.getElementById('msg').textContent = '';

  setTimeout(() => {
    const result = solveHint();
    btn.disabled = false;
    btn.textContent = '💡 ヒント';
    if (result.status === 'solved') {
      document.getElementById('msg').textContent = '✅ すでに完成しています！';
      return;
    }
    if (result.status === 'timeout' || result.tile === null) {
      document.getElementById('msg').textContent = '⚠️ ヒントを計算できませんでした';
      return;
    }
    document.getElementById('msg').textContent = `💡 タイル「${result.tile}」を動かしてください`;
    const el = tileEls.get(result.tile);
    if (el) {
      el.classList.remove('hint');
      void el.offsetWidth;
      el.classList.add('hint');
      setTimeout(() => el.classList.remove('hint'), 2000);
    }
  }, 30);
}

initTiles();

let audioCtx = null;
let soundEnabled = true;

function toggleSound() {
  soundEnabled = !soundEnabled;
  const btn = document.getElementById('soundBtn');
  if (soundEnabled) {
    btn.textContent = '🔊 音ON';
    btn.classList.remove('muted');
  } else {
    btn.textContent = '🔇 音OFF';
    btn.classList.add('muted');
  }
}

function getAudioCtx() {
  if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  return audioCtx;
}

function playClick() {
  if (!soundEnabled) return;
  const ctx = getAudioCtx();
  const bufLen = Math.floor(ctx.sampleRate * 0.04);
  const buf = ctx.createBuffer(1, bufLen, ctx.sampleRate);
  const data = buf.getChannelData(0);
  for (let i = 0; i < bufLen; i++) {
    data[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / bufLen, 6);
  }
  const src = ctx.createBufferSource();
  src.buffer = buf;
  const hipass = ctx.createBiquadFilter();
  hipass.type = 'highpass';
  hipass.frequency.value = 3000;
  const gain = ctx.createGain();
  gain.gain.setValueAtTime(1.2, ctx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.04);
  src.connect(hipass); hipass.connect(gain); gain.connect(ctx.destination);
  src.start();
}

function playFanfare() {
  if (!soundEnabled) return;
  const ctx = getAudioCtx();
  const now = ctx.currentTime;

  const master = ctx.createGain();
  master.gain.setValueAtTime(0.75, now);
  master.gain.exponentialRampToValueAtTime(0.001, now + 3.0);
  master.connect(ctx.destination);

  function playTone(freq, start, duration, volume = 0.28) {
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(freq, start);
    osc.frequency.linearRampToValueAtTime(freq * 1.006, start + duration * 0.15);
    gain.gain.setValueAtTime(0.001, start);
    gain.gain.linearRampToValueAtTime(volume, start + 0.02);
    gain.gain.exponentialRampToValueAtTime(0.001, start + duration);
    osc.connect(gain); gain.connect(master);
    osc.start(start); osc.stop(start + duration + 0.03);
  }

  const notes = [
    [523.25, 0.00, 0.18, 0.34],
    [659.25, 0.24, 0.13, 0.30],
    [783.99, 0.39, 0.13, 0.30],
    [1046.50, 0.58, 0.50, 0.32],
  ];
  notes.forEach(([freq, start, duration, volume]) => {
    playTone(freq, now + start, duration, volume);
  });

  const chordStart = now + 0.62;
  [523.25, 659.25, 783.99, 1046.50].forEach((freq) => {
    playTone(freq, chordStart, 1.65, 0.20);
  });
}

function launchConfetti() {
  playFanfare();
  const canvas = document.getElementById('confetti-canvas');
  const ctx = canvas.getContext('2d');
  canvas.width  = window.innerWidth;
  canvas.height = window.innerHeight;

  const CCOLORS = ['#e74c3c','#3498db','#2ecc71','#f39c12','#9b59b6','#1abc9c','#e67e22','#e91e63'];
  const pieces = [];
  const COUNT = 160;

  for (let i = 0; i < COUNT; i++) {
    const angle = (Math.random() * Math.PI * 2);
    const speed = 2 + Math.random() * 5;
    pieces.push({
      x: canvas.width  * 0.5 + (Math.random() - 0.5) * 100,
      y: canvas.height * 0.4 + (Math.random() - 0.5) * 60,
      vx: Math.cos(angle) * speed,
      vy: Math.sin(angle) * speed - 4,
      rot: Math.random() * Math.PI * 2,
      rotV: (Math.random() - 0.5) * 0.15,
      w: 8 + Math.random() * 8,
      h: 4 + Math.random() * 5,
      color: CCOLORS[Math.floor(Math.random() * CCOLORS.length)],
      alpha: 1,
      shape: Math.random() < 0.4 ? 'circle' : 'rect',
    });
  }

  let frame;
  let congratsShown = false;
  const congratsTimer = setTimeout(() => {
    congratsShown = true;
    showCongrats();
  }, 2200);

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    let alive = false;
    for (const p of pieces) {
      p.x  += p.vx;
      p.y  += p.vy;
      p.vy += 0.12;
      p.vx *= 0.99;
      p.rot += p.rotV;
      p.alpha -= 0.005;
      if (p.alpha <= 0) continue;
      alive = true;
      ctx.save();
      ctx.globalAlpha = Math.max(0, p.alpha);
      ctx.translate(p.x, p.y);
      ctx.rotate(p.rot);
      ctx.fillStyle = p.color;
      if (p.shape === 'circle') {
        ctx.beginPath();
        ctx.arc(0, 0, p.w / 2, 0, Math.PI * 2);
        ctx.fill();
      } else {
        ctx.fillRect(-p.w/2, -p.h/2, p.w, p.h);
      }
      ctx.restore();
    }
    if (alive) {
      frame = requestAnimationFrame(draw);
    } else {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      if (!congratsShown) {
        clearTimeout(congratsTimer);
        congratsShown = true;
        showCongrats();
      }
    }
  }
  if (frame) cancelAnimationFrame(frame);
  draw();
}

function showCongrats() {
  const overlay = document.getElementById('congrats-overlay');
  const text    = document.getElementById('congrats-text');
  text.style.animation = 'none';
  void text.offsetWidth;
  text.style.animation = '';
  overlay.classList.add('show');
  setTimeout(() => {
    text.style.animation = 'congrats-fade-out 0.8s ease-in forwards';
    setTimeout(() => overlay.classList.remove('show'), 800);
  }, 3000);
}
</script>
</body>
</html>
""", height=660)
