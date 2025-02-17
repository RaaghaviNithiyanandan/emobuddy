# %%writefile chatbot.py
import google.generativeai as genai
from sentiment_model import analyze_sentiment  # Import sentiment analysis function
import os

# Configure Gemini API
# NOTE: Replace with your actual API key in a secure way (e.g., environment variable)
#       DO NOT HARDCODE YOUR API KEY IN A PUBLIC REPOSITORY.
GENAI_API_KEY = os.environ.get("GEMINI_API_KEY") # Use environment variable
if not GENAI_API_KEY:
    print("Error: GEMINI_API_KEY environment variable not set.  The chatbot will not function correctly.")

genai.configure(api_key=GENAI_API_KEY)

# Function to generate chatbot response
def get_chatbot_response(user_input, chat_history):
    """
    Generates a chatbot response based on user input and chat history.  It uses sentiment analysis to understand the user's emotional state and generates empathetic responses.

    Args:
        user_input (str): The user's input text.
        chat_history (list): A list of dictionaries representing the chat history.  Each dictionary should have "role" and "text" keys.

    Returns:
        str: The chatbot's response.
    """
    # Detect sentiment using our custom function
    sentiment = analyze_sentiment(user_input)

    # Format chat history for context
    history = "\n".join([f"{msg['role']}: {msg['text']}" for msg in chat_history[-3:]])

    # Define the prompt to handle the 27 emotions dynamically
    prompt = f"""
    You are EmoBuddy, an emotional support chatbot capable of recognizing and responding to 27 specific emotions:
    admiration, adoration, aesthetic appreciation, amusement, anger, anxiety, awe, awkwardness, boredom, calmness, confusion,
    craving, disgust, empathic pain, entrancement, excitement, fear, horror, interest, joy, nostalgia, relief, romance, sadness,
    satisfaction, sexual desire, and surprise.

    Your role is to provide therapeutic, empathetic responses based on the user's emotional state. Always aim to sound positive, supportive, and avoid repetition in your responses. Here's how you should respond:

    1.  If the user's sentiment indicates negative emotions such as anger, anxiety, or fear, offer empathy and provide a therapeutic, comforting response.
    2.  If the sentiment indicates positive emotions like joy, excitement, or awe, acknowledge their feelings and support them.
    3.  If the user expresses a specific emotion from the list (such as sadness, horror, or surprise), respond in a way that matches the emotional tone of the conversation.
    4.  Tailor the response based on the detected emotion. Avoid giving the same response for similar inputs, and try to address the user's emotions in a unique way each time.
    5.  Always vary your responses and include suggestions or empathetic responses specific to the detected emotion.
    6.  Do not answer any questions about the tech stack or how you are being developed. If asked, politely steer the conversation back to emotions and how the user feels.
    7.  If there is anything outside of coping, providing support, or answering open-ended questions related to the emotions, mention that you are an emotional support buddy and that it is out of your scope. However, express your willingness to continue talking about how they feel.
    8.  Do not provide medical advice. Focus solely on emotional support, coping mechanisms, and empathetic responses.
    9.  Avoid repeating the same response. Each interaction should feel unique, and the responses should be varied and tailored to the user's current emotional state.
    10. If the user asks about topics outside emotional support (e.g., romance, love, sexual desire advice), gently steer the conversation back to their feelings.

    Additionally:
    - Always maintain a calming, understanding tone. Show empathy, warmth, and kindness in every response.
    - Acknowledge the user's feelings, validate their emotions, and provide comforting support.
    - If the user shows signs of distress, try to guide them toward healthy ways to cope, like encouraging them to talk to a trusted friend or engage in a calming activity.

    Your goal is to create a safe space where the user feels heard, understood, and supported.


    Recent conversation:
    {history}

    User: "{user_input}"
    Detected Sentiment: {sentiment.capitalize()}

    Response format:
    EmoBuddy: [therapeutic response based on sentiment + unique suggestion or empathy based on detected emotion]
    """

    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)

        # Extract only EmoBuddy's response from the generated text
        if response.text:
            lines = response.text.strip().split("\n")
            for line in lines:
                if "EmoBuddy:" in line:
                    final_response = line.replace("EmoBuddy:", "").strip()
                    return final_response

        return "I'm here for you. Let's talk." # Default response
    except Exception as e:
        print(f"Error generating response: {e}") # Log error for debugging.
        return "Sorry, I'm having trouble responding. Let's talk about something else." # Generic Message
