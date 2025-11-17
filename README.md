# ✈️ AI Travel Assistant

A web-based AI chat assistant that provides personalized travel itineraries. Built with a Python Flask backend and the Groq API, this assistant reads a `TravelPreference.csv` file to generate custom travel plans tailored to a specific user's budget, preferred activities, and travel history.

![Chat UI Screenshot](ss.png)

## ✨ Core Features

* **Personalized Itineraries:** Asks for a name (e.g., "plan a trip for Jane") and uses data from `TravelPreference.csv` to build a custom trip.
* **Dynamic Prompting:** Injects the user's CSV data (budget, activities, visited countries) directly into the AI prompt for a tailored response.
* **Conversational Memory:** Remembers the last 10 messages to provide context, preventing "Request Too Large" errors.
* **Markdown Rendering:** Neatly displays AI responses, including tables and lists, in the chat window.
* **Smart Error Handling:** Gracefully manages cases where a traveler isn't in the CSV or doesn't travel in the current season.

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **AI:** Groq API
* **Data:** Pandas (for CSV parsing)
* **Frontend:** HTML, CSS, JavaScript
* **Libraries:** `python-dotenv` (for API keys), `marked.js` (for Markdown rendering)

## 🚀 Getting Started

Follow these steps to get the project running on your local machine.

### 1. Prerequisites

* Python 3.7+
* Git

### 2. Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git](https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git)
    cd YOUR-REPO-NAME
    ```

2.  **Create a virtual environment** (Recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install the required libraries:**
    *Create a file named `requirements.txt` and paste the following into it:*
    ```
    flask
    groq
    pandas
    python-dotenv
    ```
    *Now, run the installer:*
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create your `.env` file:**
    Create a file named `.env` in the root folder and add your Groq API key:
    ```
    GROQ_API_KEY=gsk_YourSecretApiKeyHere
    ```

5.  **Customize your data:**
    Edit the `TravelPreference.csv` file to add your own travelers, preferences, and budgets. The app will read this file live.

## 🏃‍♀️ How to Run

1.  Run the Flask application:
    ```bash
    python app.py
    ```
2.  Open your web browser and go to:
    `http://127.0.0.1:5000`

## 💬 How to Use

* **Generic Chat:** Just type any question for a normal AI response.
* **Personalized Itinerary:** Type a message that includes a name from your CSV file. The app will automatically detect the name, pull the data, and generate a custom itinerary.

    **Examples:**
    * "Hi, I'm Jane, where should I go next?"
    * "Can you plan a trip for Jane?"
