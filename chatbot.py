import google.generativeai as genai
from sentiment_model import analyze_sentiment  # Import sentiment analysis function

# Configure Gemini API
# NOTE: Replace with your actual API key in a secure way (e.g., environment variable)
#       DO NOT HARDCODE YOUR API KEY IN A PUBLIC REPOSITORY.
GENAI_API_KEY = "<YOUR_GEMINI_API_KEY>" # Placeholder
genai.configure(api_key=GENAI_API_KEY)

# List of predefined coping strategies based on emotions
COPING_STRATEGIES = {
    "stress": "Try deep breathing exercises or a short walk to clear your mind.",
    "anxiety": "Practicing mindfulness or writing down your worries might help you feel calmer.",
    "sadness": "Listening to uplifting music or talking to a friend could help brighten your mood.",
    "anger": "Taking a few deep breaths and stepping away for a moment might help."
}

# Function to generate chatbot response
def get_chatbot_response(user_input, chat_history):
    """
    Generates a chatbot response based on user input and chat history.

    Args:
        user_input (str): The user's input text.
        chat_history (list): A list of dictionaries representing the chat history.  Each dictionary should have "role" and "text" keys.

    Returns:
        str: The chatbot's response.
    """
    # Detect sentiment using our custom function
    sentiment = analyze_sentiment(user_input)

    # Provide a coping mechanism if the emotion matches
    coping_tip = COPING_STRATEGIES.get(sentiment, "")

    # Format chat history for context
    history = "\n".join([f"{msg['role']}: {msg['text']}" for msg in chat_history[-3:]])

    # Define the prompt with explicit instruction
    prompt = f"""
    You are EmoBuddy, an emotional support chatbot that recognizes and responds to 27 emotions.

    **Step 1:** Classify the user's sentiment as positive, neutral, or negative.

    **Step 2:** If the sentiment is negative, respond with empathy and provide a coping mechanism if applicable.

    **Step 3:** If the sentiment is positive, encourage the user with a supportive response.

    **Step 4:** Keep responses short (1-2 sentences) and natural.

    Recent conversation:
    {history}

    User: "{user_input}"
    Detected Sentiment: {sentiment.capitalize()}

    Response format:
    EmoBuddy: [empathetic response + coping suggestion (if applicable)]
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

                    # If a coping strategy is available, append it
                    if coping_tip:
                        final_response += f" Here's something that might help: {coping_tip}"

                    return final_response

        return "I'm here for you. Let's talk."
    except Exception as e:
        print(f"Error generating response: {e}")  # Log the error
        return "Sorry, I'm having trouble responding. Let's talk about something else."

# Example interaction (Colab-friendly - remove or comment out for production)
if __name__ == "__main__":
    chat_history = []
    print("EmoBuddy: Your Emotional Support Chatbot\nHello! How are you feeling today?")

    while True:
        try:
            user_input = input("You: ")
        except EOFError:  # Handles abrupt termination in Colab
            break

        if user_input.lower() in ["exit", "quit"]:
            print("EmoBuddy: Take care! I'm always here if you need me.")
            break

        response = get_chatbot_response(user_input, chat_history)
        chat_history.append({"role": "user", "text": user_input})
        chat_history.append({"role": "bot", "text": response})

        print(f"EmoBuddy: {response}")
