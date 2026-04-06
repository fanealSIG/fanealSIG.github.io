// ═══════════════════════════════════════════════════════════
//  MAIN.JS — Rendering & Interactions
// ═══════════════════════════════════════════════════════════

let currentLang = localStorage.getItem('pref-lang') || 'en';

// ── NAV ──────────────────────────────────────────────────────
function buildNav() {
  const ul  = document.getElementById('navLinks');
  const mul = document.getElementById('mobileNavLinks');
  ul.innerHTML = '';
  mul.innerHTML = '';
  NAV_LABELS[currentLang].forEach((label, i) => {
    const li  = document.createElement('li');
    li.innerHTML = `<a href="${NAV_HREFS[i]}">${label}</a>`;
    ul.appendChild(li);
    const li2 = li.cloneNode(true);
    li2.querySelector('a').addEventListener('click', closeMobileMenu);
    mul.appendChild(li2);
  });
}

// ── SKILLS ───────────────────────────────────────────────────
function buildSkills() {
  const grid = document.getElementById('skillsGrid');
  grid.innerHTML = SKILLS.map(s => `
    <div class="skill-card">
      <div class="skill-icon">${s.icon}</div>
      <div class="skill-name">${s[currentLang].name}</div>
      <p class="skill-desc">${s[currentLang].desc}</p>
      <div class="skill-tags">${s.tags.map(t => `<span class="tag">${t}</span>`).join('')}</div>
    </div>`).join('');
}

// ── EXPERIENCE ───────────────────────────────────────────────
function buildExperience() {
  const tl = document.getElementById('timeline');
  tl.innerHTML = EXPERIENCE.map(e => `
    <div class="exp-item">
      <p class="exp-date">${e.date}</p>
      <h3 class="exp-role">${e[currentLang].role}</h3>
      <p class="exp-company">${e.company}</p>
      <ul class="exp-bullets">
        ${e[currentLang].bullets.map(b => `<li>${b}</li>`).join('')}
      </ul>
    </div>`).join('');
  observeTimeline();
}

// ── EDUCATION ────────────────────────────────────────────────
function buildEducation() {
  const grid = document.getElementById('eduGrid');
  grid.innerHTML = EDUCATION.map(e => `
    <div class="edu-card">
      <p class="edu-year">${e.year[currentLang]}</p>
      <h3 class="edu-degree">${e[currentLang].degree}</h3>
      <p class="edu-inst">${e.institution}</p>
      <p class="edu-note">${e[currentLang].note}</p>
    </div>`).join('');
}

// ── CERTIFICATIONS ───────────────────────────────────────────
function buildCertifications() {
  const container = document.getElementById('certsGrid');
  container.innerHTML = CERT_GROUPS.map(group => `
    <div class="cert-group">
      <h3 class="cert-group-title">${group[currentLang].group}</h3>
      <div class="certs-subgrid">
        ${group.items.map(c => `
          <div class="cert-card">
            <div class="cert-icon">${c.icon}</div>
            <div class="cert-year">${c.year[currentLang]}</div>
            <h4 class="cert-name">${c[currentLang].name}</h4>
            <p class="cert-issuer">${c[currentLang].issuer}</p>
            <p class="cert-note">${c[currentLang].note}</p>
          </div>`).join('')}
      </div>
    </div>`).join('');
}

// ── AWARDS ───────────────────────────────────────────────────
function buildAwards() {
  const list = document.getElementById('awardsList');
  list.innerHTML = AWARDS.map(a => `
    <div class="award-item">
      <div class="award-icon">${a.icon}</div>
      <div>
        <p class="award-title">${a[currentLang].title}</p>
        <p class="award-body">${a[currentLang].body}</p>
      </div>
    </div>`).join('');
}

// ── LANG ELEMENTS ────────────────────────────────────────────
function applyLangVisibility() {
  document.querySelectorAll('[data-lang]').forEach(el => {
    el.classList.toggle('on', el.dataset.lang === currentLang);
  });
}

// ── FULL RENDER ──────────────────────────────────────────────
function render() {
  buildNav();
  buildSkills();
  buildExperience();
  buildEducation();
  buildCertifications();
  buildAwards();
  applyLangVisibility();
  document.documentElement.lang = currentLang;
}

// ── LANG SWITCH ──────────────────────────────────────────────
function setLang(lang) {
  currentLang = lang;
  document.getElementById('btnEn').classList.toggle('active', lang === 'en');
  document.getElementById('btnEs').classList.toggle('active', lang === 'es');
  localStorage.setItem('pref-lang', lang);
  render();
}

document.getElementById('btnEn').addEventListener('click', () => setLang('en'));
document.getElementById('btnEs').addEventListener('click', () => setLang('es'));

// ── SCROLL REVEAL ────────────────────────────────────────────
function observeTimeline() {
  const obs = new IntersectionObserver(entries => {
    entries.forEach((e, i) => {
      if (e.isIntersecting) {
        setTimeout(() => e.target.classList.add('visible'), i * 120);
        obs.unobserve(e.target);
      }
    });
  }, { threshold: 0.1 });
  document.querySelectorAll('.exp-item').forEach(el => obs.observe(el));
}

// ── STICKY NAV SHADOW ────────────────────────────────────────
window.addEventListener('scroll', () => {
  document.getElementById('navbar').classList.toggle('scrolled', window.scrollY > 40);
});

// ── MOBILE MENU ──────────────────────────────────────────────
function closeMobileMenu() {
  document.getElementById('mobileMenu').classList.remove('open');
}
document.getElementById('hamburger').addEventListener('click', () => {
  document.getElementById('mobileMenu').classList.toggle('open');
});

// ── INIT ─────────────────────────────────────────────────────
render();

// ── CONTACT MAP ──────────────────────────────────────────────
(function initContactMap() {
  const map = L.map('contactMap', {
    center: [6.18, -75.12],
    zoom: 9,
    zoomControl: false,
    scrollWheelZoom: false,
    dragging: false,
    touchZoom: false,
    doubleClickZoom: false,
    boxZoom: false,
    keyboard: false,
    attributionControl: false
  });

  // Satellite base (ESRI World Imagery)
  L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    maxZoom: 17
  }).addTo(map);

  // Dark labels overlay (CartoDB)
  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_only_labels/{z}/{x}/{y}{r}.png', {
    subdomains: 'abcd', maxZoom: 17
  }).addTo(map);

  // Valle de Aburrá polygon
  L.geoJSON({
    type: 'Feature',
    geometry: {
      type: 'Polygon',
      coordinates: [[
        [-75.618, 6.439], [-75.565, 6.432], [-75.505, 6.395],
        [-75.462, 6.338], [-75.468, 6.273], [-75.487, 6.206],
        [-75.512, 6.148], [-75.550, 6.072], [-75.590, 6.052],
        [-75.628, 6.072], [-75.668, 6.108], [-75.688, 6.170],
        [-75.673, 6.250], [-75.648, 6.335], [-75.635, 6.408],
        [-75.618, 6.439]
      ]]
    }
  }, {
    style: { color: '#14b8a6', weight: 2, fillColor: '#0d9488', fillOpacity: 0.28 }
  }).addTo(map)
    .bindTooltip('Valle de Aburrá', { permanent: true, direction: 'center', className: 'map-tip' });

  // Oriente Antioqueño polygon
  L.geoJSON({
    type: 'Feature',
    geometry: {
      type: 'Polygon',
      coordinates: [[
        [-75.420, 6.415], [-75.355, 6.582], [-75.120, 6.805],
        [-74.780, 6.852], [-74.420, 6.738], [-74.295, 6.548],
        [-74.305, 6.250], [-74.328, 5.952], [-74.412, 5.718],
        [-74.668, 5.518], [-74.922, 5.478], [-75.182, 5.598],
        [-75.365, 5.812], [-75.415, 6.062], [-75.420, 6.415]
      ]]
    }
  }, {
    style: { color: '#818cf8', weight: 1.5, fillColor: '#6366f1', fillOpacity: 0.15 }
  }).addTo(map)
    .bindTooltip('Oriente Antioqueño', { permanent: true, direction: 'center', className: 'map-tip' });

  // Medellín marker
  L.marker([6.2442, -75.5812], {
    icon: L.divIcon({
      className: '',
      html: '<div style="width:10px;height:10px;background:#14b8a6;border-radius:50%;border:2px solid #fff;box-shadow:0 0 10px rgba(20,184,166,.9)"></div>',
      iconSize: [10, 10], iconAnchor: [5, 5]
    })
  }).addTo(map)
    .bindTooltip('Medellín', { permanent: true, direction: 'top', className: 'map-tip', offset: [0, -6] });
})();
