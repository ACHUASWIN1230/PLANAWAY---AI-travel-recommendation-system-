import math

# Supported Travel Interests
INTERESTS = [
    "Beach", "Adventure", "Hill Station", "Wildlife", 
    "Nature", "Heritage", "Spiritual", "City"
]

# Supported Travel Modes
TRAVEL_MODES = {
    "Bus": {"cost_per_km": 1.8, "base_cost": 50, "speed_kmh": 50},
    "Train": {"cost_per_km": 1.2, "base_cost": 100, "speed_kmh": 65},
    "Car": {"cost_per_km": 6.0, "base_cost": 200, "speed_kmh": 70},
    "Flight": {"cost_per_km": 5.5, "base_cost": 1500, "speed_kmh": 500}
}

# Travel Style Multipliers
TRAVEL_STYLES = {
    "Budget": 0.8,
    "Moderate": 1.0,
    "Luxury": 1.8
}

# Major Starting Cities with Latitude & Longitude
CITIES = {
    "Chennai": {"lat": 13.0827, "lng": 80.2707},
    "Mumbai": {"lat": 19.0760, "lng": 72.8777},
    "Delhi": {"lat": 28.6139, "lng": 77.2090},
    "Bengaluru": {"lat": 12.9716, "lng": 77.5946},
    "Hyderabad": {"lat": 17.3850, "lng": 78.4867},
    "Kolkata": {"lat": 22.5726, "lng": 88.3639},
    "Pune": {"lat": 18.5204, "lng": 73.8567},
    "Kochi": {"lat": 9.9312, "lng": 76.2673},
    "Jaipur": {"lat": 26.9124, "lng": 75.7873},
    "Ahmedabad": {"lat": 23.0225, "lng": 72.5714}
}

# Destination Knowledge Base
DESTINATIONS = [
    {
        "name": "Goa",
        "interest": "Beach",
        "cost_per_day": 2500,
        "min_days": 3,
        "lat": 15.4909,
        "lng": 73.8278,
        "description": "Sun-kissed beaches, vibrant nightlife, Portuguese heritage, and watersports heaven.",
        "attractions": ["Baga Beach", "Calangute Beach", "Dudhsagar Falls", "Fort Aguada", "Basilica of Bom Jesus"],
        "hotels": ["Goa Marriott Resort", "Taj Exotica Resort & Spa", "Zostel Goa", "Cidade de Goa"],
        "tips": "Rent a scooter to explore North & South Goa easily. Try authentic Goan Fish Curry."
    },
    {
        "name": "Pondicherry",
        "interest": "Beach",
        "cost_per_day": 1800,
        "min_days": 2,
        "lat": 11.9416,
        "lng": 79.8083,
        "description": "Charming French Quarter, serene promenade beaches, cobblestone streets, and spiritual Auroville.",
        "attractions": ["Promenade Beach", "Auroville", "Paradise Beach", "French Quarter", "Sri Aurobindo Ashram"],
        "hotels": ["Palais de Mahe", "The Promenade", "La Villa", "Zostel Pondicherry"],
        "tips": "Explore the French Town on foot or bicycle. Enjoy French cafes & croissants."
    },
    {
        "name": "Kovalam",
        "interest": "Beach",
        "cost_per_day": 2200,
        "min_days": 2,
        "lat": 8.4004,
        "lng": 76.9787,
        "description": "Famous crescent-shaped beaches with iconic lighthouse, Ayurvedic therapies, and serene waves.",
        "attractions": ["Lighthouse Beach", "Hawa Beach", "Samudra Beach", "Vellayani Lake"],
        "hotels": ["The Leela Kovalam", "Turtle on the Beach", "Hotel Sea Face"],
        "tips": "Try traditional Kerala Ayurvedic massage and watch sunset from the Lighthouse."
    },
    {
        "name": "Gokarna",
        "interest": "Beach",
        "cost_per_day": 1500,
        "min_days": 2,
        "lat": 14.5479,
        "lng": 74.3188,
        "description": "Laid-back beach town known for Om Beach, scenic cliff treks, and tranquil coastal vibes.",
        "attractions": ["Om Beach", "Kudle Beach", "Half Moon Beach", "Mahabaleshwar Temple"],
        "hotels": ["Kahani Paradise", "SwaSwara Resort", "Zostel Gokarna"],
        "tips": "Do the famous Gokarna Beach Trek connecting Kudle, Om, Half Moon, and Paradise beaches."
    },
    {
        "name": "Andaman",
        "interest": "Beach",
        "cost_per_day": 4500,
        "min_days": 5,
        "lat": 11.6233,
        "lng": 92.7265,
        "description": "Crystal clear turquoise waters, white sand beaches, world-class scuba diving, and coral reefs.",
        "attractions": ["Radhanagar Beach", "Cellular Jail", "Elephant Beach", "Havlock Island", "Neil Island"],
        "hotels": ["Taj Exotica Havelock", "Barefoot at Havelock", "Symphony Palms"],
        "tips": "Book ferry tickets between Port Blair and Havelock in advance. Try scuba diving at Elephant Beach."
    },
    {
        "name": "Ooty",
        "interest": "Hill Station",
        "cost_per_day": 1600,
        "min_days": 2,
        "lat": 11.4102,
        "lng": 76.6950,
        "description": "Queen of Hill Stations featuring lush tea gardens, Nilgiri Toy Train, botanical gardens, and mist.",
        "attractions": ["Ooty Lake", "Doddabetta Peak", "Botanical Gardens", "Nilgiri Mountain Railway", "Rose Garden"],
        "hotels": ["Savoy - IHCL SeleQtions", "Sterling Ooty Fern Hill", "Zostel Ooty"],
        "tips": "Take the UNESCO heritage Toy Train ride from Coonoor to Ooty for stunning valley views."
    },
    {
        "name": "Munnar",
        "interest": "Hill Station",
        "cost_per_day": 1900,
        "min_days": 3,
        "lat": 10.0889,
        "lng": 77.0595,
        "description": "Rolling green tea plantations, misty valleys, endangered Nilgiri Tahr, and cascading waterfalls.",
        "attractions": ["Eravikulam National Park", "Mattupetty Dam", "Tea Museum", "Anamudi Peak", "Top Station"],
        "hotels": ["Windermere Estate", "Fragrant Nature Munnar", "Blanket Hotel & Spa"],
        "tips": "Visit Tea Museum to taste fresh Kerala tea blends. Early morning visits avoid heavy fog."
    },
    {
        "name": "Manali",
        "interest": "Hill Station",
        "cost_per_day": 2200,
        "min_days": 3,
        "lat": 32.2432,
        "lng": 77.1892,
        "description": "Snow-capped Himalayan peaks, Solang Valley sports, Rohtang Pass, and pine forest trails.",
        "attractions": ["Solang Valley", "Rohtang Pass", "Hadimba Temple", "Old Manali", "Jogini Waterfalls"],
        "hotels": ["The Span Resort & Spa", "Sylvan Woods", "Zostel Manali"],
        "tips": "Carry warm thermals even in summer for Rohtang Pass. Explore Old Manali cafes."
    },
    {
        "name": "Coorg",
        "interest": "Hill Station",
        "cost_per_day": 2000,
        "min_days": 2,
        "lat": 12.4244,
        "lng": 75.7382,
        "description": "Scotland of India known for coffee plantations, aromatic spice estates, waterfalls, and Kodava culture.",
        "attractions": ["Abbey Falls", "Raja's Seat", "Namlokling Monastery (Bylakuppe)", "Dubare Elephant Camp", "Tadiandamol Peak"],
        "hotels": ["Evolve Back Coorg", "Tamara Coorg", "Heritage Resort Coorg"],
        "tips": "Buy fresh roasted coffee beans and local Coorg spices directly from plantation estates."
    },
    {
        "name": "Shimla",
        "interest": "Hill Station",
        "cost_per_day": 2100,
        "min_days": 2,
        "lat": 31.1048,
        "lng": 77.1734,
        "description": "Colonial capital nestled in pine hills, Mall Road shopping, Ridge view, and heritage architecture.",
        "attractions": ["The Ridge", "Mall Road", "Jakhoo Temple", "Kufri", "Christ Church"],
        "hotels": ["Wildflower Hall Shimla", "The Oberoi Cecil", "Clarkes Hotel"],
        "tips": "Walk along Mall Road during evening hours. Take the Kalka-Shimla toy train."
    },
    {
        "name": "Rishikesh",
        "interest": "Adventure",
        "cost_per_day": 1400,
        "min_days": 2,
        "lat": 30.0869,
        "lng": 78.2676,
        "description": "Yoga capital of the world and thrill-seeker hub for white-water rafting, bungee jumping, and Ganga Aarti.",
        "attractions": ["Laxman Jhula", "Triveni Ghat", "Shivpuri Rafting", "Beatles Ashram", "Neer Garh Waterfall"],
        "hotels": ["Ananda in the Himalayas", "Aloha on the Ganges", "Zostel Rishikesh"],
        "tips": "Book grade III/IV white-water rafting from Shivpuri. Attend evening Ganga Aarti at Triveni Ghat."
    },
    {
        "name": "Leh-Ladakh",
        "interest": "Adventure",
        "cost_per_day": 3500,
        "min_days": 5,
        "lat": 34.1526,
        "lng": 77.5771,
        "description": "High-altitude desert wonderland, Khardung La pass, Pangong Tso azure lake, and ancient monasteries.",
        "attractions": ["Pangong Tso Lake", "Nubra Valley", "Khardung La Pass", "Magnetic Hill", "Thiksey Monastery"],
        "hotels": ["The Grand Dragon Ladakh", "Stok Palace Heritage", "Ladakh Sarai Resort"],
        "tips": "Acclimatize for at least 24 hours in Leh city before heading to high altitude passes."
    },
    {
        "name": "Dandeli",
        "interest": "Adventure",
        "cost_per_day": 1700,
        "min_days": 2,
        "lat": 15.2361,
        "lng": 74.6173,
        "description": "Dense Western Ghats wilderness, Kali river white-water rafting, jungle safari, and kayaking.",
        "attractions": ["Kali River Rafting", "Dandeli Wildlife Sanctuary", "Syntheri Rocks", "Shiroli Peak"],
        "hotels": ["Bison River Resort", "Whistling Woodz Resort", "Dandelappa Resort"],
        "tips": "Try river jacuzzis and night jungle camping under certified adventure guides."
    },
    {
        "name": "Jim Corbett",
        "interest": "Wildlife",
        "cost_per_day": 2800,
        "min_days": 2,
        "lat": 29.5300,
        "lng": 78.7747,
        "description": "India's oldest national park, home to Bengal Tigers, wild elephants, and dense Sal forests.",
        "attractions": ["Dhikala Zone Safari", "Bijrani Zone", "Corbett Waterfalls", "Garjiya Devi Temple"],
        "hotels": ["Jim's Jungle Retreat", "Taj Corbett Resort & Spa", "Aahana The Corbett Wilderness"],
        "tips": "Book Canter/Jeep safari permits 45 days in advance via official forest website."
    },
    {
        "name": "Ranthambore",
        "interest": "Wildlife",
        "cost_per_day": 3000,
        "min_days": 2,
        "lat": 26.0173,
        "lng": 76.5026,
        "description": "Historic tiger reserve with ancient Ranthambore Fort ruins amidst wild jungle habitat.",
        "attractions": ["Ranthambore Fort", "Zone 1-5 Tiger Safari", "Padam Talao Lake", "Trinetra Ganesh Temple"],
        "hotels": ["The Oberoi Vanyavilas", "Aman-i-Khas", "Nahargarh Ranthambore"],
        "tips": "Zones 1 to 5 have higher tiger sighting probabilities during early morning safaris."
    },
    {
        "name": "Kabini",
        "interest": "Wildlife",
        "cost_per_day": 3800,
        "min_days": 2,
        "lat": 11.9168,
        "lng": 76.3537,
        "description": "Premier leopard and black panther sanctuary, boat safaris on Kabini river, and dense Nagarhole jungle.",
        "attractions": ["Kabini River Boat Safari", "Nagarhole National Park", "Jungle Jeep Safari"],
        "hotels": ["Evolve Back Kabini", "The Bison Resort", "Kabini River Lodge"],
        "tips": "Opt for both boat safari (elephants & birds) and land jeep safari (leopards & tigers)."
    },
    {
        "name": "Alleppey",
        "interest": "Nature",
        "cost_per_day": 2300,
        "min_days": 2,
        "lat": 9.4981,
        "lng": 76.3388,
        "description": "Venice of the East featuring luxury houseboat cruises, tranquil backwaters, and coconut palm groves.",
        "attractions": ["Alleppey Houseboats", "Vembanad Lake", "Marari Beach", "Kuttanad Paddy Fields"],
        "hotels": ["Xandari Riverscapes Houseboats", "Lake Palace Resort", "Lemon Tree Vembanad"],
        "tips": "Book an overnight traditional Kettuvallam houseboat with cooked Kerala Karimeen fry."
    },
    {
        "name": "Wayanad",
        "interest": "Nature",
        "cost_per_day": 1800,
        "min_days": 2,
        "lat": 11.6854,
        "lng": 76.1320,
        "description": "Picturesque Western Ghats district with prehistoric Edakkal caves, heart-shaped lake, and waterfalls.",
        "attractions": ["Edakkal Caves", "Chembra Peak", "Banasura Sagar Dam", "Kuruva Island", "Soochipara Falls"],
        "hotels": ["Vythiri Resort", "Windflower Resort & Spa", "Zostel Wayanad"],
        "tips": "Trek up Chembra Peak to view the iconic natural heart-shaped lake."
    },
    {
        "name": "Chikmagalur",
        "interest": "Nature",
        "cost_per_day": 1700,
        "min_days": 2,
        "lat": 13.3161,
        "lng": 75.7720,
        "description": "Coffee land of Karnataka, Mullayanagiri peak trek, cascading waterfalls, and serene estate walks.",
        "attractions": ["Mullayanagiri Peak", "Baba Budangiri", "Hebbe Falls", "Coffee Museum", "Z Point"],
        "hotels": ["The Serai Chikmagalur", "Trivik Hotels & Resorts", "Java Rain Resort"],
        "tips": "Trek Mullayanagiri (Karnataka's highest peak) during early sunrise hours."
    },
    {
        "name": "Jaipur",
        "interest": "Heritage",
        "cost_per_day": 2000,
        "min_days": 3,
        "lat": 26.9124,
        "lng": 75.7873,
        "description": "The Pink City famous for majestic royal palaces, Amber Fort, vibrant bazaars, and Rajasthani cuisine.",
        "attractions": ["Amber Fort", "Hawa Mahal", "City Palace", "Jantar Mantar", "Nahargarh Fort"],
        "hotels": ["Rambagh Palace", "The Leela Palace Jaipur", "Zostel Jaipur"],
        "tips": "Try authentic Dal Baati Churma at Chokhi Dhani ethnic village."
    },
    {
        "name": "Udaipur",
        "interest": "Heritage",
        "cost_per_day": 2400,
        "min_days": 3,
        "lat": 24.5854,
        "lng": 73.7125,
        "description": "City of Lakes with romantic Lake Palace, grand City Palace overlooking Lake Pichola, and sunset boats.",
        "attractions": ["City Palace Udaipur", "Lake Pichola Boat Ride", "Jagmandir", "Saheliyon-ki-Bari", "Fateh Sagar Lake"],
        "hotels": ["Taj Lake Palace", "The Oberoi Udaivilas", "Trident Udaipur", "Zostel Udaipur"],
        "tips": "Take a sunset boat cruise on Lake Pichola for breathtaking views of City Palace."
    },
    {
        "name": "Hampi",
        "interest": "Heritage",
        "cost_per_day": 1300,
        "min_days": 2,
        "lat": 15.3350,
        "lng": 76.4600,
        "description": "UNESCO World Heritage boulder landscape with magnificent 14th-century Vijayanagara Empire stone ruins.",
        "attractions": ["Virupaksha Temple", "Stone Chariot at Vittala Temple", "Hemakuta Hill", "Lotus Mahal", "Hippie Island"],
        "hotels": ["Evolve Back Hampi", "Heritage Resort Hampi", "Zostel Hampi"],
        "tips": "Rent a bicycle to explore the vast open-air museum of ruins. Sunset at Hemakuta Hill is unmissable."
    },
    {
        "name": "Varanasi",
        "interest": "Spiritual",
        "cost_per_day": 1400,
        "min_days": 2,
        "lat": 25.3176,
        "lng": 82.9739,
        "description": "Oldest living city in the world, sacred Ganges river ghats, grand evening Ganga Aarti, and ancient temples.",
        "attractions": ["Dashashwamedh Ghat", "Kashi Vishwanath Temple", "Sarnath", "Assi Ghat", "Manikarnika Ghat"],
        "hotels": ["BrijRama Palace", "Taj Nadesar Palace", "Zostel Varanasi"],
        "tips": "Take an early 5:30 AM sunrise boat ride from Assi Ghat to Dashashwamedh Ghat."
    },
    {
        "name": "Golden Temple (Amritsar)",
        "interest": "Spiritual",
        "cost_per_day": 1500,
        "min_days": 2,
        "lat": 31.6200,
        "lng": 74.8765,
        "description": "Holy spiritual center of Sikhism with glistening Sri Harmandir Sahib, Langar community kitchen, and Wagah Border.",
        "attractions": ["Golden Temple", "Jallianwala Bagh", "Wagah Border Ceremony", "Partition Museum"],
        "hotels": ["Taj Swarna Amritsar", "Hyatt Regency Amritsar", "Zostel Amritsar"],
        "tips": "Experience the world's largest free community kitchen (Langar) and visit Wagah Border sunset ceremony."
    },
    {
        "name": "Mumbai",
        "interest": "City",
        "cost_per_day": 3000,
        "min_days": 2,
        "lat": 19.0760,
        "lng": 72.8777,
        "description": "City of Dreams, iconic Gateway of India, Marine Drive Queen's Necklace, Bollywood, and coastal energy.",
        "attractions": ["Gateway of India", "Marine Drive", "Colaba Causeway", "Elephanta Caves", "Chhatrapati Shivaji Terminus"],
        "hotels": ["The Taj Mahal Palace", "Trident Nariman Point", "Zostel Mumbai"],
        "tips": "Walk Marine Drive at sunset and grab local street food like Vada Pav and Pav Bhaji."
    }
]

def calculate_haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculates the great circle distance between two points on Earth (in km)
    using the Haversine formula.
    """
    R = 6371.0 # Earth radius in kilometers
    
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = (math.sin(delta_phi / 2.0) ** 2 +
         math.cos(phi1) * math.cos(phi2) * (math.sin(delta_lambda / 2.0) ** 2))
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return round(distance, 2)

def estimate_travel_costs(distance_km, travel_mode, persons, days, cost_per_day, travel_style="Moderate"):
    """
    Calculates detailed estimated travel & accommodation costs.
    """
    mode_info = TRAVEL_MODES.get(travel_mode, TRAVEL_MODES["Bus"])
    style_mult = TRAVEL_STYLES.get(travel_style, 1.0)
    
    # Travel cost per person based on distance & mode
    travel_cost_per_person = mode_info["base_cost"] + (distance_km * mode_info["cost_per_km"])
    total_travel_cost = travel_cost_per_person * persons
    
    # Accommodation cost
    stay_cost_per_day_adjusted = cost_per_day * style_mult
    total_stay_cost = stay_cost_per_day_adjusted * days * persons
    
    # Food & activities estimate (approx 40% of stay cost)
    food_activity_cost = total_stay_cost * 0.4
    
    total_estimated_cost = total_travel_cost + total_stay_cost + food_activity_cost
    
    return {
        "travel_cost": round(total_travel_cost, 2),
        "stay_cost": round(total_stay_cost, 2),
        "food_activity_cost": round(food_activity_cost, 2),
        "total_cost": round(total_estimated_cost, 2),
        "travel_cost_per_person": round(travel_cost_per_person, 2)
    }

def calculate_rule_suitability_score(interest_user, dest_interest, budget_user, total_cost, 
                                      days_user, min_days, distance_km, travel_mode):
    """
    Calculates rule-based suitability score (0 - 100).
    """
    score = 0.0
    
    # 1. Interest Match (Up to 40 pts)
    if interest_user.lower() == dest_interest.lower():
        score += 40.0
    else:
        # Partial match if categories share common vibes
        score += 10.0

    # 2. Budget Suitability (Up to 30 pts)
    if total_cost <= budget_user:
        # Perfect fit
        budget_ratio = total_cost / max(budget_user, 1.0)
        # Higher score if it uses 50%-95% of budget, slightly less if way under budget
        if 0.4 <= budget_ratio <= 0.95:
            score += 30.0
        elif budget_ratio < 0.4:
            score += 25.0 # Very cheap, comfortable
        else:
            score += 28.0
    else:
        # Over budget: penalize based on overshot percentage
        over_ratio = (total_cost - budget_user) / max(budget_user, 1.0)
        penalty = min(over_ratio * 40.0, 28.0)
        score += max(30.0 - penalty, 0.0)

    # 3. Duration Match (Up to 15 pts)
    if days_user >= min_days:
        score += 15.0
    else:
        score += (days_user / max(min_days, 1)) * 10.0

    # 4. Distance & Mode Suitability (Up to 15 pts)
    # Checks if travel mode is appropriate for distance
    if travel_mode == "Bus" or travel_mode == "Car":
        if distance_km <= 600:
            score += 15.0
        elif distance_km <= 1000:
            score += 10.0
        else:
            score += 4.0 # Bus/Car for >1000km is tiring
    elif travel_mode == "Train":
        if distance_km <= 1200:
            score += 15.0
        else:
            score += 10.0
    elif travel_mode == "Flight":
        if distance_km >= 400:
            score += 15.0
        else:
            score += 8.0 # Short flights have high overhead

    return round(min(max(score, 0.0), 100.0), 2)
