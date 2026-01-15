# MCP Azure DevOps Assistant

An MCP server that connects Azure DevOps to AI assistants like Claude, enabling natural language queries about your CI/CD pipelines and build failures.

## What is MCP?

Model Context Protocol (MCP) is an open standard that connects AI assistants to external tools and data. It allows Claude to directly access your Azure DevOps data instead of requiring copy-paste interactions.

## Architecture

```
┌─────────────────┐
│ Claude Desktop  │
│   (AI Chat)     │
└────────┬────────┘
         │ MCP Protocol (stdio)
         │
┌────────▼────────────────────┐
│ MCP Server (server.py)      │
│  • list_pipelines()         │
│  • get_failed_pipeline_runs()│
└────────┬────────────────────┘
         │
┌────────▼────────────────────┐
│ AzureDevOpsClient           │
│ (azure_devops_client.py)    │
└────────┬────────────────────┘
         │ REST API + PAT Auth
         │
┌────────▼────────────────────┐
│ Azure DevOps REST API       │
└─────────────────────────────┘
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file:

```env
AZDO_ORG=your-organization
AZDO_PROJECT=your-project
AZDO_PAT=your-personal-access-token
```

Get your PAT from Azure DevOps: **User Settings** → **Personal Access Tokens**  
Required scopes: **Build (Read)**, **Pipeline (Read)**

### 3. Configure Claude Desktop

Edit your Claude Desktop config file:

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`  
**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "azure-devops": {
      "command": "python",
      "args": ["C:\\Projects\\mcp-azure-devops-assistant\\server.py"],
      "env": {
        "AZDO_ORG": "your-organization",
        "AZDO_PROJECT": "your-project",
        "AZDO_PAT": "your-personal-access-token"
      }
    }
  }
}
```

Restart Claude Desktop.

### 4. Test the Server

```bash
python server.py
```

## Available Tools

### `list_pipelines()`
Returns all pipelines in your Azure DevOps project.

### `get_failed_pipeline_runs(hours=24)`
Returns failed pipeline runs within the specified time window.

## Example Prompts

```
"What pipelines do we have?"

"Show me failed builds from the last 24 hours"

"Which pipeline has failed most often this week?"

"Give me a summary of overnight build failures with links"
```

## Example Output

```
User: Any failed runs today?

Claude: Let me check for you.

Yes, there have been 2 failed runs:

1. frontend-build
   - Failed at: 2026-01-14 10:30 UTC
   - Link: https://dev.azure.com/org/project/_build/results?buildId=12345

2. integration-tests
   - Failed at: 2026-01-14 08:15 UTC
   - Link: https://dev.azure.com/org/project/_build/results?buildId=12340
```

## What I Learned

**MCP is Simple:** FastMCP makes building MCP servers incredibly straightforward. The entire server is ~30 lines of Python.

**Authentication:** Azure DevOps uses Basic Auth with base64-encoded PAT tokens. Keep credentials in environment variables, not code.

**Natural Language Power:** Users can ask complex questions without knowing API structures. Claude combines tool calls intelligently to answer sophisticated queries.

**Rapid Development:** From idea to working integration took just a few hours. MCP dramatically reduces the friction of connecting AI to existing tools.

**Future Ideas:** Add more tools (trigger builds, view logs, work items), implement caching, add webhook support for real-time updates.

## Contributing

Contributions welcome! Open an issue or submit a pull request.

## License

MIT License
