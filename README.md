
*   **`README.md`:**

```markdown
# EmoBuddy: Your Emotional Support Chatbot

EmoBuddy is a chatbot designed to provide emotional support and coping strategies based on user input. It uses sentiment analysis to understand the user's emotional state and generates empathetic responses.

## Features

*   **Sentiment Analysis:** Detects the sentiment (positive, negative, or neutral) of user input.
*   **Empathetic Responses:** Generates responses that acknowledge and validate the user's feelings.
*   **Coping Strategies:** Suggests coping mechanisms based on the detected sentiment.
*   **Streamlit UI:** Provides a simple and interactive user interface.

## Setup Instructions

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd emobuddy
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```
    (Create a `requirements.txt` file listing the project's dependencies: `nltk`, `streamlit`, `transformers`, `requests`, `google-generativeai`, `pyngrok`)

3.  **Obtain API Keys:**

    *   **Google Gemini API Key:**  You'll need a Google Gemini API key to use the chatbot's generative capabilities.  Follow the instructions on the Google AI platform to obtain one.
    *   **Ngrok Authtoken:** To run the Streamlit app publicly (e.g., from Google Colab), you'll need an Ngrok authtoken. Sign up for a free Ngrok account and obtain your authtoken from the Ngrok dashboard.

4.  **Configure API Keys:**

    *   **Environment Variables (Recommended):** Set the `GEMINI_API_KEY` and `NGROK_AUTHTOKEN` environment variables.  This is the most secure way to store your API keys.

        ```bash
        export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
        export NGROK_AUTHTOKEN="YOUR_NGROK_AUTHTOKEN"
        ```

    *   **Direct Assignment (Less Secure):** You can directly assign the API keys in the `chatbot.py` and the Colab notebook, but be extremely careful not to commit them to a public repository.

5.  **Run the Streamlit App:**

    *   **Locally:** If you're running the app locally, execute:

        ```bash
        streamlit run app.py
        ```

    *   **Google Colab:** Open the `emobuddy_colab.ipynb` notebook in Google Colab and follow the instructions in the notebook.

## Running in Google Colab

The `emobuddy_colab.ipynb` notebook provides a convenient way to run the EmoBuddy chatbot in a Google Colab environment.  Follow the instructions within the notebook to set up the environment, configure API keys, and launch the chatbot.

