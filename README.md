# Frappe MCP Client

A Python Bridge Client that exposes Frappe server capabilities via the Model Context Protocol (MCP). This client connects to a remote Frappe instance where the `mcp_server` app is installed and forwards requests.

## Installation

### From Source

```bash
git clone https://github.com/mascor/frappe-mcp-client
cd frappe-mcp-client
pip install .
```

## Usage

### CLI

To start the MCP server locally:

```bash
mcp-frappe --url "https://yoursite.com" --token "api_key:api_secret"
```

You can also use environment variables:

```bash
export FRAPPE_MCP_URL="https://yoursite.com"
export FRAPPE_MCP_TOKEN="api_key:api_secret"
mcp-frappe
```

### Configuration with Claude Desktop

Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "frappe": {
      "command": "mcp-frappe",
      "args": [
        "--url",
        "https://yoursite.com",
        "--token",
        "api_key:api_secret"
      ]
    }
  }
}
```

## Features

This client exposes the following tools from the remote Frappe server:

- `search_docs(doctype, filters, fields)`
- `create_doc(doctype, data)`
- `update_doc(doctype, name, data)`
- `get_doc(doctype, name)`
- `get_meta(doctype)`
- `ping()`
