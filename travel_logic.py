import pandas as pd
from datetime import date

def get_current_season(today=date.today()):
    """
    Determines the current season in the Northern Hemisphere.
    """
    month = today.month
    if 3 <= month <= 5:
        return "Spring"
    elif 6 <= month <= 8:
        return "Summer"
    elif 9 <= month <= 11:
        return "Autumn"
    else:
        return "Winter"

def get_traveler_profile(traveler_name, season):
    """
    Reads the CSV and returns a dictionary of the traveler's full profile.
    """
    try:
        df = pd.read_csv("TravelPreference.csv") 
        
        # Using the correct column name 'Traveller_Name'
        profile_row = df[df['Traveller_Name'].str.lower() == traveler_name.lower()]
        
        if profile_row.empty:
            print(f"No profile found for traveler: {traveler_name}")
            return None
            
        traveler_data = profile_row.iloc[0]
        
        # Clean the "quoted" strings from your CSV
        raw_seasons = traveler_data['Preferred_Time_of_Year']
        clean_seasons_str = raw_seasons.strip('"')  
        
        raw_activities = traveler_data['Preferred_Activities']
        clean_activities_str = raw_activities.strip('"')
        
        raw_visited = traveler_data['Countries_Visited']
        clean_visited_str = raw_visited.strip('"')

        preferred_seasons = [s.strip().lower() for s in clean_seasons_str.split(',')]
        
        if season.lower() not in preferred_seasons:
            print(f"{traveler_name} does not prefer to travel in the {season}. (Seasons found: {preferred_seasons})")
            return {"error": f"According to my data, {traveler_name} doesn't like to travel in the {season}."}
            
        # Success! Build and return the full profile
        profile = {
            "name": traveler_data['Traveller_Name'],
            "activities": [a.strip() for a in clean_activities_str.split(',')],
            "budget": traveler_data['Max_Budget'],
            "visited": [c.strip() for c in clean_visited_str.split(',')],
            "season": season,
            "preferred_seasons_list": preferred_seasons
        }
        return profile

    except FileNotFoundError:
        print("Error: TravelPreference.csv not found.")
        return None
    except Exception as e:
        print(f"Error processing CSV or profile: {e}")
        return None

# --- THIS FUNCTION IS MODIFIED ---
def create_personalized_system_prompt(profile):
    """
    Creates a new, highly-contextual system prompt for the AI.
    """
    activities_str = "\n".join(f"* {a}" for a in profile['activities'])
    visited_str = ", ".join(profile['visited'])
    
    system_prompt = f"""
    You are a helpful and personal travel assistant. You are speaking directly to a user named {profile['name']}.
    
    You have access to {profile['name']}'s private travel preferences. Here is her profile:
    * **Current Season:** {profile['season']}
    * **Preferred Travel Seasons:** {', '.join(profile['preferred_seasons_list'])}
    
    --- BUDGET FIX ---
    * **Maximum Budget:** {profile['budget']} (INR) 
    --- END FIX ---
    
    * **Preferred Activities:**
        {activities_str}
    * **Countries Already Visited:** {visited_str}

    YOUR TASK:
    1. Read the user's question.
    2. Use the profile data above to give a specific, personalized answer.
    3. Do NOT mention that you are an AI. Speak naturally, as an assistant.
    4. If the user asks a generic question (like "hi"), just give a normal answer.
    5. If the user asks for travel advice (like "where should I go?"), use their profile to suggest a *new* country they have *not* visited that matches their activities and budget for the current season.
    6. When suggesting a location, **you must** create a simple 5-day itinerary.
    """
    return system_prompt