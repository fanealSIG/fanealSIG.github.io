# Bulk Backup, Deletion and Restore of ArcGIS Online Content with Python Toolbox

When an organization migrates from one AGOL account to another, or needs to clean up years of accumulated content without losing anything, the manual process is infeasible: item by item, download, delete, re-upload. With hundreds of layers, web maps, and dashboards spread across folders, that can take days.

In this post I explain how I built a **Python Toolbox** with three chained tools—backup, bulk deletion, and restore—that automate this complete cycle using the **ArcGIS API for Python**.

---

## The Problem

The situation that motivated this toolbox: an AGOL account with over 400 items in 12 folders that needed to migrate to a new account. Risks of the manual process were:

- Items forgotten or downloaded in wrong format
- Accidental deletions without prior backup
- Loss of folder structure and original metadata
- No traceability of what was migrated and what wasn't

The solution: automate each stage and leave a **JSON manifest** as the source of truth.

---

![AGOL Backup Architecture](images/flujo-backup-estrategia.png)
*Download strategy: direct download for Web Maps and native files, export to FGDB for Feature Services*

## Toolbox Architecture

The `.pyt` exposes three independent tools designed to work in sequence:

```
BackupAGOL  →  manifest.json  →  DeleteAGOL
                                      ↓
                               RestoreAGOL  →  restore_id_map.json
```

1. **BackupAGOL** — downloads all content and generates the manifest
2. **DeleteAGOL** — reads the manifest and deletes items (with ID protection)
3. **RestoreAGOL** — uploads local files recreating folders and metadata

---

## Key Capabilities

- **Direct Download**: Web Maps, Notebooks, Dashboards, Shapefiles, PDFs and other formats that AGOL delivers as native file
- **Export**: Feature Services and Feature Layers are exported to File Geodatabase before downloading, since they don't have an equivalent local file
- **Manifest**: Complete account structure with folders, items, types, access, and dependencies between Web Maps and their operational layers
- **Dry-Run Mode**: Execute all logic without destructive operations or writes

For complete implementation details and code examples, refer to the Spanish version of this article.

---

## Results

With this toolbox, a migration that would have taken several days of manual work is reduced to three sequential executions in ArcGIS Pro. The JSON manifest acts as a complete audit: there's a record of what existed, in what folder it was, and what was migrated.

---

## Next Steps

- Automatic dependency remapping in Web Maps using `restore_id_map.json`
- Support for items with related data (Related Tables, Attachments)
- Backup filter by modification date (only items updated since X date)
- Export to GeoPackage or CSV to reduce credits on large layers

---

*Questions or improvements? Write to me at [faneal14@gmail.com](mailto:faneal14@gmail.com) or on [LinkedIn](https://linkedin.com/in/faneal).*

<span class="post-ai-note">Written with AI assistance · Code reviewed and validated in production</span>
