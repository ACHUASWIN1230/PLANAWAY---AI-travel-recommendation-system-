import os
import joblib
import pandas as pd
import numpy as np

from knowledge_base import (
    CITIES, DESTINATIONS, INTERESTS, TRAVEL_MODES,
    calculate_haversine_distance, estimate_travel_costs,
    calculate_rule_suitability_score
)

class PlanAwayRecommendationEngine:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.model_path = os.path.join(self.base_dir, "model.pkl")
        self.encoders_path = os.path.join(self.base_dir, "label_encoders.pkl")
        self.metrics_path = os.path.join(self.base_dir, "model_metrics.pkl")
        
        self.model = None
        self.encoders = None
        self.metrics = None
        self.load_artifacts()
        
    def load_artifacts(self):
        """Loads serialized ML model and label encoders if available."""
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.encoders_path):
                self.model = joblib.load(self.model_path)
                self.encoders = joblib.load(self.encoders_path)
                if os.path.exists(self.metrics_path):
                    self.metrics = joblib.load(self.metrics_path)
                print("[Recommendation Engine] Successfully loaded ML model and encoders.")
            else:
                print("[Recommendation Engine] Artifacts not found. Will train or fallback to travel logic rules.")
        except Exception as e:
            print(f"[Recommendation Engine] Error loading artifacts: {e}")
            self.model = None

    def predict_recommendations(self, user_input):
        """
        Receives user requirements dict:
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
        Evaluates candidate destinations, runs ML prediction + rule logic, ranks top results.
        """
        from_city = user_input.get("from", "Chennai")
        interest = user_input.get("interest", "Beach")
        budget = float(user_input.get("budget", 15000))
        persons = int(user_input.get("persons", 2))
        days = int(user_input.get("days", 3))
        travel_mode = user_input.get("travel_mode", "Bus")
        travel_style = user_input.get("travel_style", "Budget")
        
        city_coords = CITIES.get(from_city, CITIES["Chennai"])
        
        recommendations = []
        
        for dest in DESTINATIONS:
            dest_name = dest["name"]
            dest_interest = dest["interest"]
            
            # Distance
            distance = calculate_haversine_distance(
                city_coords["lat"], city_coords["lng"],
                dest["lat"], dest["lng"]
            )
            
            # Costs
            costs = estimate_travel_costs(
                distance, travel_mode, persons, days,
                dest["cost_per_day"], travel_style
            )
            
            # Rule score
            rule_score = calculate_rule_suitability_score(
                interest, dest_interest, budget, costs["total_cost"],
                days, dest["min_days"], distance, travel_mode
            )
            
            # Additional feature values
            interest_match = 1 if interest.lower() == dest_interest.lower() else 0
            budget_ratio = round(budget / max(costs["total_cost"], 1.0), 4)
            
            # ML Score Prediction
            ml_score = rule_score
            if self.model and self.encoders:
                try:
                    from_enc = self.encoders["From"].transform([from_city])[0] if from_city in self.encoders["From"].classes_ else 0
                    interest_enc = self.encoders["Interest"].transform([interest])[0] if interest in self.encoders["Interest"].classes_ else 0
                    mode_enc = self.encoders["TravelMode"].transform([travel_mode])[0] if travel_mode in self.encoders["TravelMode"].classes_ else 0
                    dest_enc = self.encoders["Destination"].transform([dest_name])[0] if dest_name in self.encoders["Destination"].classes_ else 0
                    
                    features = pd.DataFrame([{
                        "From": from_enc,
                        "Interest": interest_enc,
                        "Budget": budget,
                        "Persons": persons,
                        "Days": days,
                        "TravelMode": mode_enc,
                        "Destination": dest_enc,
                        "Distance": distance,
                        "EstTotalCost": costs["total_cost"],
                        "BudgetRatio": budget_ratio,
                        "InterestMatch": interest_match
                    }])
                    
                    pred = self.model.predict(features)[0]
                    ml_score = round(float(np.clip(pred, 0, 100)), 2)
                except Exception as ex:
                    print(f"Prediction error for {dest_name}: {ex}")
                    ml_score = rule_score

            final_score = round(0.7 * ml_score + 0.3 * rule_score, 2)
            
            recommendations.append({
                "destination": dest_name,
                "interest": dest_interest,
                "distance": distance,
                "recommended_mode": travel_mode,
                "cost_per_day": dest["cost_per_day"],
                "min_days": dest["min_days"],
                "costs": costs,
                "rule_score": rule_score,
                "ml_score": ml_score,
                "score": final_score,
                "description": dest["description"],
                "attractions": dest["attractions"],
                "hotels": dest["hotels"],
                "tips": dest["tips"],
                "budget_fit": "Within Budget" if costs["total_cost"] <= budget else f"Exceeds by ₹{int(costs['total_cost'] - budget):,}"
            })
            
        recommendations.sort(key=lambda x: x["score"], reverse=True)
        
        return recommendations
