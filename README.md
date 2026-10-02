# 🍳 AI Cook Master

AI Cook Master is an AI-powered cooking assistant built with **Streamlit and Google Gemini**.

The application allows users to ask cooking-related questions or upload a photo of a meal. Gemini analyzes the user's input and provides useful information such as ingredients, cooking instructions, cooking time, and other relevant details.

After receiving an AI-generated response, users can send a summarized version of their conversation directly to their personal **Telegram chat** using a Telegram Bot.

---

## ✨ Features

- 🤖 AI-powered cooking assistant using Google Gemini
- 💬 Ask cooking-related questions using natural language
- 📷 Upload a photo of a meal for AI analysis
- 🥕 Get ingredients and cooking information
- 👨‍🍳 Get step-by-step cooking instructions
- ⏱️ Get estimated cooking time when applicable
- 🧠 Maintains the conversation context during the session
- 📤 Send an AI-generated conversation summary to Telegram
- 🔐 API keys and sensitive credentials are stored securely using Streamlit Secrets
- 💻 Simple and interactive Streamlit interface

---

## 🛠️ Technologies Used

- **Python**
- **Streamlit** – Web application framework
- **Google Gemini API** – AI-powered food and cooking analysis
- **python-telegram-bot** – Send AI-generated summaries to Telegram
- **Asyncio** – Handle asynchronous Telegram operations
- **Git & GitHub** – Version control and source code management

---

## 📁 Project Structure

```text
AI_chat_Bot/
│
├── .streamlit/
│   └── secrets.toml       # API keys and private credentials
│
├── venv/                  # Python virtual environment
│
├── app.py                 # Main Streamlit application
├── prompt.py              # AI system prompts and prompt templates
├── requirements.txt       # Python dependencies
├── .gitignore             # Files ignored by Git
└── README.md              # Project documentation


## Telegram Chat Bot creation 

@BotFather => just click on start read the message and click the step that create bot and follow remaining step as it say


#Runnning proccess in localy 

cd AI_chat_Bot
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r .\requirement.txt    #This install all the packages that need to be installed only which are in requirements.txt

streamlit run app.py    => helps to run locally