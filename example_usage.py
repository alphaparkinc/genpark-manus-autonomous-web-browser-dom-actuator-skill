from client import ManusAutonomousWebBrowserDOMActuator

def main():
    actuator = ManusAutonomousWebBrowserDOMActuator()
    sample_dom = [
        {"tag": "input", "id": "flight_origin", "text": "From Airport", "is_visible": True},
        {"tag": "input", "id": "flight_dest", "text": "To Destination", "is_visible": True},
        {"tag": "button", "id": "btn_find_flights", "text": "Find Flights Now", "is_visible": True}
    ]
    plan = actuator.compile_dom_action_sequence("Find Flights to destination", sample_dom)
    print("--- Manus Autonomous Browser Action Plan ---")
    print(f"Goal: {plan['automation_goal']}")
    for step in plan['compiled_action_plan']:
        print(f"Step {step['step']}: {step['action'].upper()} -> Selector: {step['target_selector']} (Label: '{step['element_label']}')")

if __name__ == "__main__":
    main()
