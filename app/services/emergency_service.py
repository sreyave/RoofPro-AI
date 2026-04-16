def get_emergency_guidance(issue):
    issue = issue.lower()

    safety = [
        "Do NOT climb onto the roof.",
        "Stay away from electrical wires or exposed cables.",
        "Take photos only if it is safe.",
        "Evacuate the area if structural damage is severe.",
        "Call emergency services if there is immediate danger."
    ]

    responses = {
        "tree": "🌳 Tree Damage Detected:\n- Stay away from impact zone\n- Check for structural cracks\n- Avoid entering damaged rooms",
        "storm": "⛈ Storm Damage Detected:\n- Check for leaks inside house\n- Avoid wet electrical areas\n- Secure loose objects",
        "leak": "💧 Roof Leakage Detected:\n- Place buckets to collect water\n- Avoid ceiling collapse zones\n- Switch off electricity if near water"
    }

    reply = responses.get(issue, "⚠ Emergency detected. Follow safety steps below:")

    return reply + "\n\nSafety Instructions:\n- " + "\n- ".join(safety)
