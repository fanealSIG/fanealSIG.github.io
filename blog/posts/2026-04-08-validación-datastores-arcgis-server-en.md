# Automated Data Store Validation in ArcGIS Server with Python

In an ArcGIS Enterprise infrastructure with multiple production servers, knowing whether registered Data Stores remain accessible is critical. A database layer or data folder that loses its connection can disable dozens of published services without the team noticing until a user reports the failure.

In this post, I describe how I built a monitoring script that automatically validates all registered items—folders and databases—across multiple ArcGIS Server nodes and sends an email alert when any fails validation.

---

## The Problem

The manual process was: open ArcGIS Server Manager on each node, navigate to *Data Stores*, review the status of each registered item, and note any failures. With four production servers and dozens of Data Stores per server, this was repetitive work that no one executed with the necessary frequency.

Concrete risks:

- A Data Store failing overnight goes undetected until the next day
- No traceability of when the failure occurred or on which server
- Alert emails must be generated manually when something is detected

The solution: automate validation with `arcpy.ValidateDataStoreItem` and schedule the script as an operating system task.

---

## Tools Used

- **ArcPy** — Esri's Python library included in ArcGIS Pro / ArcGIS Server
- **arcpy.ListDataStoreItems** — lists registered items by type on a server
- **arcpy.ValidateDataStoreItem** — verifies if a Data Store item remains accessible
- **smtplib** — standard Python module for sending alerts via SMTP
- **logging** — standard module for structured traceability in console and log

---

![Data Store validation flow](images/flujo-datastores-arcgis-server.png)
*The script traverses each server, validates all items and sends alert only when it detects a failure*

## How the Script Works

The flow has three clear steps:

1. **Iterate connections** — traverses a list of `.ags` files, one per server
2. **List and validate** — for each server calls `ListDataStoreItems` (type `FOLDER` and `DATABASE`) then `ValidateDataStoreItem` for each item found
3. **Alert** — if validation returns a status other than `"valid"`, or if an exception is thrown, sends an email with the failure details

This approach keeps infrastructure monitoring proactive rather than reactive. For complete implementation details and configuration, refer to the Spanish version of this article.

---

## Results

| Situation | Without Script | With Script |
|---|---|---|
| Data Store failure detection | Manual, reactive (user reports) | Proactive, immediate email on failure |
| Server coverage | Only manually checked ones | All servers in one execution |
| Traceability | None | Log with timestamp per item and server |
| Review time | 15-20 min per server | < 2 min total (automatic execution) |

---

## Federated Environment Compatibility

The script works in federated ArcGIS Enterprise without modification. `ListDataStoreItems` and `ValidateDataStoreItem` connect directly to **ArcGIS Server** through the `.ags` file — they don't pass through the federation layer or Portal. Data Stores are registered at the Server level in both cases, so behavior is identical.

For unattended automated executions, use the **internal Server URL** when creating the `.ags`, not the Web Adaptor's public URL.

---

*Questions or improvements? Write to me at [faneal14@gmail.com](mailto:faneal14@gmail.com) or on [LinkedIn](https://linkedin.com/in/faneal).*

<span class="post-ai-note">Written with AI assistance · Code reviewed and validated in production</span>
