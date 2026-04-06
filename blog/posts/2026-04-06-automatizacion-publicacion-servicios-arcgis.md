# Automatizando la publicación de servicios en ArcGIS Enterprise con Python

Publicar servicios web en ArcGIS Enterprise de forma manual puede tomar entre 15 y 30 minutos por capa: abrir ArcGIS Pro, configurar propiedades del servicio, compartir, verificar que quedó disponible... y repetir. En entornos corporativos con múltiples capas y unidades de negocio, ese tiempo se multiplica rápidamente.

En este post comparto cómo resolví ese problema automatizando el ciclo completo de publicación con **Python Toolboxes** y **ArcPy**.

---

## El problema

En un entorno con más de 3 unidades de negocio y demanda continua de nuevos servicios web, el proceso manual era:

- Lento (~20 min por servicio en promedio)
- Propenso a errores de configuración (nombre incorrecto, carpeta equivocada, permisos)
- Difícil de auditar (¿quién publicó qué y cuándo?)

La solución obvia: automatizarlo.

---

## Herramientas utilizadas

- **ArcPy** — librería Python de ESRI incluida en ArcGIS Pro
- **Python Toolbox (.pyt)** — interfaz gráfica integrada en ArcGIS Pro
- **ArcGIS Enterprise 11.x** — servidor destino federado con Portal

---

## El flujo de publicación

El proceso tiene tres pasos que ArcPy puede ejecutar en secuencia:

1. Generar el borrador del servicio (`.sddraft`)
2. Empacar el servicio (`.sd`)
3. Subir y publicar en el servidor

```python
import arcpy
import os

def publicar_servicio(ruta_aprx, nombre_mapa, nombre_servicio, servidor_url):
    """
    Publica un mapa como servicio de imagen en ArcGIS Enterprise.
    
    Parámetros:
        ruta_aprx     : Ruta al archivo .aprx de ArcGIS Pro
        nombre_mapa   : Nombre del mapa dentro del proyecto
        nombre_servicio: Nombre que tendrá el servicio publicado
        servidor_url  : URL del servidor federado (ej. https://servidor/arcgis)
    """
    aprx = arcpy.mp.ArcGISProject(ruta_aprx)
    mapa = aprx.listMaps(nombre_mapa)[0]

    # Rutas temporales
    carpeta_temp  = os.environ.get("TEMP", os.getcwd())
    ruta_sddraft  = os.path.join(carpeta_temp, f"{nombre_servicio}.sddraft")
    ruta_sd       = os.path.join(carpeta_temp, f"{nombre_servicio}.sd")

    # 1. Crear borrador del servicio
    sharing_draft = mapa.getWebLayerSharingDraft(
        server_type="FEDERATED_SERVER",
        service_type="MAP_IMAGE",
        service_name=nombre_servicio,
        server=servidor_url
    )
    sharing_draft.overwriteExistingService = True
    sharing_draft.exportToSDDraft(ruta_sddraft)

    # 2. Empacar (Stage)
    arcpy.server.StageService(ruta_sddraft, ruta_sd)

    # 3. Subir y publicar
    arcpy.server.UploadServiceDefinition(
        in_sd_file=ruta_sd,
        in_server=servidor_url,
        in_override="OVERRIDE_DEFINITION",
        in_public="PUBLIC",
        in_organization="SHARE_ORGANIZATION"
    )

    print(f"✅ Servicio '{nombre_servicio}' publicado exitosamente.")
```

---

## Publicación en lote desde un CSV

Lo más útil: publicar múltiples servicios desde un archivo `.csv` con la lista de mapas.

```python
import csv

def publicar_desde_csv(ruta_aprx, ruta_csv, servidor_url):
    """
    Lee un CSV con columnas: nombre_mapa, nombre_servicio
    y publica cada uno automáticamente.
    """
    with open(ruta_csv, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for fila in reader:
            try:
                publicar_servicio(
                    ruta_aprx=ruta_aprx,
                    nombre_mapa=fila['nombre_mapa'],
                    nombre_servicio=fila['nombre_servicio'],
                    servidor_url=servidor_url
                )
            except Exception as e:
                print(f"❌ Error en '{fila['nombre_servicio']}': {e}")
```

El CSV se ve así:

```
nombre_mapa,nombre_servicio
Predios_Urbanos,svc_predios_urbanos
Red_Vial,svc_red_vial
Cobertura_Suelo,svc_cobertura_suelo
```

---

## Integrarlo como Python Toolbox

Para que el equipo pueda usarlo sin tocar código, lo envolví en un `.pyt`:

```python
class PublicarServicio(object):
    def __init__(self):
        self.label = "Publicar Servicio en Enterprise"
        self.description = "Automatiza la publicación de un mapa como servicio web."

    def getParameterInfo(self):
        return [
            arcpy.Parameter(displayName="Proyecto ArcGIS Pro (.aprx)",
                            name="aprx", datatype="DEFile",        parameterType="Required", direction="Input"),
            arcpy.Parameter(displayName="Nombre del Mapa",
                            name="mapa", datatype="GPString",      parameterType="Required", direction="Input"),
            arcpy.Parameter(displayName="Nombre del Servicio",
                            name="servicio", datatype="GPString",  parameterType="Required", direction="Input"),
            arcpy.Parameter(displayName="URL del Servidor",
                            name="servidor", datatype="GPString",  parameterType="Required", direction="Input"),
        ]

    def execute(self, parameters, messages):
        publicar_servicio(
            ruta_aprx=parameters[0].valueAsText,
            nombre_mapa=parameters[1].valueAsText,
            nombre_servicio=parameters[2].valueAsText,
            servidor_url=parameters[3].valueAsText
        )
```

---

## Resultados

Con este toolbox el equipo redujo el tiempo de publicación de ~20 min por servicio a menos de 3 min, eliminando errores manuales de configuración y dejando un registro trazable de cada publicación.

---

## Próximos pasos

- Agregar validación previa del mapa (capas rotas, fuentes de datos no disponibles)
- Registrar publicaciones en un log `.csv` automático
- Extender para Feature Services y Tile Layers

---

*¿Tienes preguntas o mejoras? Escríbeme a [faneal14@gmail.com](mailto:faneal14@gmail.com) o en [LinkedIn](https://linkedin.com/in/faneal).*
