# Extraccion y catalogacion de archivos fuente desde arcgisinput en ArcGIS Server

ArcGIS Server almacena los documentos fuente de los servicios publicados —archivos `.mxd` y `.mapx`— en una carpeta llamada `arcgisinput`, organizada por subcarpetas que corresponden a grupos del catálogo de servicios. Cada servicio genera su propia subcarpeta interna con el patrón `NombreServicio.MapServer/`, que es la ruta que el servidor usa internamente, no el nombre que el equipo conoce.

Cuando surgió la necesidad de auditar y reorganizar los archivos fuente de decenas de servicios, navegar esa estructura a mano era lento y propenso a errores. Construí un script que recorre `arcgisinput` de forma recursiva, extrae todos los `.mxd` y `.mapx`, los renombra con el nombre del servicio al que pertenecen y los copia a una estructura limpia en el escritorio, junto con un reporte Excel del inventario completo.

---

## El problema

La situacion concreta: multiples subcarpetas en `arcgisinput` con archivos fuente cuyos nombres internos no coinciden necesariamente con los nombres de los servicios publicados. El proceso manual era:

- Abrir el explorador de archivos y navegar por `arcgisinput`
- Identificar visualmente la carpeta `NombreServicio.MapServer` correcta para cada servicio
- Copiar el `.mxd` o `.mapx` a una ubicacion de trabajo con el nombre correcto
- Repetir por cada servicio involucrado, sin ningún registro de lo que se copió

Sin un inventario estructurado, era fácil confundir versiones o perder de vista qué archivos correspondían a qué servicios activos.

---

## Herramientas utilizadas

- **os / os.walk** — recorrido recursivo del sistema de archivos sin dependencias externas
- **shutil.copy2** — copia de archivos preservando metadatos de sistema operativo
- **pandas** — generacion del reporte Excel con el inventario completo de rutas y nombres

---

![Flujo de extraccion MXD MAPX](images/flujo-extraccion-mxd-mapx.png)
*El script recorre arcgisinput, detecta los archivos fuente, extrae el nombre del servicio desde la carpeta .MapServer y los copia organizados*

## Como funciona el script

El flujo tiene cuatro pasos:

1. **Recorrer el directorio** — `os.walk` itera recursivamente toda la estructura bajo `arcgisinput`
2. **Filtrar por extension** — procesa solo archivos `.mxd` y `.mapx`, ignora el resto
3. **Determinar el nombre destino** — busca en la ruta el segmento que termina en `.MapServer` y usa la parte anterior como nombre del archivo destino; si no hay `.MapServer` en la ruta, conserva el nombre original como fallback
4. **Copiar y registrar** — copia el archivo a `MXD_new/<subcarpeta>/` o `MAPX_new/<subcarpeta>/`, agrega sufijo numerico si ya existe un archivo con ese nombre, y acumula la entrada en el inventario

La subcarpeta se determina por el nivel inmediatamente siguiente a `arcgisinput` en la ruta, lo que refleja la organización del catálogo de servicios.

---

## Codigo

```python
import os
import shutil
import pandas as pd


def extraer_archivos_fuente(directorio_raiz, carpeta_salida):
    """
    Recorre arcgisinput y copia todos los .mxd y .mapx a una
    estructura organizada por subcarpeta, renombrandolos con
    el nombre del servicio al que pertenecen.

    :param directorio_raiz: Ruta a la carpeta arcgisinput del servidor
    :param carpeta_salida:  Nombre de la carpeta destino en el escritorio
    """
    escritorio  = os.path.join(os.environ["USERPROFILE"], "Desktop")
    carpeta_mxd  = os.path.join(escritorio, carpeta_salida, "MXD_new")
    carpeta_mapx = os.path.join(escritorio, carpeta_salida, "MAPX_new")
    os.makedirs(carpeta_mxd,  exist_ok=True)
    os.makedirs(carpeta_mapx, exist_ok=True)

    nombre_raiz = os.path.basename(directorio_raiz).lower()
    resultados  = []

    for root, _, files in os.walk(directorio_raiz):
        for file in files:
            if not file.endswith((".mxd", ".mapx")):
                continue

            ruta_completa = os.path.join(root, file)
            partes = ruta_completa.replace("\\", "/").split("/")

            # Subcarpeta inmediatamente despues de arcgisinput
            try:
                idx = next(i for i, p in enumerate(partes)
                           if p.lower() == nombre_raiz)
                subcarpeta = partes[idx + 1]
            except (StopIteration, IndexError):
                subcarpeta = "sin_clasificar"

            # Nombre del servicio desde la carpeta .MapServer
            nombre_servicio = ""
            if ".MapServer" in root:
                segmentos_ms = [p for p in root.split(os.sep) if ".MapServer" in p]
                if segmentos_ms:
                    nombre_servicio = segmentos_ms[0].split(".MapServer")[0]

            ext = os.path.splitext(file)[1]
            nombre_destino = f"{nombre_servicio}{ext}" if nombre_servicio else file

            resultados.append({
                "Subcarpeta":      subcarpeta,
                "Servicio":        nombre_servicio,
                "Archivo origen":  file,
                "Archivo destino": nombre_destino,
                "Ruta completa":   ruta_completa,
            })

            base = carpeta_mxd if file.endswith(".mxd") else carpeta_mapx
            carpeta_final = os.path.join(base, subcarpeta)
            os.makedirs(carpeta_final, exist_ok=True)

            ruta_destino = os.path.join(carpeta_final, nombre_destino)
            if os.path.exists(ruta_destino):
                stem, ext2 = os.path.splitext(nombre_destino)
                contador = 1
                while os.path.exists(ruta_destino):
                    ruta_destino = os.path.join(carpeta_final, f"{stem}_{contador}{ext2}")
                    contador += 1

            try:
                shutil.copy2(ruta_completa, ruta_destino)
                print(f"Copiado: {os.path.basename(ruta_destino)}")
            except Exception as e:
                print(f"Error: {e}")

    excel_path = os.path.join(escritorio, "inventario_archivos_fuente.xlsx")
    pd.DataFrame(resultados).to_excel(excel_path, index=False)
    print(f"\nInventario guardado en: {excel_path}")


if __name__ == "__main__":
    directorio = r"C:\arcgisserver\directories\arcgisinput"  # ajustar segun el servidor
    carpeta    = "ArchivosServer_2026"
    extraer_archivos_fuente(directorio, carpeta)
```

---

## Resultados

| Tarea | Proceso manual | Con el script |
|---|---|---|
| Localizar archivos fuente de 50 servicios | 20-40 min navegando carpetas | < 2 min de ejecucion |
| Nombre de los archivos copiados | Nombre interno del servidor (a veces ilegible) | Nombre del servicio publicado |
| Organizacion por categoria | Manual, propenso a errores | Automatica por subcarpeta de arcgisinput |
| Inventario documentado | Inexistente o en Excel manual | Excel generado automaticamente con rutas completas |
| Conflictos de nombre | Sin control | Sufijo numerico automatico |

---

## Compatibilidad con ambientes federados

El script accede directamente al sistema de archivos del servidor —no usa ArcPy ni hace llamadas REST— por lo que funciona igual en ambientes federados y no federados. Solo requiere acceso de lectura a la carpeta `arcgisinput`.

El punto crítico en entornos federados es **desde dónde se ejecuta el script**:

| Escenario | ¿Funciona? | Nota |
|---|---|---|
| Ejecución en el mismo servidor ArcGIS Server | Sí, siempre | Acceso local directo a `arcgisinput` |
| Ejecución remota vía ruta UNC compartida | Sí, si el share está habilitado | Requiere permisos de lectura de red |
| Ejecución en máquina sin acceso al share | No | `os.walk` no puede recorrer la ruta |

En infraestructuras federadas, `arcgisinput` suele estar en el directorio de datos del servidor. Si el share no está habilitado por defecto, el administrador puede exponerlo como carpeta compartida de red con permisos de solo lectura:

```
# Ruta local — ejecución directa en el servidor
C:\arcgisserver\directories\arcgisinput

# Ruta UNC — ejecución remota (requiere share habilitado)
\\nombre-servidor\arcgisinput
```

El script no escribe nada en `arcgisinput`; toda la salida va al escritorio del usuario que lo ejecuta. No hay riesgo de alterar los archivos del servidor.

---

## Próximos pasos

- Agregar filtro por fecha de modificación para procesar solo archivos actualizados recientemente
- Generar un reporte adicional que liste los servicios del catálogo REST sin archivo fuente localizado en `arcgisinput`
- Encapsular como Python Toolbox para ejecutarlo directamente desde ArcGIS Pro con interfaz gráfica
- Extender para incluir archivos `.lyrx` y `.stylx` que también se almacenan en el directorio del servidor

---

*¿Tienes preguntas o mejoras? Escríbeme a [faneal14@gmail.com](mailto:faneal14@gmail.com) o en [LinkedIn](https://linkedin.com/in/faneal).*

<span class="post-ai-note">Redactado con asistencia de IA generativa · Código revisado y validado en producción</span>
