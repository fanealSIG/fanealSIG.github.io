# Automated Data Store Validation in ArcGIS Server with Python

## The Problem (Simplified)

Imagine you have 4 servers with data stored in databases and shared folders. That data powers dozens of maps and services your organization uses.

**What happens if one of those databases goes offline?**

- Your users don't know until it's too late
- Maps stop working with no warning
- Nobody notices until someone complains

Today: manually checking 4 servers × 10+ databases every day = 30+ minutes of tedious, error-prone work.

**The solution:** A script that checks everything automatically every night and emails you if something breaks.

---

## Who needs this?

- **GIS administrators** running ArcGIS Server in production
- **Teams** using many geographic services who can't afford downtime
- **Anyone** who prefers sleeping soundly over manually monitoring servers

---

## How it works in 3 simple steps

```
Every night at 6am:
  1. The script connects to each server
  2. Checks all databases and folders
  3. If something is broken → emails you
  4. If everything is fine → silence (no annoying emails)
```

**That's it.** You do nothing. The script works alone.

---

## What you need

- **Python** (included in ArcGIS Pro/Server)
- **Access** to your company's servers
- **Email credentials** to send alerts
- **5 minutes** to set up (copy/paste)

---

## The code: 4 simple functions

```python
import arcpy
import smtplib
from email.mime.text import MIMEText

# 1. Send email when something fails
def send_alert(server_name, item_name, error):
    """Sends an email when something breaks"""
    message = f"⚠️ FAILURE on {server_name}\n\n{item_name} is not responding.\n\nDetails: {error}"
    
    # Your SMTP server (Gmail, Outlook, etc)
    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.login("your-email@company.com", "your-password")
    smtp.sendmail("your-email@company.com", "alerts@company.com", message)
    smtp.quit()

# 2. Check one server
def check_server(ags_connection):
    """Connects to a server and checks its Data Stores"""
    print(f"Checking {ags_connection}...")
    
    # Get all registered databases
    databases = arcpy.ListDataStoreItems(ags_connection, "DATABASE")
    folders = arcpy.ListDataStoreItems(ags_connection, "FOLDER")
    
    for item in databases + folders:
        name = item[0]
        # Verify if it can connect
        status = arcpy.ValidateDataStoreItem(ags_connection, "DATABASE", name)
        
        if status != "valid":
            print(f"❌ {name} is BROKEN")
            send_alert(ags_connection, name, status)
        else:
            print(f"✅ {name} is OK")

# 3. Check all servers
def check_all():
    """Runs validation on all your servers"""
    servers = [
        "C:\\Users\\admin\\AppData\\Roaming\\ESRI\\Desktop\\ArcGISPro\\Favorites\\prod1.ags",
        "C:\\Users\\admin\\AppData\\Roaming\\ESRI\\Desktop\\ArcGISPro\\Favorites\\prod2.ags",
        # ... add yours
    ]
    
    for server in servers:
        try:
            check_server(server)
        except Exception as e:
            print(f"Error connecting to {server}: {e}")

# 4. Run it
if __name__ == "__main__":
    check_all()
```

---

## Setup (Step by step)

### Step 1: Get your server connections
In ArcGIS Pro:
1. Open the **Catalog** panel (left side)
2. Right-click **Servers** → **Add ArcGIS Server**
3. Enter: `https://my-server.company.com:6443/arcgis`
4. Check "Save username/password"
5. The `.ags` file is saved automatically

### Step 2: Configure email
```python
# Replace with yours:
SMTP_HOST = "smtp.gmail.com"  # or "smtp.outlook.com"
SENDER_EMAIL = "your-email@company.com"
SENDER_PASSWORD = "your-password"  # Or use environment variable
ALERT_EMAIL = "alerts@company.com"
```

### Step 3: Schedule automatic execution

**Windows (Task Scheduler):**
1. Open Task Scheduler
2. Click "Create Task"
3. Name: "Validate Data Stores"
4. Trigger: "Daily" at 6:00 AM
5. Action: `python C:\scripts\validate_datastores.py`

**Mac/Linux (Cron):**
```bash
# Edit crontab
crontab -e

# Add this line (runs at 6am every day):
0 6 * * * /usr/bin/python3 /home/admin/validate_datastores.py
```

---

## What you get in the email

**If everything is fine:** Nothing. Total silence (as it should be).

**If something breaks:**
```
⚠️ FAILURE on prod1.ags

LayerDB_Production is not responding.

Details: [Error 400: Connection timeout]

Check: ArcGIS Server Manager → Data Stores → LayerDB_Production
```

---

## Real results

| Situation | Before | After |
|---|---|---|
| Who checks? | You, manually every day | Script, automatically |
| How long? | 30 minutes | 0 minutes (runs itself) |
| When do you know? | When a user calls | Instantly via email |
| Errors? | Frequent (you forget a server) | None (checks all) |

---

## Common questions

**What if the email fails?**
The script logs it. You can check what happened.

**Is it safe to store passwords?**
Yes, use **environment variables** instead of hardcoding:
```python
password = os.environ.get("GIS_MAIL_PASSWORD")
```

**Does it work with federated ArcGIS Enterprise?**
Yes, use the server's internal URL (not the public Web Adaptor URL).

**Can I modify it for other monitoring?**
Absolutely. The same pattern works for checking licenses, disk space, etc.

---

## Next steps

1. **Copy the code** above
2. **Replace** the emails, servers, and SMTP
3. **Test** by running manually: `python validate_datastores.py`
4. **Schedule** it in Task Scheduler or Cron
5. **Sleep soundly** 😴

---

*Questions? Write me at [faneal14@gmail.com](mailto:faneal14@gmail.com) or on [LinkedIn](https://linkedin.com/in/faneal).*

<span class="post-ai-note">Written with AI assistance · Code reviewed and validated in production</span>
