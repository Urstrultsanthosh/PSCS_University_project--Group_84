from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from openai import OpenAI
import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'my-secret-key-for-mining-bot')
# Initialize OpenAI client with new format
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
app.permanent_session_lifetime = timedelta(minutes=30)

# Simple database setup - keeping it basic for now
def setup_database():
    """Initialize the user database - learned this from Flask tutorials"""
    if not os.path.exists('users.db'):  # Changed name to be more specific
        try:
            conn = sqlite3.connect('users.db')
            # Basic user table - might add more fields later
            conn.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)')
            conn.close()
            print("Database created successfully")  # Added for debugging
        except sqlite3.Error as e:
            print(f"Database setup error: {e}")

@app.route('/')
def home():
    """Main page - redirects to login"""
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page - basic authentication"""
    login_failed = False
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check credentials in database
        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            user = cursor.fetchone()
            conn.close()
            
            if user:
                session['username'] = username  # Changed from 'user' to 'username'
                return redirect(url_for('select_language'))
            else:
                login_failed = True
        except sqlite3.Error as e:
            print(f"Login error: {e}")
            login_failed = True
            
    return render_template('login.html', invalid_credentials=login_failed)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration - simple version"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Basic validation - can improve this later
        if not username or not password:
            flash("Please fill all fields", "error")
            return render_template('register.html')
            
        try:
            conn = sqlite3.connect("users.db")
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            flash("Registration successful!", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Username already exists", "error")
        except sqlite3.Error as e:
            print(f"Registration error: {e}")
            flash("Registration failed", "error")
            
    return render_template('register.html')

@app.route('/select_language', methods=['GET', 'POST'])
def select_language():
    """Language selection page - supports 4 languages for now"""
    if 'username' not in session:  # Simple session check
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        selected_lang = request.form['language']
        session['language'] = selected_lang
        return redirect(url_for('chatbot'))
    return render_template('select_language.html')

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    """Main chatbot interface"""
    if 'username' not in session:
        return redirect(url_for('login'))
        
    bot_response = ""
    if request.method == 'POST':
        user_question = request.form['query']
        user_language = session.get('language', 'english')
        bot_response = get_mining_response(user_question, user_language)
        
    language = session.get('language', 'english')
    return render_template('chatbot.html', response=bot_response, language=language)

def get_mining_response(question, language):
    """Get response from OpenAI for mining-related questions"""
    # Check if question is about mining - basic keyword matching
    mining_terms = [
        "mining", "coal", "dgms", "regulation", "explosives", "colliery",
        "wages", "circulars", "cba", "land acquisition", "act", "rules",
        "payment", "mines", "proceedings"
    ]
    
    # Simple validation - checking if any mining keyword exists
    is_mining_related = any(term.lower() in question.lower() for term in mining_terms)
    
    if not is_mining_related:
        return "Sorry, I can only help with mining-related Acts, Rules, and Regulations."

    # Language-specific prompts - keeping it simple
    language_prompts = {
        "english": "Answer in English: ",
        "hindi": "हिंदी में उत्तर दें: ",
        "telugu": "తెలుగులో సమాధానం ఇవ్వండి: ",
        "kannada": "ಕನ್ನಡದಲ್ಲಿ ಉತ್ತರ ನೀಡಿ: "
    }
    
    prompt_prefix = language_prompts.get(language, "Answer in English: ")
    full_question = prompt_prefix + question

    try:
        # Using OpenAI API - this part I learned from documentation
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": full_question}],
            max_tokens=500  # Added limit to control response length
        )
        return response.choices[0].message.content
    except Exception as e:  # Simplified error handling
        print(f"OpenAI API error: {e}")
        return "Sorry, I'm having trouble connecting to the service right now. Please try again."

@app.route('/logout')
def logout():
    """Logout and clear session"""
    session.clear()
    return redirect(url_for('login'))

# Run the application
if __name__ == '__main__':
    setup_database()  # Initialize database on startup
    # Using debug=True for development - will change for production
    app.run(debug=True, host='0.0.0.0', port=5000)
