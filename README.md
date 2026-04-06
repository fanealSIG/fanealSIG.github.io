# Fabio Neira Alzate — Portfolio

**GIS Infrastructure Specialist & Environmental Engineer**  
[faneal14@gmail.com](mailto:faneal14@gmail.com) · [linkedin.com/in/faneal](https://linkedin.com/in/faneal) · Medellín, Colombia

---

## 🚀 Deploy to GitHub Pages (step by step)

### 1. Create the repository
1. Go to [github.com](https://github.com) → **New repository**
2. Name it exactly: `faneal.github.io` (replace `faneal` with your GitHub username)
3. Set it to **Public**
4. Click **Create repository**

### 2. Upload the files
Option A — drag & drop in GitHub:
1. Open the new repo
2. Click **Add file → Upload files**
3. Drag the entire contents of this folder (index.html + css/ + js/)
4. Commit changes

Option B — via terminal:
```bash
git init
git add .
git commit -m "Initial portfolio"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_USERNAME.github.io.git
git push -u origin main
```

### 3. Enable GitHub Pages
1. Go to repo **Settings → Pages**
2. Source: **Deploy from a branch**
3. Branch: **main** / root
4. Save

✅ Your site will be live at: `https://YOUR_USERNAME.github.io`  
*(takes ~2 minutes to go live)*

---

## 📁 File structure

```
portfolio/
├── index.html          ← Main page
├── css/
│   └── style.css       ← All styles
├── js/
│   ├── data.js         ← ✏️ Edit this to update content
│   └── main.js         ← Rendering & interactions
└── README.md           ← This file
```

## ✏️ How to update content

**All content** (experience, education, certifications, awards, skills) lives in `js/data.js`.  
You never need to touch `index.html` or `main.js` to update text.

Example — add a new certification:
```javascript
// In js/data.js, inside the CERTIFICATIONS array:
{
  icon: '📜',
  year: { en: '2026', es: '2026' },
  en: { name: 'New Cert Name', issuer: 'Issuing Organization', note: 'Description in English.' },
  es: { name: 'Nombre del Certificado', issuer: 'Organización emisora', note: 'Descripción en español.' }
}
```

## 🌐 Bilingual

The site defaults to **English**. Visitors can switch to Spanish with the EN/ES toggle in the nav.  
Language preference is saved in the browser (localStorage).

---

*Built with vanilla HTML, CSS & JS — no frameworks, no build tools, zero dependencies.*
