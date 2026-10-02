import streamlit as st
from google import genai 
from google.genai import types
from twilio.rest import Client as TwilioClient
from telegram import Bot
import asyncio

from prompt import SYSTEM_PROMPT,WELCOME_MESSAGE_TEMPLATE,SUMMARY_REQUEST_PROMPT

GEMINI_API_KEY = st.secrets['GEMINI_API_KEY']
TWILIO_ACCOUNT_SID = st.secrets['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = st.secrets['TWILIO_AUTHO_TOKEN']
TELEGRAM_BOT_TOKEN = st.secrets['TELEGRAM_TOKEN']
TELEGRAM_CHAT_ID = st.secrets['TELEGRAM_CHAT_ID']


def send_telegram(chat_id, text):
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        asyncio.run(
            bot.send_message(
                chat_id=chat_id,
                text=text
            )
        )
        return True, "Message sent successfully"
    except Exception as error:
        return False, str(error)



@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key=GEMINI_API_KEY)

@st.cache_resource
def get_twilio_client():
    return TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


twilio_client = get_twilio_client()
gemini_client = get_gemini_client()


def render_message(message):
    with st.chat_message(message['role']):
        if message['kind'] == 'text':
            st.write(message['content'])
        elif message['kind'] == 'image':
            st.image(message['content'])


def add_message(role, kind, content): #adding message
    st.session_state.message.append({'role':role,'kind':kind, 'content':content})
    render_message(st.session_state.message[-1])

def ask_gemini(parts):
    try:
        return st.session_state.chat.send_message(parts).text
    except Exception as error:
        return f"Sorry, something went wrong {error}"



if 'onboarded' not in st.session_state:
    st.title("AI Cook Master 👩‍🍳")
    st.caption('Snap it, Share it , cook it in out style.')

    with st.form('onboarding_form'):
        name = st.text_input('Your_name')
        number = st.text_input(
            'Number (with country code)',
            placeholder="+91xxxxxxxxxx",
            help='This is the number AI Chef Master will text your summary.'
        )

        submitted = st.form_submit_button('Start')
    if submitted:
        if not name.strip() or not number.strip():
            st.warning("Please fill all the above fields")
        else:

            st.session_state.name = name
            st.session_state.number = number

            st.session_state.chat = gemini_client.chats.create(
                model='gemini-3.6-flash',
                config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT)
            )

            st.session_state.message = []
            st.session_state.onboarded = True
            st.rerun()
    st.stop()
    
#chat interface 

header_col , button_col = st.columns([5,2], vertical_alignment='center')

with header_col:
    st.title("AI Cook Master 👩‍🍳")

with button_col:
    send_disabled = len(st.session_state.message) < 1
    if st.button("📤 Send to Telegram", disabled=send_disabled, use_container_width=True):
        with st.spinner("Summarizing your day..."):
            summary = ask_gemini([SUMMARY_REQUEST_PROMPT])
        success, info = send_telegram( TELEGRAM_CHAT_ID,summary)
        if success:
            st.success("Sent! Check your Telegram 📲")
        else:
           st.error(f"Couldn't send that: {info}")

st.caption(f"logged in as {st.session_state.name} - updates goes to @AIMasterChefBot")

if not st.session_state.message:
    add_message('assistant','text',WELCOME_MESSAGE_TEMPLATE.format(name=st.session_state.name))
else:
    for i in st.session_state.message:
        render_message(i)


user_input = st.chat_input(
    "Ask a question, or attach a photo of your meal.",
    accept_file=True,
    file_type=['jpg','jpeg','png'],

)

if user_input:
    photo = user_input.files[0] if user_input.files else None
    text = user_input.text 
    parts = []

    if photo is not None:
        photo_bytes = photo.getvalue()
        add_message("user", "image", photo_bytes)
        parts.append(types.Part.from_bytes(data=photo_bytes, mime_type=photo.type))
    if text:
        add_message("user", "text", text)
        parts.append(text) 
    elif photo is not None:
        parts.append("What is this meal? Give me the Ingredients and cooking process.")

    with st.spinner("Crunching the numbers..."):
        answer = ask_gemini(parts)

    add_message("assistant", "text", answer)



