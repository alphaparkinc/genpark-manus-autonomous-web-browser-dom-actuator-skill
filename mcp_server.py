#!/usr/bin/env python3
import json
import sys
from client import ManusAutonomousWebBrowserDOMActuator

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        actuator = ManusAutonomousWebBrowserDOMActuator()
        dom = [
            {"tag": "input", "id": "search_box", "text": "Search Products", "is_visible": True},
            {"tag": "button", "id": "btn_submit", "text": "Search", "is_visible": True},
            {"tag": "div", "id": "footer_dec", "text": "Copyright 2026", "is_visible": False}
        ]
        res = actuator.compile_dom_action_sequence("Search for item", dom)
        assert len(res["compiled_action_plan"]) >= 1
        assert res["verdict"] == "ACTION_PLAN_SYNTHESIZED"
        print(f"[TEST PASS] Manus DOM Action Plan Synthesized ({len(res['compiled_action_plan'])} steps)")
        sys.exit(0)

    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            if method == "initialize":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"serverInfo": {"name": "genpark-manus-actuator", "version": "1.0.0"}}}))
            elif method == "tools/list":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [{"name": "compile_dom_action_sequence", "description": "Manus autonomous web browser DOM actuator"}]}}))
            elif method == "tools/call":
                args = req.get("params", {}).get("arguments", {})
                actuator = ManusAutonomousWebBrowserDOMActuator()
                out = actuator.compile_dom_action_sequence(args.get("goal", ""), args.get("raw_dom_elements", []))
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(out)}]}}))
            else:
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
