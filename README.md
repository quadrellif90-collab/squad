# Squad — Multi-Agent Orchestrator

Squad is a portable MCP server that orchestrates 11 copilot disciplines across multiple CLI agents. Works with Orca, Claude Code, Qwen, Mimo and any MCP-compatible harness.

## Features

- 11 disciplines / copilots: researcher, architect, engineer, tester, critic, devops, writer, analyst, marketer, arbiter, coordinator
- Auto-detect CLI agents at startup with silent replacement + notifications
- Dynamic mapping via `squad.config.set`
- MCP tools: `squad.dispatch`, `squad.status`, `squad.reload`, `squad.config.get/set`, `squad.agents.list`, `squad.copilots.map`
- Portable: single Python process, no cloud dependency

## Quick Start

```bash
git clone https://github.com/<you>/squad.git
cd squad
pip install -r requirements.txt
cp config/config.yml.example ~/.agents/squad/config.yml
# edit paths to your agents
orca mcp add squad python src/squad_server.py
```

## Config

Edit `~/.agents/squad/config.yml`:
- `orchestrator.agent` — CLI that runs coordination
- `agents.*.cli` — absolute paths
- `copilots.*.primary/fallback` — mapping
- `autodetect.enabled` — true for auto-scan

## Development

```bash
python src/squad_server.py
```

## License

MIT
