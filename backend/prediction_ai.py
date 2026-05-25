import os
import json
from groq import Groq
from dotenv import load_dotenv

# ======================================
# LOAD ENV
# ======================================

load_dotenv()

# ======================================
# GROQ CLIENT
# ======================================

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ======================================
# AI PREDICTION FUNCTION
# ======================================

def generate_ai_prediction(area):

    prompt = f"""
    You are an advanced Smart Traffic AI system.

    Analyze traffic conditions for:
    {area}

    Generate:

    1. congestion_percent
    2. congestion_level
    3. best_travel_time
    4. avoid_route
    5. predicted_travel_time
    6. ai_alert
    7. weather_impact
    8. peak_hours

    Return ONLY valid JSON.

    Example:

    {{
        "congestion_percent":"78%",
        "congestion_level":"High",
        "best_travel_time":"After 10 AM",
        "avoid_route":"Mumbai Pune Expressway",
        "predicted_travel_time":"45 mins",
        "ai_alert":"Heavy traffic expected",
        "weather_impact":"Moderate",
        "peak_hours":"6 PM - 9 PM"
    }}
    """

    try:

        response = client.chat.completions.create(

            model="llama3-70b-8192",

            messages=[
                {
                    "role":"user",
                    "content":prompt
                }
            ],

            temperature=0.7
        )

        text = response.choices[0].message.content

        data = json.loads(text)

        return data

    except Exception as e:

        return {

            "congestion_percent":"72%",

            "congestion_level":"High",

            "best_travel_time":"After 10 AM",

            "avoid_route":"Mumbai Pune Expressway",

            "predicted_travel_time":"42 mins",

            "ai_alert":"Heavy traffic expected",

            "weather_impact":"Moderate",

            "peak_hours":"6 PM - 9 PM"
        }