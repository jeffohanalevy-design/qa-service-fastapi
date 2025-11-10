# qa-service-fastapi
 Question-answering system that can answer natural-language questions about member data provided by Aurora's public API

# Question Answering API (FastAPI)

A simple Question Answering API that answers natural-language questions about member messages retrieved from a public API.

Example questions:
- “When is Layla planning her trip to London?”
- “How many cars does Vikram Desai have?”
- “What are Amira’s favorite restaurants?”

---

## Local Setup (Service Deployment)

- Dowmload the files (main.py and requirements.txt) in your Desktop

- Open your Terminal and change the directory to Desktop

- `pip install -r requirements.txt` on your Terminal 

- Run the server locally on your terminal as follow: `uvicorn main:app --reload --port 8080`

- Then open on your browser: `http://127.0.0.1:8080/docs` to try out and ask questions to the system obtaining an answer

---

## Bonus 1: Design Notes

The algorithm design in main.py is the following:
- Load data from the API and compute the messages' embedding using SentenceTransformer("all-MiniLM-L6-v2")
- Receive question from user 
- Detect if a username or part of it is present in the question; will fetch only messages corresponding to the username in the question; if no username is mentionned, will fetch all messages
- Handle "simple" questions: if no topic is mentionned like “What did Layla say?”; The algorithm directly summarizes the user’s recent messages
- 

