/* ============================================
   EcoLoop — Frontend Logic
   ============================================ */

const API_BASE = 'http://127.0.0.1:5000/api/analyze';
let mode = 'real';
let currentImage = null;
let analyzing = false;

// ============================================
// Navigation
// ============================================
function navigateTo(page) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.getElementById(`page-${page}`)?.classList.add('active');

  document.querySelectorAll('.nav-link').forEach(link => {
    link.classList.toggle('active', link.dataset.page === page);
  });

  if (page === 'dashboard') {
    animateLoopBars();
  }

  window.scrollTo(0, 0);
}

document.addEventListener('click', (e) => {
  const link = e.target.closest('.nav-link');
  if (link) {
    e.preventDefault();
    const page = link.dataset.page;
    if (page) navigateTo(page);
  }
});

// ============================================
// Mode Toggle
// ============================================
function setMode(m) {
  mode = m;
}

// ============================================
// Camera
// ============================================
let cameraStream = null;

async function openCamera() {
  try {
    cameraStream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
    const video = document.getElementById('camera-video');
    video.srcObject = cameraStream;
    document.getElementById('camera-modal')?.classList.remove('hidden');
  } catch (err) {
    console.error('Camera error:', err);
    alert('Unable to access camera. Please use image upload instead.');
  }
}

function closeCamera() {
  if (cameraStream) {
    cameraStream.getTracks().forEach(t => t.stop());
    cameraStream = null;
  }
  document.getElementById('camera-modal')?.classList.add('hidden');
}

function capturePhoto() {
  const video = document.getElementById('camera-video');
  const canvas = document.getElementById('camera-canvas');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext('2d').drawImage(video, 0, 0);
  const dataUrl = canvas.toDataURL('image/jpeg');
  setImagePreview(dataUrl);
  closeCamera();
}

// ============================================
// Image Upload
// ============================================
function handleImageUpload(event) {
  const file = event.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = (e) => setImagePreview(e.target.result);
  reader.readAsDataURL(file);
}

function setImagePreview(dataUrl) {
  currentImage = dataUrl;
  const img = document.getElementById('uploaded-image');
  img.src = dataUrl;

  document.getElementById('upload-prompt')?.classList.add('hidden');
  document.getElementById('preview-container')?.classList.remove('hidden');
  document.getElementById('btn-analyze').disabled = false;

  document.getElementById('result-panel')?.classList.add('hidden');
  document.getElementById('detection-overlay').innerHTML = '';
}

// ============================================
// Analysis Flow
// ============================================
async function startAnalysis() {
  if (analyzing || !currentImage) return;
  analyzing = true;

  const btnAnalyze = document.getElementById('btn-analyze');
  btnAnalyze.disabled = true;

  const analysisStatus = document.getElementById('analysis-status');
  analysisStatus?.classList.remove('hidden');
  document.getElementById('result-panel')?.classList.add('hidden');

  const lines = [
    document.getElementById('status-line-1'),
    document.getElementById('status-line-2'),
    document.getElementById('status-line-3'),
    document.getElementById('status-line-4'),
    document.getElementById('status-line-5'),
  ];

  lines.forEach((l, i) => {
    if (l) l.classList.toggle('dim', i > 0);
  });

  for (let i = 1; i < lines.length; i++) {
    await delay(350 + Math.random() * 200);
    if (lines[i]) lines[i].classList.remove('dim');
  }

  const scanLine = document.getElementById('scan-line');
  scanLine?.classList.add('active');

  await delay(600);

  let result;
  try {
    if (mode === 'real') {
      result = await callAPI(currentImage);
    } else {
      result = getMockResult();
    }
  } catch (err) {
    console.error('Analysis error:', err);
    alert('Analysis failed. Switching to demo mode for this run.');
    result = getMockResult();
  }

  scanLine?.classList.remove('active');

  renderResult(result);
  updateDashboard(result);
  updateImpact(result);

  analysisStatus?.classList.add('hidden');
  analyzing = false;
  btnAnalyze.disabled = false;
}

// ============================================
// API
// ============================================
async function callAPI(dataUrl) {
  const blob = dataUrlToBlob(dataUrl);
  const formData = new FormData();
  formData.append('image', blob, 'waste.jpg');

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 15000);

  try {
    const res = await fetch(API_BASE, {
      method: 'POST',
      body: formData,
      signal: controller.signal,
    });

    clearTimeout(timeout);

    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const json = await res.json();

    if (!json.success || !json.result) {
      throw new Error('Invalid response');
    }

    return normalizeResult(json);
  } catch (err) {
    clearTimeout(timeout);
    throw err;
  }
}

function normalizeResult(json) {
  const r = json.result || json;
  const items = Array.isArray(r.items) ? r.items : (r.item ? [r] : []);

  return {
    items: items.map(it => ({
      item: it.item || it.label || 'Unknown',
      material: it.material || '—',
      class: it.class || it.category || 'Other',
      confidence: it.confidence || 0,
      disposal: it.disposal || 'General waste',
      points: it.points || 5,
      waste_diverted_kg: it.waste_diverted_kg || 0.01,
      co2_saved_kg: it.co2_saved_kg || 0.02,
      explanation: it.explanation || '',
      box_2d: it.box_2d || null,
    })),
    summary: json.summary || {
      total_items: items.length,
      classes_detected: [...new Set(items.map(i => i.class || i.category || 'Other'))],
      dominant_class: items[0]?.class || items[0]?.category || 'Other',
    },
  };
}

// ============================================
// Result Rendering
// ============================================
function renderResult(result) {
  const panel = document.getElementById('result-panel');
  const container = document.getElementById('result-items');
  panel?.classList.remove('hidden');

  const total = result.items.length;
  document.getElementById('result-objects').textContent = `${String(total).padStart(2, '0')} OBJECTS DETECTED`;

  document.getElementById('tel-objects').textContent = String(total).padStart(2, '0');

  const totalPoints = result.items.reduce((sum, it) => sum + (it.points || 0), 0);
  const totalWaste = result.items.reduce((sum, it) => sum + (it.waste_diverted_kg || 0), 0);
  const totalCo2 = result.items.reduce((sum, it) => sum + (it.co2_saved_kg || 0), 0);

  container.innerHTML = result.items.map((it, idx) => {
    const classLower = String(it.class || 'other').toLowerCase();
    let classType = 'nonrecyclable';
    if (classLower.includes('biogas') || classLower.includes('organic')) classType = 'biogas';
    else if (classLower.includes('recyclable') || classLower.includes('plastic') || classLower.includes('metal') || classLower.includes('paper')) classType = 'recyclable';
    else if (classLower.includes('e-waste') || classLower.includes('hazardous') || classLower.includes('battery')) classType = 'ewaste';

    return `
      <div class="result-item" style="animation-delay: ${idx * 0.1}s">
        <div class="result-item-header">
          <span class="result-item-name">${escapeHtml(it.item)}</span>
          <span class="result-item-class ${classType}">${escapeHtml(it.class || 'OTHER')}</span>
        </div>
        <div class="result-item-meta">
          <span class="result-item-confidence">${it.confidence}% CONFIDENCE</span>
          <span>${escapeHtml(it.material || '—')}</span>
        </div>
        <p class="result-item-explanation">${escapeHtml(it.explanation || 'Place in appropriate waste stream after emptying and rinsing if needed.')}</p>
      </div>
    `;
  }).join('');

  renderDetectionBoxes(result.items);

  animateValue('reward-points', 0, totalPoints, 800);
  animateValue('reward-co2', 0, parseFloat(totalCo2.toFixed(3)), 800);
  animateValue('reward-waste', 0, parseFloat(totalWaste.toFixed(3)), 800);

  const latency = (Math.random() * 1.5 + 0.8).toFixed(2);
  const telLatency = document.getElementById('tel-latency');
  if (telLatency) telLatency.textContent = `${latency}s`;
}

function renderDetectionBoxes(items) {
  const overlay = document.getElementById('detection-overlay');
  overlay.innerHTML = '';

  items.forEach((it, idx) => {
    if (!it.box_2d || it.box_2d.length < 4) return;

    const [ymin, xmin, ymax, xmax] = it.box_2d;
    const top = ymin / 10;
    const left = xmin / 10;
    const width = (xmax - xmin) / 10;
    const height = (ymax - ymin) / 10;

    const box = document.createElement('div');
    box.className = 'detection-box cb-tl cb-tr cb-bl cb-br';
    box.style.cssText = `
      top: ${top}%;
      left: ${left}%;
      width: ${width}%;
      height: ${height}%;
      animation-delay: ${idx * 0.15 + 0.5}s;
    `;

    const label = document.createElement('div');
    label.className = 'detection-label';
    label.style.animationDelay = `${idx * 0.15 + 0.7}s`;
    label.innerHTML = `${escapeHtml(it.item)}<span class="detection-confidence">${it.class} · ${it.confidence}%</span>`;

    box.appendChild(label);
    overlay.appendChild(box);
  });
}

// ============================================
// Dashboard Updates
// ============================================
function updateDashboard(result) {
  const totalPoints = result.items.reduce((sum, it) => sum + (it.points || 0), 0);
  const totalWaste = result.items.reduce((sum, it) => sum + (it.waste_diverted_kg || 0), 0);
  const totalCo2 = result.items.reduce((sum, it) => sum + (it.co2_saved_kg || 0), 0);

  const currentPoints = parseInt(document.getElementById('dashboard-ecopoints')?.textContent.replace(/,/g, '') || '0');
  const newPoints = currentPoints + totalPoints;

  animateValue('dashboard-ecopoints', currentPoints, newPoints, 600, true);
  animateValue('metric-points', currentPoints, newPoints, 600, true);

  const currentWaste = parseFloat(document.getElementById('metric-waste')?.textContent || '0');
  const currentCo2 = parseFloat(document.getElementById('metric-co2')?.textContent || '0');
  const currentSorts = parseInt(document.getElementById('metric-sorts')?.textContent || '0');

  animateValue('metric-waste', currentWaste, currentWaste + totalWaste, 600);
  animateValue('metric-co2', currentCo2, currentCo2 + totalCo2, 600);
  document.getElementById('metric-sorts').textContent = currentSorts + result.items.length;

  const scanEp = document.getElementById('scan-ecopoints');
  if (scanEp) scanEp.textContent = newPoints.toLocaleString();
}

function updateImpact(result) {
  const totalWaste = result.items.reduce((sum, it) => sum + (it.waste_diverted_kg || 0), 0);
  const totalCo2 = result.items.reduce((sum, it) => sum + (it.co2_saved_kg || 0), 0);

  const currentWaste = parseFloat(document.getElementById('impact-waste')?.textContent || '0');
  const currentCo2 = parseFloat(document.getElementById('impact-co2')?.textContent || '0');

  animateValue('impact-waste', currentWaste, currentWaste + totalWaste, 600);
  animateValue('impact-co2', currentCo2, currentCo2 + totalCo2, 600);
}

// ============================================
// Animations
// ============================================
function animateLoopBars() {
  document.querySelectorAll('.loop-bar').forEach((bar, i) => {
    const width = bar.dataset.width;
    bar.style.width = '0';
    setTimeout(() => {
      bar.style.width = width;
    }, i * 100);
  });
}

function animateValue(id, start, end, duration, isPoints = false) {
  const el = document.getElementById(id);
  if (!el) return;

  const startTime = performance.now();
  const diff = end - start;

  function update(now) {
    const elapsed = now - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = start + diff * eased;

    if (isPoints) {
      el.textContent = Math.round(current).toLocaleString();
    } else {
      el.textContent = Number.isInteger(end) ? Math.round(current) : current.toFixed(2);
    }

    if (progress < 1) {
      requestAnimationFrame(update);
    }
  }

  requestAnimationFrame(update);
}

// ============================================
// Mock / Demo Data
// ============================================
function getMockResult() {
  const mocks = [
    {
      items: [
        {
          item: 'Plastic Bottle',
          material: 'PET Plastic',
          class: 'Recyclable',
          confidence: 94,
          disposal: 'Dry / Recyclable Waste',
          points: 10,
          waste_diverted_kg: 0.02,
          co2_saved_kg: 0.08,
          explanation: 'This appears to be a PET plastic bottle. Place it in the dry/recyclable stream after emptying and rinsing it.',
          box_2d: [120, 200, 600, 420],
        },
      ],
      summary: { total_items: 1, classes_detected: ['Recyclable'], dominant_class: 'Recyclable' },
    },
    {
      items: [
        {
          item: 'Banana Peel',
          material: 'Organic Matter',
          class: 'Biogas',
          confidence: 96,
          disposal: 'Organic / Biogas Feedstock',
          points: 15,
          waste_diverted_kg: 0.10,
          co2_saved_kg: 0.05,
          explanation: 'Organic waste detected. This will be converted to biogas through anaerobic digestion.',
          box_2d: [80, 150, 500, 350],
        },
        {
          item: 'Aluminium Can',
          material: 'Aluminium',
          class: 'Recyclable',
          confidence: 97,
          disposal: 'Dry / Recyclable Waste',
          points: 10,
          waste_diverted_kg: 0.01,
          co2_saved_kg: 0.12,
          explanation: 'Aluminium can detected. Place in recyclable stream. Rinse if needed.',
          box_2d: [80, 450, 500, 650],
        },
      ],
      summary: { total_items: 2, classes_detected: ['Biogas', 'Recyclable'], dominant_class: 'Biogas' },
    },
    {
      items: [
        {
          item: 'Battery',
          material: 'Lithium-ion',
          class: 'E-Waste',
          confidence: 91,
          disposal: 'Special Handling Required',
          points: 20,
          waste_diverted_kg: 0.05,
          co2_saved_kg: 0.15,
          explanation: 'E-waste detected. Do not dispose in regular waste. Take to designated e-waste collection point.',
          box_2d: [100, 180, 550, 380],
        },
        {
          item: 'Vegetable Scraps',
          material: 'Organic Matter',
          class: 'Biogas',
          confidence: 94,
          disposal: 'Organic / Biogas Feedstock',
          points: 15,
          waste_diverted_kg: 0.12,
          co2_saved_kg: 0.06,
          explanation: 'Organic waste detected. Diverted to biogas recovery pathway.',
          box_2d: [80, 400, 580, 680],
        },
        {
          item: 'Wrapper',
          material: 'Multi-layer Plastic',
          class: 'Non-Recyclable',
          confidence: 88,
          disposal: 'General Waste',
          points: 2,
          waste_diverted_kg: 0.005,
          co2_saved_kg: 0.01,
          explanation: 'Multi-layer packaging is not recyclable in standard facilities. Dispose in general waste.',
          box_2d: [50, 320, 700, 500],
        },
      ],
      summary: { total_items: 3, classes_detected: ['E-Waste', 'Biogas', 'Non-Recyclable'], dominant_class: 'Biogas' },
    },
  ];

  return mocks[Math.floor(Math.random() * mocks.length)];
}

// ============================================
// Utilities
// ============================================
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

function dataUrlToBlob(dataUrl) {
  const parts = dataUrl.split(',');
  const mime = parts[0].match(/:(.*?);/)[1];
  const b64 = atob(parts[1]);
  const arr = new Uint8Array(b64.length);
  for (let i = 0; i < b64.length; i++) arr[i] = b64.charCodeAt(i);
  return new Blob([arr], { type: mime });
}

// ============================================
// Lithos Hero — Spotlight & Animations
// ============================================
function initLithosHero() {
  const reveal = document.getElementById('reveal-layer');
  if (!reveal) return;

  const SPOTLIGHT_R = 260;
  const mouse = { x: -999, y: -999 };
  const smooth = { x: -999, y: -999 };
  let rafRef = null;
  let lastRenderX = -9999;
  let lastRenderY = -9999;

  const canvas = document.createElement('canvas');
  canvas.style.cssText = 'position:absolute;inset:0;pointer-events:none;display:none;';
  reveal.appendChild(canvas);

  const ctx = canvas.getContext('2d');

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  resize();
  window.addEventListener('resize', resize);

  document.addEventListener('mousemove', (e) => {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
  });

  function drawMask() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const r = SPOTLIGHT_R;
    const x = smooth.x;
    const y = smooth.y;

    const gradient = ctx.createRadialGradient(x, y, 0, x, y, r);
    gradient.addColorStop(0, 'rgba(255,255,255,1)');
    gradient.addColorStop(0.4, 'rgba(255,255,255,1)');
    gradient.addColorStop(0.6, 'rgba(255,255,255,0.75)');
    gradient.addColorStop(0.75, 'rgba(255,255,255,0.4)');
    gradient.addColorStop(0.88, 'rgba(255,255,255,0.12)');
    gradient.addColorStop(1, 'rgba(255,255,255,0)');

    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fill();

    const url = canvas.toDataURL();
    reveal.style.maskImage = `url(${url})`;
    reveal.style.webkitMaskImage = `url(${url})`;
    reveal.style.maskSize = '100% 100%';
    reveal.style.webkitMaskSize = '100% 100%';
  }

  function loop() {
    smooth.x += (mouse.x - smooth.x) * 0.1;
    smooth.y += (mouse.y - smooth.y) * 0.1;

    if (Math.abs(smooth.x - lastRenderX) > 0.5 || Math.abs(smooth.y - lastRenderY) > 0.5) {
      drawMask();
      lastRenderX = smooth.x;
      lastRenderY = smooth.y;
    }

    rafRef = requestAnimationFrame(loop);
  }

  loop();

  if (typeof gsap !== 'undefined') {
    gsap.to('.hero-bg', {
      scale: 1,
      duration: 1.8,
      ease: 'power3.out'
    });

    gsap.fromTo('.hero-line',
      { opacity: 0, y: 28, filter: 'blur(12px)' },
      {
        opacity: 1,
        y: 0,
        filter: 'blur(0px)',
        duration: 1.1,
        stagger: 0.17,
        ease: 'power3.out',
        delay: 0.25
      }
    );

    gsap.fromTo('.hero-subtitle, .hero-actions',
      { opacity: 0, y: 20 },
      {
        opacity: 1,
        y: 0,
        duration: 1,
        stagger: 0.15,
        ease: 'power3.out',
        delay: 0.7
      }
    );
  }

  return () => {
    if (rafRef) cancelAnimationFrame(rafRef);
    window.removeEventListener('resize', resize);
  };
}

// ============================================
// Init
// ============================================
document.addEventListener('DOMContentLoaded', () => {
  initLithosHero();

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateLoopBars();
      }
    });
  }, { threshold: 0.2 });

  const dashPage = document.getElementById('page-dashboard');
  if (dashPage) observer.observe(dashPage);

  const uploadArea = document.getElementById('upload-area');
  if (uploadArea) {
    uploadArea.addEventListener('dragover', (e) => {
      e.preventDefault();
      uploadArea.style.borderColor = 'rgba(204, 255, 0, 0.3)';
    });

    uploadArea.addEventListener('dragleave', () => {
      uploadArea.style.borderColor = '';
    });

    uploadArea.addEventListener('drop', (e) => {
      e.preventDefault();
      uploadArea.style.borderColor = '';
      const file = e.dataTransfer.files[0];
      if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (ev) => setImagePreview(ev.target.result);
        reader.readAsDataURL(file);
      }
    });
  }
});
