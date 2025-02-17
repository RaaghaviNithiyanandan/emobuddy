import streamlit as st
from chatbot import get_chatbot_response  # Import chatbot logic
from PIL import Image  # For loading the avatar image
import base64
from io import BytesIO

st.set_page_config(page_title="EmoBuddy", page_icon="avatar.jpg", layout="wide")  # Set avatar.jpg as tab icon

st.title("🫂 EmoBuddy: Your Emotional Support Chatbot")
st.write("Hello! How are you feeling today? Share your thoughts below.")

# Initialize session state for messages and user input
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# Function to handle input submission
def handle_input():
    user_input = st.session_state.user_input.strip()

    if user_input:
        response = get_chatbot_response(user_input, st.session_state.messages)

        # Store new messages
        st.session_state.messages.append({"role": "You", "text": user_input})
        st.session_state.messages.append({"role": "EmoBuddy", "text": response})

        # Clear input field
        st.session_state.user_input = ""

# Load avatar image (ensure it’s in the same directory as your app.py)
try:
    avatar_image = Image.open("avatar.jpg")
except FileNotFoundError:
    st.warning("Avatar image 'avatar.jpg' not found.  Using a default.")
    # You could replace this with a default avatar image if you have one.
    avatar_image = None  # Or load a default

# Convert avatar image to base64
def convert_image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

# Convert avatar to base64
avatar_base64 = None
if avatar_image:
    avatar_base64 = convert_image_to_base64(avatar_image)

# Custom CSS for chat styling
st.markdown(
    """
    <style>
        .user-message {
            display: flex;
            justify-content: flex-end;
            margin: 10px 0;
        }
        .bot-message {
            display: flex;
            justify-content: flex-start;
            margin: 10px 0;
        }
        .message-box {
            padding: 10px;
            border-radius: 8px;
            max-width: 60%;
            word-wrap: break-word;
        }
        .user-message .message-box {
            background-color: #e0f7fa;
        }
        .bot-message .message-box {
            background-color: #f1f8e9;
            display: flex;
            align-items: center;
        }
        .bot-message img {
            border-radius: 50%;
            width: 40px;  /* Set fixed width for the avatar */
            height: 40px; /* Set fixed height for the avatar */
            margin-right: 10px;
        }
        .message-box p {
            margin: 0;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Display chat history with proper alignment and avatar for EmoBuddy
st.divider()
for msg in st.session_state.messages:
    if msg["role"] == "You":
        # User message (right aligned)
        with st.container():
            st.markdown(f'<div class="user-message"><div class="message-box"><p><strong>You:</strong> {msg["text"]}</p></div></div>', unsafe_allow_html=True)
    else:
        # Bot message (left aligned with avatar)
        with st.container():
            avatar_html = ""
            if avatar_base64:
                avatar_html = f'<img src="data:image/jpeg;base64,{avatar_base64}" alt="EmoBuddy Avatar">'
            st.markdown(f'<div class="bot-message">{avatar_html}<div class="message-box"><p><strong>EmoBuddy:</strong> {msg["text"]}</p></div></div>', unsafe_allow_html=True)

st.divider()

# User input at bottom with automatic handling
st.text_input("Enter your thoughts:", key="user_input", on_change=handle_input, label_visibility="collapsed")
