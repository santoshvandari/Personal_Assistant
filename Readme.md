
# Personal Assistant with Google Generative AI

This project is a versatile personal assistant application built with Python, Streamlit, LangChain, and Google Generative AI. It leverages Google’s generative language model to draft emails, generate study plans, answer knowledge-based questions, extract action items, and more.

## Project Structure

```bash
personal_assistant_project/
├── .env                     # Environment variables including the API key
├── app.py                   # Main Streamlit app for user interaction
├── utils.py                 # Backend functions and helper utilities
└── requirements.txt         # Project dependencies
```

## Features

- **Draft Professional Emails**: Generate emails based on provided context.
- **Knowledge-Based Q&A**: Answer questions based on a specific knowledge domain.
- **Generate Study Plans**: Create structured study plans based on topic and duration.
- **Extract Action Items**: Summarize key action items from meeting notes.
- **Tool-Using Agent**: A general-purpose agent that can execute tasks based on user queries.

## Setup

### Prerequisites

- Python 3.7+
- Google Gemini API Key for Generative AI (Gemini)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/santoshvandari/Personal_Assistant.git
    cd Personal_Assistant
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up the `.env` file with your Google Generative AI API key:
    ```plaintext
    API_KEY="YOUR_GOOGLE_GENERATIVEAI_API_KEY"
    ```

### Configure Google Generative AI

Make sure your Google Cloud project has the Generative AI API enabled, and create an API key for the project. Update the API key in the `.env` file as shown above.
Get the API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

## Usage

Run the Streamlit app to start using the personal assistant:

```bash
streamlit run app.py
```

1. Open the provided `localhost` link in your browser.
2. Choose a task from the sidebar (e.g., "Draft Email," "Knowledge-Based Q&A").
3. Enter the relevant information, and click the button to generate a response.
4. View the generated output in the text area below.

## Example Tasks

### 1. Draft a Professional Email
   - **Context**: "Write a thank-you email to the team for their hard work on the recent project."
   - **Generated Email**: A professionally drafted thank-you email ready to send.

### 2. Generate a Study Plan
   - **Topic**: "Data Science"
   - **Duration**: "3 months"
   - **Generated Plan**: A structured weekly plan covering essential data science topics.

### 3. Knowledge-Based Q&A
   - **Domain**: "Finance"
   - **Question**: "What are the main benefits of compound interest?"
   - **Generated Answer**: A detailed answer explaining compound interest benefits.

### 4. Extract Action Items
   - **Meeting Notes**: Enter meeting notes to extract key action items.
   - **Generated Action Items**: A list of main action points for easy follow-up.

### 5. Tool-Using Agent
   - **Query**: "Draft an email thanking the team for their hard work."
   - **Generated Output**: The agent processes the input and uses appropriate tools to generate a meaningful response.

## Contributing
We welcome contributions! If you'd like to contribute to this Code, please check out our [Contribution Guidelines](Contribution.md).

## Code of Conduct
Please review our [Code of Conduct](CodeOfConduct.md) before participating in this app.

## License
This project is licensed under the [License](LICENSE).
