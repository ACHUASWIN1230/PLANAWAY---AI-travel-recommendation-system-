import os
import random
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

from knowledge_base import CITIES, DESTINATIONS, INTERESTS, TRAVEL_MODES, calculate_haversine_distance, estimate_travel_costs, calculate_rule_suitability_score

# Set seed for reproducibility
random.seed(42)
np.random.seed(42)

def generate_travel_dataset(num_samples=150000):
    """
    Generates synthetic travel recommendation dataset based on knowledge base rules.
    Contains features: From, Interest, Budget, Persons, Days, TravelMode, Destination, Distance, EstTotalCost, BudgetRatio, InterestMatch, SuitabilityScore.
    """
    print(f"Generating {num_samples:,} synthetic travel dataset records...")
    
    city_names = list(CITIES.keys())
    modes = list(TRAVEL_MODES.keys())
    styles = ["Budget", "Moderate", "Luxury"]
    
    data = []
    
    for _ in range(num_samples):
        start_city = random.choice(city_names)
        interest = random.choice(INTERESTS)
        persons = random.randint(1, 5)
        days = random.randint(1, 8)
        travel_mode = random.choice(modes)
        travel_style = random.choice(styles)
        
        dest = random.choice(DESTINATIONS)
        dest_name = dest["name"]
        
        city_coords = CITIES[start_city]
        distance = calculate_haversine_distance(
            city_coords["lat"], city_coords["lng"],
            dest["lat"], dest["lng"]
        )
        
        costs = estimate_travel_costs(distance, travel_mode, persons, days, dest["cost_per_day"], travel_style)
        total_cost = costs["total_cost"]
        
        budget_options = [
            total_cost * random.uniform(0.6, 1.5),
            random.randint(5000, 100000)
        ]
        budget = round(random.choice(budget_options), -2)
        
        interest_match = 1 if interest.lower() == dest["interest"].lower() else 0
        budget_ratio = round(budget / max(total_cost, 1.0), 4)
        
        score = calculate_rule_suitability_score(
            interest, dest["interest"], budget, total_cost,
            days, dest["min_days"], distance, travel_mode
        )
        
        noisy_score = float(np.clip(score + np.random.normal(0, 0.8), 0, 100))
        
        data.append({
            "From": start_city,
            "Interest": interest,
            "Budget": budget,
            "Persons": persons,
            "Days": days,
            "TravelMode": travel_mode,
            "Destination": dest_name,
            "Distance": distance,
            "EstTotalCost": total_cost,
            "BudgetRatio": budget_ratio,
            "InterestMatch": interest_match,
            "SuitabilityScore": round(noisy_score, 2)
        })
        
    df = pd.DataFrame(data)
    print(f"Dataset generated successfully with shape: {df.shape}")
    return df

def train_and_evaluate():
    """
    Encodes dataset, splits into 80/20 train-test, compares Decision Tree, Random Forest,
    and Gradient Boosting models, prints metrics, and serializes the best model to disk.
    """
    df = generate_travel_dataset(num_samples=150000)
    
    cat_cols = ["From", "Interest", "TravelMode", "Destination"]
    encoders = {}
    
    df_encoded = df.copy()
    for col in cat_cols:
        le = LabelEncoder()
        df_encoded[col] = le.fit_transform(df[col])
        encoders[col] = le
        
    feature_cols = ["From", "Interest", "Budget", "Persons", "Days", "TravelMode", "Destination", "Distance", "EstTotalCost", "BudgetRatio", "InterestMatch"]
    X = df_encoded[feature_cols]
    y = df_encoded["SuitabilityScore"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
    print(f"Training set: {X_train.shape[0]:,} records | Testing set: {X_test.shape[0]:,} records\n")
    
    models = {
        "Decision Tree": DecisionTreeRegressor(max_depth=20, random_state=42),
        "Random Forest": RandomForestRegressor(n_estimators=100, max_depth=22, random_state=42, n_jobs=-1),
        "Gradient Boosting": GradientBoostingRegressor(n_estimators=70, max_depth=6, random_state=42)
    }
    
    results = {}
    best_model = None
    best_r2 = -1.0
    best_name = ""
    
    print("=" * 60)
    print(f"{'MODEL COMPARISON & EVALUATION RESULTS':^60}")
    print("=" * 60)
    
    for name, model in models.items():
        print(f"Training {name} Regressor...")
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        
        mae = float(mean_absolute_error(y_test, preds))
        rmse = float(np.sqrt(mean_squared_error(y_test, preds)))
        r2 = float(r2_score(y_test, preds))
        
        results[name] = {"MAE": mae, "RMSE": rmse, "R2": r2}
        
        print(f"[{name}]")
        print(f"   MAE  : {mae:.4f}")
        print(f"   RMSE : {rmse:.4f}")
        print(f"   R²   : {r2 * 100:.2f}%\n")
        
        if r2 > best_r2:
            best_r2 = r2
            best_model = model
            best_name = name
            
    print("=" * 60)
    print(f"Selected Model: {best_name} Regressor (R² = {best_r2 * 100:.2f}%)")
    print("=" * 60)
    
    output_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(output_dir, "model.pkl")
    encoders_path = os.path.join(output_dir, "label_encoders.pkl")
    metrics_path = os.path.join(output_dir, "model_metrics.pkl")
    
    joblib.dump(best_model, model_path)
    joblib.dump(encoders, encoders_path)
    joblib.dump(results, metrics_path)
    
    print(f"Saved best model to: {model_path}")
    print(f"Saved label encoders to: {encoders_path}")
    return results

if __name__ == "__main__":
    train_and_evaluate()
