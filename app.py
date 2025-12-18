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
    """Generate comprehensive system prompt with portfolio data"""
    return f"""You are an AI assistant representing {PORTFOLIO_DATA['personal_info']['name']}, a professional portfolio chatbot.

IDENTITY & ROLE:
- Name: {PORTFOLIO_DATA['personal_info']['name']}
- Current Role: {PORTFOLIO_DATA['personal_info']['title']}
- Location: {PORTFOLIO_DATA['personal_info']['location']}

PROFESSIONAL SUMMARY:
{PORTFOLIO_DATA['summary']}

TOP SKILLS:
{', '.join(PORTFOLIO_DATA['top_skills'])}

KEY EXPERIENCE:
{json.dumps(PORTFOLIO_DATA['experience'][:3], indent=2)}

EDUCATION:
{json.dumps(PORTFOLIO_DATA['education'], indent=2)}

MAJOR PROJECT - PayNback:
{PORTFOLIO_DATA['projects'][0]['description']}
Impact: {PORTFOLIO_DATA['projects'][0]['impact']}

SERVICES OFFERED:
{', '.join(PORTFOLIO_DATA['services'])}

CONTACT INFORMATION:
- Phone: {PORTFOLIO_DATA['personal_info']['contact']['phone']}
- LinkedIn: {PORTFOLIO_DATA['personal_info']['contact']['linkedin']}
- Email: {PORTFOLIO_DATA['personal_info']['contact']['email']}

INSTRUCTIONS:
1. Answer questions about Bony Thomas's professional background, skills, experience, projects, and services
2. Be professional, confident, and concise
3. If asked about projects, focus on PayNback and its impact
4. If asked about experience, highlight CEO role at PayNback and relevant past positions
5. Encourage contact for business opportunities or collaborations
6. If question is unrelated to portfolio, politely redirect to professional topics
7. Never hallucinate information not provided above
8. Keep responses under 100 words unless detailed explanation is requested
9. Use a warm, professional tone that reflects entrepreneurial spirit

Current date: {datetime.now().strftime('%B %d, %Y')}"""

def get_conversation_history():
    """Retrieve last 5 messages from session"""
    if 'conversation' not in session:
        session['conversation'] = []
    return session['conversation'][-10:]  # Last 5 exchanges (10 messages)

def save_message(role, content):
    """Save message to conversation history"""
    if 'conversation' not in session:
        session['conversation'] = []
    session['conversation'].append({"role": role, "content": content})
    session.modified = True

def call_openrouter(messages):
    """Call OpenRouter API"""
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://portfolio-chatbot.com",
            "X-Title": "Portfolio AI Chatbot"
        }
        
        data = {
            "model": "meta-llama/llama-3.2-3b-instruct:free",
            "messages": messages
        }
        
        response = requests.post(OPENROUTER_URL, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result['choices'][0]['message']['content']
    
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return "I'm having trouble connecting right now. Please try again in a moment."
    except Exception as e:
        print(f"Unexpected error: {e}")
        return "An unexpected error occurred. Please try again."

@app.route('/')
def home():
    """Render main chat interface"""
    session.clear()  # Clear session on new visit
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        user_message = request.json.get('message', '').strip()
        
        if not user_message:
            return jsonify({"error": "Empty message"}), 400
        
        # Save user message
        save_message("user", user_message)
        
        # Build messages for API
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
        return jsonify({"error": "Failed to process message"}), 500

@app.route('/clear', methods=['POST'])
def clear_conversation():
    """Clear conversation history"""
    session.clear()
    return jsonify({"status": "success"})

@app.route('/portfolio-data', methods=['GET'])
def get_portfolio_data():
    """Return portfolio data for frontend display"""
    return jsonify(PORTFOLIO_DATA)

if __name__ == '__main__':
    # For development
    app.run(debug=True, host='0.0.0.0', port=5000)
