# 🚀 MCP Azure DevOps Assistant

A Model Context Protocol (MCP) server that integrates Azure DevOps with AI assistants like Claude, enabling intelligent conversations about your CI/CD pipelines, build failures, and DevOps workflows.

## 📋 Table of Contents

- [What is MCP?](#what-is-mcp)
- [Architecture](#architecture)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Available Tools](#available-tools)
- [Example AI Prompts](#example-ai-prompts)
- [Screenshots & Logs](#screenshots--logs)
- [Lessons Learned](#lessons-learned)
- [Contributing](#contributing)
- [License](#license)

## 🤖 What is MCP?

**Model Context Protocol (MCP)** is an open protocol developed by Anthropic that standardizes how AI assistants connect to external data sources and tools. Think of it as a universal adapter that allows AI models like Claude to:

- Access your local files, databases, and APIs
- Execute tools and functions on your behalf
- Maintain context across conversations
- Interact with third-party services securely

Instead of copying and pasting data into AI chats, MCP enables direct, real-time access to your development tools—making AI assistants far more useful for software engineering tasks.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Claude Desktop                         │
│                    (AI Assistant)                           │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            │ MCP Protocol (stdio)
                            │
┌───────────────────────────▼─────────────────────────────────┐
│              MCP Azure DevOps Server (server.py)            │
│                                                              │
│  ┌──────────────────┐      ┌──────────────────┐            │
│  │ list_pipelines() │      │ get_failed_      │            │
│  │                  │      │ pipeline_runs()  │            │
│  └────────┬─────────┘      └────────┬─────────┘            │
│           │                         │                       │
│           └────────┬────────────────┘                       │
│                    │                                        │
│         ┌──────────▼──────────┐                             │
│         │ AzureDevOpsClient   │                             │
│         │ (azure_devops_      │                             │
│         │  client.py)         │                             │
│         └──────────┬──────────┘                             │
└────────────────────┼────────────────────────────────────────┘
                     │
                     │ REST API (HTTPS)
                     │ + Personal Access Token (PAT)
                     │
┌────────────────────▼────────────────────────────────────────┐
│              Azure DevOps REST API                          │
│                                                              │
│  • Pipelines API                                            │
│  • Builds API                                               │
│  • Project/Organization Resources                           │
└─────────────────────────────────────────────────────────────┘
```

### Architecture Components:

1. **Claude Desktop**: AI assistant that interacts with users and calls MCP tools
2. **MCP Server**: Python server exposing Azure DevOps functionality as MCP tools
3. **Azure DevOps Client**: Wrapper around Azure DevOps REST APIs with authentication
4. **Azure DevOps**: Cloud service hosting your CI/CD pipelines and build data

## ✨ Features

- 🔍 **List all pipelines** in your Azure DevOps project
- ❌ **Track failed pipeline runs** with customizable time windows
- 🔗 **Direct links** to Azure DevOps web interface for investigation
- 🤖 **Natural language queries** through Claude or compatible AI assistants
- 🔐 **Secure authentication** using Personal Access Tokens (PAT)
- ⚡ **Real-time data** directly from Azure DevOps APIs

## 📦 Installation

### Prerequisites

- Python 3.10 or higher
- An Azure DevOps account with appropriate permissions
- Claude Desktop (or compatible MCP client)
- Personal Access Token (PAT) from Azure DevOps

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/mcp-azure-devops-assistant.git
   cd mcp-azure-devops-assistant
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file** in the project root:
   ```env
   AZDO_ORG=your-organization-name
   AZDO_PROJECT=your-project-name
   AZDO_PAT=your-personal-access-token
   ```

4. **Test the server:**
   ```bash
   python server.py
   ```

## ⚙️ Configuration

### Azure DevOps Setup

1. Navigate to your Azure DevOps organization
2. Go to **User Settings** → **Personal Access Tokens**
3. Create a new token with the following scopes:
   - **Build**: Read
   - **Pipeline**: Read
4. Copy the token and add it to your `.env` file

### Claude Desktop Configuration

Add the MCP server to your Claude Desktop configuration file:

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "azure-devops": {
      "command": "python",
      "args": ["C:\\Projects\\mcp-azure-devops-assistant\\server.py"],
      "env": {
        "AZDO_ORG": "your-organization-name",
        "AZDO_PROJECT": "your-project-name",
        "AZDO_PAT": "your-personal-access-token"
      }
    }
  }
}
```

After editing the configuration, restart Claude Desktop.

## 🛠️ Available Tools

### 1. `list_pipelines()`

Lists all Azure DevOps pipelines in your configured project.

**Returns:**
```json
[
  {
    "id": 123,
    "name": "frontend-build"
  },
  {
    "id": 456,
    "name": "backend-deploy"
  }
]
```

### 2. `get_failed_pipeline_runs(hours: int = 24)`

Retrieves all failed pipeline runs within the specified time window.

**Parameters:**
- `hours` (int, optional): Number of hours to look back. Default: 24

**Returns:**
```json
[
  {
    "pipeline": "frontend-build",
    "finished_at": "2026-01-14T10:30:00Z",
    "url": "https://dev.azure.com/org/project/_build/results?buildId=789"
  }
]
```

## 💬 Example AI Prompts

Here are some natural language prompts you can use with Claude once the MCP server is configured:

### Basic Queries

```
"What pipelines do we have in Azure DevOps?"
```

```
"Show me all failed pipeline runs from the last 24 hours"
```

```
"Have any builds failed in the past week?"
```

### Advanced Analysis

```
"Which pipeline has failed most frequently in the last 48 hours?"
```

```
"Summarize the failed builds from today and provide direct links to investigate"
```

```
"List all pipelines and tell me which ones had failures in the last 3 days"
```

### DevOps Workflow

```
"Check if any builds failed overnight and give me a morning standup summary"
```

```
"Monitor our CI/CD health - show me any failures in the last 12 hours with timestamps"
```

```
"Generate a report of all pipeline failures this week grouped by pipeline name"
```

## 📸 Screenshots & Logs

### Example Conversation

```
User: What pipelines do we have?

Claude: I'll check your Azure DevOps pipelines.

[Uses list_pipelines() tool]

You have 3 pipelines in your project:
1. frontend-build (ID: 123)
2. backend-deploy (ID: 456)
3. integration-tests (ID: 789)

---

User: Any failed runs in the last 24 hours?

Claude: Let me check for recent failures.

[Uses get_failed_pipeline_runs(hours=24) tool]

Yes, there have been 2 failed runs:

1. **frontend-build**
   - Failed at: 2026-01-14 10:30 UTC
   - Link: https://dev.azure.com/myorg/myproject/_build/results?buildId=12345

2. **integration-tests**
   - Failed at: 2026-01-14 08:15 UTC
   - Link: https://dev.azure.com/myorg/myproject/_build/results?buildId=12340

Would you like me to help investigate what went wrong?
```

### Server Logs

```
✅ MCP Azure DevOps Server starting...
INFO: Started server process
INFO: Waiting for application startup.
INFO: Application startup complete.
```

## 📚 Lessons Learned

### Technical Insights

1. **MCP Protocol Simplicity**: The MCP protocol using stdio transport is remarkably simple to implement. The `FastMCP` library abstracts away most complexity.

2. **Authentication Patterns**: Azure DevOps uses Basic Authentication with PAT tokens encoded in base64. Keeping credentials in environment variables (`.env`) keeps them out of code.

3. **API Design Matters**: Azure DevOps APIs are well-documented but require careful attention to API versions and parameter formatting. Using query parameters for filtering (like `resultFilter=failed`) makes the client code clean.

4. **Error Handling**: Production-ready MCP servers need robust error handling around API calls, authentication failures, and rate limiting.

### Development Experience

- **Rapid Prototyping**: Going from idea to working MCP server took just a few hours thanks to FastMCP
- **Debugging**: Testing MCP servers directly via `python server.py` before integrating with Claude speeds up development
- **Environment Variables**: Using `python-dotenv` made configuration management clean and secure

### AI Integration Discoveries

- **Natural Language Power**: Users don't need to know API endpoints or JSON structures—they just ask questions
- **Context Awareness**: Claude can combine multiple tool calls to answer complex questions (e.g., "which pipeline fails most often?")
- **Human-Friendly Output**: The AI naturally formats timestamps, creates links, and summarizes data in readable ways

### Future Improvements

- Add more tools (create pipeline runs, get logs, work items)
- Implement caching to reduce API calls
- Add webhook support for real-time notifications
- Support multiple projects/organizations
- Add retry logic and rate limiting
- Provide more detailed error messages in tool responses

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Anthropic](https://www.anthropic.com/) for developing the Model Context Protocol
- [FastMCP](https://github.com/jlowin/fastmcp) library for simplifying MCP server development
- Azure DevOps team for comprehensive REST APIs

---

**Made with ❤️ for the DevOps community**

*Questions? Issues? Feel free to open an issue or reach out!*
