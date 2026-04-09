"""
Genera los diagramas para el blog de Fabio Neira.
Paleta del portafolio: navy #0F2044, teal #0D9488, teal2 #14B8A6,
                       white #FFFFFF, cream #F8F7F4, gray #94A3B8
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

OUT = os.path.dirname(os.path.abspath(__file__))

# ── Paleta ──────────────────────────────────────────────────────────────────
NAVY   = "#0F2044"
TEAL   = "#0D9488"
TEAL2  = "#14B8A6"
WHITE  = "#FFFFFF"
CREAM  = "#F8F7F4"
GRAY   = "#94A3B8"
DGRAY  = "#334155"
LGRAY  = "#E2E8F0"

# ── Helpers ──────────────────────────────────────────────────────────────────
def box(ax, x, y, w, h, label, sublabel=None,
        fc=NAVY, ec=TEAL2, tc=WHITE, radius=0.04, fontsize=10):
    rect = FancyBboxPatch((x - w/2, y - h/2), w, h,
                          boxstyle=f"round,pad=0",
                          facecolor=fc, edgecolor=ec, linewidth=1.5,
                          zorder=3)
    # manual rounded via ellipse trick not needed — just use round corners
    rect = FancyBboxPatch((x - w/2, y - h/2), w, h,
                          boxstyle="round,pad=0.02",
                          facecolor=fc, edgecolor=ec, linewidth=1.8, zorder=3)
    ax.add_patch(rect)
    if sublabel:
        ax.text(x, y + 0.055, label, ha='center', va='center',
                color=tc, fontsize=fontsize, fontweight='bold', zorder=4)
        ax.text(x, y - 0.065, sublabel, ha='center', va='center',
                color=GRAY, fontsize=7.5, zorder=4)
    else:
        ax.text(x, y, label, ha='center', va='center',
                color=tc, fontsize=fontsize, fontweight='bold', zorder=4)

def arrow(ax, x1, y1, x2, y2, color=TEAL2, lw=1.8):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color,
                                lw=lw, mutation_scale=14),
                zorder=2)

def label_arrow(ax, x, y, text, color=GRAY, fontsize=7.5):
    ax.text(x, y, text, ha='center', va='center',
            color=color, fontsize=fontsize,
            bbox=dict(fc=NAVY, ec='none', pad=1), zorder=5)

# ════════════════════════════════════════════════════════════════════════════
# DIAGRAMA 1 — Portada Enterprise Publishing
# ════════════════════════════════════════════════════════════════════════════
def cover_enterprise():
    fig, ax = plt.subplots(figsize=(11, 5))
    fig.patch.set_facecolor(NAVY)
    ax.set_facecolor(NAVY)
    ax.set_xlim(0, 11); ax.set_ylim(0, 5)
    ax.axis('off')

    # Título
    ax.text(5.5, 4.5, "Automatización de Publicación de Servicios",
            ha='center', va='center', color=WHITE,
            fontsize=15, fontweight='bold')
    ax.text(5.5, 4.1, "ArcGIS Enterprise · Python Toolbox · ArcPy",
            ha='center', va='center', color=TEAL2, fontsize=10)

    # Línea decorativa
    ax.plot([1, 10], [3.75, 3.75], color=TEAL, lw=0.6, alpha=0.4)

    # ── Fila superior: flujo individual ──────────────────────────────────
    y_top = 2.9
    items_top = [
        (1.3,  "MXD / MAPX",  ".mxd / .mapx"),
        (3.2,  "APRX Base",   "plantilla en blanco"),
        (5.1,  "SDDraft",     ".sddraft"),
        (6.9,  "Stage",       ".sd compilado"),
        (8.7,  "Upload",      "servidor federado"),
        (10.5, "Enterprise",  "servicio activo"),
    ]
    for (x, lbl, sub) in items_top:
        fc = TEAL if lbl in ("SDDraft","Stage","Upload") else DGRAY
        ec = TEAL2 if lbl in ("SDDraft","Stage","Upload") else TEAL
        box(ax, x, y_top, 1.55, 0.55, lbl, sub, fc=fc, ec=ec, fontsize=9)

    xs = [x for (x,_,__) in items_top]
    for i in range(len(xs)-1):
        arrow(ax, xs[i]+0.78, y_top, xs[i+1]-0.78, y_top)

    ax.text(0.35, y_top, "Publicación\nindividual",
            ha='center', va='center', color=GRAY, fontsize=7.5)

    # ── Fila inferior: flujo masivo ───────────────────────────────────────
    y_bot = 1.8
    items_bot = [
        (1.3,  "Carpeta raíz", "subcarpetas"),
        (3.2,  "Escaneo",      "os.listdir()"),
        (5.1,  "Portal",       "crear carpetas"),
        (6.9,  "Lote SDDraft", "por archivo"),
        (8.7,  "Stage+Upload", "en secuencia"),
        (10.5, "CSV Reporte",  "exitosos/errores"),
    ]
    for (x, lbl, sub) in items_bot:
        fc = TEAL if lbl in ("Lote SDDraft","Stage+Upload") else DGRAY
        ec = TEAL2 if lbl in ("Lote SDDraft","Stage+Upload") else TEAL
        box(ax, x, y_bot, 1.55, 0.55, lbl, sub, fc=fc, ec=ec, fontsize=9)

    xs2 = [x for (x,_,__) in items_bot]
    for i in range(len(xs2)-1):
        arrow(ax, xs2[i]+0.78, y_bot, xs2[i+1]-0.78, y_bot)

    ax.text(0.35, y_bot, "Publicación\nmasiva",
            ha='center', va='center', color=GRAY, fontsize=7.5)

    # Línea separadora
    ax.plot([0.7, 10.8], [2.35, 2.35], color=DGRAY, lw=0.5, linestyle='--')

    # Footer
    ax.text(5.5, 0.35, "SDDraft  →  Stage  →  UploadServiceDefinition",
            ha='center', va='center', color=DGRAY, fontsize=8.5, fontstyle='italic')

    plt.tight_layout(pad=0.3)
    path = os.path.join(OUT, "cover-enterprise-publishing.png")
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor=NAVY)
    plt.close()
    print("OK  " + path)


# ════════════════════════════════════════════════════════════════════════════
# DIAGRAMA 2 — Flujo detallado Enterprise (para dentro del post)
# ════════════════════════════════════════════════════════════════════════════
def flow_enterprise():
    fig, ax = plt.subplots(figsize=(12, 4.2))
    fig.patch.set_facecolor(NAVY)
    ax.set_facecolor(NAVY)
    ax.set_xlim(0, 12); ax.set_ylim(0, 4.2)
    ax.axis('off')

    ax.text(6, 3.85, "Ciclo de publicación: 5 pasos",
            ha='center', va='center', color=WHITE, fontsize=13, fontweight='bold')

    steps = [
        (1.1,  "PASO 1",  "Validar\narchivo"),
        (3.0,  "PASO 2",  "Importar\nal APRX"),
        (4.9,  "PASO 3",  "Conectar\nal Portal"),
        (6.8,  "PASO 4",  "Gestionar\ncarpeta"),
        (8.7,  "PASO 5",  "SDDraft"),
        (10.1, "PASO 5b", "Stage"),
        (11.5, "PASO 5c", "Upload"),
    ]

    y = 2.2
    for (x, step, lbl) in steps:
        is_main = step in ("PASO 5","PASO 5b","PASO 5c")
        fc = TEAL if is_main else DGRAY
        ec = TEAL2
        w  = 1.5 if not is_main else 1.2
        box(ax, x, y, w, 0.85, lbl, step, fc=fc, ec=ec, fontsize=9)

    xs = [x for (x,_,__) in steps]
    for i in range(len(xs)-1):
        gap = (steps[i][0] + steps[i+1][0]) / 2
        lbl_arrow = ""
        if i == 3: lbl_arrow = "token\nREST"
        if i == 4: lbl_arrow = ".sddraft"
        if i == 5: lbl_arrow = ".sd"
        x1 = xs[i] + (0.75 if i < 4 else 0.6)
        x2 = xs[i+1] - (0.75 if i < 4 else 0.6)
        arrow(ax, x1, y, x2, y)
        if lbl_arrow:
            label_arrow(ax, (x1+x2)/2, y + 0.55, lbl_arrow)

    # Nota error 00374
    ax.text(9.4, 1.0,
            "Si Stage falla con error 00374:\n_fix_layer_ids_sddraft()  →  reintentar",
            ha='center', va='center', color=GRAY, fontsize=8,
            bbox=dict(fc=DGRAY, ec=TEAL, pad=5, boxstyle='round,pad=0.3'))

    arrow(ax, 10.1, 1.78, 10.1, 1.28, color=TEAL)

    plt.tight_layout(pad=0.3)
    path = os.path.join(OUT, "flujo-publicacion-enterprise.png")
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor=NAVY)
    plt.close()
    print("OK  " + path)


# ════════════════════════════════════════════════════════════════════════════
# DIAGRAMA 3 — Portada AGOL Backup
# ════════════════════════════════════════════════════════════════════════════
def cover_agol():
    fig, ax = plt.subplots(figsize=(11, 5))
    fig.patch.set_facecolor(NAVY)
    ax.set_facecolor(NAVY)
    ax.set_xlim(0, 11); ax.set_ylim(0, 5)
    ax.axis('off')

    ax.text(5.5, 4.5, "Backup, Eliminación y Restauración de ArcGIS Online",
            ha='center', va='center', color=WHITE,
            fontsize=14, fontweight='bold')
    ax.text(5.5, 4.1, "Python Toolbox · ArcGIS API for Python · 3 herramientas encadenadas",
            ha='center', va='center', color=TEAL2, fontsize=10)
    ax.plot([1, 10], [3.75, 3.75], color=TEAL, lw=0.6, alpha=0.4)

    # Herramientas principales
    y_tools = 2.7
    tools = [
        (2.0,  "BackupAGOL",  "descarga + manifiesto"),
        (5.5,  "DeleteAGOL",  "eliminación masiva"),
        (9.0,  "RestoreAGOL", "restauración completa"),
    ]
    for (x, lbl, sub) in tools:
        box(ax, x, y_tools, 2.5, 0.8, lbl, sub,
            fc=TEAL, ec=TEAL2, fontsize=11)

    # Artefactos
    y_art = 1.5
    arts = [
        (3.75, "manifest.json",       "carpetas + ítems\n+ dependencias"),
        (7.25, "restore_id_map.json", "IDs originales\n→ IDs nuevos"),
    ]
    for (x, lbl, sub) in arts:
        box(ax, x, y_art, 2.3, 0.72, lbl, sub,
            fc=DGRAY, ec=TEAL, tc=TEAL2, fontsize=9)

    # Flechas horizontales entre herramientas
    arrow(ax, 3.25, y_tools, 4.25, y_tools)
    arrow(ax, 6.75, y_tools, 7.75, y_tools)

    # Flechas hacia artefactos
    arrow(ax, 2.0, y_tools - 0.4, 3.75, y_art + 0.36)
    arrow(ax, 3.75, y_art - 0.36, 5.5, y_tools - 0.4)
    arrow(ax, 9.0, y_tools - 0.4, 7.25, y_art + 0.36)

    # Labels flechas
    label_arrow(ax, 3.5, y_tools + 0.15, "lee")
    label_arrow(ax, 7.0, y_tools + 0.15, "genera")

    # Footer
    ax.text(5.5, 0.45,
            "Dry-run disponible en las 3 herramientas  ·  Soporta 400+ ítems  ·  Reporte CSV por lote",
            ha='center', va='center', color=DGRAY, fontsize=8.5, fontstyle='italic')

    plt.tight_layout(pad=0.3)
    path = os.path.join(OUT, "cover-agol-backup.png")
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor=NAVY)
    plt.close()
    print("OK  " + path)


# ════════════════════════════════════════════════════════════════════════════
# DIAGRAMA 4 — Estrategia de descarga BackupAGOL (para dentro del post)
# ════════════════════════════════════════════════════════════════════════════
def flow_backup_strategy():
    fig, ax = plt.subplots(figsize=(11, 5.5))
    fig.patch.set_facecolor(NAVY)
    ax.set_facecolor(NAVY)
    ax.set_xlim(0, 11); ax.set_ylim(0, 5.5)
    ax.axis('off')

    ax.text(5.5, 5.1, "Estrategia de descarga — BackupAGOL",
            ha='center', va='center', color=WHITE, fontsize=13, fontweight='bold')

    # Inicio
    box(ax, 5.5, 4.3, 2.2, 0.55, "Ítem AGOL", fc=DGRAY, ec=TEAL2)
    arrow(ax, 5.5, 4.02, 5.5, 3.6)

    # Decisión: tipo?
    # Rombo manual con polígono
    diamond_x = [5.5, 7.0, 5.5, 4.0, 5.5]
    diamond_y = [3.55, 3.0, 2.45, 3.0, 3.55]
    ax.fill(diamond_x, diamond_y, color=DGRAY, zorder=3)
    ax.plot(diamond_x, diamond_y, color=TEAL2, lw=1.8, zorder=4)
    ax.text(5.5, 3.0, "¿Tipo\nde ítem?", ha='center', va='center',
            color=WHITE, fontsize=9, fontweight='bold', zorder=5)

    # Rama izquierda: descarga directa
    arrow(ax, 4.0, 3.0, 2.0, 3.0)
    label_arrow(ax, 3.0, 3.2, "Web Map, Dashboard\nNotebook, Shapefile…")

    box(ax, 1.6, 2.0, 2.6, 0.65, "Descarga directa", "item.download()",
        fc=TEAL, ec=TEAL2, fontsize=9)
    arrow(ax, 2.0, 2.72, 1.6, 2.33)

    box(ax, 1.6, 0.9, 2.6, 0.65, "archivo + .json\n(metadatos)", None,
        fc=DGRAY, ec=TEAL, tc=TEAL2, fontsize=9)
    arrow(ax, 1.6, 1.67, 1.6, 1.23)

    # Rama derecha: exportación
    arrow(ax, 7.0, 3.0, 9.0, 3.0)
    label_arrow(ax, 8.0, 3.2, "Feature Service\nFeature Layer, Table")

    box(ax, 9.4, 2.0, 2.6, 0.65, "Exportar → FGDB", "item.export(wait=True)",
        fc=TEAL, ec=TEAL2, fontsize=9)
    arrow(ax, 9.0, 2.72, 9.4, 2.33)

    box(ax, 9.4, 0.9, 2.6, 0.65, "Descargar + eliminar\nexportación temporal",
        None, fc=DGRAY, ec=TEAL, tc=TEAL2, fontsize=9)
    arrow(ax, 9.4, 1.67, 9.4, 1.23)

    # Merge al manifiesto
    arrow(ax, 1.6, 0.57, 5.5, 0.2, color=GRAY)
    arrow(ax, 9.4, 0.57, 5.5, 0.2, color=GRAY)
    box(ax, 5.5, 0.2, 2.8, 0.38, "manifest.json  ·  entrada de ítem",
        fc=DGRAY, ec=TEAL2, tc=TEAL2, fontsize=8.5)

    plt.tight_layout(pad=0.3)
    path = os.path.join(OUT, "flujo-backup-estrategia.png")
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor=NAVY)
    plt.close()
    print("OK  " + path)


if __name__ == "__main__":
    cover_enterprise()
    flow_enterprise()
    cover_agol()
    flow_backup_strategy()
    print("\nTodos los diagramas generados."  )
