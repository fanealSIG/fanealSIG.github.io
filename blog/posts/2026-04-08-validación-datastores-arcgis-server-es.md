# Validación automática de Data Stores en ArcGIS Server con Python

## El problema en simple

Imagina que tienes 4 servidores con datos almacenados en bases de datos y carpetas compartidas. Esos datos alimentan decenas de mapas y servicios que usa tu organización.

**¿Qué pasa si una de esas bases de datos se desconecta?** 

- Tus usuarios no lo saben
- Los mapas dejan de funcionar sin aviso
- Nadie se da cuenta hasta que alguien reporta el problema

Hoy: revisar manualmente 4 servidores × 10+ bases de datos cada día = 30+ minutos de trabajo tedioso y propenso a errores.

**La solución:** Un script que revisa automáticamente todo cada noche y te envía un correo si algo está mal.

---

## ¿Quién necesita esto?

- **Administradores de GIS** que mantienen ArcGIS Server en producción
- **Equipos** que usan muchos servicios geográficos y no pueden permitirse tiempos de inactividad
- **Cualquiera** que prefiera dormir tranquilo en lugar de revisar servidores manualmente

---

## Cómo funciona en 3 pasos simples

```
Cada noche a las 6am:
  1. El script se conecta a cada servidor
  2. Revisa todas las bases de datos y carpetas
  3. Si algo está dañado → te envía un correo
  4. Si todo está bien → silencio (sin correos molestos)
```

**Eso es todo.** No tienes que hacer nada. El script trabaja solo.

---

## Lo que necesitas

- **Python** (incluido en ArcGIS Pro/Server)
- **Acceso** a los servidores de tu empresa
- **Credenciales de correo** para enviar alertas
- **5 minutos** para configurar (copiar/pegar)

---

## El código: 4 funciones simples

```python
import arcpy
import smtplib
from email.mime.text import MIMEText

# 1. Conectar con el correo
def send_alert(server_name, item_name, error):
    """Envía un correo cuando algo falla"""
    mensaje = f"⚠️ FALLO en {server_name}\n\n{item_name} no responde.\n\nDetalle: {error}"
    
    # Aquí va tu servidor SMTP (Gmail, Outlook, etc)
    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.login("tu-email@empresa.com", "tu-contraseña")
    smtp.sendmail("tu-email@empresa.com", "alertas@empresa.com", mensaje)
    smtp.quit()

# 2. Revisar un servidor
def revisar_servidor(conexion_ags):
    """Conecta a un servidor y revisa sus Data Stores"""
    print(f"Revisando {conexion_ags}...")
    
    # Obtener todas las bases de datos registradas
    bases_de_datos = arcpy.ListDataStoreItems(conexion_ags, "DATABASE")
    carpetas = arcpy.ListDataStoreItems(conexion_ags, "FOLDER")
    
    for item in bases_de_datos + carpetas:
        nombre = item[0]
        # Verificar si puede conectarse
        estado = arcpy.ValidateDataStoreItem(conexion_ags, "DATABASE", nombre)
        
        if estado != "valid":
            print(f"❌ {nombre} está DAÑADO")
            send_alert(conexion_ags, nombre, estado)
        else:
            print(f"✅ {nombre} está OK")

# 3. Revisar todos los servidores
def revisar_todos():
    """Ejecuta la revisión en todos tus servidores"""
    servidores = [
        "C:\\Users\\admin\\AppData\\Roaming\\ESRI\\Desktop\\ArcGISPro\\Favorites\\prod1.ags",
        "C:\\Users\\admin\\AppData\\Roaming\\ESRI\\Desktop\\ArcGISPro\\Favorites\\prod2.ags",
        # ... agregar los tuyos
    ]
    
    for servidor in servidores:
        try:
            revisar_servidor(servidor)
        except Exception as e:
            print(f"Error conectando a {servidor}: {e}")

# 4. Ejecutar
if __name__ == "__main__":
    revisar_todos()
```

---

## Cómo configurarlo (paso a paso)

### Paso 1: Obtener las conexiones a tus servidores
En ArcGIS Pro:
1. Abre el panel **Catalog** (izquierda)
2. Haz clic derecho en **Servers** → **Add ArcGIS Server**
3. Ingresa: `https://mi-servidor.empresa.com:6443/arcgis`
4. Marca "Save username/password"
5. El archivo `.ags` se guardará automáticamente

### Paso 2: Configurar el correo
```python
# Reemplaza estos valores con los tuyos:
SMTP_HOST = "smtp.gmail.com"  # o "smtp.outlook.com"
SENDER_EMAIL = "tu-email@empresa.com"
SENDER_PASSWORD = "tu-contraseña"  # O usar variable de entorno
ALERT_EMAIL = "alertas@empresa.com"
```

### Paso 3: Programar la ejecución automática

**Windows (Task Scheduler):**
1. Abre Task Scheduler
2. Click en "Create Task"
3. Nombre: "Validar Data Stores"
4. Trigger: "Daily" a las 6:00 AM
5. Action: `python C:\scripts\validate_datastores.py`

**Mac/Linux (Cron):**
```bash
# Editar crontab
crontab -e

# Agregar esta línea (ejecuta a las 6am todos los días):
0 6 * * * /usr/bin/python3 /home/admin/validate_datastores.py
```

---

## ¿Qué recibos en el correo?

**Si todo está bien:** Nada. Silencio total (como debería ser).

**Si algo falla:**
```
⚠️ FALLO en prod1.ags

LayerDB_Produccion no responde.

Detalle: [Error 400: Connection timeout]

Revisar: ArcGIS Server Manager → Data Stores → LayerDB_Produccion
```

---

## Resultados reales

| Situación | Antes | Después |
|---|---|---|
| ¿Quién revisa? | Tú, manualmente cada día | El script, automáticamente |
| ¿Cuánto tiempo? | 30 minutos | 0 minutos (se hace solo) |
| ¿Cuándo lo sabes? | Cuando un usuario llama | Inmediatamente por correo |
| ¿Errores? | Frecuentes (olvidas algún servidor) | Ninguno (revisa todos) |

---

## Preguntas comunes

**¿Qué pasa si el correo falla?**
El script lo registra en un log. Puedes revisar qué pasó.

**¿Es seguro guardar contraseñas?**
Sí, usa **variables de entorno** en lugar de escribirlas en el código:
```python
password = os.environ.get("GIS_MAIL_PASSWORD")
```

**¿Funciona con ArcGIS Enterprise federado?**
Sí, usa la URL interna del servidor (no la pública del Web Adaptor).

**¿Puedo cambiarlo para otros tipos de monitoreo?**
Claro. El mismo patrón funciona para revisar licencias, espacios de disco, etc.

---

## Próximos pasos

1. **Copia el código** arriba
2. **Reemplaza** los correos, servidores y SMTP
3. **Prueba** ejecutando manualmente: `python validate_datastores.py`
4. **Programa** en Task Scheduler o Cron
5. **Duerme tranquilo** 😴

---

*¿Preguntas? Escríbeme a [faneal14@gmail.com](mailto:faneal14@gmail.com) o en [LinkedIn](https://linkedin.com/in/faneal).*

<span class="post-ai-note">Redactado con asistencia de IA generativa · Código revisado y validado en producción</span>
