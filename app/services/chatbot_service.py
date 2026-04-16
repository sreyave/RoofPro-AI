from app.services.estimate_service import calculate_full_estimate
from app.services.ai_service import get_ai_response
from app.services.google_sheets_service import save_lead
from app.services.rag_service import search_knowledge
import re

user_state = {}
user_data = {}
user_completed_lead = {}
user_last_intent = {}
user_estimate_data = {}




def handle_chat(user_input, user_id="default"):
    user_input = user_input.lower().strip()

    # ======================
    # 📥 LEAD CAPTURE FLOW
    # ======================

    # NAME
    if user_state.get(user_id) == "waiting_for_name":
      user_data[user_id] = {"name": user_input.strip().title()}
      user_state[user_id] = "waiting_for_phone"
      return "Great 😊 Please enter your phone number:"

    # PHONE
    elif user_state.get(user_id) == "waiting_for_phone":

     

      # simple phone validation
      if not re.fullmatch(r"\d{6,}", user_input):
        return "Please enter a valid phone number (digits only)"

      user_data[user_id]["phone"] = user_input
      user_state[user_id] = "waiting_for_issue"
      return "Thanks! What roofing issue are you facing?"

    # ISSUE
    elif user_state.get(user_id) == "waiting_for_issue":
      user_data[user_id]["issue"] = user_input

      # Save lead
      save_lead(
        user_data[user_id]["name"],
        user_data[user_id]["phone"],
        user_data[user_id]["issue"]
      )

      # mark completed
      user_completed_lead[user_id] = True

      # reset state + data
      user_state[user_id] = None
      user_data[user_id] = {}

      return (
        "Thank you! Our team will contact you shortly 😊\n\n"
        "If it's urgent, please stay safe and avoid damaged areas.\n"
        "Feel free to ask if you need anything else!"
      )


    # ======================
    # 💰 ESTIMATE FLOW
    # ======================

    elif user_state.get(user_id) == "waiting_for_sqft":
        numbers = re.findall(r"\d+", user_input)
    
        if numbers:
            user_estimate_data[user_id] = {"sqft": int(numbers[0])}
            user_state[user_id] = "waiting_for_material"
            return "What roofing material do you want? (asphalt / metal / clay / flat)"
        return "Please enter a valid square footage (e.g., 1200)"


    elif user_state.get(user_id) == "waiting_for_material":
        user_estimate_data[user_id]["material"] = user_input
        user_state[user_id] = "waiting_for_pitch"
        return "What is the roof pitch? (low / medium / high)"
    

    elif user_state.get(user_id) == "waiting_for_pitch":
        user_estimate_data[user_id]["pitch"] = user_input
        user_state[user_id] = "waiting_for_complexity"
        return "What is the roof complexity? (simple / medium / complex)"


    elif user_state.get(user_id) == "waiting_for_complexity":
        user_estimate_data[user_id]["complexity"] = user_input
        user_state[user_id] = "waiting_for_floors"
        return "How many floors does the building have?"


    elif user_state.get(user_id) == "waiting_for_floors":
        numbers = re.findall(r"\d+", user_input)
    
        if not numbers:
            return "Please enter number of floors (e.g., 2)"

        user_estimate_data[user_id]["floors"] = int(numbers[0])

        # 🧠 CALCULATE FINAL PRICE
        data = user_estimate_data[user_id]

        price = calculate_full_estimate(    
        data["sqft"],
        data["material"],
        data["pitch"],
        data["complexity"],
        data["floors"]
    )

        user_state[user_id] = None
        user_estimate_data[user_id] = {}

        return f"""    
📐 Estimated Roofing Cost

• Area: {data['sqft']} sq ft  
• Material: {data['material']}  
• Pitch: {data['pitch']}  
• Complexity: {data['complexity']}  
• Floors: {data['floors']}  

💰 Estimated Cost: ₹{price}

⚠️ This is an approximate estimate based on market rates.
"""
    

    # ======================
    # 📋 MENU OPTIONS
    # ======================

    if user_input in ["1", "services"]:
        return (
            "We offer:\n"
            "• Roof Installation\n"
            "• Roof Repair\n"
            "• Roof Replacement\n"
            "• Inspection & Maintenance"
        )

    elif user_input in ["2", "emergency", "leak"]:
        return (
            "In case of emergency:\n"
            "• Avoid standing under damaged areas\n"
            "• Use temporary cover if possible\n"
            "• Contact professionals immediately"
        )

    elif user_input in ["3", "estimate"]:
        user_state[user_id] = "waiting_for_sqft"
        return "Please enter your roof size in square feet (e.g., 1200)"

    elif user_input in ["4", "contact"]:
     if user_completed_lead.get(user_id):
         return (
            "You're already connected with our team 😊\n\n"
            "They will reach out to you shortly.\n"
            "📞 If urgent, call: +91 9876543210"
        )
     user_state[user_id] = "waiting_for_name"
     return "Sure 😊 Please enter your name:"


    # ======================
    # 👋 GREETING
    # ======================

    if user_input in ["hi", "hello", "hey"]:
        return (
            "Hello! 👋\n\n"
            "How can I assist you today?\n\n"
            "🏠 1 · Our Services\n"
            "🚨 2 · Emergency Repair Guide\n"
            "📐 3 · Get a Roof Estimate\n"
            "👤 4 · Contact a Human"
        )
    
    # ======================
    # ✅ YES / NO HANDLING (TOP PRIORITY)
    # ======================

    if user_input in ["yes", "yeah", "y", "sure", "ok", "okay"]:

        last_intent = user_last_intent.get(user_id)

        if last_intent == "contact":

            user_last_intent[user_id] = None  # clear

            if user_completed_lead.get(user_id):
                return "Our team will contact you shortly 😊"

            user_state[user_id] = "waiting_for_name"
            return "Sure 😊 Please enter your name:"

        return "Great 😊 How can I assist you further?"


    if user_input in ["no", "nope", "not now"]:
        user_last_intent[user_id] = None
        return (
            "No problem 😊\n\n"
            "You can choose an option:\n\n"
            "🏠 1 · Our Services\n"
            "🚨 2 · Emergency Repair Guide\n"
            "📐 3 · Get a Roof Estimate\n"
            "👤 4 · Contact a Human"
        )
    


    # ======================
    # 📞 CONTACT INTENT (STRONG)
    # ======================

    if any(phrase in user_input for phrase in [
        "talk", "call", "contact", "connect", "speak",
        "professional", "expert", "support", "help me", "someone", "team", "number"
    ]):
        if user_completed_lead.get(user_id):
            return (
                "Our team will contact you shortly 😊\n\n"
                "📞 For immediate help, you can also call us at: +91 9876543210"
            )

        user_state[user_id] = "waiting_for_name"
        return (
            "Sure 😊 I’ll connect you with our team.\n\n"
            "Please enter your name:"
        )
    


    # ======================
    # 🤔 EXPENSIVE / DOUBT HANDLING
    # ======================

    if any(word in user_input for word in ["high", "expensive", "costly"]):

        # ✅ SAVE INTENT (IMPORTANT for YES)
        user_last_intent[user_id] = "contact"

        return (
            "I understand your concern 😊\n\n"
            "Roofing costs depend on materials, labor, and roof condition.\n"
            "Our estimate is a general range.\n\n"
            "Would you like a detailed quote or to speak with our team?"
        )


    # ======================
    # 💰 COST QUESTIONS
    # ======================

    if "cost" in user_input or "price" in user_input:
        return "To get an accurate estimate, please choose option 3 📐"


    # ======================
    # 🏠 MORE SERVICES
    # ======================

    if "more" in user_input and "service" in user_input:
        return (
            "Yes 😊 In addition to installation and repair, we also provide:\n\n"
            "• Roof replacement\n"
            "• Preventive maintenance\n"
            "• Roof inspections\n"
            "• Emergency repair services"
        )



    # ======================
    # 🚨 EMERGENCY / DAMAGE HANDLING
    # ======================

    if any(word in user_input for word in ["emergency", "urgent", "broken", "leak", "damage"]):

        # ✅ SAVE INTENT (VERY IMPORTANT)
        user_last_intent[user_id] = "contact"

        return (
           "⚠️ It looks like an urgent roofing issue.\n\n"
           "For immediate safety:\n"
           "• Stay away from damaged areas\n"
           "• Use a temporary cover (like tarp) if safe\n"
           "• Avoid water accumulation\n\n"
           "Would you like me to connect you with our professionals right away?"
        )


    # ======================
    # 🔧 REPAIR HELP (NON-EMERGENCY)
    # ======================

    if "repair" in user_input:

        # also allow contact follow-up
        user_last_intent[user_id] = "contact"

        return (
           "Here’s what you can do for a temporary fix:\n\n"
           "• Cover the damaged area with waterproof material\n"
           "• Avoid standing under the roof\n"
           "• Try to prevent further water leakage\n\n"
           "Would you like me to connect you with our professionals?"
        )
   



    # ======================
    # 📞 DIRECT NUMBER REQUEST
    # ======================

    if any(word in user_input for word in ["number", "phone number"]):
        return (
            "Our team will contact you shortly 😊\n\n"
            "For immediate assistance, please choose option 4 to connect with us."
        )

    # ======================
    # 🤖 RAG + SMART FALLBACK
    # ======================

    context = search_knowledge(user_input)

    if not context:
        return (
            "I'm not completely sure about that 🤔\n\n"
            "But I can help you with:\n\n"
            "🏠 1 · Our Services\n"
            "🚨 2 · Emergency Repair Guide\n"
            "📐 3 · Get a Roof Estimate\n"
            "👤 4 · Contact a Human\n\n"
            "Please choose an option 😊"
        )

    return get_ai_response(user_input, context)
