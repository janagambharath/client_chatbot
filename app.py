from flask import Flask, render_template, request, jsonify, session
import requests
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# Load portfolio data
with open('portfolio_data.json', 'r') as f:
    PORTFOLIO_DATA = json.load(f)

# OpenRouter API Configuration
OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY', 'your-api-key-here')
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def create_system_prompt():
    """Generate CONCISE system prompt with portfolio data"""
    return f"""You are an AI assistant for {PORTFOLIO_DATA['personal_info']['name']}'s portfolio.

NAME: {PORTFOLIO_DATA['personal_info']['name']}
ROLE: {PORTFOLIO_DATA['personal_info']['title']}
LOCATION: {PORTFOLIO_DATA['personal_info']['location']}

KEY FACTS:
- CEO of PayNback (AI-driven retail rewards platform)
- Target: 5 lakh merchants, 5 crore users across India
- Focus: Tier-2/3 cities, digitizing local retail
- Skills: Data Analysis, Brand Development, Team Building
- 15+ years experience in business development

EXPERIENCE HIGHLIGHTS:
- PayNback CEO (2022-Present): Leading AI commerce platform
- LC Pay Project Manager (2019-Present): Multi-market expansion
- B&N Group PM (2005-2015): 10 years UAE operations

EDUCATION:
- Amity University: Business Administration
- NCVT: Mechanical Engineering

CONTACT:
Phone: {PORTFOLIO_DATA['personal_info']['contact']['phone']}
LinkedIn: {PORTFOLIO_DATA['personal_info']['contact']['linkedin']}
Email: {PORTFOLIO_DATA['personal_info']['contact']['email']}

INSTRUCTIONS:
1. Keep responses under 50 words unless asked for details
2. Be direct and conversational
3. If unrelated question, politely redirect
4. Never make up information
5. Encourage contact for opportunities"""

def get_conversation_history():
    """Retrieve last 3 exchanges (6 messages) to save tokens"""
    if 'conversation' not in session:
        session['conversation'] = []
    return session['conversation'][-6:]  # Only last 3 exchanges

def save_message(role, content):
    """Save message to conversation history"""
    if 'conversation' not in session:
        session['conversation'] = []
    session['conversation'].append({"role": role, "content": content})
    # Keep only last 10 messages to prevent memory buildup
    if len(session['conversation']) > 10:
        session['conversation'] = session['conversation'][-10:]
    session.modified = True

def call_openrouter(messages):
    """Call OpenRouter API with optimized settings"""
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://portfolio-chatbot.com",
            "X-Title": "Portfolio AI Chatbot"
        }
        
        data = {
            "model": "meta-llama/llama-3.3-70b-instruct:free",  # Updated to Llama 3.3 70B
            "messages": messages,
            "max_tokens": 200,  # Increased slightly for better responses from larger model
            "temperature": 0.7,  # Balanced creativity
            "top_p": 0.9
        }
        
        response = requests.post(OPENROUTER_URL, headers=headers, json=data, timeout=20)
        
        # Handle rate limiting
        if response.status_code == 429:
            return "I'm receiving too many requests. Please wait a moment and try again."
        
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    
    except requests.exceptions.Timeout:
        return "Response timed out. Please try a shorter question."
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return "Connection issue. Please try again shortly."
    except Exception as e:
        print(f"Unexpected error: {e}")
        return "An error occurred. Please try again."

@app.route('/')
def home():
    """Render main chat interface"""
    session.clear()  # Clear session on new visit
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages with optimized processing"""
    try:
        user_message = request.json.get('message', '').strip()
        
        if not user_message:
            return jsonify({"error": "Empty message"}), 400
        
        # Limit message length
        if len(user_message) > 500:
            return jsonify({
                "response": "Please keep your questions under 500 characters for faster responses.",
                "timestamp": datetime.now().isoformat()
            })
        
        # Save user message
        save_message("user", user_message)
        
        # Build messages for API (limited history)
        conversation_history = get_conversation_history()
        messages = [
            {"role": "system", "content": create_system_prompt()}
        ] + conversation_history
        
        # Get AI response
        bot_response = call_openrouter(messages)
        
        # Save bot response
        save_message("assistant", bot_response)
        
        return jsonify({
            "response": bot_response,
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({
            "response": "Error processing your message. Please try again.",
            "timestamp": datetime.now().isoformat()
        }), 200  # Return 200 to prevent frontend errors

@app.route('/clear', methods=['POST'])
def clear_conversation():
    """Clear conversation history"""
    session.clear()
    return jsonify({"status": "success"})

@app.route('/portfolio-data', methods=['GET'])
def get_portfolio_data():
    """Return portfolio data for frontend display"""
    return jsonify(PORTFOLIO_DATA)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    # For development
    app.run(debug=True, host='0.0.0.0', port=5000)
