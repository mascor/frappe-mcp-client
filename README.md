# Frappe MCP Client

A Python Bridge Client that exposes [Frappe](https://frappeframework.com) server capabilities via the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/).

This client connects to a remote Frappe instance where the **MCP Server App** is installed and forwards requests, allowing AI agents (like Claude Desktop or Cursor) to interact securely with your ERPNext/Frappe data.

## Prerequisites (Server Side)

Before using this client, you must prepare your Frappe site:

1.  **Install the App**:
    Ensure the `mcp_server` app is installed on your site.
    ```bash
    bench get-app https://github.com/mascor/frappe-mcp-server
    bench --site <your-site> install-app mcp_server
    ```

2.  **Setup MCP User & Token**:
    Run the setup script to generate an API key/secret or use the dedicated MCP User.
    ```bash
    bench --site <your-site> execute mcp_server.mcp_server.setup.setup_mcp
    ```
    *Copy the generated Token (API Key:Secret) immediately.*

3.  **Configure Access (Effectively Empty by Default)**:
    By default, the server acts as a firewall and blocks EVERYTHING. You must explicitly allow DocTypes.
    *   Go to **MCP Doctype Allowlist** in Frappe Desk.
    *   Add a new record for `ToDo` (or any other DocType).
    *   Check `Allow Read`, `Allow Create` etc. to enable capabilities.

## Installation

```bash
git clone https://github.com/mascor/frappe-mcp-client
cd frappe-mcp-client
pip install .
```

## Configuration & Usage

### 1. Standalone CLI

You can run the MCP server locally to test connections:

```bash
# Using flag arguments
mcp-frappe --url "https://yoursite.com" --token "api_key:api_secret"

# OR using environment variables
export FRAPPE_MCP_URL="https://yoursite.com"
export FRAPPE_MCP_TOKEN="api_key:api_secret"
mcp-frappe
```

### 2. Claude Desktop Integration

To use with Claude Desktop, add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "frappe": {
      "command": "mcp-frappe",
      "args": [
        "--url", "https://yoursite.com",
        "--token", "api_key:api_secret"
      ]
    }
  }
}
```

## Step-by-Step Testing Guide

Want to verify everything works? Follow this flow:

1.  **Server Setup**:
    *   On your Frappe site, go to **MCP Doctype Allowlist**.
    *   Create a rule for **DocType**: `ToDo`.
    *   Check **Allow Create** and **Allow Read**.

2.  **Connect Client**:
    *   Configure Claude Desktop as shown above.
    *   Restart Claude Desktop.

3.  **Test with AI**:
    *   Open Claude and look for the 🔌 icon to confirm "frappe" is connected.
    *   Ask: *"Create a new ToDo in Frappe with description 'Hello from MCP' and status 'Open'"*.
    *   Ask: *"Search for my open ToDos"*.

4.  **Verify**:
    *   Check your Frappe Desk **ToDo** list to see the new item.
    *   Check **MCP Audit Log** to see the entry for the request.

## Available Tools

This client exposes the following tools:

*   `search_docs(doctype, filters, fields)`
*   `create_doc(doctype, data)`
*   `update_doc(doctype, name, data)`
*   `get_doc(doctype, name)`
*   `get_meta(doctype)`
*   `ping()`
