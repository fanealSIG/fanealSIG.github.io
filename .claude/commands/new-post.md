# /new-post

El usuario comparte código o documentación técnica. Tu trabajo es redactar, ilustrar y publicar un post completo en el blog con el mismo estilo y calidad de los existentes.

---

## Contexto del blog

- Sitio: `fanealSIG.github.io` — GitHub Pages estático
- Posts en: `blog/posts/YYYY-MM-DD-slug.md`
- Imágenes en: `blog/images/`
- Metadata en: `blog/posts.json`
- Stubs OG en: `blog/YYYY-MM-DD-slug.html`
- Python para diagramas: `"/c/Program Files/ArcGIS/Pro/bin/Python/envs/arcgispro-py3/python.exe"`
- Script de diagramas: `blog/images/generate_diagrams.py`

Paleta de colores del portafolio:
- `NAVY2 = "#0a1730"`, `NAVY = "#0F2044"`, `TEAL = "#0D9488"`, `TEAL2 = "#14B8A6"`
- `WHITE = "#FFFFFF"`, `GRAY = "#94A3B8"`, `DGRAY = "#1e3a5f"`, `MGRAY = "#2d4a6e"`

---

## Pasos a ejecutar — en este orden

### 1. Leer los posts existentes para mantener el estilo
Lee ambos posts en `blog/posts/` para calibrar tono, estructura y nivel de detalle antes de escribir.

### 2. Definir el slug y fecha
- Formato: `YYYY-MM-DD-titulo-en-kebab-case` (usar fecha actual)
- Sin tildes ni caracteres especiales en el slug

### 3. Redactar el post en Markdown

Estructura obligatoria:
```
# Título del post

Párrafo de introducción: contexto del problema que motivó el trabajo.

---

## El problema
(qué pasaba antes, por qué era ineficiente o riesgoso)

---

## Herramientas utilizadas
(lista con bullets: tecnología + descripción breve)

---

## [Secciones técnicas según el contenido]
(código real del usuario, limpio y generalizado — sin datos internos, sin URLs reales, sin nombres de empresas)

---

## Resultados
(tabla comparativa antes/después cuando aplique)

---

## Próximos pasos
(mejoras posibles, extensiones del toolbox)

---

*¿Tienes preguntas o mejoras? Escríbeme a [faneal14@gmail.com](mailto:faneal14@gmail.com) o en [LinkedIn](https://linkedin.com/in/faneal).*

<span class="post-ai-note">Redactado con asistencia de IA generativa · Código revisado y validado en producción</span>
```

Reglas de redacción:
- Tono técnico pero directo, sin jerga innecesaria
- Primera persona cuando describe decisiones de diseño ("resolví", "opté por")
- Sin mencionar empresas, URLs internas, rutas de red ni nombres de personas
- Generalizar nombres de capas, servicios y carpetas con ejemplos genéricos
- Los bloques de código van con triple backtick y lenguaje (`python`, `json`, etc.)
- Insertar la imagen de flujo justo antes de la sección técnica principal:
  ```markdown
  ![Descripción](images/flujo-nombre-del-post.png)
  *Descripción breve del diagrama*
  ```

### 4. Crear los diagramas

Agregar dos funciones nuevas al final de `blog/images/generate_diagrams.py` (antes del `if __name__ == "__main__":`):

**`cover_nombre()`** — portada para la tarjeta del blog:
- Tamaño: `figsize=(12, 5.25)`, DPI 200
- Layout editorial: barra teal vertical izquierda (0.22 ancho) + bloque texto izquierdo + diagrama simplificado derecho
- Bloque texto: categoría en TEAL2 (8pt bold), título en WHITE (19pt bold, 2 líneas), subtítulo en GRAY (9pt), métrica destacada en recuadro MGRAY
- Divisor vertical a x=4.8
- Diagrama derecho: 3 boxes TEAL con los pasos clave del proceso
- Guardar como `cover-nombre-del-post.png`

**`flow_nombre()`** — diagrama de flujo para dentro del post:
- Tamaño: `figsize=(12, 5)` o `(11, 7.5)` según si es horizontal o vertical
- Usar `step_box()` con badges numerados para pasos secuenciales
- Usar rombo (`plt.Polygon`) para decisiones
- Nodos de color TEAL para pasos principales, DGRAY para preparatorios
- Líneas ortogonales para las conexiones (no diagonales)
- Guardar como `flujo-nombre-del-post.png`

Luego actualizar el bloque `if __name__ == "__main__":` para incluir las nuevas funciones y ejecutar:
```bash
"/c/Program Files/ArcGIS/Pro/bin/Python/envs/arcgispro-py3/python.exe" blog/images/generate_diagrams.py
```

Revisar visualmente las imágenes generadas antes de continuar.

### 5. Actualizar `posts.json`

Insertar al inicio del array:
```json
{
  "slug": "YYYY-MM-DD-slug",
  "date": "YYYY-MM-DD",
  "image": "images/cover-nombre-del-post.png",
  "title": {
    "es": "Título en español",
    "en": "Title in English"
  },
  "excerpt": {
    "es": "2-3 oraciones que resumen el post. Sin spoilers del código.",
    "en": "2-3 sentences summarizing the post."
  },
  "tags": ["Python", "ArcGIS", "..."]
}
```

### 6. Crear el stub HTML para Open Graph

Crear `blog/YYYY-MM-DD-slug.html` copiando la estructura de cualquiera de los stubs existentes y reemplazando:
- `og:url` → URL completa del stub
- `og:title` y `twitter:title` → título del post
- `og:description` y `twitter:description` → excerpt en español
- `og:image` y `twitter:image` → URL completa de la imagen de portada
- `canonical` → URL del stub
- `meta http-equiv="refresh"` → slug correcto
- `<script>` redirect → slug correcto
- `<title>` → título del post

URL base del sitio: `https://fanealSIG.github.io`

### 7. Commit y push

```bash
git add blog/posts/SLUG.md blog/images/cover-*.png blog/images/flujo-*.png blog/images/generate_diagrams.py blog/posts.json blog/SLUG.html
git commit -m "Add blog post: título resumido"
git push
```

---

## Checklist antes de hacer push

- [ ] El slug no tiene tildes ni espacios
- [ ] No hay datos internos (empresas, URLs reales, rutas de red)
- [ ] El código en el post es genérico y reproducible
- [ ] La portada tiene layout editorial (barra + texto + diagrama)
- [ ] El flujo no tiene texto superpuesto (labels con posiciones fijas separadas)
- [ ] `posts.json` tiene la entrada al inicio del array
- [ ] El stub HTML tiene todas las OG tags con URLs absolutas
- [ ] El post termina con la línea de IA generativa
