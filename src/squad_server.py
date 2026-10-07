#!/usr/bin/env python3
"""
Squad MCP Server
Orchestrator for multi-agent copilot system.
Runs as MCP server for Orca and any other harness.
"""
import os
import json
import yaml
import subprocess
from pathlib import Path
from datetime import datetime

SQUAD_DIR = Path.home() / ".agents" / "squad"
CONFIG_PATH = SQUAD_DIR / "config.yml"
WORKSPACE = SQUAD_DIR / "workspace"
LOG_PATH = WORKSPACE / "squad.log"

def load_config():
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)

def save_config(cfg):
    with open(CONFIG_PATH, "w") as f:
        yaml.dump(cfg, f)

def log(msg):
    ts = datetime.utcnow().isoformat()
    line = f"[{ts}] {msg}\n"
    with open(LOG_PATH, "a") as f:
        f.write(line)

def detect_agents(cfg):
    """Scan PATH for configured CLI agents, update config if changed."""
    changed = False
    agents_cfg = cfg.get("agents", {})
    for name, info in agents_cfg.items():
        cli = info.get("cli")
        if cli and not Path(cli).exists():
            # try which
            # simplified: mark missing
            pass
    return changed

# MCP tool handlers (simplified)
def squad_status():
    cfg = load_config()
    log("status requested")
    return {
        "orchestrator": cfg.get("orchestrator"),
        "agents": list(cfg.get("agents", {}).keys()),
        "copilots": list(cfg.get("copilots", {}).keys()),
        "autodetect": cfg.get("autodetect")
    }

def squad_agents_list():
    cfg = load_config()
    return {"agents": cfg.get("agents", {})}

def squad_copilots_map():
    cfg = load_config()
    return {"copilots": cfg.get("copilots", {})}

def squad_config_get(key=None):
    cfg = load_config()
    if key:
        return json.loads(json.dumps({key: cfg.get(key)}))
    return cfg

def squad_config_set(key, value):
    cfg = load_config()
    # simple dot notation not implemented, just top-level
    cfg[key] = value
    save_config(cfg)
    log(f"config set {key}")
    return {"ok": True}

def squad_reload():
    cfg = load_config()
    changed = detect_agents(cfg)
    log(f"reload, changed={changed}")
    return {"changed": changed}

def squad_dispatch(chain, request):
    cfg = load_config()
    log(f"dispatch chain={chain} request={request[:100]}")
    # Minimal implementation: return chain steps with agent mapping
    chain_def = cfg.get("chains", {}).get(chain, {})
    steps = chain_def.get("steps", [])
    mapping = {}
    for step in steps:
        disc = step["discipline"]
        copilot = cfg.get("copilots", {}).get(disc, {})
        primary = copilot.get("primary")
        mapping[disc] = primary
    return {"chain": chain, "mapping": mapping, "status": "queued"}

# Simple MCP JSON-RPC loop (stub)
# In production use mcp.server stdio
if __name__ == "__main__":
    import sys
    log("Squad MCP server started")
    # Stub: read stdin line, respond
    for line in sys.stdin:
        try:
            req = json.loads(line)
            method = req.get("method")
            params = req.get("params", {})
            if method == "squad.status":
                res = squad_status()
            elif method == "squad.agents.list":
                res = squad_agents_list()
            elif method == "squad.copilots.map":
                res = squad_copilots_map()
            elif method == "squad.config.get":
                res = squad_config_get(params.get("key"))
            elif method == "squad.config.set":
                res = squad_config_set(params.get("key"), params.get("value"))
            elif method == "squad.reload":
                res = squad_reload()
            elif method == "squad.dispatch":
                res = squad_dispatch(params.get("chain"), params.get("request"))
            else:
                res = {"error": "unknown method"}
            print(json.dumps({"result": res}))
        except Exception as e:
            print(json.dumps({"error": str(e)}))
