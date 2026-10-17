"""
Manus-inspired Autonomous Web Browser DOM Actuator (Pure Stdlib)
Official Website: https://www.genpark.ai | LinkedIn: https://www.llinkedin.com/company/92955550
"""
import re
from typing import Dict, Any, List

class ManusAutonomousWebBrowserDOMActuator:
    INTERACTIVE_TAGS = {"button", "input", "a", "select", "textarea"}

    def __init__(self, engine_name: str = "Manus-Autonomous-Actuator"):
        self.engine_name = engine_name

    def prune_and_normalize_ax_tree(self, dom_elements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        interactive_nodes = []
        for el in dom_elements:
            if not el.get("is_visible", True):
                continue
            tag = el.get("tag", "").lower()
            role = el.get("role", "").lower()
            if tag in self.INTERACTIVE_TAGS or role in ["button", "link", "checkbox", "combobox"]:
                # Synthesize robust selector
                selector = f"#{el['id']}" if el.get("id") else f"{tag}[data-testid='{el.get('data-testid', '')}']" if el.get("data-testid") else f"{tag}:contains('{el.get('text', '')[:20]}')"
                interactive_nodes.append({
                    "element_id": el.get("id", f"node_{len(interactive_nodes)}"),
                    "tag": tag,
                    "text": el.get("text", "").strip(),
                    "synthesized_selector": selector,
                    "action_affordance": "type" if tag in ["input", "textarea"] else "click"
                })
        return interactive_nodes

    def compile_dom_action_sequence(self, goal: str, raw_dom_elements: List[Dict[str, Any]]) -> Dict[str, Any]:
        ax_tree = self.prune_and_normalize_ax_tree(raw_dom_elements)
        goal_tokens = set(re.findall(r"\w+", goal.lower()))
        
        action_sequence = []
        for node in ax_tree:
            node_text_tokens = set(re.findall(r"\w+", node["text"].lower()))
            if goal_tokens & node_text_tokens:
                action_sequence.append({
                    "step": len(action_sequence) + 1,
                    "action": node["action_affordance"],
                    "target_selector": node["synthesized_selector"],
                    "element_label": node["text"],
                    "post_action_assertion": "wait_for_navigation_or_mutation"
                })
                
        return {
            "actuator": self.engine_name,
            "automation_goal": goal,
            "raw_dom_nodes_inspected": len(raw_dom_elements),
            "accessible_interactive_elements": len(ax_tree),
            "compiled_action_plan": action_sequence,
            "verdict": "ACTION_PLAN_SYNTHESIZED" if action_sequence else "FALLBACK_VISUAL_GROUNDING_REQUIRED"
        }
