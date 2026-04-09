# -*- coding: utf-8 -*-
"""
Diagramas del blog - Fabio Neira Alzate
Mejoras v2: portadas editoriales, flujos corregidos, 200 DPI
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import os

OUT = os.path.dirname(os.path.abspath(__file__))

# Paleta
NAVY    = "#0F2044"
NAVY2   = "#0a1730"
TEAL    = "#0D9488"
TEAL2   = "#14B8A6"
WHITE   = "#FFFFFF"
GRAY    = "#94A3B8"
DGRAY   = "#1e3a5f"
MGRAY   = "#2d4a6e"

# Fuente comun
plt.rcParams['font.family'] = 'DejaVu Sans'


# ── helpers ──────────────────────────────────────────────────────────────────
def gradient_bg(ax, fig, c1=NAVY2, c2=NAVY):
    """Fondo con gradiente vertical sutil."""
    grad = np.linspace(0, 1, 256).reshape(256, 1)
    ax.imshow(grad, aspect='auto', extent=[0, 1, 0, 1],
              origin='lower', transform=ax.transAxes, zorder=0,
              cmap=LinearSegmentedColormap.from_list('bg', [c1, c2]))

def rbox(ax, x, y, w, h, fc=DGRAY, ec=TEAL2, lw=1.6, radius=0.3, zorder=3):
    p = FancyBboxPatch((x - w/2, y - h/2), w, h,
                       boxstyle="round,pad=0.02",
                       facecolor=fc, edgecolor=ec, linewidth=lw, zorder=zorder)
    ax.add_patch(p)

def arrow(ax, x1, y1, x2, y2, color=TEAL2, lw=1.6, mutation=14):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color,
                                lw=lw, mutation_scale=mutation), zorder=4)

def pill(ax, x, y, text, fc=TEAL, tc=WHITE, fontsize=8):
    """Badge tipo etiqueta."""
    ax.text(x, y, text, ha='center', va='center', color=tc,
            fontsize=fontsize, fontweight='bold', zorder=6,
            bbox=dict(facecolor=fc, edgecolor='none',
                      boxstyle='round,pad=0.25'))

def step_box(ax, x, y, w, h, number, label, sub=None,
             fc=DGRAY, ec=TEAL2, active=False):
    """Box con numero en badge superior y texto bien separado."""
    rbox(ax, x, y, w, h, fc=fc, ec=ec, lw=2 if active else 1.4)
    badge_fc = TEAL if active else MGRAY
    pill(ax, x - w/2 + 0.28, y + h/2 - 0.14, str(number),
         fc=badge_fc, fontsize=7.5)
    if sub:
        ax.text(x, y + 0.09, label, ha='center', va='center',
                color=WHITE, fontsize=9.5, fontweight='bold', zorder=5)
        ax.text(x, y - 0.16, sub, ha='center', va='center',
                color=GRAY, fontsize=7.5, zorder=5)
    else:
        ax.text(x, y, label, ha='center', va='center',
                color=WHITE, fontsize=9.5, fontweight='bold', zorder=5)

def float_label(ax, x, y, text, fontsize=7.5):
    ax.text(x, y, text, ha='center', va='center', color=GRAY,
            fontsize=fontsize, zorder=6,
            bbox=dict(facecolor=NAVY2, edgecolor='none', pad=1.5))


# ════════════════════════════════════════════════════════════════════════════
# COVER 1 — Enterprise Publishing  (editorial, 16:7)
# ════════════════════════════════════════════════════════════════════════════
def cover_enterprise():
    fig, ax = plt.subplots(figsize=(12, 5.25))
    fig.patch.set_facecolor(NAVY2)
    ax.set_facecolor(NAVY2)
    ax.set_xlim(0, 12); ax.set_ylim(0, 5.25)
    ax.axis('off')
    gradient_bg(ax, fig, NAVY2, NAVY)

    # Barra acento izquierda
    ax.add_patch(plt.Rectangle((0, 0), 0.22, 5.25,
                                facecolor=TEAL, zorder=5))

    # --- Bloque texto izquierdo ---
    ax.text(0.6, 4.5, "PYTHON TOOLBOX", color=TEAL2,
            fontsize=8, fontweight='bold', va='center', zorder=5)
    ax.text(0.6, 3.65,
            "Publicacion de Servicios\nen ArcGIS Enterprise",
            color=WHITE, fontsize=19, fontweight='bold',
            va='center', linespacing=1.25, zorder=5)
    ax.text(0.6, 2.7, "Automatizacion con ArcPy · SDDraft > Stage > Upload",
            color=GRAY, fontsize=9, va='center', zorder=5)

    # Metrica destacada
    rbox(ax, 1.7, 1.7, 2.8, 0.75, fc=MGRAY, ec=TEAL, lw=1.5)
    ax.text(1.7, 1.85, "10 min  ->  < 5 min",
            ha='center', va='center', color=TEAL2,
            fontsize=11, fontweight='bold', zorder=5)
    ax.text(1.7, 1.52, "por servicio publicado",
            ha='center', va='center', color=GRAY,
            fontsize=8, zorder=5)

    # Divisor
    ax.plot([4.8, 4.8], [0.4, 4.85], color=TEAL, lw=0.8, alpha=0.35, zorder=3)

    # --- Diagrama derecho simplificado ---
    # 3 grandes etapas del ciclo
    stages = [
        (6.3,  3.6, "SDDraft",  ".sddraft", True),
        (8.5,  3.6, "Stage",    ".sd compilado", True),
        (10.7, 3.6, "Upload",   "servidor federado", True),
    ]
    for (x, y, lbl, sub, _) in stages:
        rbox(ax, x, y, 2.8, 1.1, fc=TEAL, ec=TEAL2, lw=2)
        ax.text(x, y + 0.17, lbl,
                ha='center', va='center', color=WHITE,
                fontsize=13, fontweight='bold', zorder=5)
        ax.text(x, y - 0.2, sub,
                ha='center', va='center', color=NAVY,
                fontsize=8, zorder=5)

    arrow(ax, 7.65, 3.6, 8.08, 3.6, lw=2, mutation=16)
    arrow(ax, 9.85, 3.6, 10.28, 3.6, lw=2, mutation=16)

    # Fuentes de entrada
    inputs = [(6.3, "MXD / MAPX"), (8.5, "APRX base")]
    for (x, lbl) in inputs:
        rbox(ax, x, 2.1, 2.4, 0.6, fc=MGRAY, ec=TEAL2, lw=1.2)
        ax.text(x, 2.1, lbl, ha='center', va='center',
                color=WHITE, fontsize=9, zorder=5)
        arrow(ax, x, 2.42, x, 3.05, lw=1.4, mutation=12)

    # Resultado final
    rbox(ax, 10.7, 2.1, 2.4, 0.6, fc=MGRAY, ec=TEAL2, lw=1.2)
    ax.text(10.7, 2.1, "Servicio activo",
            ha='center', va='center', color=WHITE, fontsize=9, zorder=5)
    arrow(ax, 10.7, 3.05, 10.7, 2.42, lw=1.4, mutation=12)

    # Modo masivo
    rbox(ax, 8.5, 1.0, 6.8, 0.55, fc=DGRAY, ec=TEAL, lw=1.2)
    ax.text(8.5, 1.17, "PUBLICACION MASIVA",
            ha='center', va='center', color=TEAL2,
            fontsize=7.5, fontweight='bold', zorder=5)
    ax.text(8.5, 0.85,
            "Escaneo de subcarpetas  ->  pre-crear carpetas portal  ->  lote SDDraft+Stage+Upload  ->  reporte CSV",
            ha='center', va='center', color=GRAY, fontsize=7, zorder=5)

    plt.tight_layout(pad=0)
    path = os.path.join(OUT, "cover-enterprise-publishing.png")
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor=NAVY2)
    plt.close()
    print("OK " + path)


# ════════════════════════════════════════════════════════════════════════════
# COVER 2 — AGOL Backup  (editorial, 16:7)
# ════════════════════════════════════════════════════════════════════════════
def cover_agol():
    fig, ax = plt.subplots(figsize=(12, 5.25))
    fig.patch.set_facecolor(NAVY2)
    ax.set_facecolor(NAVY2)
    ax.set_xlim(0, 12); ax.set_ylim(0, 5.25)
    ax.axis('off')
    gradient_bg(ax, fig, NAVY2, NAVY)

    ax.add_patch(plt.Rectangle((0, 0), 0.22, 5.25,
                                facecolor=TEAL, zorder=5))

    # --- Texto izquierdo ---
    ax.text(0.6, 4.5, "ARCGIS API FOR PYTHON", color=TEAL2,
            fontsize=8, fontweight='bold', zorder=5)
    ax.text(0.6, 3.6,
            "Backup, Eliminacion\ny Restauracion AGOL",
            color=WHITE, fontsize=19, fontweight='bold',
            va='center', linespacing=1.25, zorder=5)
    ax.text(0.6, 2.7,
            "3 herramientas encadenadas · Manifiesto JSON · Dry-run",
            color=GRAY, fontsize=9, va='center', zorder=5)

    rbox(ax, 1.7, 1.7, 2.8, 0.75, fc=MGRAY, ec=TEAL, lw=1.5)
    ax.text(1.7, 1.85, "400+ items · 12 carpetas",
            ha='center', va='center', color=TEAL2,
            fontsize=11, fontweight='bold', zorder=5)
    ax.text(1.7, 1.52, "migracion completa automatizada",
            ha='center', va='center', color=GRAY,
            fontsize=8, zorder=5)

    ax.plot([4.8, 4.8], [0.4, 4.85], color=TEAL, lw=0.8, alpha=0.35)

    # --- 3 herramientas con numeros ---
    tools = [
        (6.1,  3.5, "1", "BackupAGOL",  "descarga + manifiesto"),
        (8.65, 3.5, "2", "DeleteAGOL",  "eliminacion masiva"),
        (11.2, 3.5, "3", "RestoreAGOL", "restauracion completa"),
    ]
    for (x, y, num, lbl, sub) in tools:
        rbox(ax, x, y, 2.7, 1.1, fc=TEAL, ec=TEAL2, lw=2)
        pill(ax, x - 1.1, y + 0.38, num, fc=NAVY, tc=TEAL2, fontsize=9)
        ax.text(x, y + 0.15, lbl,
                ha='center', va='center', color=WHITE,
                fontsize=12, fontweight='bold', zorder=5)
        ax.text(x, y - 0.2, sub,
                ha='center', va='center', color=NAVY,
                fontsize=8, zorder=5)

    arrow(ax, 7.45, 3.5, 7.98, 3.5, lw=2, mutation=16)
    arrow(ax, 9.98, 3.5, 10.51, 3.5, lw=2, mutation=16)

    # Artefactos bajo las herramientas
    arts = [
        (7.35, 2.05, "manifest.json",       "items + carpetas + dependencias"),
        (9.95, 2.05, "restore_id_map.json", "IDs originales -> IDs nuevos"),
    ]
    for (x, y, lbl, sub) in arts:
        rbox(ax, x, y, 2.9, 0.72, fc=DGRAY, ec=TEAL, lw=1.4)
        ax.text(x, y + 0.13, lbl,
                ha='center', va='center', color=TEAL2,
                fontsize=9, fontweight='bold', zorder=5)
        ax.text(x, y - 0.15, sub,
                ha='center', va='center', color=GRAY,
                fontsize=7.5, zorder=5)

    # Flechas verticales herramienta -> artefacto
    arrow(ax, 6.1, 2.95, 6.75, 2.42, lw=1.4, mutation=11)   # Backup -> manifest
    arrow(ax, 8.65, 2.95, 8.1, 2.42, lw=1.4, mutation=11)   # Delete  <- manifest
    arrow(ax, 11.2, 2.95, 10.4, 2.42, lw=1.4, mutation=11)  # Restore -> id_map

    plt.tight_layout(pad=0)
    path = os.path.join(OUT, "cover-agol-backup.png")
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor=NAVY2)
    plt.close()
    print("OK " + path)


# ════════════════════════════════════════════════════════════════════════════
# FLUJO 1 — Ciclo publicacion Enterprise (in-post)
# ════════════════════════════════════════════════════════════════════════════
def flow_enterprise():
    fig, ax = plt.subplots(figsize=(13, 5.5))
    fig.patch.set_facecolor(NAVY2)
    ax.set_facecolor(NAVY2)
    ax.set_xlim(0, 13); ax.set_ylim(0, 5.5)
    ax.axis('off')
    gradient_bg(ax, fig)

    ax.text(6.5, 5.1, "Ciclo de publicacion: 5 pasos",
            ha='center', va='center', color=WHITE,
            fontsize=14, fontweight='bold')

    # Paso 1-4 en fila superior
    top = [
        (1.2,  1, "Validar\narchivo"),
        (3.2,  2, "Importar\nal APRX"),
        (5.2,  3, "Conectar\nal Portal"),
        (7.2,  4, "Gestionar\ncarpeta"),
    ]
    for (x, n, lbl) in top:
        step_box(ax, x, 3.5, 1.75, 1.0, n, lbl, fc=DGRAY, ec=TEAL2)

    for i in range(len(top) - 1):
        x1 = top[i][0] + 0.88
        x2 = top[i+1][0] - 0.88
        arrow(ax, x1, 3.5, x2, 3.5)

    # Paso 5a-5c en fila inferior (teal, mas destacados)
    bot = [
        (9.2,  "5a", "SDDraft",  ".sddraft"),
        (10.9, "5b", "Stage",    ".sd"),
        (12.6, "5c", "Upload",   "servidor"),
    ]
    for (x, n, lbl, sub) in bot:
        rbox(ax, x, 3.5, 1.55, 1.0, fc=TEAL, ec=TEAL2, lw=2.2)
        pill(ax, x - 0.6, 3.98, n, fc=NAVY, tc=TEAL2, fontsize=7.5)
        ax.text(x, 3.62, lbl, ha='center', va='center',
                color=WHITE, fontsize=11, fontweight='bold', zorder=5)
        ax.text(x, 3.23, sub, ha='center', va='center',
                color=NAVY, fontsize=8, zorder=5)

    # Flecha entre bloque preparatorio y bloque SDDraft
    arrow(ax, 8.08, 3.5, 8.42, 3.5, lw=1.8, mutation=14)
    float_label(ax, 8.25, 3.82, "token\nREST")

    arrow(ax, 9.98, 3.5, 10.12, 3.5, lw=1.8, mutation=14)
    arrow(ax, 11.68, 3.5, 11.82, 3.5, lw=1.8, mutation=14)

    # Etiqueta artefactos entre flechas 5a->5b y 5b->5c
    float_label(ax, 10.05, 3.82, ".sddraft")
    float_label(ax, 11.75, 3.82, ".sd")

    # Nota error 00374
    rbox(ax, 10.9, 1.9, 4.5, 0.8, fc=DGRAY, ec=TEAL, lw=1.4)
    ax.text(10.9, 2.12, "Si Stage falla con error 00374:",
            ha='center', va='center', color=GRAY,
            fontsize=8.5, zorder=5)
    ax.text(10.9, 1.78,
            "_fix_layer_ids_sddraft()  ->  parchea XML  ->  reintentar",
            ha='center', va='center', color=TEAL2,
            fontsize=8, zorder=5)
    arrow(ax, 10.9, 3.0, 10.9, 2.32, lw=1.4, mutation=11)

    # Leyenda colores
    rbox(ax, 1.55, 1.6, 2.7, 0.55, fc=DGRAY, ec=TEAL2, lw=1)
    ax.text(1.55, 1.6, "Pasos preparatorios",
            ha='center', va='center', color=GRAY, fontsize=8, zorder=5)
    rbox(ax, 4.65, 1.6, 2.7, 0.55, fc=TEAL, ec=TEAL2, lw=1)
    ax.text(4.65, 1.6, "Ciclo de publicacion",
            ha='center', va='center', color=WHITE, fontsize=8, zorder=5)

    plt.tight_layout(pad=0.3)
    path = os.path.join(OUT, "flujo-publicacion-enterprise.png")
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor=NAVY2)
    plt.close()
    print("OK " + path)


# ════════════════════════════════════════════════════════════════════════════
# FLUJO 2 — Estrategia descarga BackupAGOL (in-post)
# ════════════════════════════════════════════════════════════════════════════
def flow_backup():
    fig, ax = plt.subplots(figsize=(11, 7.5))
    fig.patch.set_facecolor(NAVY2)
    ax.set_facecolor(NAVY2)
    ax.set_xlim(0, 11); ax.set_ylim(0, 7.5)
    ax.axis('off')
    gradient_bg(ax, fig)

    ax.text(5.5, 7.1, "Estrategia de descarga — BackupAGOL",
            ha='center', va='center', color=WHITE,
            fontsize=14, fontweight='bold')

    # Nodo inicial
    rbox(ax, 5.5, 6.1, 2.6, 0.72, fc=TEAL, ec=TEAL2, lw=2)
    ax.text(5.5, 6.1, "Item AGOL",
            ha='center', va='center', color=WHITE,
            fontsize=12, fontweight='bold', zorder=5)
    arrow(ax, 5.5, 5.74, 5.5, 5.2)

    # Rombo decision (mas grande y claro)
    dx, dy, dw, dh = 5.5, 4.7, 1.5, 0.85
    diamond = plt.Polygon(
        [[dx, dy+dh], [dx+dw, dy], [dx, dy-dh], [dx-dw, dy]],
        facecolor=MGRAY, edgecolor=TEAL2, linewidth=2, zorder=4)
    ax.add_patch(diamond)
    ax.text(dx, dy + 0.22, "Tipo", ha='center', va='center',
            color=WHITE, fontsize=10, fontweight='bold', zorder=5)
    ax.text(dx, dy - 0.22, "de item?", ha='center', va='center',
            color=GRAY, fontsize=9, zorder=5)

    # Rama izquierda — descarga directa
    ax.text(2.5, 4.95, "Web Map · Dashboard\nNotebook · Shapefile · PDF",
            ha='center', va='center', color=GRAY, fontsize=8, zorder=5)
    arrow(ax, 4.0, 4.7, 3.4, 4.7, lw=1.6, mutation=12)

    rbox(ax, 2.2, 3.6, 3.2, 0.85, fc=TEAL, ec=TEAL2, lw=2)
    ax.text(2.2, 3.72, "Descarga directa",
            ha='center', va='center', color=WHITE,
            fontsize=11, fontweight='bold', zorder=5)
    ax.text(2.2, 3.42, "item.download()",
            ha='center', va='center', color=NAVY,
            fontsize=8.5, zorder=5)
    arrow(ax, 2.2, 3.17, 2.2, 2.52)

    rbox(ax, 2.2, 2.15, 3.2, 0.72, fc=DGRAY, ec=TEAL, lw=1.5)
    ax.text(2.2, 2.28, "archivo descargado",
            ha='center', va='center', color=TEAL2,
            fontsize=9, fontweight='bold', zorder=5)
    ax.text(2.2, 2.02, "+ .json con metadatos",
            ha='center', va='center', color=GRAY,
            fontsize=8, zorder=5)

    # Rama derecha — exportacion
    ax.text(8.5, 4.95, "Feature Service\nFeature Layer · Table",
            ha='center', va='center', color=GRAY, fontsize=8, zorder=5)
    arrow(ax, 7.0, 4.7, 7.6, 4.7, lw=1.6, mutation=12)

    rbox(ax, 8.8, 3.6, 3.2, 0.85, fc=TEAL, ec=TEAL2, lw=2)
    ax.text(8.8, 3.72, "Exportar a FGDB",
            ha='center', va='center', color=WHITE,
            fontsize=11, fontweight='bold', zorder=5)
    ax.text(8.8, 3.42, "item.export(wait=True)",
            ha='center', va='center', color=NAVY,
            fontsize=8.5, zorder=5)
    arrow(ax, 8.8, 3.17, 8.8, 2.52)

    rbox(ax, 8.8, 2.15, 3.2, 0.72, fc=DGRAY, ec=TEAL, lw=1.5)
    ax.text(8.8, 2.28, "descargar + eliminar",
            ha='center', va='center', color=TEAL2,
            fontsize=9, fontweight='bold', zorder=5)
    ax.text(8.8, 2.02, "exportacion temporal de AGOL",
            ha='center', va='center', color=GRAY,
            fontsize=8, zorder=5)

    # Convergencia al manifiesto con lineas ortogonales
    mid_y = 0.9
    # Izquierda baja -> linea horizontal al centro
    ax.plot([2.2, 2.2], [1.79, mid_y + 0.15], color=TEAL2, lw=1.6, zorder=3)
    ax.plot([2.2, 5.5], [mid_y + 0.15, mid_y + 0.15], color=TEAL2, lw=1.6, zorder=3)
    # Derecha baja -> linea horizontal al centro
    ax.plot([8.8, 8.8], [1.79, mid_y + 0.15], color=TEAL2, lw=1.6, zorder=3)
    ax.plot([8.8, 5.5], [mid_y + 0.15, mid_y + 0.15], color=TEAL2, lw=1.6, zorder=3)
    arrow(ax, 5.5, mid_y + 0.15, 5.5, mid_y + 0.54, lw=1.6, mutation=13)

    # Nodo manifest final
    rbox(ax, 5.5, 0.68, 4.2, 0.65, fc=MGRAY, ec=TEAL2, lw=2)
    ax.text(5.5, 0.8, "manifest.json",
            ha='center', va='center', color=TEAL2,
            fontsize=11, fontweight='bold', zorder=5)
    ax.text(5.5, 0.52, "entrada registrada por item",
            ha='center', va='center', color=GRAY,
            fontsize=8, zorder=5)

    plt.tight_layout(pad=0.3)
    path = os.path.join(OUT, "flujo-backup-estrategia.png")
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor=NAVY2)
    plt.close()
    print("OK " + path)


# ════════════════════════════════════════════════════════════════════════════
# COVER 3 — DataStore Validation  (editorial, 16:7)
# ════════════════════════════════════════════════════════════════════════════
def cover_datastores():
    fig, ax = plt.subplots(figsize=(12, 5.25))
    fig.patch.set_facecolor(NAVY2)
    ax.set_facecolor(NAVY2)
    ax.set_xlim(0, 12); ax.set_ylim(0, 5.25)
    ax.axis('off')
    gradient_bg(ax, fig, NAVY2, NAVY)

    # Barra acento izquierda
    ax.add_patch(plt.Rectangle((0, 0), 0.22, 5.25,
                                facecolor=TEAL, zorder=5))

    # --- Bloque texto izquierdo ---
    ax.text(0.6, 4.5, "ARCPY · ARCGIS SERVER", color=TEAL2,
            fontsize=8, fontweight='bold', va='center', zorder=5)
    ax.text(0.6, 3.6,
            "Validacion de Data Stores\nen ArcGIS Enterprise",
            color=WHITE, fontsize=19, fontweight='bold',
            va='center', linespacing=1.25, zorder=5)
    ax.text(0.6, 2.72,
            "Monitoreo automatico · Alertas SMTP · Multi-servidor",
            color=GRAY, fontsize=9, va='center', zorder=5)

    # Metrica destacada
    rbox(ax, 1.85, 1.72, 3.0, 0.75, fc=MGRAY, ec=TEAL, lw=1.5)
    ax.text(1.85, 1.87, "4 servidores · 2 tipos",
            ha='center', va='center', color=TEAL2,
            fontsize=11, fontweight='bold', zorder=5)
    ax.text(1.85, 1.54, "FOLDER + DATABASE validados",
            ha='center', va='center', color=GRAY,
            fontsize=8, zorder=5)

    # Divisor
    ax.plot([4.8, 4.8], [0.4, 4.85], color=TEAL, lw=0.8, alpha=0.35, zorder=3)

    # --- Diagrama derecho: 3 etapas clave ---
    stages = [
        (6.3,  3.6, "Listar Items",    "ListDataStoreItems"),
        (8.65, 3.6, "Validar",         "ValidateDataStoreItem"),
        (11.0, 3.6, "Alertar",         "send_alert via SMTP"),
    ]
    for (x, y, lbl, sub) in stages:
        rbox(ax, x, y, 2.7, 1.1, fc=TEAL, ec=TEAL2, lw=2)
        ax.text(x, y + 0.18, lbl,
                ha='center', va='center', color=WHITE,
                fontsize=13, fontweight='bold', zorder=5)
        ax.text(x, y - 0.20, sub,
                ha='center', va='center', color=NAVY,
                fontsize=8, zorder=5)

    arrow(ax, 7.65, 3.6, 8.15, 3.6, lw=2, mutation=16)
    arrow(ax, 9.98, 3.6, 10.48, 3.6, lw=2, mutation=16)

    # Labels de flujo sobre las flechas
    ax.text(7.9, 3.85, "items[]", ha='center', va='center',
            color=GRAY, fontsize=7.5, zorder=5)
    ax.text(10.23, 3.85, "validity != 'valid'",
            ha='center', va='center', color=GRAY, fontsize=7.5, zorder=5)

    # Nodo de entrada (servidores)
    rbox(ax, 8.65, 1.9, 6.8, 0.62, fc=DGRAY, ec=TEAL, lw=1.2)
    ax.text(8.65, 2.06, "CONEXIONES DE SERVIDOR",
            ha='center', va='center', color=TEAL2,
            fontsize=7.5, fontweight='bold', zorder=5)
    ax.text(8.65, 1.78,
            "prod1.ags  ·  prod2.ags  ·  prod3.ags  ·  prod4.ags",
            ha='center', va='center', color=GRAY, fontsize=7.5, zorder=5)

    plt.tight_layout(pad=0)
    path = os.path.join(OUT, "cover-datastores-arcgis-server.png")
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor=NAVY2)
    plt.close()
    print("OK " + path)


# ════════════════════════════════════════════════════════════════════════════
# FLUJO 3 — Validacion DataStores (in-post, horizontal)
# ════════════════════════════════════════════════════════════════════════════
def flow_datastores():
    fig, ax = plt.subplots(figsize=(13, 5.5))
    fig.patch.set_facecolor(NAVY2)
    ax.set_facecolor(NAVY2)
    ax.set_xlim(0, 13); ax.set_ylim(0, 5.5)
    ax.axis('off')
    gradient_bg(ax, fig)

    ax.text(6.5, 5.1, "Flujo de validacion — validate_datastores.py",
            ha='center', va='center', color=WHITE,
            fontsize=14, fontweight='bold')

    # Paso 1 — Inicio / cargar conexiones (DGRAY)
    step_box(ax, 1.2, 3.7, 1.85, 1.0, 1, "Cargar\nconexiones",
             fc=DGRAY, ec=TEAL2)
    ax.text(1.2, 2.95, "lista de .ags",
            ha='center', va='center', color=GRAY, fontsize=7.5)

    # Paso 2 — Para cada servidor (DGRAY)
    step_box(ax, 3.3, 3.7, 1.85, 1.0, 2, "Para cada\nservidor",
             fc=DGRAY, ec=TEAL2)
    ax.text(3.3, 2.95, ".ags file",
            ha='center', va='center', color=GRAY, fontsize=7.5)

    # Paso 3 — ListDataStoreItems (TEAL, activo)
    step_box(ax, 5.5, 3.7, 1.95, 1.0, 3, "ListDataStore\nItems",
             fc=TEAL, ec=TEAL2, active=True)
    ax.text(5.5, 2.95, "FOLDER + DATABASE",
            ha='center', va='center', color=GRAY, fontsize=7.5)

    # Paso 4 — ValidateDataStoreItem (TEAL, activo)
    step_box(ax, 7.7, 3.7, 1.95, 1.0, 4, "Validate\nDataStoreItem",
             fc=TEAL, ec=TEAL2, active=True)
    ax.text(7.7, 2.95, "por cada item",
            ha='center', va='center', color=GRAY, fontsize=7.5)

    # Flechas pasos 1..4
    arrow(ax, 2.12, 3.7, 2.37, 3.7)
    arrow(ax, 4.22, 3.7, 4.52, 3.7)
    arrow(ax, 6.48, 3.7, 6.72, 3.7)

    # Rombo decision (valido?)
    dx, dy, dw, dh = 9.8, 3.7, 0.95, 0.72
    diamond = plt.Polygon(
        [[dx, dy+dh], [dx+dw, dy], [dx, dy-dh], [dx-dw, dy]],
        facecolor=MGRAY, edgecolor=TEAL2, linewidth=2, zorder=4)
    ax.add_patch(diamond)
    ax.text(dx, dy + 0.22, "valid?", ha='center', va='center',
            color=WHITE, fontsize=9, fontweight='bold', zorder=5)
    ax.text(dx, dy - 0.22, "", ha='center', zorder=5)
    arrow(ax, 8.68, 3.7, 8.85, 3.7)

    # Rama SI — log OK (derecha del rombo)
    rbox(ax, 11.6, 3.7, 1.9, 0.85, fc=DGRAY, ec=TEAL2, lw=1.5)
    ax.text(11.6, 3.78, "log INFO",
            ha='center', va='center', color=WHITE,
            fontsize=10, fontweight='bold', zorder=5)
    ax.text(11.6, 3.52, "[store] name: VALID",
            ha='center', va='center', color=GRAY, fontsize=8, zorder=5)
    arrow(ax, 10.75, 3.7, 10.65, 3.7)
    ax.text(11.1, 3.95, "SI", ha='center', va='center',
            color=TEAL2, fontsize=9, fontweight='bold', zorder=5)

    # Rama NO — send_alert (abajo del rombo)
    rbox(ax, 9.8, 1.9, 2.6, 0.85, fc=TEAL, ec=TEAL2, lw=2)
    ax.text(9.8, 2.0, "send_alert()",
            ha='center', va='center', color=WHITE,
            fontsize=11, fontweight='bold', zorder=5)
    ax.text(9.8, 1.73, "correo con detalle del fallo",
            ha='center', va='center', color=NAVY, fontsize=8, zorder=5)
    ax.plot([9.8, 9.8], [2.98, 2.35], color=TEAL2, lw=1.6, zorder=3)
    ax.annotate("", xy=(9.8, 2.35), xytext=(9.8, 2.98),
                arrowprops=dict(arrowstyle="-|>", color=TEAL2,
                                lw=1.6, mutation_scale=14), zorder=4)
    ax.text(9.3, 2.6, "NO", ha='center', va='center',
            color=TEAL2, fontsize=9, fontweight='bold', zorder=5)

    # Leyenda
    rbox(ax, 1.55, 1.6, 2.7, 0.55, fc=DGRAY, ec=TEAL2, lw=1)
    ax.text(1.55, 1.6, "Pasos de control",
            ha='center', va='center', color=GRAY, fontsize=8, zorder=5)
    rbox(ax, 4.65, 1.6, 2.7, 0.55, fc=TEAL, ec=TEAL2, lw=1)
    ax.text(4.65, 1.6, "Llamadas ArcPy",
            ha='center', va='center', color=WHITE, fontsize=8, zorder=5)

    plt.tight_layout(pad=0.3)
    path = os.path.join(OUT, "flujo-datastores-arcgis-server.png")
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor=NAVY2)
    plt.close()
    print("OK " + path)


if __name__ == "__main__":
    cover_enterprise()
    cover_agol()
    flow_enterprise()
    flow_backup()
    cover_datastores()
    flow_datastores()
    print("\nTodos los diagramas generados.")
