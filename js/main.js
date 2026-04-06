// ═══════════════════════════════════════════════════════════
//  MAIN.JS — Rendering & Interactions
// ═══════════════════════════════════════════════════════════

let currentLang = localStorage.getItem('pref-lang') || 'es';

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
    center: [10, -30],
    zoom: 2,
    zoomControl: true,
    scrollWheelZoom: false,
    attributionControl: false
  });

  const baseLayers = {
    '🛰️ Satellite': L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
      maxZoom: 19
    }),
    '🗺️ Streets': L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      subdomains: 'abc', maxZoom: 19
    }),
    '🧭 Topo': L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
      subdomains: 'abc', maxZoom: 17
    })
  };

  baseLayers['🛰️ Satellite'].addTo(map);
  L.control.layers(baseLayers, null, { position: 'topright', collapsed: false }).addTo(map);

  L.marker([6.2442, -75.5812], {
    icon: L.divIcon({
      className: '',
      html: '<div style="width:14px;height:14px;background:#14b8a6;border-radius:50%;border:2.5px solid #fff;box-shadow:0 0 14px rgba(20,184,166,.9)"></div>',
      iconSize: [14, 14], iconAnchor: [7, 7]
    })
  }).addTo(map)
    .bindTooltip('Medellín, Colombia', { permanent: true, direction: 'top', className: 'map-tip', offset: [0, -8] });
})();
