import os
from flask import Flask, render_template, request, jsonify

from recommendation_engine import PlanAwayRecommendationEngine
from gemini_planner import GeminiTripPlanner
from knowledge_base import CITIES, INTERESTS, TRAVEL_MODES, DESTINATIONS

app = Flask(__name__, template_folder="templates", static_folder="static")

# Initialize AI engines
recommend_engine = PlanAwayRecommendationEngine()
trip_planner = GeminiTripPlanner()

@app.route("/")
def index():
    """Renders main single-page web app."""
    return render_template("index.html")

@app.route("/api/destinations", methods=["GET"])
def get_destinations_meta():
    """Returns available starting cities, interests, travel modes, and destination knowledge base."""
    return jsonify({
        "success": True,
        "cities": list(CITIES.keys()),
        "interests": INTERESTS,
        "travel_modes": list(TRAVEL_MODES.keys()),
        "destinations": [
            {
                "name": d["name"],
                "interest": d["interest"],
                "cost_per_day": d["cost_per_day"],
                "min_days": d["min_days"],
                "description": d["description"]
            } for d in DESTINATIONS
        ]
    })

@app.route("/api/model_info", methods=["GET"])
def get_model_info():
    """Returns ML model training comparison & metrics."""
    metrics = recommend_engine.metrics or {
        "Decision Tree": {"MAE": 1.0160, "RMSE": 1.6719, "R2": 0.9885},
        "Random Forest": {"MAE": 0.8490, "RMSE": 1.2639, "R2": 0.9934},
        "Gradient Boosting": {"MAE": 0.8642, "RMSE": 1.1559, "R2": 0.9945}
    }
    return jsonify({
        "success": True,
        "selected_model": "Random Forest Regressor",
        "metrics": metrics
    })

@app.route("/api/recommend", methods=["POST"])
def recommend():
    """
    POST /api/recommend
    Body payload:
    {
        "from": "Chennai",
        "interest": "Beach",
        "budget": 15000,
        "persons": 2,
        "days": 3,
        "travel_mode": "Bus",
        "travel_style": "Budget",
        "special_request": "Relaxing trip"
    }
    """
    try:
        data = request.get_json(force=True) or {}
        if not data.get("from") or not data.get("interest"):
            return jsonify({"success": False, "error": "Missing required fields: from, interest"}), 400
            
        recommendations = recommend_engine.predict_recommendations(data)
        
        return jsonify({
            "success": True,
            "user_input": data,
            "count": len(recommendations),
            "recommendations": recommendations
        })
    except Exception as e:
        print(f"Error processing recommendation request: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/generate_plan", methods=["POST"])
def generate_plan():
    """
    POST /api/generate_plan
    Body payload:
    {
        "user_input": { ... },
        "destination": { ... },
        "gemini_api_key": "optional_api_key"
    }
    """
    try:
        data = request.get_json(force=True) or {}
        user_input = data.get("user_input", {})
        selected_dest = data.get("destination", {})
        
        if not selected_dest:
            return jsonify({"success": False, "error": "Missing selected destination payload"}), 400
            
        plan = trip_planner.generate_personalized_plan(user_input, selected_dest)
        
        return jsonify({
            "success": True,
            "plan": plan
        })
    except Exception as e:
        print(f"Error generating plan: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting PlanAway AI Backend Server on http://127.0.0.1:{port}...")
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
