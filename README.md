# qa-service-fastapi
 Question-answering system that can answer natural-language questions about member data provided by Aurora's public API

# Question Answering API (FastAPI)

A simple Question Answering API that answers natural-language questions about member messages retrieved from a public API.

---

## Local Setup (Service Deployment)

- Dowmload the files (main.py and requirements.txt) in your Desktop

- Open your Terminal and change the directory to Desktop

- `pip install -r requirements.txt` on your Terminal 

- Run the server locally on your terminal as follow: `uvicorn main:app --reload --port 8080`

- Then open on your browser: `http://127.0.0.1:8080/docs` to try out and ask questions to the system obtaining an answer

Example questions that trigger an answer:
- "When is Sofia intending to book a private jet?"
- "What kind of seats does Layla want for her flight?"
- "What does Armand Dupont need tickets for ?"

Example questions that trigger no answer (the algorithm does not find relevant messages):
- "When is Layla planning her trip to London?"
- "How many cars does Vikram Desai have?"
- "What are Amira’s favorite restaurants?"

Short screen recording demonstrating example queries: https://drive.google.com/file/d/1zF5L5qA-TQJn6gvL4PYmykN1wFFPPdYI/view?usp=share_link

---

## Bonus 1: Design Notes

The algorithm design in main.py is the following:
- Load data from the public API of the company and compute the messages' embedding using SentenceTransformer("all-MiniLM-L6-v2")
- Receive question from user 
- Detect if a username or part of it is present in the question; will fetch only messages corresponding to the username in the question; if no username is mentionned, will fetch all messages
- Semantic Search (if topic-based question): select top message based on cosine simmilarity between the messages and the question
- Summarize the message into an answer and mention the timestamp only if it is a date related question

So this algorithm uses SentenceTransformer("all-MiniLM-L6-v2") to create the embeddings for both the question and messages and compare them to check for similarities. Initially, Instead of the embeddings comparaison, I used a very basic keyword search logic: Looks for messages containing a name mentioned in the question, then returns message content as the answer. I realized that the answers were way out of the question's scope. Then, I switched to the embeddings and the answers were making more sense. 

Initially I also left over the timestamp from the data to consider in the answers. But I ended up realizing that it would be useful to insert the date a message was sent if the question is time related. For instance, if the question is "when is Leyla travelling?", then a possible answer comes from the message "book me a flight for tomorrow" where the timestamp would be relevant to answer when Leyla is travelling. 

## Bonus 2: Data Insights 

The data is very coherent and structured. It is easy to access the usernames, timestamps, and messages with the JSON library in Python. There are no inconsistencies or missing data. 


