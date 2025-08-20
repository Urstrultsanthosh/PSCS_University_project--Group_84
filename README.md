# Mining Industry Chatbot

A multilingual chatbot designed to answer queries about various Acts, Rules, and Regulations applicable to Mining Industries in India.

## Features

- **Multi-language Support**: English, Hindi, Telugu, Kannada
- **Mining-focused**: Specialized for mining industry regulations
- **User Authentication**: Secure login and registration system
- **Session Management**: Maintains user sessions and language preferences

## Technologies Used

- **Backend**: Flask (Python)
- **Database**: SQLite
- **AI Integration**: OpenAI GPT-3.5-turbo
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: Session-based login system

## Setup Instructions

### Prerequisites
- Python 3.7+
- OpenAI API key

### Installation

1. Clone the repository
```bash
git clone https://github.com/Urstrultsanthosh/PSCS_University_project--Group_84.git
cd PSCS_University_project--Group_84
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Create environment file
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openai_api_key_here
FLASK_SECRET_KEY=your_secret_key_here
```

4. Run the application
```bash
python app.py
```

5. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Register a new account or login with existing credentials
2. Select your preferred language
3. Ask questions related to mining regulations, acts, and rules
4. Get responses in your selected language

## Project Structure

```
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (not in repo)
├── templates/         # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── select_language.html
│   └── chatbot.html
└── static/           # Static files
    ├── css/
    └── js/
```

## Features Implemented

- User registration and authentication
- Multi-language interface
- Mining domain-specific query validation
- OpenAI integration for intelligent responses
- Session management
- Responsive web interface

## Future Improvements

- Add more mining regulations to the knowledge base
- Implement advanced NLP for better query understanding
- Add export functionality for chat history
- Mobile app development

## Contributing

This project was developed as part of a university assignment. Contributions and suggestions are welcome.

## License

This project is for educational purposes.