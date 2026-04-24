# Extracting and Cataloging Source Files from arcgisinput in ArcGIS Server

ArcGIS Server stores the source documents of published services—`.mxd` and `.mapx` files—in a folder called `arcgisinput`, organized by subfolders that correspond to service catalog groups. Each service generates its own internal subfolder with the pattern `ServiceName.MapServer/`, which is the path the server uses internally, not the name the team knows.

When the need arose to audit and reorganize source files for dozens of services, navigating that structure by hand was slow and error-prone. I built a script that recursively traverses `arcgisinput`, extracts all `.mxd` and `.mapx` files, renames them with the name of the published service they belong to, and copies them to a clean structure on the desktop, along with an automated Excel inventory report.

---

## The Problem

The concrete situation: multiple subfolders in `arcgisinput` with source files whose internal names don't necessarily match the published service names. The manual process was:

- Open file explorer and navigate through `arcgisinput`
- Visually identify the correct `ServiceName.MapServer` folder for each service
- Copy the `.mxd` or `.mapx` to a working location with the correct name
- Repeat for each service involved, with no record of what was copied

Without a structured inventory, it was easy to confuse versions or lose track of which files corresponded to which active services.

---

## Tools Used

- **os / os.walk** — recursive filesystem traversal without external dependencies
- **shutil.copy2** — file copying while preserving operating system metadata
- **pandas** — generating the Excel report with the complete inventory of paths and names

---

![MXD MAPX extraction flow](images/flujo-extraccion-mxd-mapx.png)
*The script traverses arcgisinput, detects source files, extracts the service name from the .MapServer folder and copies them organized*

## How the Script Works

The flow has four steps:

1. **Traverse the directory** — `os.walk` recursively iterates the entire structure under `arcgisinput`
2. **Filter by extension** — processes only `.mxd` and `.mapx` files, ignores the rest
3. **Determine destination name** — searches the path for the segment ending in `.MapServer` and uses the preceding part as the destination filename; if no `.MapServer` exists in the path, keeps the original name as fallback
4. **Copy and register** — copies the file to `MXD_new/<subfolder>/` or `MAPX_new/<subfolder>/`, adds numeric suffix if a file with that name already exists, and accumulates the entry in the inventory

The subfolder is determined by the level immediately following `arcgisinput` in the path, reflecting the organization of the service catalog.

---

## Results

| Task | Manual Process | With the Script |
|---|---|---|
| Locate source files for 50 services | 20-40 min browsing folders | < 2 min execution |
| Name of copied files | Server internal name (sometimes illegible) | Published service name |
| Organization by category | Manual, error-prone | Automatic by arcgisinput subfolder |
| Documented inventory | Non-existent or manual Excel | Auto-generated Excel with complete paths |
| Name conflicts | No control | Automatic numeric suffix |

---

## Federated Environment Compatibility

The script accesses the server filesystem directly—it doesn't use ArcPy or make REST calls—so it works the same in federated and non-federated environments. It only requires read access to the `arcgisinput` folder.

The critical point in federated environments is **where the script is executed from**.

In federated infrastructures, `arcgisinput` is usually in the server's data directory. If the share isn't enabled by default, the administrator can expose it as a network shared folder with read-only permissions.

The script doesn't write anything to `arcgisinput`; all output goes to the desktop of the user running it. There's no risk of altering server files.

---

*Questions or improvements? Write to me at [faneal14@gmail.com](mailto:faneal14@gmail.com) or on [LinkedIn](https://linkedin.com/in/faneal).*

<span class="post-ai-note">Written with AI assistance · Code reviewed and validated in production</span>
