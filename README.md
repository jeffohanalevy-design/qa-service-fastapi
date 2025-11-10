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

Dowmload the files in your Desktop

Open your Terminal and change the directory to Desktop

`pip install -r requirements.txt` on your Terminal 

Run the server locally on your terminal:

`uvicorn main:app --reload --port 8080`

Then open:

`http://127.0.0.1:8080/docs` to try out and ask questions to the system obtaining an answer

