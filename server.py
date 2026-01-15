from mcp.server.fastmcp import FastMCP
from azure_devops_client import AzureDevOpsClient

mcp = FastMCP("azure-devops-mcp")

ado_client = AzureDevOpsClient()


@mcp.tool()
def list_pipelines():
    """
    List all Azure DevOps pipelines for the configured project
    """
    pipelines = ado_client.list_pipelines()
    return [
        {
            "id": p["id"],
            "name": p["name"]
        }
        for p in pipelines.get("value", [])
    ]

@mcp.tool()
def get_failed_runs(hours: int = 24):
    """
    Get failed pipeline runs in the last X hours (default: 24)
    """
    result = ado_client.get_failed_runs(hours)

    return [
        {
            "pipeline": run["definition"]["name"],
            "build_number": run["buildNumber"],
            "finished_at": run["finishTime"]
        }
        for run in result.get("value", [])
    ]

if __name__ == "__main__":
    print("✅ MCP Azure DevOps Server starting...")
    mcp.run()

@mcp.tool()
def health():
    """
    Health check for the MCP server
    """
    return {
        "status": "ok",
        "service": "azure-devops-mcp"
    }
