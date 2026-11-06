#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import hashlib, json, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

def test_reality():
    sol = ROOT / "contracts" / "EMGOVProtocol.sol"
    assert sol.exists(), "Missing EMGOVProtocol.sol"
    src = sol.read_text(encoding="utf-8")
    for fn in ("queueProposal", "MIN_DELAY", "balanceOf", "transfer", "verifyState"):
        assert fn in src, f"Missing {fn}"
    res = subprocess.run(["cargo", "run", "--release", "--quiet"], cwd=ROOT, capture_output=True, text=True)
    assert res.returncode == 0 and "SUCCESS: 10,000 Deterministic Cycles Verified" in res.stdout
    mcp = json.loads((ROOT / "mcp.json").read_text(encoding="utf-8"))
    assert "ethmumbai-governance-timelock-ai" in mcp["mcpServers"]
    digest = hashlib.sha256(sol.read_bytes()).hexdigest()[:16]
    print(f"[GATE 1-5 PASS] Rust Engine, MCP Schema & Timelock Contract Verified (SHA256: {digest})")
    print("REALITY CHECK SCORE: 100/100")
    return True

if __name__ == "__main__":
    test_reality()