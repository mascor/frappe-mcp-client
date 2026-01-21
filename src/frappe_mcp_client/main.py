import argparse
import os
import sys
import asyncio
from typing import Optional, Dict, List, Any
from mcp.server.fastmcp import FastMCP
from .client import FrappeClient

# Initialize FastMCP server
mcp = FastMCP("Frappe")

# Global client placeholder
client: Optional[FrappeClient] = None

@mcp.tool()
async def search_docs(doctype: str, filters: Optional[Dict[str, Any]] = None, fields: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """
    Search for documents in the Frappe instance.
    
    Args:
        doctype: The DocType to search for (e.g. "User", "ToDo")
        filters: Dictionary of filters to apply (e.g. {"status": "Open"})
        fields: List of fields to retrieve (e.g. ["name", "description"])
    """
    if not client:
        raise RuntimeError("Client not initialized")
    return await client.search_docs(doctype, filters, fields)

@mcp.tool()
async def create_doc(doctype: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new document.
    
    Args:
        doctype: The DocType to create
        data: Dictionary of fields and values for the new document
    """
    if not client:
        raise RuntimeError("Client not initialized")
    return await client.create_doc(doctype, data)

@mcp.tool()
async def update_doc(doctype: str, name: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update an existing document.
    
    Args:
        doctype: The DocType of the document
        name: The name/ID of the document
        data: Dictionary of fields to update
    """
    if not client:
        raise RuntimeError("Client not initialized")
    return await client.update_doc(doctype, name, data)

@mcp.tool()
async def get_doc(doctype: str, name: str) -> Dict[str, Any]:
    """
    Get a specific document by name.
    
    Args:
        doctype: The DocType of the document
        name: The name/ID of the document
    """
    if not client:
        raise RuntimeError("Client not initialized")
    return await client.get_doc(doctype, name)

@mcp.tool()
async def get_meta(doctype: str) -> Dict[str, Any]:
    """
    Get metadata for a DocType.
    
    Args:
        doctype: The DocType to get metadata for
    """
    if not client:
        raise RuntimeError("Client not initialized")
    return await client.get_meta(doctype)

@mcp.tool()
async def delete_doc(doctype: str, name: str) -> Dict[str, Any]:
    """
    Delete a document.
    
    Args:
        doctype: The DocType of the document
        name: The name/ID of the document to delete
    """
    if not client:
        raise RuntimeError("Client not initialized")
    return await client.delete_doc(doctype, name)

@mcp.tool()
async def ping() -> str:
    """
    Ping the Frappe server to check connection.
    """
    if not client:
        raise RuntimeError("Client not initialized")
    return await client.ping()

def main():
    global client
    parser = argparse.ArgumentParser(description="Frappe MCP Client")
    parser.add_argument("--url", help="Frappe Site URL (or set FRAPPE_MCP_URL)")
    parser.add_argument("--token", help="API Token in format 'key:secret' (or set FRAPPE_MCP_TOKEN)")
    
    args, unknown = parser.parse_known_args()
    
    # Get config from args or env vars
    url = args.url or os.environ.get("FRAPPE_MCP_URL")
    token = args.token or os.environ.get("FRAPPE_MCP_TOKEN")
    
    if not url or not token:
        print("Error: URL and Token must be provided via arguments or environment variables.")
        print("Usage: mcp-frappe --url <url> --token <api_key:api_secret>")
        sys.exit(1)
        
    client = FrappeClient(url, token)
    
    # Remove our custom args from sys.argv so FastMCP doesn't get confused
    # FastMCP might use uvloop or other things taking args, but primarily it runs on stdio
    # We just need to make sure we don't pass our args to it if it parses sys.argv
    # The mcp.run() call handles the server loop.
    
    # Clean up sys.argv for FastMCP/Typer underlying
    sys.argv = [sys.argv[0]] + unknown
    
    mcp.run()

if __name__ == "__main__":
    main()
