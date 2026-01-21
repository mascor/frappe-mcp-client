# Client Frappe MCP

[![Read in English](https://img.shields.io/badge/lang-en-red.svg)](README.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green)](https://modelcontextprotocol.io)
[![Frappe MCP Server](https://img.shields.io/badge/Server-frappe--mcp--server-blue)](https://github.com/mascor/frappe-mcp-server)

Un Client Bridge Python che espone le funzionalità del server [Frappe](https://frappeframework.com) tramite il [Model Context Protocol (MCP)](https://modelcontextprotocol.io/).

Questo client si connette a un'istanza Frappe remota dove è installata la **App MCP Server** e inoltra le richieste, permettendo agli agenti AI (come Claude Desktop o Cursor) di interagire in modo sicuro con i tuoi dati ERPNext/Frappe.

## Prerequisiti (Lato Server)

Prima di utilizzare questo client, devi preparare il tuo sito Frappe:

1.  **Installa l'App**:
    Assicurati che l'app `mcp_server` sia installata sul tuo sito.
    ```bash
    bench get-app https://github.com/mascor/frappe-mcp-server
    bench --site <tuo-sito> install-app mcp_server
    ```

2.  **Configura Utente e Chiavi MCP**:
    Esegui lo script di setup per generare API Key & Secret per l'utente MCP.
    ```bash
    bench --site <tuo-sito> execute mcp_server.setup.setup_mcp
    ```
    *Copia immediatamente `api_key` e `api_secret` generati.*

3.  **Configura Accessi (Default: Tutto Bloccato)**:
    Di default, il server agisce come un firewall e blocca TUTTO. Devi esplicitamente consentire i DocType.
    *   Vai su **MCP Doctype Allowlist** nella Scrivania Frappe.
    *   Aggiungi un nuovo record per `ToDo` (o qualsiasi altro DocType).
    *   Spunta `Allow Read`, `Allow Create` ecc. per abilitare le funzionalità.

## Installazione

```bash
git clone https://github.com/mascor/frappe-mcp-client
cd frappe-mcp-client

# Crea e attiva un virtual environment (Consigliato per evitare problemi di permessi)
python3 -m venv .venv
source .venv/bin/activate

# Installa il pacchetto
pip install .
```

## Configurazione e Utilizzo

### 1. CLI Standalone

Puoi eseguire il server MCP localmente per testare le connessioni:

```bash
# Usando argomenti flag
mcp-frappe --url "https://tuosito.com" --token "api_key:api_secret"

# OPPURE usando variabili d'ambiente
export FRAPPE_MCP_URL="https://tuosito.com"
export FRAPPE_MCP_TOKEN="api_key:api_secret"
mcp-frappe
```

### 2. Integrazione Claude Desktop

Per utilizzarlo con Claude Desktop, aggiungi questo al tuo `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "frappe": {
      "command": "mcp-frappe",
      "args": [
        "--url", "https://tuosito.com",
        "--token", "api_key:api_secret"
      ]
    }
  }
}
```

## Guida Passo-Passo per il Testing

Vuoi verificare che tutto funzioni? Segui questo flusso:

1.  **Setup Server**:
    *   Sul tuo sito Frappe, vai su **MCP Doctype Allowlist**.
    *   Crea una regola per il **DocType**: `ToDo`.
    *   Spunta **Allow Create** e **Allow Read**.

2.  **Connetti Client**:
    *   Configura Claude Desktop come mostrato sopra.
    *   Riavvia Claude Desktop.

3.  **Test con AI**:
    *   Apri Claude e cerca l'icona 🔌 per confermare che "frappe" è connesso.
    *   Chiedi: *"Crea un nuovo ToDo in Frappe con descrizione 'Ciao da MCP' e stato 'Open'"*.
    *   Chiedi: *"Cerca i miei ToDo aperti"*.

4.  **Verifica**:
    *   Controlla la lista **ToDo** nella tua Scrivania Frappe per vedere il nuovo elemento.
    *   Controlla **MCP Audit Log** per vedere la voce relativa alla richiesta.

## Tool Disponibili

Questo client espone i seguenti tool:

*   `search_docs(doctype, filters, fields)`
*   `create_doc(doctype, data)`
*   `update_doc(doctype, name, data)`
*   `delete_doc(doctype, name)`
*   `get_doc(doctype, name)`
*   `get_meta(doctype)`
*   `ping()`
