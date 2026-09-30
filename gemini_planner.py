import os
import json
import requests
from knowledge_base import DESTINATIONS

class GeminiTripPlanner:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY", "").strip()

    def generate_personalized_plan(self, user_input, selected_dest):
        """
        Generates a personalized structured travel plan using Gemini AI or local fallback engine.
        Returns dict matching standard PlanAway JSON structure.
        """
        api_key = user_input.get("gemini_api_key", "").strip() or self.api_key
        
        if api_key:
            try:
                ai_plan = self._call_gemini_api(api_key, user_input, selected_dest)
                if ai_plan:
                    return ai_plan
            except Exception as e:
                print(f"[GeminiTripPlanner] API call error: {e}. Falling back to rule-based AI generator.")
                
        return self._generate_fallback_plan(user_input, selected_dest)

    def _call_gemini_api(self, api_key, user_input, selected_dest):
        """Calls Google Gemini REST API endpoint for structured JSON output."""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        
        prompt = f"""
You are PlanAway AI Travel Planner. Generate a comprehensive, personalized travel plan as valid JSON only.

User Request:
- From: {user_input.get('from')}
- Destination: {selected_dest.get('destination')}
- Interest: {user_input.get('interest')}
- Budget: ₹{user_input.get('budget')}
- Travellers: {user_input.get('persons')}
- Days: {user_input.get('days')}
- Travel Mode: {user_input.get('travel_mode')}
- Travel Style: {user_input.get('travel_style')}
- Special Request: {user_input.get('special_request', 'None')}

Output JSON format strictly with keys:
"tripSummary", "destinations", "routes", "itinerary", "budget", "hotels", "tips".

Structure specs:
- tripSummary: {{ "destination": str, "days": int, "persons": int, "totalBudget": int, "estimatedCost": int, "travelStyle": str, "vibe": str }}
- destinations: list of {{ "name": str, "description": str, "highlights": list of str }}
- routes: list of {{ "mode": str, "route": str, "estimatedTime": str, "estimatedCostPerPerson": int, "advice": str }}
- itinerary: list of {{ "day": int, "title": str, "morning": str, "afternoon": str, "evening": str, "recommendedFood": str }}
- budget: {{ "transportCost": int, "stayCost": int, "foodCost": int, "activityCost": int, "totalEstimatedCost": int, "savingsOrDeficit": str }}
- hotels: list of {{ "name": str, "category": str, "pricePerNight": int, "rating": str, "whyRecommended": str }}
- tips: list of str (at least 4 practical travel tips)
"""
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.7,
                "response_mime_type": "application/json"
            }
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=12)
        if response.status_code == 200:
            res_data = response.json()
            text_content = res_data["candidates"][0]["content"]["parts"][0]["text"]
            return json.loads(text_content)
        else:
            print(f"Gemini API returned status {response.status_code}: {response.text}")
            return None

    def _generate_fallback_plan(self, user_input, selected_dest):
        """Generates a rich, highly detailed rule-based travel plan."""
        dest_name = selected_dest.get("destination", "Goa")
        from_city = user_input.get("from", "Chennai")
        days = int(user_input.get("days", 3))
        persons = int(user_input.get("persons", 2))
        budget = float(user_input.get("budget", 15000))
        mode = user_input.get("travel_mode", "Bus")
        style = user_input.get("travel_style", "Budget")
        special_req = user_input.get("special_request", "").strip()

        costs = selected_dest.get("costs", {
            "travel_cost": 3000,
            "stay_cost": 6000,
            "food_activity_cost": 3000,
            "total_cost": 12000
        })

        # Match destination knowledge base item
        kb_dest = next((d for d in DESTINATIONS if d["name"].lower() == dest_name.lower()), None)
        attractions = kb_dest["attractions"] if kb_dest else ["Main Sightseeing Spot", "Local Market", "Sunset Viewpoint"]
        hotel_list = kb_dest["hotels"] if kb_dest else ["Comfort Inn", "Grand Heritage Hotel", "Zostel Hostel"]

        # Build day-by-day itinerary dynamically
        itinerary = []
        for d in range(1, days + 1):
            if d == 1:
                morning = f"Depart early morning from {from_city} via {mode}. Enjoy scenic en-route landscapes."
                afternoon = f"Arrive in {dest_name}, check into hotel, refresh, and savor local authentic cuisine."
                evening = f"Visit {attractions[0]} for a relaxing sunset experience and evening stroll."
                food = "Local regional thali and refreshing natural drinks."
            elif d == days:
                morning = f"Early breakfast and visit {attractions[-1]} for souvenir shopping."
                afternoon = "Check out from hotel, pack local specialties, and begin return journey."
                evening = f"Arrive back safely in {from_city} with unforgettable memories."
                food = "Snacks, local bakery treats, and evening tea."
            else:
                att1 = attractions[(d - 1) % len(attractions)]
                att2 = attractions[d % len(attractions)]
                morning = f"Morning tour to {att1} for sightseeing and photography."
                afternoon = f"Post lunch visit to {att2} and local artisan markets."
                evening = f"Leisure time, cultural street explore in {dest_name}, and live music or local night market."
                food = "Specialty seafood / grill or traditional vegetarian feast."
                
            itinerary.append({
                "day": d,
                "title": f"Day {d}: Exploring {dest_name}",
                "morning": morning,
                "afternoon": afternoon,
                "evening": evening,
                "recommendedFood": food
            })

        # Route info
        speed_map = {"Bus": "10-14 hours", "Train": "8-12 hours", "Car": "7-10 hours", "Flight": "1.5-2.5 hours (plus airport transit)"}
        est_time = speed_map.get(mode, "8-12 hours")

        routes = [
            {
                "mode": mode,
                "route": f"Direct route from {from_city} to {dest_name}",
                "estimatedTime": est_time,
                "estimatedCostPerPerson": int(costs["travel_cost"] / max(persons, 1)),
                "advice": f"Book your {mode} tickets 1-2 weeks in advance for optimal seat selection and discounts."
            },
            {
                "mode": "Train" if mode != "Train" else "Flight",
                "route": f"Alternative rail/air connection between {from_city} and {dest_name}",
                "estimatedTime": "6-10 hours",
                "estimatedCostPerPerson": int(costs["travel_cost"] * 0.9 / max(persons, 1)),
                "advice": "Consider overnight sleeper journeys to save daytime for sightseeing."
            }
        ]

        # Hotel suggestions
        hotels = [
            {
                "name": hotel_list[0],
                "category": f"{style} Resort / Hotel",
                "pricePerNight": int(costs["stay_cost"] / max(days * persons, 1)),
                "rating": "4.5 / 5.0",
                "whyRecommended": f"Top rated location in {dest_name} matching your {style} travel preferences."
            },
            {
                "name": hotel_list[1] if len(hotel_list) > 1 else "Boutique Heritage Stay",
                "category": "Boutique / Homestay",
                "pricePerNight": int(costs["stay_cost"] * 0.8 / max(days * persons, 1)),
                "rating": "4.3 / 5.0",
                "whyRecommended": "Offers authentic local hospitality, central access, and great breakfast options."
            }
        ]

        # Tips
        tips = [
            f"Best time to start daily sightseeing in {dest_name} is around 8:30 AM to beat peak tourist rush.",
            f"Keep digital copies of tickets & IDs accessible on your phone.",
            f"Travel style '{style}' estimated total cost is ₹{int(costs['total_cost']):,} for {persons} traveller(s).",
            f"Special Note: {special_req if special_req else 'Enjoy your personalized AI-curated travel experience!'}"
        ]

        if kb_dest and kb_dest.get("tips"):
            tips.append(kb_dest["tips"])

        total_est = int(costs["total_cost"])
        budget_int = int(budget)
        diff = budget_int - total_est

        return {
            "tripSummary": {
                "destination": dest_name,
                "days": days,
                "persons": persons,
                "totalBudget": budget_int,
                "estimatedCost": total_est,
                "travelStyle": style,
                "vibe": f"Personalized {selected_dest.get('interest', 'Vacation')} getaway tailor-made from {from_city}"
            },
            "destinations": [
                {
                    "name": dest_name,
                    "description": selected_dest.get("description", ""),
                    "highlights": selected_dest.get("attractions", [])
                }
            ],
            "routes": routes,
            "itinerary": itinerary,
            "budget": {
                "transportCost": int(costs["travel_cost"]),
                "stayCost": int(costs["stay_cost"]),
                "foodCost": int(costs.get("food_activity_cost", costs["stay_cost"] * 0.4)),
                "activityCost": int(costs.get("food_activity_cost", costs["stay_cost"] * 0.4) * 0.5),
                "totalEstimatedCost": total_est,
                "savingsOrDeficit": f"Savings of ₹{diff:,}" if diff >= 0 else f"Deficit of ₹{abs(diff):,}"
            },
            "hotels": hotels,
            "tips": tips
        }
