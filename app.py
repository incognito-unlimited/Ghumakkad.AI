import os
import re
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, jsonify, session
from groq import Groq
from travel_logic import get_current_season, get_traveler_profile, create_personalized_system_prompt

# --- Initialization ---
app = Flask(__name__)
app.secret_key = os.urandom(24) 

try:
    # Using your original client setup
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
        default_headers={
            "Groq-Model-Version": "latest"
        }
    )
    if not os.environ.get("GROQ_API_KEY"):
        print("Warning: GROQ_API_KEY not found. Make sure .env file is correct.")
except Exception as e:
    print(f"Error initializing Groq client: {e}")
    client = None

def extract_name_from_message(message):
    """
    Looks for patterns like "I'm Jane", "my name is Jane", or "for Jane".
    """
    match_intro = re.search(r'(?:I\'m|I\s+am|my\s+name\s+is)\s+([a-zA-Z]+)', message, re.IGNORECASE)
    if match_intro:
        return match_intro.group(1).capitalize()
    
    match_for = re.search(r'for\s+([a-zA-Z]+)', message, re.IGNORECASE)
    if match_for:
        return match_for.group(1).capitalize()
    
    return None

# --- Main Route ---
@app.route("/")
def index():
    """Serves the main chat page."""
    # This is the "base" system prompt
    if 'messages' not in session:
        session['messages'] = [
            {"role": "system", "content": "You are a helpful chat assistant."}
        ]
    return render_template("index.html")

# --- Chat Endpoint (Final Logic) ---
@app.route("/chat", methods=["POST"])
def chat():
    """
    Handles chat, checks for name, and includes chat history.
    """
    if not client:
        return jsonify({"error": "Groq client not initialized."}), 500

    try:
        user_message = request.json["message"]
        
        # 1. Always check for a name
        traveler_name = extract_name_from_message(user_message)
        profile = None
        
        if traveler_name:
            season = get_current_season()
            profile = get_traveler_profile(traveler_name, season)

        # 2. Build the message list for the API
        
        # --- FIX: Implement sliding window ---
        # Get the full history from the session
        full_history = session.get('messages', [])
        
        # Keep only the last 10 messages (5 turns)
        # This prevents the 413 "Request Too Large" error
        recent_history = full_history[-10:] 
        
        # --- END FIX ---
        
        messages_for_api = []
        
        if profile and "error" not in profile:
            # --- CASE A: PERSONALIZED ---
            print(f"Creating personalized prompt for {traveler_name}...")
            system_prompt = create_personalized_system_prompt(profile)
            messages_for_api = [
                {"role": "system", "content": system_prompt},
                *recent_history, # Add the recent history
                {"role": "user", "content": user_message} # Add the new message
            ]
            
        else:
            # --- CASE B: GENERIC ---
            print("Creating generic prompt...")
            # Get the basic system prompt
            base_system_prompt = full_history[0] if full_history else {"role": "system", "content": "You are a helpful chat assistant."}
            
            messages_for_api = [
                base_system_prompt,
                *recent_history, # Add the recent history
                {"role": "user", "content": user_message} # Add the new message
            ]

        # Handle the "wrong season" error case
        if profile and "error" in profile:
            # We must add the user's message to session history even if we return an error
            session['messages'].append({"role": "user", "content": user_message})
            session['messages'].append({"role": "assistant", "content": profile["error"]})
            session.modified = True
            return jsonify({"response": profile["error"]})

        # 3. Call Groq API with your specified model
        completion = client.chat.completions.create(
            model="groq/compound",
            messages=messages_for_api,
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stop=None,
            compound_custom={"tools":{"enabled_tools":["web_search","code_interpreter","visit_website"]}},
            stream=False
        )
        ai_response = completion.choices[0].message.content
        
        # 4. Save the new turn to the session history
        session['messages'].append({"role": "user", "content": user_message})
        session['messages'].append({"role": "assistant", "content": ai_response})
        session.modified = True
        
        return jsonify({"response": ai_response})

    except Exception as e:
        print(f"Error in /chat: {e}")
        return jsonify({"error": str(e)}), 500

# --- Run the App ---
if __name__ == "__main__":
    app.run(debug=True, port=5000)