# 🤖 Bony Thomas AI Portfolio Assistant

An intelligent, conversational AI assistant that represents Bony Thomas, Founder & CEO of PayNback. Built with Flask and powered by Meta's Llama 3.3 70B model, featuring a sleek dark-mode professional interface designed for business networking and portfolio showcase.

## 🌟 Live Demo

**[Chat with Bony's AI Assistant](https://bonys-ai.onrender.com/)**

## 📋 Overview

This AI-powered portfolio chatbot serves as an interactive digital representative for Bony Thomas, providing comprehensive information about his professional background, PayNback venture, experience across multiple industries, and business expertise. The assistant responds naturally in first-person, creating an engaging conversational experience for potential investors, partners, and collaborators.

## ✨ Key Features

### 🎯 Core Capabilities
- **AI-Powered Conversations**: Leverages Meta Llama 3.3 70B for intelligent, context-aware responses
- **First-Person Representation**: Speaks as Bony Thomas for authentic, personalized interactions
- **Session-Based Memory**: Maintains conversation context for natural, flowing dialogue
- **Professional Focus**: Specialized knowledge about PayNback, business ventures, and strategic vision

### 🎨 Design & UX
- **Modern Dark Theme**: Professional dark-mode interface optimized for business contexts
- **Responsive Layout**: Two-column design with chat interface and quick info panel
- **Real-Time Feedback**: Typing indicators and smooth animations
- **Quick Actions**: Pre-defined questions for instant access to key information
- **Mobile-Optimized**: Fully responsive design for all device sizes

### 🚀 Technical Features
- Session-based conversation history (maintains last 12 messages)
- Rate limiting protection
- Timeout handling with user-friendly error messages
- Health check endpoint for monitoring
- JSON-based portfolio data management
- Optimized API calls with token management

## 🛠️ Tech Stack

### Backend
- **Flask 3.0.0** - Lightweight Python web framework
- **OpenRouter API** - Access to Meta Llama 3.3 70B Instruct model
- **Session Management** - Server-side conversation persistence
- **Gunicorn 21.2.0** - Production-grade WSGI HTTP server

### Frontend
- **HTML5 & CSS3** - Semantic markup and modern styling
- **Vanilla JavaScript** - Zero dependencies, pure JS implementation
- **Inter Font** - Professional, readable typography
- **CSS Grid & Flexbox** - Responsive layout system

### Design System
- Dark theme with carefully chosen color palette
- Gradient accents for visual interest
- Smooth transitions and hover effects
- Custom scrollbars for polished appearance
- Glassmorphism effects on certain elements

## 📋 Prerequisites

- Python 3.8 or higher
- OpenRouter API key ([Sign up here](https://openrouter.ai/))
- pip (Python package installer)
- Modern web browser

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd bony-portfolio-chatbot
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
SECRET_KEY=your_secure_secret_key_for_sessions
```

**Security Note**: Generate a strong secret key:
```python
import secrets
print(secrets.token_hex(32))
```

### 5. Run the Application

**Development Mode:**
```bash
python app.py
```
Access at: `http://localhost:5000`

**Production Mode with Gunicorn:**
```bash
gunicorn app:app --bind 0.0.0.0:5000 --workers 2
```

## 📁 Project Structure

```
bony-portfolio-chatbot/
│
├── app.py                      # Flask application & API routes
├── portfolio_data.json         # Portfolio information (Bony's data)
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not in repo)
├── .gitignore                 # Git ignore configuration
│
├── static/
│   ├── css/
│   │   └── style.css          # Dark theme professional styling
│   └── js/
│       └── script.js          # Frontend interaction logic
│
└── templates/
    └── index.html             # Main chat interface
```

## 🎨 Customization Guide

### Update Portfolio Information

Edit `portfolio_data.json`:

```json
{
  "personal_info": {
    "name": "Your Name",
    "title": "Your Title",
    "location": "Your Location",
    "contact": {
      "email": "your@email.com",
      "phone": "1234567890",
      "linkedin": "linkedin.com/in/yourprofile"
    }
  },
  "experience": [...],
  "projects": [...]
}
```

### Modify AI Behavior

Edit the `create_system_prompt()` function in `app.py` to adjust:
- Conversation tone and style
- Areas of expertise emphasis
- Response structure
- Communication guidelines

### Customize Appearance

**Color Scheme** - Edit CSS variables in `style.css`:
```css
:root {
    --primary-bg: #0f172a;
    --accent: #3b82f6;
    --text-primary: #f1f5f9;
    /* ... customize colors */
}
```

**Layout** - Modify grid structure:
```css
.container {
    grid-template-columns: 1fr 320px; /* Adjust column widths */
}
```

## 🔌 API Endpoints

| Endpoint | Method | Description | Request Body |
|----------|--------|-------------|--------------|
| `/` | GET | Main chat interface | - |
| `/chat` | POST | Send message, receive AI response | `{message: string}` |
| `/clear` | POST | Clear conversation history | - |
| `/portfolio-data` | GET | Retrieve portfolio JSON | - |
| `/health` | GET | Health check for monitoring | - |

### Example API Usage

**Send a Chat Message:**
```javascript
fetch('/chat', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    message: 'Tell me about PayNback'
  })
})
.then(res => res.json())
.then(data => console.log(data.response));
```

**Response Format:**
```json
{
  "response": "AI assistant's reply text",
  "timestamp": "2025-01-15T10:30:00.000Z"
}
```

## 🌐 Deployment

### Deploy to Render

1. **Create New Web Service**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configure Settings**
   - **Name**: bony-portfolio-chatbot
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

3. **Set Environment Variables**
   - `OPENROUTER_API_KEY`: Your OpenRouter API key
   - `SECRET_KEY`: Your secure session secret key

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Access via provided URL

### Deploy to Heroku

```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create new Heroku app
heroku create bony-portfolio-chatbot

# Set environment variables
heroku config:set OPENROUTER_API_KEY=your_key
heroku config:set SECRET_KEY=your_secret

# Deploy
git push heroku main

# Open in browser
heroku open
```

### Deploy to Railway

1. Connect GitHub repository
2. Add environment variables in Railway dashboard
3. Railway auto-detects Python and deploys
4. Access via generated URL

## 🔒 Security Best Practices

- ✅ Never commit `.env` file to version control
- ✅ Use strong, randomly generated secret keys
- ✅ Rotate API keys periodically
- ✅ Enable HTTPS in production (Render provides this automatically)
- ✅ Implement rate limiting for production deployments
- ✅ Monitor API usage and costs
- ✅ Validate and sanitize all user inputs
- ✅ Keep dependencies updated

## ⚡ Performance Optimization

### Current Optimizations
- **Token Limit**: 400 tokens for balanced response quality and speed
- **Conversation History**: Maintains last 12 messages (6 exchanges)
- **Request Timeout**: 25 seconds to prevent hanging
- **Message Length Limit**: 500 characters max per message
- **Rate Limiting Handling**: Graceful fallback on API rate limits

### Recommended Production Settings
```python
# In app.py, adjust these for your needs:
"max_tokens": 400,        # Response length
"temperature": 0.7,       # Creativity (0.0-1.0)
"top_p": 0.9,            # Response diversity
timeout=25               # API request timeout
```

## 🐛 Troubleshooting

### Common Issues & Solutions

**Issue: API Timeout Errors**
```python
# Solution: Increase timeout in app.py
response = requests.post(..., timeout=30)
```

**Issue: Rate Limiting (429 Error)**
- Wait a few moments before retrying
- Consider upgrading OpenRouter plan
- Implement request queuing

**Issue: Session Not Persisting**
```python
# Ensure SECRET_KEY is set
app.secret_key = os.environ.get('SECRET_KEY')
# Always mark session as modified
session.modified = True
```

**Issue: Static Files Not Loading**
- Clear browser cache (Ctrl+Shift+R)
- Check Flask static file paths
- Verify file locations in `static/` directory

**Issue: Long Response Times**
- Reduce `max_tokens` in API call
- Optimize system prompt length
- Limit conversation history depth

## 📊 Monitoring & Analytics

### Health Check Endpoint
```bash
curl https://bonys-ai.onrender.com/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-15T10:30:00.000Z"
}
```

### Recommended Monitoring
- Set up uptime monitoring (e.g., UptimeRobot)
- Track API usage and costs via OpenRouter dashboard
- Monitor response times
- Log error rates and types

## 🤝 About PayNback

PayNback is an AI-driven in-store rewards and customer engagement platform building a B2B2C commerce ecosystem across India. The platform connects small retailers, MSMEs, and local shoppers through:
- Instant digital rewards
- Actionable data insights
- Hyperlocal engagement tools

**Vision**: Become India's most trusted community commerce network, empowering neighbourhood retailers and digitizing local commerce across Tier-2 and Tier-3 cities.

## 📝 License

This project is available under the [MIT License](LICENSE).

## 👤 Contact & Connect

**Bony Thomas**
- **Role**: Founder & CEO, PayNback
- **Email**: contact@paynback.com
- **Phone**: +91 9656512573
- **LinkedIn**: [bony-thomas-2b0186b](https://www.linkedin.com/in/bony-thomas-2b0186b)
- **Location**: Bengaluru, Karnataka, India

## 🙏 Acknowledgments

- Meta AI for Llama 3.3 70B Instruct model
- OpenRouter for seamless API access
- Flask community for excellent documentation
- Render for reliable hosting platform
- Inter typeface by Rasmus Andersson

## 📞 Support

For questions, issues, or collaboration inquiries:
1. Review existing documentation
2. Check troubleshooting section
3. Contact via email: contact@paynback.com
4. Connect on LinkedIn for business opportunities

---

**Built with 💼 Professional Excellence** | Powered by AI & Innovation 🚀

*Representing Bony Thomas's vision to digitize and empower India's neighbourhood commerce ecosystem.*
