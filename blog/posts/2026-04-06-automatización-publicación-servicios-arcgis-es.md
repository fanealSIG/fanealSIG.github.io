# Automatizando la publicación de servicios en ArcGIS Enterprise con Python

Publicar servicios web en ArcGIS Enterprise de forma manual implica entre 8 y 15 pasos en ArcGIS Pro por cada mapa: abrir el proyecto, importar el documento, configurar propiedades del servicio, generar el borrador, compilarlo, subirlo al servidor y verificar que quedó disponible. En entornos con múltiples capas y grupos de trabajo, ese proceso se repite decenas o cientos de veces.

En este post describo cómo resolví ese problema construyendo un **Python Toolbox (.pyt)** que automatiza el ciclo completo de publicación, reduciendo el tiempo de más de 10 minutos por servicio a menos de 5, y permitiendo publicaciones masivas sin intervención manual.

---

## ¿Qué es un Python Toolbox?

Un archivo `.pyt` es un script Python que ArcGIS Pro reconoce como caja de herramientas de geoprocesamiento. Sus herramientas aparecen en el panel **Catalog** con la misma interfaz de formulario que las herramientas nativas de Esri: parámetros tipados, validación automática y mensajes en tiempo de ejecución.

La ventaja principal es que el usuario final puede ejecutar el proceso sin tocar ninguna línea de código.

---

## Herramientas utilizadas

- **ArcPy** — librería Python de Esri incluida en ArcGIS Pro
- **Python Toolbox (.pyt)** — interfaz gráfica integrada en ArcGIS Pro
- **ArcGIS Enterprise 11.x** — servidor ArcGIS Server federado con Portal
- **REST API del Portal** — para gestión de carpetas en *My Content*

---

## Estructura del toolbox

El `.pyt` expone dos herramientas y un conjunto de funciones auxiliares compartidas:

| Componente | Tipo | Descripción |
|---|---|---|
| `PublicarServicio` | Herramienta | Publicación individual de un MXD o MAPX |
| `PublicarMasivo` | Herramienta | Publicación masiva desde estructura de subcarpetas con reporte CSV |
| `_gestionar_carpeta_portal()` | Función | Verifica y crea carpetas en el portal vía REST API |
| `_portal_token()` | Función | Obtiene token de autenticación REST |
| `_fix_layer_ids_sddraft()` | Función | Fallback XML para error 00374 |
| `_ssl_ctx()` | Función | Llamadas HTTP con SSL sin verificación (certificados autofirmados) |
| `msg_step / msg_ok / msg_error` | Funciones | Mensajería unificada a ArcGIS Messages y consola Python |

> **Nota:** las funciones auxiliares deben declararse **antes** de `class Toolbox` en el archivo `.pyt`. ArcGIS Pro carga el módulo de forma diferente al intérprete estándar y las funciones definidas después de las clases no están disponibles en tiempo de ejecución.

---

![Ciclo de publicación automatizado en ArcGIS Enterprise](images/flujo-publicacion-enterprise.png)
*Ciclo completo: validación → importación → conexión al portal → gestión de carpetas → SDDraft → Stage → Upload*

## El ciclo de publicación: SDDraft → Stage → Upload

El proceso tiene tres etapas que ArcPy ejecuta en secuencia:

1. **SDDraft** — genera la definición XML del servicio
2. **Stage** — compila el SDDraft en un archivo `.sd`
3. **Upload** — sube el `.sd` al servidor federado y activa el servicio

```python
import arcpy
import os

def publicar_servicio(aprx_base, ruta_mxd, nombre_servicio,
                      portal_url, server_url, carpeta=None,
                      tipo_svc="MAP_IMAGE", sobrescribir=True):
    """
    Publica un documento de mapa como servicio en ArcGIS Enterprise.

    Parámetros:
        aprx_base      : Ruta a un proyecto .aprx en blanco (plantilla)
        ruta_mxd       : Ruta al archivo .mxd o .mapx a publicar
        nombre_servicio: Nombre del servicio (sin espacios)
        portal_url     : URL del Portal (ej. https://enterprise.example.com/portal)
        server_url     : URL del servidor federado
        carpeta        : Carpeta destino en Portal y Server (None = raíz)
        tipo_svc       : MAP_IMAGE, FEATURE o TILE
        sobrescribir   : Si True, sobreescribe el servicio existente
    """
    import tempfile, shutil

    # Copiar el APRX base para no modificar el original
    dir_temp = tempfile.mkdtemp()
    ruta_aprx = os.path.join(dir_temp, "trabajo.aprx")
    shutil.copy(aprx_base, ruta_aprx)

    aprx = arcpy.mp.ArcGISProject(ruta_aprx)

    # Detectar el mapa importado comparando antes y después
    mapas_antes = set(m.name for m in aprx.listMaps())
    aprx.importDocument(ruta_mxd)
    aprx.save()
    aprx = arcpy.mp.ArcGISProject(ruta_aprx)
    mapas_despues = set(m.name for m in aprx.listMaps())

    nombre_mapa = (mapas_despues - mapas_antes).pop()
    mapa = aprx.listMaps(nombre_mapa)[0]

    # Conectar al portal
    arcpy.SignInToPortal(portal_url, "usuario", "contrasena")

    # Rutas temporales para los archivos intermedios
    ruta_sddraft = os.path.join(dir_temp, f"{nombre_servicio}.sddraft")
    ruta_sd      = os.path.join(dir_temp, f"{nombre_servicio}.sd")

    # Paso 1: Generar SDDraft
    draft = mapa.getWebLayerSharingDraft(
        server_type="FEDERATED_SERVER",
        service_type=tipo_svc,
        service_name=nombre_servicio
    )
    draft.federatedServerUrl        = server_url
    draft.overwriteExistingService  = sobrescribir
    draft.copyDataToServer          = False   # los datos deben estar registrados como Data Store
    draft.portalFolder              = carpeta or ""
    draft.serverFolder              = carpeta or ""

    if tipo_svc == "MAP_IMAGE":
        draft.checkUniqueIDAssignment = False  # evita error 00374 en MXDs antiguos

    draft.exportToSDDraft(ruta_sddraft)

    # Paso 2: Stage
    try:
        arcpy.server.StageService(ruta_sddraft, ruta_sd)
    except Exception as e:
        if "00374" in str(e):
            # Fallback: parchar IDs en el XML y reintentar
            _fix_layer_ids_sddraft(ruta_sddraft)
            arcpy.server.StageService(ruta_sddraft, ruta_sd)
        else:
            raise

    # Paso 3: Upload
    # in_folder_type determina cómo ArcGIS Server trata la carpeta destino
    if not carpeta:
        folder_type = "ROOT"
    elif sobrescribir:
        folder_type = "EXISTING"
    else:
        folder_type = "NEW"

    arcpy.server.UploadServiceDefinition(
        in_sd_file=ruta_sd,
        in_server=server_url,
        in_folder_type=folder_type,
        in_folder=carpeta or "",
        in_override="OVERRIDE_DEFINITION",
        in_public="PUBLIC",
        in_organization="SHARE_ORGANIZATION"
    )

    print(f"✅ '{nombre_servicio}' publicado.")
```

---

## Herramienta 1: Publicar Servicio (individual)

Expone la función anterior como herramienta de geoprocesamiento con formulario en ArcGIS Pro. Útil para publicaciones puntuales o para verificar la configuración antes de ejecutar un lote.

```python
class PublicarServicio(object):
    def __init__(self):
        self.label = "Publicar Servicio desde MXD o MAPX"
        self.description = "Publica un único documento de mapa como servicio web en ArcGIS Enterprise."

    def getParameterInfo(self):
        params = [
            arcpy.Parameter(displayName="Formato del archivo fuente",
                            name="formato", datatype="GPString",
                            parameterType="Required", direction="Input"),
            arcpy.Parameter(displayName="Archivo MXD o MAPX",
                            name="archivo", datatype="DEFile",
                            parameterType="Required", direction="Input"),
            arcpy.Parameter(displayName="APRX base (proyecto en blanco)",
                            name="aprx_base", datatype="DEFile",
                            parameterType="Required", direction="Input"),
            arcpy.Parameter(displayName="URL del Portal",
                            name="portal_url", datatype="GPString",
                            parameterType="Required", direction="Input"),
            arcpy.Parameter(displayName="URL del Server federado",
                            name="server_url", datatype="GPString",
                            parameterType="Required", direction="Input"),
            arcpy.Parameter(displayName="Usuario del Portal",
                            name="usuario", datatype="GPString",
                            parameterType="Required", direction="Input"),
            arcpy.Parameter(displayName="Contraseña del Portal",
                            name="contrasena", datatype="GPStringHidden",
                            parameterType="Required", direction="Input"),
            arcpy.Parameter(displayName="Nombre del Servicio",
                            name="nombre_svc", datatype="GPString",
                            parameterType="Required", direction="Input"),
            arcpy.Parameter(displayName="Carpeta Portal/Server",
                            name="carpeta", datatype="GPString",
                            parameterType="Optional", direction="Input"),
            arcpy.Parameter(displayName="Tipo de servicio",
                            name="tipo_svc", datatype="GPString",
                            parameterType="Required", direction="Input"),
            arcpy.Parameter(displayName="Sobrescribir servicio",
                            name="sobrescribir", datatype="GPBoolean",
                            parameterType="Optional", direction="Input"),
        ]
        params[0].filter.list = ["MXD (ArcMap)", "MAPX (ArcGIS Pro)"]
        params[9].filter.list = ["MAP_IMAGE", "FEATURE", "TILE"]
        params[9].value       = "MAP_IMAGE"
        params[10].value      = True
        return params

    def execute(self, parameters, messages):
        publicar_servicio(
            aprx_base       = parameters[2].valueAsText,
            ruta_mxd        = parameters[1].valueAsText,
            nombre_servicio = parameters[7].valueAsText,
            portal_url      = parameters[3].valueAsText,
            server_url      = parameters[4].valueAsText,
            carpeta         = parameters[8].valueAsText,
            tipo_svc        = parameters[9].valueAsText,
            sobrescribir    = parameters[10].value
        )
```

> **Seguridad:** `GPStringHidden` enmascara la contraseña en el formulario y la excluye del historial de geoprocesamiento. Las credenciales no se escriben a disco en ningún momento.

---

## Herramienta 2: Publicación Masiva

Recorre una carpeta raíz con subcarpetas y publica todos los MXD/MAPX encontrados. El nombre de cada subcarpeta se usa directamente como nombre de carpeta en el Portal y en ArcGIS Server. Genera un reporte CSV al finalizar.

### Estructura de carpetas esperada

```
Carpeta_raiz/
  Grupo_A/                  <-- carpeta en Portal y Server
    mapa_01.mxd
    mapa_02.mxd
  Grupo_B/
    mapa_03.mxd
  mapa_suelto.mxd           <-- archivos en raíz: sin carpeta asignada
```

### Flujo de ejecución

| Paso | Nombre | Descripción |
|---|---|---|
| 1 | Escanear subcarpetas | Recorre la carpeta raíz e informa el total de archivos antes de iniciar |
| 2 | Conectar al Portal | `arcpy.SignInToPortal()` una sola vez para todo el lote |
| 3 | Pre-crear carpetas | Gestiona todas las carpetas del Portal antes de publicar cualquier servicio |
| 4 | Publicar por subcarpeta | Para cada archivo: importa el mapa, genera SDDraft, Stage y Upload |
| 5 | Reporte final | Muestra totales (exitosos/fallidos) y genera CSV con marca de tiempo |

### Reporte CSV

El archivo `reporte_masivo_YYYYMMDD_HHMMSS.csv` contiene:

| Columna | Contenido |
|---|---|
| `subcarpeta` | Nombre de la subcarpeta. `(raíz)` para archivos sin subcarpeta |
| `archivo` | Nombre del MXD o MAPX procesado |
| `servicio` | Nombre del servicio publicado |
| `estado` | `EXITOSO` o `ERROR` |
| `detalle` | Duración si exitoso; mensaje de excepción si error |
| `duracion_s` | Duración en segundos |

---

## Errores conocidos y soluciones

Durante el desarrollo surgieron varios errores no documentados en la documentación oficial de Esri. El toolbox los maneja internamente, pero vale la pena conocerlos:

| Error | Causa | Solución |
|---|---|---|
| `'Layout' object has no attribute 'listLayers'` | `importDocument()` retorna un `Layout` en MXDs con página de diseño | No usar el retorno directo; detectar el mapa nuevo comparando `listMaps()` antes y después del import |
| `Please check input parameters: 'targetServer'` | La propiedad `targetServer` no existe en ArcGIS Pro 3.x | Usar `federatedServerUrl` según la documentación actual de Esri |
| `Incompatible server_type HOSTING_SERVER with MAP_IMAGE` | `HOSTING_SERVER` no admite servicios MAP_IMAGE | Usar siempre `FEDERATED_SERVER` para publicar en ArcGIS Server federado |
| `ERROR 00374: Unique numeric IDs not assigned` | MXDs creados en versiones antiguas de ArcMap sin IDs numéricos | (1) `checkUniqueIDAssignment=False` en el `SharingDraft`; (2) si igual falla, parchear el XML del SDDraft con `_fix_layer_ids_sddraft()` y reintentar Stage |
| `SSL: CERTIFICATE_VERIFY_FAILED` | Enterprise on-premise usa certificados autofirmados que Python rechaza | Todas las llamadas REST usan contexto SSL con `check_hostname=False` y `CERT_NONE` |
| `in_folder_type=EXISTING` falla en primera publicación | Sí la carpeta no existe aún en ArcGIS Server, `EXISTING` lanza error | Lógica dinámica: `ROOT` (sin carpeta), `EXISTING` (sobrescribir), `NEW` (primera vez en esa carpeta) |

---

## Consideraciones técnicas

**APRX base:** el toolbox requiere un proyecto ArcGIS Pro en blanco sin mapas ni capas. Se copia por cada servicio que se publica; el original no se modifica nunca. Una sola copia compartida en red es suficiente para todo el equipo.

**Datos registrados:** el toolbox asume `copyDataToServer=False`, lo que significa que las capas deben tener sus datos registrados como **Data Stores** en ArcGIS Server. Si los datos no están registrados, `StageService` fallará. Para registrar: *ArcGIS Server Manager > Site > Data Stores > Register*.

**Separación Portal/Server:** en ArcGIS Enterprise existen dos espacios de carpetas independientes. El toolbox los gestiona de forma coordinada asignando el mismo nombre a `portalFolder` (vía REST API) y `serverFolder` (vía `UploadServiceDefinition`).

**Directorio temporal:** por cada servicio se generan dos archivos intermedios (`.sddraft` y `.sd`). En la publicación masiva cada servicio usa su propio subdirectorio para evitar colisiones de nombres. El toolbox no limpia el temporal al finalizar, lo que permite inspeccionar los archivos en caso de error.

---

## Resultados

| Capacidad | Sin toolbox | Con toolbox |
|---|---|---|
| Publicar 1 servicio | 8-15 pasos manuales | 1 ejecución del formulario |
| Publicar 50 servicios | Proceso repetido 50 veces | 1 ejecución masiva |
| Crear carpetas en el portal | Manual en el portal web | Automático vía REST API |
| Trazabilidad | Ninguna | Reporte CSV por lote |

El tiempo de publicación individual pasó de más de 10 minutos a menos de 5, eliminando errores de configuración manual y dejando un registro auditable de cada publicación.

---

*¿Tienes preguntas o mejoras? Escríbeme a [faneal14@gmail.com](mailto:faneal14@gmail.com) o en [LinkedIn](https://linkedin.com/in/faneal).*

<span class="post-ai-note">Redactado con asistencia de IA generativa · Código revisado y validado en producción</span>
