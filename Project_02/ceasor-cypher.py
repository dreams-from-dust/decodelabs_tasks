import http.server, socketserver, json

PORT = 8002

# ── Core Cryptographic Logic ────────────────────────────────
def caesar_encrypt(plaintext: str, shift: int) -> str:
    """Shift each letter forward by `shift` positions (mod 26)."""
    result = []
    for char in plaintext:
        if char.isupper():
            result.append(chr((ord(char) - 65 + shift) % 26 + 65))
        elif char.islower():
            result.append(chr((ord(char) - 97 + shift) % 26 + 97))
        else:
            result.append(char)
    return ''.join(result)

def caesar_decrypt(ciphertext: str, shift: int) -> str:
    """Reverse the shift , same function, negative direction."""
    return caesar_encrypt(ciphertext, -shift)

# ── HTML ─────────────────────────────────────────────────────
HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Caesar Cipher , Encrypt & Decrypt</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/remixicon/4.2.0/remixicon.min.css">
<style>
/* ── Reset ─────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; font-size: 16px; }
body {
  font-family: 'Poppins', sans-serif;
  background: #F0F4FA;
  color: #0A1628;
  min-height: 100vh;
  overflow-x: hidden;
}

/* ── Tokens ─────────────────────────────────────────────────── */
:root {
  --blue:     #1A4FBF;
  --blue-d:   #0E2E7A;
  --blue-m:   #2563EB;
  --blue-l:   #5B9BF5;
  --blue-xl:  #93BFFF;
  --bg:       #F0F4FA;
  --bg-pale:  #FAFBFF;
  --white:    #FFFFFF;
  --ink:      #0A1628;
  --ink-mid:  #334560;
  --ink-faint:#6B80A0;
  --border:   #D4DEF0;
  --gray-100: #EEF2FA;
  --radius-lg:20px;
  --radius-md:12px;
  --radius-sm:8px;
  --shadow-sm:0 2px 8px rgba(26,79,191,0.07);
  --shadow-md:0 8px 28px rgba(26,79,191,0.13);
  --trans:    0.28s cubic-bezier(0.4, 0, 0.2, 1);
}

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--blue-l); border-radius: 10px; }

/* ── Hero ─────────────────────────────────────────────────── */
.hero {
  position: relative;
  min-height: 100vh;
  background: #0B1E42;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  padding: 80px 24px 60px;
  overflow: hidden;
}

.content-section.alt .vi-title { color: var(--ink); }
.content-section.alt .vi-desc { color: var(--ink-mid); }
.content-section.alt .vuln-item { background: rgba(26, 79, 191, 0.05); border-color: var(--border); }

/* circuit-dot grid */
.hero::before {
  content:''; position:absolute; inset:0;
  background-image: radial-gradient(circle, rgba(91,155,245,0.08) 1px, transparent 1px);
  background-size: 36px 36px;
  pointer-events: none;
}

.orb {
  position:absolute; border-radius:50%;
  pointer-events:none; filter:blur(90px);
}
.orb-a {
  width:500px; height:500px;
  background:rgba(26,79,191,0.35);
  top:-140px; right:-100px;
  animation: drift 12s ease-in-out infinite;
}
.orb-b {
  width:360px; height:360px;
  background:rgba(37,99,235,0.22);
  bottom:-90px; left:-70px;
  animation: drift 15s ease-in-out infinite reverse;
}
.orb-c {
  width:240px; height:240px;
  background:rgba(91,155,245,0.15);
  top:45%; left:35%;
  animation: drift 9s ease-in-out infinite 2s;
}
@keyframes drift {
  0%,100%{transform:translate(0,0) scale(1);}
  50%{transform:translate(22px,-28px) scale(1.06);}
}


.live-dot {
  width:6px; height:6px; border-radius:50%;
  background:#34D399;
  animation:pulseAnim 1.6s infinite;
}
@keyframes pulseAnim { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.4;transform:scale(1.5)} }

.hero-title {
  position:relative;
  font-size:clamp(5rem, 10vw, 10rem);
  font-weight:800; line-height:1.06;
  letter-spacing:-0.04em; text-align:center;
  color:var(--white); margin-bottom:48px;
  animation:riseIn 0.7s 0.1s ease both;
}
.hero-title em {
  font-style:normal;
  background:linear-gradient(120deg, var(--blue-l), var(--blue-xl));
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
  background-clip:text;
}

.hero-lead {
  position:relative;
  font-size:2rem; font-weight:300; line-height:2;
  color:rgba(255,255,255,0.42); text-align:center;
  max-width:700px; margin-bottom:78px;
  animation:riseIn 0.7s 0.18s ease both;
}

@keyframes riseIn {
  from{opacity:0;transform:translateY(22px);}
  to{opacity:1;transform:translateY(0);}
}

/* ── Tool Panel ─────────────────────────────────────────── */
.panel {
  position:relative;
  width:100%; max-width:620px;
  background:rgba(255,255,255,0.045);
  border:1px solid rgba(91,155,245,0.16);
  border-radius:var(--radius-lg);
  padding:36px 32px;
  backdrop-filter:blur(28px);
  animation:riseIn 0.8s 0.25s ease both;
}

/* Mode tabs */
.mode-tabs {
  display:flex;
  background:rgba(0,0,0,0.25);
  border:1px solid rgba(255,255,255,0.07);
  border-radius:var(--radius-md); padding:4px; gap:4px;
  margin-bottom:30px;
}
.tab-btn {
  flex:1; padding:10px 16px;
  border:none; border-radius:9px;
  font-family:'Poppins',sans-serif; font-size:0.84rem; font-weight:600;
  cursor:pointer; transition:all var(--trans);
  background:transparent; color:rgba(255,255,255,0.32);
  letter-spacing:0.01em;
  display:flex; align-items:center; justify-content:center; gap:7px;
}
.tab-btn.active {
  background:var(--blue-m);
  color:var(--white);
  box-shadow:0 2px 14px rgba(37,99,235,0.45);
}

.field-label {
  font-size:0.68rem; font-weight:600;
  letter-spacing:0.15em; text-transform:uppercase;
  color:rgba(255,255,255,0.32); margin-bottom:9px; display:block;
}

.cipher-ta {
  width:100%;
  background:rgba(0,0,0,0.25);
  border:1.5px solid rgba(255,255,255,0.07);
  border-radius:var(--radius-md);
  padding:15px 16px;
  font-family:'Inter', monospace; font-size:0.97rem;
  color:var(--white); outline:none; resize:none;
  line-height:1.65; transition:border-color var(--trans), box-shadow var(--trans);
  margin-bottom:22px;
}
.cipher-ta::placeholder { color:rgba(255,255,255,0.18); }
.cipher-ta:focus {
  border-color:var(--blue-l);
  box-shadow:0 0 0 3px rgba(91,155,245,0.16);
}

/* shift slider */
.slider-section { margin-bottom:24px; }
.slider-header {
  display:flex; justify-content:space-between; align-items:center;
  margin-bottom:11px;
}
.slider-header span {
  font-size:0.7rem; font-weight:600;
  letter-spacing:0.15em; text-transform:uppercase;
  color:rgba(255,255,255,0.32);
}
.shift-pill {
  background:rgba(37,99,235,0.22);
  border:1px solid rgba(91,155,245,0.3);
  border-radius:7px; padding:3px 12px;
  font-family:'Inter', monospace; font-size:0.9rem; font-weight:700;
  color:var(--blue-xl); transition:color var(--trans);
}

input[type=range] {
  width:100%; height:4px; border-radius:100px;
  background:rgba(255,255,255,0.08);
  appearance:none; outline:none; cursor:pointer;
  accent-color:var(--blue-m);
}
input[type=range]::-webkit-slider-thumb {
  appearance:none; width:18px; height:18px; border-radius:50%;
  background:var(--blue-m); border:3px solid var(--blue-xl);
  box-shadow:0 0 12px rgba(37,99,235,0.55); cursor:pointer;
}
.slider-ticks {
  display:flex; justify-content:space-between; margin-top:6px;
  font-family:'Inter', monospace; font-size:0.65rem;
  color:rgba(255,255,255,0.2);
}

/* output */
.output-wrap { position:relative; }
.output-box {
  width:100%;
  background:rgba(37,99,235,0.08);
  border:1.5px solid rgba(91,155,245,0.18);
  border-radius:var(--radius-md);
  padding:15px 50px 15px 16px;
  font-family:'Inter', monospace; font-size:0.97rem;
  color:var(--blue-xl); min-height:76px;
  word-break:break-all; line-height:1.65;
}
.copy-btn {
  position:absolute; right:12px; top:12px;
  background:rgba(91,155,245,0.14);
  border:1px solid rgba(91,155,245,0.22);
  border-radius:7px; padding:5px 10px;
  font-size:0.72rem; font-weight:600;
  color:var(--blue-xl); cursor:pointer;
  transition:background var(--trans);
  display:flex; align-items:center; gap:5px;
}
.copy-btn:hover { background:rgba(91,155,245,0.25); }

/* formula strip */
.formula-strip {
  display:flex; align-items:center; gap:10px; flex-wrap:wrap;
  margin-top:18px; padding:11px 15px;
  background:rgba(0,0,0,0.2); border-radius:9px;
  font-family:'Inter', monospace; font-size:0.8rem;
  color:rgba(255,255,255,0.3);
}
.formula-strip .fk { color:var(--blue-xl); font-weight:700; }
.formula-strip .fe { margin-left:auto; font-size:0.72rem; opacity:0.6; }

/* scroll hint */
.scroll-hint {
  position:relative; margin-top:44px;
  display:flex; flex-direction:column; align-items:center; gap:7px;
  animation:riseIn 1s 0.55s ease both; cursor:pointer; user-select:none;
}
.scroll-hint span {
  font-size:0.65rem; letter-spacing:0.2em; text-transform:uppercase;
  color:rgba(255,255,255,0.2);
}
.scroll-arrow {
  width:30px; height:30px;
  border:1.5px solid rgba(91,155,245,0.2); border-radius:50%;
  display:flex; align-items:center; justify-content:center;
  color:rgba(91,155,245,0.35); font-size:0.9rem;
  animation:bob 2.2s ease-in-out infinite;
}
@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(7px)}}

/* ── Light sections ─────────────────────────────────────── */
.content-section { padding:80px 24px; }
.content-section.alt { background:var(--bg-pale); }
.content-section.dark { background:#0B1E42; padding:72px 24px; }

.sec-eyebrow {
  font-size:0.68rem; font-weight:700;
  letter-spacing:0.2em; text-transform:uppercase;
  color:var(--blue); margin-bottom:10px; text-align:center;
}
.dark .sec-eyebrow { color:rgba(91,155,245,0.7); }

.sec-title {
  font-size:clamp(1.75rem, 3.8vw, 2.6rem);
  font-weight:800; letter-spacing:-0.03em;
  color:var(--blue-d); margin-bottom:10px;
  text-align:center; line-height:1.15;
}
.dark .sec-title { color:var(--white); }

.sec-sub {
  font-size:0.93rem; font-weight:300; line-height:1.8;
  color:var(--ink-faint); text-align:center;
  max-width:480px; margin:0 auto 52px;
}
.dark .sec-sub { color:rgba(255,255,255,0.36); }

/* IPO flow */
.ipo-flow {
  display:flex; align-items:stretch; justify-content:center;
  gap:0; flex-wrap:wrap; max-width:860px; margin:0 auto;
}
.ipo-block {
  flex:1; min-width:200px;
  background:var(--white); border:1.5px solid var(--border);
  border-radius:var(--radius-lg); padding:30px 24px;
  text-align:center;
  transition:transform var(--trans), box-shadow var(--trans), border-color var(--trans);
  opacity:0; transform:translateY(16px);
  transition:opacity 0.5s ease, transform 0.5s ease, box-shadow 0.28s, border-color 0.28s;
}
.ipo-block.visible { opacity:1; transform:translateY(0); }
.ipo-block:hover {
  transform:translateY(-4px) !important;
  box-shadow:var(--shadow-md); border-color:rgba(26,79,191,0.28);
}
.ipo-ico {
  width:54px; height:54px; border-radius:15px;
  background:var(--gray-100);
  display:flex; align-items:center; justify-content:center;
  margin:0 auto 16px; font-size:1.4rem; color:var(--blue);
}
.ipo-label {
  font-size:0.65rem; font-weight:700; letter-spacing:0.18em;
  text-transform:uppercase; color:var(--blue-m); margin-bottom:6px;
}
.ipo-name  { font-size:1rem; font-weight:700; color:var(--blue-d); margin-bottom:8px; }
.ipo-desc  { font-size:0.82rem; color:var(--ink-faint); line-height:1.65; }

.ipo-arrow {
  display:flex; align-items:center; padding:0 10px;
  color:var(--blue-l); font-size:1.6rem; flex-shrink:0;
  animation:arrowPulse 2s ease-in-out infinite;
}
@keyframes arrowPulse{0%,100%{opacity:0.4;transform:scaleX(1)}50%{opacity:1;transform:scaleX(1.18)}}

/* Alphabet visual */
.alpha-card {
  max-width:820px; margin:0 auto;
  background:var(--white); border:1.5px solid var(--border);
  border-radius:var(--radius-lg); padding:36px 32px;
}
.alpha-row-label {
  font-size:0.65rem; font-weight:700; letter-spacing:0.18em;
  text-transform:uppercase; color:var(--ink-faint); margin-bottom:10px;
}
.alpha-row {
  display:flex; flex-wrap:wrap; gap:5px; margin-bottom:14px;
}
.al {
  width:36px; height:36px; border-radius:7px;
  display:flex; align-items:center; justify-content:center;
  font-family:'Inter', monospace; font-size:0.82rem; font-weight:700;
  background:var(--gray-100); color:var(--ink-mid);
  border:1.5px solid var(--border); cursor:pointer;
  transition:all 0.22s;
}
.al:hover { border-color:var(--blue-l); color:var(--blue); }
.al.plain-hi {
  background:var(--gray-100); color:var(--blue-m);
  border-color:var(--blue-m); transform:translateY(-2px);
  box-shadow:0 4px 12px rgba(26,79,191,0.18);
}
.al.cipher-hi {
  background:var(--blue-m); color:var(--white);
  border-color:var(--blue-d); transform:translateY(-2px);
  box-shadow:0 4px 16px rgba(37,99,235,0.4);
}
.alpha-connector {
  display:flex; align-items:center; gap:10px;
  font-size:0.82rem; font-weight:600; color:var(--ink-mid);
  font-family:'Inter', monospace; margin:14px 0;
}
.alpha-connector i { color:var(--blue-m); font-size:1rem; }
.alpha-formula-box {
  background:var(--gray-100); border:1.5px solid var(--border);
  border-radius:10px; padding:12px 16px;
  font-family:'Inter', monospace; font-size:0.84rem;
  color:var(--ink); text-align:center; margin-top:16px;
}
.alpha-formula-box .fk { color:var(--blue-m); font-weight:700; }
.alpha-formula-box .fv { color:#0D9E60; font-weight:700; }

/* concept cards */
.cards {
  display:grid;
  grid-template-columns:repeat(auto-fit, minmax(252px, 1fr));
  gap:18px; max-width:980px; margin:0 auto;
}
.card {
  background:var(--white); border:1.5px solid var(--border);
  border-radius:var(--radius-lg); padding:30px 26px;
  position:relative; overflow:hidden;
  opacity:0; transform:translateY(20px);
  transition:opacity 0.5s ease, transform 0.5s ease, box-shadow 0.28s, border-color 0.28s;
}
.card.visible { opacity:1; transform:translateY(0); }
.card:hover {
  transform:translateY(-5px) !important;
  box-shadow:var(--shadow-md); border-color:rgba(26,79,191,0.22);
}
.card::after {
  content:''; position:absolute; bottom:0; left:0; right:0; height:3px;
  background:linear-gradient(90deg, var(--blue), var(--blue-l));
  transform:scaleX(0); transform-origin:left; transition:transform 0.4s;
}
.card:hover::after { transform:scaleX(1); }
.card-ico {
  width:46px; height:46px; border-radius:13px;
  background:var(--gray-100);
  display:flex; align-items:center; justify-content:center;
  margin-bottom:18px; font-size:1.2rem; color:var(--blue);
}
.card-heading { font-size:0.97rem; font-weight:700; color:var(--blue-d); margin-bottom:9px; }
.card-body {
  font-size:0.84rem; line-height:1.78; color:var(--ink-mid); font-weight:400;
}
.card-body code {
  font-family:'Inter',monospace; font-size:0.78rem;
  background:var(--gray-100); color:var(--blue); padding:1px 6px; border-radius:5px;
}

/* dark steps */
.steps { max-width:660px; margin:0 auto; position:relative; }
.steps::before {
  content:''; position:absolute; left:23px; top:0; bottom:0; width:1px;
  background:linear-gradient(to bottom, transparent, rgba(91,155,245,0.4), transparent);
}
.step {
  display:flex; gap:22px; padding:20px 0;
  opacity:0; transform:translateX(-18px);
  transition:opacity 0.5s ease, transform 0.5s ease;
}
.step.visible { opacity:1; transform:translateX(0); }
.step-num {
  width:46px; height:46px; flex-shrink:0; border-radius:50%;
  background:#0B1E42; border:1.5px solid var(--blue-l);
  display:flex; align-items:center; justify-content:center;
  font-family:'Inter', monospace; font-size:0.78rem; font-weight:700;
  color:var(--blue-l); position:relative; z-index:1;
}
.step-body .step-heading { font-size:0.95rem; font-weight:700; color:var(--white); margin-bottom:5px; }
.step-body .step-text { font-size:0.83rem; font-weight:300; color:rgba(255,255,255,0.4); line-height:1.75; }
.step-body code {
  font-family:'Inter',monospace; font-size:0.76rem;
  background:rgba(91,155,245,0.16); color:var(--blue-xl);
  padding:1px 7px; border-radius:5px;
}

/* vuln awareness */
.vuln-row {
  display:flex; flex-wrap:wrap; gap:16px;
  justify-content:center; max-width:720px; margin:0 auto;
}
.vuln-item {
  flex:1; min-width:240px;
  display:flex; align-items:flex-start; gap:14px;
  background:rgba(255,255,255,0.04);
  border:1px solid rgba(91,155,245,0.14);
  border-radius:var(--radius-lg); padding:22px;
  opacity:0; transform:translateY(18px);
  transition:opacity 0.5s ease, transform 0.5s ease;
}
.vuln-item.visible { opacity:1; transform:translateY(0); }
.vi-ico {
  width:40px; height:40px; flex-shrink:0; border-radius:10px;
  background:rgba(91,155,245,0.1);
  display:flex; align-items:center; justify-content:center;
  font-size:1.1rem; color:var(--blue-xl); margin-top:2px;
}
.vi-title { font-size:0.9rem; font-weight:700; color:var(--white); margin-bottom:5px; }
.vi-desc  { font-size:0.82rem; color: #e0e0e0; line-height:1.65; }

footer {
  background:#060E1F; padding:26px 24px; text-align:center;
  border-top:1px solid rgba(91,155,245,0.08);
}
footer p { font-size:0.78rem; color:rgba(255,255,255,0.22); }
</style>
</head>
<body>

<section class="hero">
  <div class="orb orb-a"></div>
  <div class="orb orb-b"></div>
  <div class="orb orb-c"></div>


  <h1 class="hero-title">Caesar<br><em>Cipher</em></h1>
  <p class="hero-lead">Shift every letter by a fixed key to hide your message, then shift it back to reveal it.</p>

  <div class="panel">

    <div class="mode-tabs">
      <button class="tab-btn active" id="tab-enc" onclick="setMode('encrypt')">
        <i class="ri-lock-line"></i> Encrypt
      </button>
      <button class="tab-btn" id="tab-dec" onclick="setMode('decrypt')">
        <i class="ri-lock-unlock-line"></i> Decrypt
      </button>
    </div>

    <label class="field-label" id="in-label">Plain text , what you want to hide</label>
    <textarea class="cipher-ta" id="input-ta" rows="3"
              placeholder="Type your message here…"
              oninput="processText()" spellcheck="false"></textarea>

    <div class="slider-section">
      <div class="slider-header">
        <span>Shift key (n)</span>
        <div class="shift-pill" id="shift-pill">3</div>
      </div>
      <input type="range" id="slider" min="1" max="25" value="3" oninput="onSlide()">
      <div class="slider-ticks"><span>1</span><span>13 , ROT13</span><span>25</span></div>
    </div>

    <label class="field-label" id="out-label">Cipher text , the encrypted result</label>
    <div class="output-wrap">
      <div class="output-box" id="output-box">Output appears here…</div>
      <button class="copy-btn" onclick="doCopy()">
        <i class="ri-clipboard-line"></i> Copy
      </button>
    </div>

    <div class="formula-strip">
      <span>Formula:</span>
      <span>E<sub>n</sub>(x) = (x + <span class="fk" id="fn">3</span>) mod 26</span>
      <span class="fe" id="fe">A → D</span>
    </div>
  </div>

  <div class="scroll-hint" onclick="document.querySelector('.ipo-section').scrollIntoView({behavior:'smooth'})">
    <span>See how it works</span>
    <div class="scroll-arrow"><i class="ri-arrow-down-s-line"></i></div>
  </div>
</section>

<section class="content-section ipo-section">
  <p class="sec-eyebrow">The structure</p>
  <h2 class="sec-title">Input , Process , Output</h2>
  <p class="sec-sub">Every cryptographic system follows this three-stage model. Your program is the middle stage.</p>

  <div class="ipo-flow" id="ipo-flow">
    <div class="ipo-block">
      <div class="ipo-ico"><i class="ri-file-text-line"></i></div>
      <div class="ipo-label">Input</div>
      <div class="ipo-name">Plain Text</div>
      <div class="ipo-desc">The readable message the user wants to protect. Also called cleartext.</div>
    </div>
    <div class="ipo-arrow"><i class="ri-arrow-right-line"></i></div>
    <div class="ipo-block">
      <div class="ipo-ico"><i class="ri-settings-3-line"></i></div>
      <div class="ipo-label">Process</div>
      <div class="ipo-name">Algorithm + Key</div>
      <div class="ipo-desc">The Caesar shift formula applied to every letter, using <code style="font-family:Inter,monospace;font-size:0.76rem;background:#EEF2FA;color:#1A4FBF;padding:1px 5px;border-radius:4px">ord()</code>, <code style="font-family:Inter,monospace;font-size:0.76rem;background:#EEF2FA;color:#1A4FBF;padding:1px 5px;border-radius:4px">% 26</code>, and <code style="font-family:Inter,monospace;font-size:0.76rem;background:#EEF2FA;color:#1A4FBF;padding:1px 5px;border-radius:4px">chr()</code>.</div>
    </div>
    <div class="ipo-arrow"><i class="ri-arrow-right-line"></i></div>
    <div class="ipo-block">
      <div class="ipo-ico"><i class="ri-lock-2-line"></i></div>
      <div class="ipo-label">Output</div>
      <div class="ipo-name">Cipher Text</div>
      <div class="ipo-desc">The scrambled result. Unreadable to anyone who does not know the shift key.</div>
    </div>
  </div>
</section>

<section class="content-section alt">
  <p class="sec-eyebrow">Visual walkthrough</p>
  <h2 class="sec-title">The shift in action</h2>
  <p class="sec-sub">Select any letter in the top row to see exactly which cipher letter it maps to , and the arithmetic behind it.</p>

  <div class="alpha-card">
    <div class="alpha-row-label">Plain text , A to Z</div>
    <div class="alpha-row" id="plain-row"></div>
    <div class="alpha-connector">
      <i class="ri-arrow-right-circle-line"></i>
      <span>Each letter shifts forward by</span>
      <strong id="demo-shift" style="color:#1A4FBF">3 positions</strong>
      <i class="ri-arrow-right-circle-line"></i>
    </div>
    <div class="alpha-row-label">Cipher text , shifted result</div>
    <div class="alpha-row" id="cipher-row"></div>
    <div class="alpha-formula-box" id="alpha-formula">
      Select a letter above to see the calculation
    </div>
  </div>
</section>

<section class="content-section">
  <p class="sec-eyebrow">What to implement</p>
  <h2 class="sec-title">The six things your code does</h2>
  <p class="sec-sub">Each step teaches a real idea in cryptography, not just Python syntax.</p>

  <div class="cards" id="cards-main">
    <div class="card">
      <div class="card-ico"><i class="ri-numbers-line"></i></div>
      <h3 class="card-heading">Text becomes numbers , <code>ord()</code></h3>
      <p class="card-body">You cannot do arithmetic on letters. <code>ord('A')</code> returns 65 , the ASCII number for that character. Subtracting the base (65 for uppercase, 97 for lowercase) maps it to a 0–25 range.</p>
    </div>
    <div class="card">
      <div class="card-ico"><i class="ri-add-circle-line"></i></div>
      <h3 class="card-heading">The shift addition</h3>
      <p class="card-body">Add the key <em>n</em> to the 0-based index. A (index 0) with shift 3 gives 3. Convert back and you get D. The encryption is literally one addition per character.</p>
    </div>
    <div class="card">
      <div class="card-ico"><i class="ri-loop-left-line"></i></div>
      <h3 class="card-heading">Wrap-around , modulo 26</h3>
      <p class="card-body">The alphabet is circular. Z shifted by 3 should give C, not an undefined character. <code>% 26</code> keeps the result inside 0–25 automatically, no if-statements needed.</p>
    </div>
    <div class="card">
      <div class="card-ico"><i class="ri-text"></i></div>
      <h3 class="card-heading">Numbers back to text , <code>chr()</code></h3>
      <p class="card-body">After the math, add the base back and call <code>chr()</code>. <code>chr(68)</code> gives <code>'D'</code>. That's your cipher character, ready to append to the result string.</p>
    </div>
    <div class="card">
      <div class="card-ico"><i class="ri-arrow-go-back-line"></i></div>
      <h3 class="card-heading">Decrypt = negative shift</h3>
      <p class="card-body">Decryption uses the exact same function , just pass <code>-n</code> as the shift. This is symmetric encryption: the same key that locks the message also unlocks it.</p>
    </div>
    <div class="card">
      <div class="card-ico"><i class="ri-space"></i></div>
      <h3 class="card-heading">Leave non-letters unchanged</h3>
      <p class="card-body">Spaces, digits, and punctuation are not shifted. Check <code>char.isalpha()</code> before applying the formula. Everything else passes straight through to the output.</p>
    </div>
  </div>
</section>

<section class="content-section dark" id="steps-section">
  <p class="sec-eyebrow">Step by step</p>
  <h2 class="sec-title">How the code runs</h2>
  <p class="sec-sub">The exact sequence your Python program follows for every character it processes.</p>

  <div class="steps" id="steps-list">
    <div class="step">
      <div class="step-num">01</div>
      <div class="step-body">
        <div class="step-heading">Read the character</div>
        <div class="step-text">Loop through every character in the input string. Python strings are sequences , you can iterate directly with <code>for char in text</code>.</div>
      </div>
    </div>
    <div class="step">
      <div class="step-num">02</div>
      <div class="step-body">
        <div class="step-heading">Check if it is a letter</div>
        <div class="step-text"><code>char.isalpha()</code> returns True for letters only. If it returns False, append the character unchanged and move to the next one.</div>
      </div>
    </div>
    <div class="step">
      <div class="step-num">03</div>
      <div class="step-body">
        <div class="step-heading">Determine the base</div>
        <div class="step-text">Use <code>65</code> if the character is uppercase (<code>char.isupper()</code>), or <code>97</code> if it is lowercase. This keeps the two cases separate.</div>
      </div>
    </div>
    <div class="step">
      <div class="step-num">04</div>
      <div class="step-body">
        <div class="step-heading">Apply the formula</div>
        <div class="step-text"><code>chr((ord(char) - base + shift) % 26 + base)</code> , subtract the base, add the shift, mod 26, add the base back, convert to character. One line.</div>
      </div>
    </div>
    <div class="step">
      <div class="step-num">05</div>
      <div class="step-body">
        <div class="step-heading">Build and return the result</div>
        <div class="step-text">Append each processed character to a result list, then <code>''.join(result)</code> at the end. Joining a list is faster than string concatenation in a loop.</div>
      </div>
    </div>
  </div>
</section>

<section class="content-section alt" id="vuln-section">
  <p class="sec-eyebrow">Security awareness</p>
  <h2 class="sec-title">Why this cipher is not secure</h2>
  <p class="sec-sub">Knowing the limits of what you build is part of understanding how it works.</p>

  <div class="vuln-row" id="vuln-row">
    <div class="vuln-item">
      <div class="vi-ico"><i class="ri-key-2-line"></i></div>
      <div>
        <div class="vi-title">Only 25 possible keys</div>
        <div class="vi-desc">An attacker can try every shift value from 1 to 25 in seconds , no computer needed. This is called a brute-force attack, and a tiny key space makes it trivial.</div>
      </div>
    </div>
    <div class="vuln-item">
      <div class="vi-ico"><i class="ri-bar-chart-grouped-line"></i></div>
      <div>
        <div class="vi-title">Frequency analysis</div>
        <div class="vi-desc">In English text, 'E' appears about 13% of the time. A Caesar cipher preserves that pattern. Whoever gets the ciphertext can find the key by counting which letter appears most often.</div>
      </div>
    </div>
    <div class="vuln-item">
      <div class="vi-ico"><i class="ri-shield-star-line"></i></div>
      <div>
        <div class="vi-title">The path forward , AES</div>
        <div class="vi-desc">Modern AES encryption uses 128-bit keys , 2¹²⁸ possibilities , combined with multiple rounds of substitution and permutation. Caesar is the foundation; AES is what production systems use.</div>
      </div>
    </div>
  </div>
</section>

<footer>
  <p>Caesar Cipher &mdash; Encryption &amp; Decryption</p>
</footer>

<script>
// ── State ───────────────────────────────────────────────────
const ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
let mode  = 'encrypt';
let shift = 3;

// ── Cipher functions (mirror Python) ───────────────────────
function shiftChar(ch, n) {
  if (ch >= 'A' && ch <= 'Z') return String.fromCharCode(((ch.charCodeAt(0)-65+n+26)%26)+65);
  if (ch >= 'a' && ch <= 'z') return String.fromCharCode(((ch.charCodeAt(0)-97+n+26)%26)+97);
  return ch;
}
function applyShift(text, n) { return text.split('').map(c => shiftChar(c, n)).join(''); }

// ── Mode toggle ──────────────────────────────────────────────
function setMode(m) {
  mode = m;
  const enc = m === 'encrypt';
  document.getElementById('tab-enc').className = 'tab-btn' + (enc ? ' active' : '');
  document.getElementById('tab-dec').className = 'tab-btn' + (!enc ? ' active' : '');
  document.getElementById('in-label').textContent  = enc ? 'Plain text , what you want to hide' : 'Cipher text , paste to decrypt';
  document.getElementById('out-label').textContent = enc ? 'Cipher text , the encrypted result'  : 'Plain text , the decrypted result';
  document.getElementById('input-ta').placeholder  = enc ? 'Type your message here…' : 'Paste encrypted text here…';
  processText();
}

// ── Slider ──────────────────────────────────────────────────
function onSlide() {
  shift = parseInt(document.getElementById('slider').value);
  document.getElementById('shift-pill').textContent = shift;
  document.getElementById('demo-shift').textContent = shift + ' position' + (shift !== 1 ? 's' : '');
  updateCipherRow();
  processText();
  updateFormula();
}

// ── Process text ─────────────────────────────────────────────
function processText() {
  const text  = document.getElementById('input-ta').value;
  const n     = mode === 'encrypt' ? shift : -shift;
  const out   = text ? applyShift(text, n) : '';
  const box   = document.getElementById('output-box');
  box.textContent = out || 'Output appears here…';
  updateFormula();
}

// ── Formula strip ─────────────────────────────────────────────
function updateFormula() {
  const n   = shift;
  const enc = mode === 'encrypt';
  document.getElementById('fn').textContent = (enc ? '' : '−') + n;
  const ex = enc
    ? `A \u2192 ${shiftChar('A', n)}`
    : `${shiftChar('A', n)} \u2192 A`;
  document.getElementById('fe').textContent = ex;
}

// ── Copy ─────────────────────────────────────────────────────
function doCopy() {
  const t = document.getElementById('output-box').textContent;
  if (!t || t === 'Output appears here…') return;
  navigator.clipboard.writeText(t).then(() => {
    const btn = document.querySelector('.copy-btn');
    btn.innerHTML = '<i class="ri-check-line"></i> Copied';
    setTimeout(() => { btn.innerHTML = '<i class="ri-clipboard-line"></i> Copy'; }, 1600);
  });
}

// ── Alphabet rows ─────────────────────────────────────────────
function buildAlphaRows() {
  const pr = document.getElementById('plain-row');
  const cr = document.getElementById('cipher-row');
  
  ALPHA.split('').forEach((ch, i) => {
    // Helper to create the cell with the index label
    const createCell = (char, index, isCipher) => {
      const div = document.createElement('div');
      div.className = 'al';
      div.innerHTML = `${char}<span style="position:absolute; bottom:2px; font-size:7px; opacity:0.5;">${index}</span>`;
      div.style.position = 'relative'; // Required for absolute positioning of the index
      if (!isCipher) {
        div.dataset.i = index;
        div.onclick = () => highlight(index);
      } else {
        div.dataset.c = index;
      }
      return div;
    };

    pr.appendChild(createCell(ch, i, false));
    cr.appendChild(createCell(ch, i, true));
  });
}

function updateCipherRow() {
  const n = mode === 'encrypt' ? shift : -shift;
  document.querySelectorAll('[data-c]').forEach((el, i) => {
    // This shifts the entire alphabet row by N
    el.textContent = ALPHA[((i + n) % 26 + 26) % 26]; 
  });
}

function highlight(idx) {
  document.querySelectorAll('.al').forEach(e => e.classList.remove('plain-hi','cipher-hi'));
  document.querySelector(`[data-i="${idx}"]`).classList.add('plain-hi');
  const n  = mode === 'encrypt' ? shift : -shift;
  const ci = ((idx + n) % 26 + 26) % 26;
  document.querySelectorAll('[data-c]')[ci].classList.add('cipher-hi');
  const p  = ALPHA[idx], c = ALPHA[ci];
  document.getElementById('alpha-formula').innerHTML =
    `<span class="fk">${p}</span> (position ${idx}) + shift <span class="fk">${shift}</span> = position <span class="fv">${ci}</span> &rarr; cipher letter <span class="fk">${c}</span> &nbsp;&nbsp; (${idx} + ${shift}) % 26 = ${ci}`;
}

// ── Intersection observer for reveals ────────────────────────
function observeGroup(selector, items, delay = 90) {
  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.querySelectorAll(items).forEach((el, i) => {
          setTimeout(() => el.classList.add('visible'), i * delay);
        });
        obs.unobserve(e.target);
      }
    });
  }, { threshold: 0.0, rootMargin: '0px 0px -50px 0px' });
  document.querySelectorAll(selector).forEach(el => obs.observe(el));
}
observeGroup('#ipo-flow', '.ipo-block', 120);
observeGroup('#cards-main', '.card', 90);
observeGroup('#steps-list', '.step', 100);
observeGroup('#vuln-row', '.vuln-item', 120);

buildAlphaRows();
processText();
</script>
</body>
</html>"""

class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(HTML.encode())

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body   = self.rfile.read(length)
        params = json.loads(body) if body else {}
        action = params.get("action", "encrypt")
        text   = params.get("text", "")
        key    = int(params.get("shift", 3))
        if action == "encrypt":
            result = caesar_encrypt(text, key)
        else:
            result = caesar_decrypt(text, key)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"result": result}).encode())

print(f"Caesar Cipher running at  http://localhost:{PORT}")
with socketserver.TCPServer(("", PORT), Handler) as srv:
    srv.serve_forever()
