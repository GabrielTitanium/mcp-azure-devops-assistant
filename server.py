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

if __name__ == "__main__":
    print("✅ MCP Azure DevOps Server starting...")
    mcp.run()

@mcp.tool()
def get_failed_pipeline_runs(hours: int = 24):
    """
    Get failed pipeline runs in the last X hours
    """
    runs = ado_client.get_failed_runs(hours)
    return [
        {
            "pipeline": r["definition"]["name"],
            "finished_at": r["finishTime"],
            "url": r.get("_links", {}).get("web", {}).get("href", "")
        }
        for r in runs.get("value", [])
    ]
