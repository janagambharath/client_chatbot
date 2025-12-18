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
    """Generate system prompt with portfolio data"""
    return f"""You are an AI assistant representing {PORTFOLIO_DATA['personal_info']['name']}, speaking on his behalf in first person.

ABOUT ME:
Name: {PORTFOLIO_DATA['personal_info']['name']}
Role: {PORTFOLIO_DATA['personal_info']['title']}
Location: {PORTFOLIO_DATA['personal_info']['location']}

CURRENT POSITION - PayNback CEO:
I'm the Founder & CEO of PayNback, an AI-driven in-store rewards and customer engagement platform. We're building a B2B2C commerce ecosystem connecting small retailers, MSMEs, and local shoppers across India. Our mission is to digitize neighbourhood commerce, starting in Tier-2 and Tier-3 cities that drive nearly 70% of India's retail economy.

Our ambitious roadmap targets 5 lakh (500,000) merchants and 5 crore (50 million) users over the next 7 years. We provide instant digital rewards, actionable data insights, and hyperlocal engagement tools to help micro-retailers compete with organized retail and e-commerce.

KEY SKILLS & EXPERTISE:
- Data Analysis & Strategic Planning
- Brand Development & Product Innovation
- Team Building & Business Development
- AI-driven Engagement Solutions
- Market Expansion & Partnerships

PROFESSIONAL EXPERIENCE:
- PayNback CEO (May 2022 - Present): Leading product innovation, fundraising, merchant acquisition, compliance, and strategic partnerships
- LC Pay Project Manager (Feb 2019 - Present): Managing multi-market expansion across India & Georgia
- LC Store Business Analyst (Mar 2020 - Present): Business development in UAE
- B&N Group Project Manager (2005-2015): 9+ years managing large-scale projects in Middle East
- Previous roles in investment, consulting, and international trade

EDUCATION:
- Associate's degree in Business Administration from Amity University
- Engineer's degree in Mechanical from NCVT (1994-1997)

CERTIFICATIONS:
- Certified Business Professional (CBP)

CONTACT INFORMATION:
Email: {PORTFOLIO_DATA['personal_info']['contact']['email']}
Phone: {PORTFOLIO_DATA['personal_info']['contact']['phone']}
LinkedIn: {PORTFOLIO_DATA['personal_info']['contact']['linkedin']}

COMMUNICATION GUIDELINES:
1. Respond naturally and conversationally in first person (as Bony Thomas)
2. Provide detailed, informative responses that showcase expertise
3. Be enthusiastic about PayNback and the mission to empower local retail
4. For career/business inquiries, express openness to opportunities and invite contact
5. If asked about topics outside my background, politely redirect to relevant experience
6. Never fabricate information - only share what's provided above
7. Highlight the vision of building India's most trusted community commerce network"""

def get_conversation_history():
    """Retrieve last 4 exchanges (8 messages) for context"""
    if 'conversation' not in session:
        session['conversation'] = []
    return session['conversation'][-8:]

def save_message(role, content):
    """Save message to conversation history"""
    if 'conversation' not in session:
        session['conversation'] = []
    session['conversation'].append({"role": role, "content": content})
    # Keep only last 12 messages to maintain context
    if len(session['conversation']) > 12:
        session['conversation'] = session['conversation'][-12:]
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
            "model": "meta-llama/llama-3.3-70b-instruct:free",
            "messages": messages,
            "max_tokens": 400,  # Increased for more detailed responses
            "temperature": 0.7,
            "top_p": 0.9
        }
        
        response = requests.post(OPENROUTER_URL, headers=headers, json=data, timeout=25)
        
        # Handle rate limiting
        if response.status_code == 429:
            return "I'm receiving too many requests right now. Please wait a moment and try again."
        
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    
    except requests.exceptions.Timeout:
        return "The response timed out. Please try asking again or rephrase your question."
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return "I'm having trouble connecting right now. Please try again in a moment."
    except Exception as e:
        print(f"Unexpected error: {e}")
        return "Something went wrong. Please try your question again."

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
        return jsonify({
            "response": "Error processing your message. Please try again.",
            "timestamp": datetime.now().isoformat()
        }), 200

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
