
# careerlens-ai
A local AI résumé and job description comparison app

# CareerLens

CareerLens is a beginner-built résumé and job description comparison app. It highlights listed skills found in both texts, shows the résumé sentence supporting each match, and uses a local AI model to summarize that evidence.

## Features

- Compare pasted résumé text with a job description.
- Show which listed skills appear in both texts.
- Display résumé evidence for each detected skill.
- Generate a short evidence summary using a local model through Ollama.

## Tools

- Python
- Streamlit
- Ollama
- Llama 3.2 3B

No paid API key or cloud service is required for the local AI summary.

## Run locally on Windows

1. Install [Ollama](https://ollama.com/download/windows).
2. Download the model:

   ```powershell
   ollama run llama3.2:3b
   ```

   After it finishes downloading, enter `/bye` to return to the terminal. Ollama will run in the background.

3. From the project folder, create a virtual environment and install the Python packages:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

4. Start the app:

   ```powershell
   .\.venv\Scripts\python.exe -m streamlit run app.py
   ```

## Current limitations


- Skill detection uses simple keyword matching against a list in the code.
- The app accepts pasted text; it does not read résumé files yet.
- The AI summary can make mistakes. Review it against the displayed résumé evidence.
- A detected keyword does not prove a person's skill level.
