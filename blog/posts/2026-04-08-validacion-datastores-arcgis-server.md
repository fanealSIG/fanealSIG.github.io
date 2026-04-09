# Validacion automatica de Data Stores en ArcGIS Server con Python

En una infraestructura de ArcGIS Enterprise con varios servidores de produccion, saber si los Data Stores registrados siguen siendo accesibles es critico. Una capa de base de datos o una carpeta de datos que pierde su conexion puede inutilizar decenas de servicios publicados sin que el equipo lo note hasta que un usuario reporta el fallo.

En este post describo como construi un script de monitoreo que valida automaticamente todos los items registrados — carpetas y bases de datos — en multiples servidores ArcGIS Server, y envia una alerta por correo cuando alguno no pasa la validacion.

---

## El problema

El proceso manual era: abrir ArcGIS Server Manager en cada nodo, navegar a *Data Stores*, revisar el estado de cada item registrado y anotar cualquier fallo. Con cuatro servidores de produccion y decenas de Data Stores por servidor, eso era trabajo repetitivo que nadie ejecutaba con la frecuencia necesaria.

Los riesgos concretos:

- Un Data Store que falla de madrugada no se detecta hasta el dia siguiente
- No hay trazabilidad de cuando ocurrio el fallo ni en cual servidor
- El correo de alerta hay que generarlo manualmente cuando se detecta algo

La solucion: automatizar la validacion con `arcpy.ValidateDataStoreItem` y programar el script como una tarea del sistema operativo.

---

## Herramientas utilizadas

- **ArcPy** — libreria Python de Esri incluida en ArcGIS Pro / ArcGIS Server
- **arcpy.ListDataStoreItems** — lista los items registrados por tipo en un servidor
- **arcpy.ValidateDataStoreItem** — verifica si un item de Data Store sigue siendo accesible
- **smtplib** — modulo estandar de Python para envio de alertas por SMTP
- **logging** — modulo estandar para trazabilidad estructurada en consola y log

---

![Flujo de validacion de Data Stores](images/flujo-datastores-arcgis-server.png)
*El script recorre cada servidor, valida todos los items y envia alerta solo cuando detecta un fallo*

## Como funciona el script

El flujo tiene tres pasos claros:

1. **Iterar conexiones** — recorre una lista de archivos `.ags`, uno por servidor
2. **Listar y validar** — para cada servidor llama a `ListDataStoreItems` (tipo `FOLDER` y `DATABASE`) y luego `ValidateDataStoreItem` por cada item encontrado
3. **Alertar** — si la validacion devuelve un estado distinto de `"valid"`, o si se lanza una excepcion, envia un correo con el detalle del fallo

---

## Codigo mejorado

El siguiente codigo es una version limpia y generalizada del script original. Se eliminaron imports no utilizados, se corrigio la importacion faltante de `time`, se centralizo la configuracion y se paso de variables globales a parametros explicitos.

```python
"""
validate_datastores.py
Validates all registered data stores (FOLDER and DATABASE) across
one or more ArcGIS Server connections and sends an email alert on failure.
"""
import arcpy
import os
import time
import smtplib
import logging
from email.mime.text import MIMEText

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

# ─── configuracion ────────────────────────────────────────────────────────────
SMTP_HOST    = "smtp-mail.outlook.com"
SMTP_PORT    = 587
SENDER_EMAIL = "gis@example.com"
ALERT_TO     = "alerts@example.com"

# Rutas a los archivos de conexion .ags (uno por servidor)
AGS_CONNECTIONS = [
    "connections/prod1.ags",
    "connections/prod2.ags",
    "connections/prod3.ags",
    "connections/prod4.ags",
]

STORE_TYPES = ["FOLDER", "DATABASE"]
# ──────────────────────────────────────────────────────────────────────────────


def get_smtp_password() -> str:
    """
    Retorna la contrasena SMTP del remitente.
    Reemplazar el cuerpo con la logica de recuperacion de credenciales
    que use tu organizacion (variable de entorno, secrets manager, etc.).
    """
    password = os.environ.get("GIS_MAIL_PASSWORD", "")
    if not password:
        raise EnvironmentError(
            "GIS_MAIL_PASSWORD environment variable is not set."
        )
    return password


def send_alert(subject: str, body: str) -> None:
    """Envia una alerta por SMTP cuando falla la validacion de un Data Store."""
    try:
        password = get_smtp_password()
        msg = MIMEText(f"\n{body}")
        msg["Subject"] = subject
        msg["From"]    = SENDER_EMAIL
        msg["To"]      = ALERT_TO

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, password)
            server.sendmail(SENDER_EMAIL, ALERT_TO, msg.as_string())

        log.info("Alerta enviada: %s", subject)
    except Exception as exc:
        log.error("Error al enviar alerta: %s", exc)


def validate_connection(ags_file: str) -> None:
    """
    Lista y valida todos los Data Store items de un servidor.

    :param ags_file: Ruta al archivo de conexion .ags
    """
    log.info("=== Servidor: %s ===", ags_file)

    for store_type in STORE_TYPES:
        log.info("-- Tipo: %s --", store_type)
        try:
            items = arcpy.ListDataStoreItems(ags_file, store_type)
        except Exception as exc:
            log.error("No se pudo listar %s en %s: %s", store_type, ags_file, exc)
            continue

        for item in items:
            name       = item[0]
            is_managed = (item[3] == "managed")

            try:
                validity = arcpy.ValidateDataStoreItem(
                    ags_file, store_type, name
                )
                status = "VALID" if validity == "valid" else validity.upper()
                info   = f"[{store_type}] {name}: {status}"
                if is_managed:
                    info += " (managed DB)"
                log.info(info)
                arcpy.AddMessage(info)

                if validity != "valid":
                    send_alert(
                        subject=f"[DataStore WARNING] {name} — {ags_file}",
                        body=(
                            f"Item '{name}' ({store_type}) "
                            f"reporto estado: {validity}\n"
                            f"Servidor: {ags_file}"
                        ),
                    )

            except Exception as exc:
                log.error("Error validando '%s': %s", name, exc)
                arcpy.AddError(f"Error validando '{name}': {exc}")
                send_alert(
                    subject=f"[DataStore ERROR] {name} — {ags_file}",
                    body=(
                        f"Excepcion al validar '{name}' ({store_type}):\n"
                        f"{exc}\nServidor: {ags_file}"
                    ),
                )


def main() -> None:
    log.info("Inicio: %s", time.strftime("%Y-%m-%d %H:%M:%S"))
    arcpy.AddMessage("Inicio: " + time.strftime("%Y-%m-%d %H:%M:%S"))

    for ags_file in AGS_CONNECTIONS:
        if not os.path.isfile(ags_file):
            log.warning("Archivo no encontrado, omitido: %s", ags_file)
            arcpy.AddWarning(f"Archivo no encontrado: {ags_file}")
            continue
        validate_connection(ags_file)

    log.info("Fin: %s", time.strftime("%Y-%m-%d %H:%M:%S"))
    arcpy.AddMessage("Fin: " + time.strftime("%Y-%m-%d %H:%M:%S"))


if __name__ == "__main__":
    main()
```

---

## Que se cambio respecto al original

| Problema original | Solucion aplicada |
|---|---|
| `import time` faltaba — `time.strftime()` fallaba en ejecucion | Agregado correctamente |
| 7 imports no utilizados (`calendar`, `datetime`, `httplib`, `urllib`, `json`, `sys`, `MIMEBase`, `MIMEMultipart`, `encoders`) | Eliminados |
| `import os` duplicado | Consolidado en una sola linea |
| Variables globales usadas dentro de funciones sin pasar como parametros | Configuracion centralizada en bloque de constantes al inicio del modulo |
| `get_param()` llamada dos veces para el mismo valor en `send_email` | Consolidado en una sola llamada |
| Bare `except:` sin capturar la excepcion | Reemplazado por `except Exception as exc:` con log del error |
| La cadena de if/elif para construir la ruta del servidor | Lista de archivos `.ags` directamente iterable |
| Receptor de alertas hardcodeado en el codigo | Extraido a constante `ALERT_TO` en la seccion de configuracion |
| Password recuperada en multiples pasos con logica de descifrado mezclada | Encapsulada en `get_smtp_password()` — facil de reemplazar con cualquier secrets manager |
| Bloque `with` ausente en `smtplib.SMTP` — conexion no se cerraba en caso de error | Reemplazado por `with smtplib.SMTP(...) as server:` |

---

## Programar la ejecucion automatica

El script esta disenado para correrse sin supervision. Opciones comunes:

**Windows Task Scheduler:**
```cmd
"C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" ^
    C:\geoprocesos\validate_datastores.py
```

**Linux cron** (diario a las 6:00 a.m.):
```bash
0 6 * * * /arcgisstore/python/envs/arcgispro/bin/python \
    /arcgisstore/geoprocesos/validate_datastores.py \
    >> /arcgisstore/logs/datastores.log 2>&1
```

---

## Resultados

| Situacion | Sin script | Con script |
|---|---|---|
| Deteccion de fallo en Data Store | Manual, reactiva (usuario reporta) | Proactiva, correo inmediato al fallar |
| Cobertura de servidores | Solo el que se revisa manualmente | Todos los servidores en una ejecucion |
| Trazabilidad | Ninguna | Log con timestamp por item y servidor |
| Tiempo de revision | 15-20 min por servidor | < 2 min total (ejecucion automatica) |

---

## Compatibilidad con ambientes federados

El script funciona en ArcGIS Enterprise federado sin modificaciones. `ListDataStoreItems` y `ValidateDataStoreItem` se conectan directamente al **ArcGIS Server** a traves del archivo `.ags` — no pasan por la capa de federacion ni por el Portal. Los Data Stores se registran a nivel de Server en ambos casos, asi que el comportamiento es identico.

El unico punto critico es **como se creo el archivo `.ags`**:

| Tipo de conexion `.ags` | Funciona? | Nota |
|---|---|---|
| Credenciales de administrador del Server | Si, siempre | Opcion mas robusta para tareas programadas |
| Credenciales de Portal (usuario publisher) | Si, mientras el token sea valido | El token expira (tipicamente cada 2 h) |
| Apunta al Web Adaptor (URL publica) | A veces | Algunas funciones ArcPy prefieren la URL interna del Server |

Para ejecuciones automaticas sin supervision, usar la **URL interna del Server** al crear el `.ags`, no la del Web Adaptor:

```
# URL interna — recomendada para scripts automatizados
https://server-interno.dominio.local:6443/arcgis

# URL publica via Web Adaptor — evitar para ArcPy geoprocessing
https://portal.dominio.com/server
```

En ArcGIS Pro: *Catalog > Servers > Add ArcGIS Server*, ingresar la URL interna y marcar **Save username/password** para que el `.ags` incluya credenciales persistentes.

---

## Proximos pasos

- Integrar con un sistema de tickets: convertir la alerta en un issue automatico en Jira o ServiceNow
- Exportar los resultados a un CSV por fecha para tendencias historicas
- Encapsular como Python Toolbox para que el equipo pueda ejecutarlo desde ArcGIS Pro con interfaz grafica
- Agregar validacion de disponibilidad del servidor antes de intentar listar items

---

*Tienes preguntas o mejoras? Escribeme a [faneal14@gmail.com](mailto:faneal14@gmail.com) o en [LinkedIn](https://linkedin.com/in/faneal).*

<span class="post-ai-note">Redactado con asistencia de IA generativa · Codigo revisado y validado en produccion</span>
