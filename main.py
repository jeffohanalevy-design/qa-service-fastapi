#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  9 13:33:08 2025

@author: josephohana
"""

from fastapi import FastAPI, HTTPException, Query
import requests
from sentence_transformers import SentenceTransformer
import numpy as np
from datetime import datetime
import re

app = FastAPI()

MESSAGES_API = "https://november7-730026606190.europe-west1.run.app/messages"

# Load local semantic model
model = SentenceTransformer("all-MiniLM-L6-v2")

message_cache = []

@app.on_event("startup")
def load_messages():
    """Load messages and precompute embeddings."""
    global message_cache
    try:
        response = requests.get(MESSAGES_API)
        response.raise_for_status()
        data = response.json()
        messages = data.get("items", [])
    except Exception as e:
        raise RuntimeError(f"Failed to fetch messages: {e}")

    for msg in messages:
        content = msg.get("message", "").strip()
        if not content:
            continue
        embedding = model.encode(content)
        message_cache.append({
            "user_name": msg.get("user_name", ""),
            "message": content,
            "timestamp": msg.get("timestamp", ""),
            "embedding": embedding
        })


@app.get("/ask")
def ask(question: str = Query(..., description="Your natural-language question")):
    """
    Answer a question using semantic search restricted to the mentioned user.
    """
    if not message_cache:
        raise HTTPException(status_code=500, detail="Message cache is empty.")

    # Detect which user's messages to consider
    target_user = detect_user_from_question(question)

    if target_user:
        user_msgs = [m for m in message_cache if target_user.lower() in m["user_name"].lower()]
        if not user_msgs:
            return {"answer": f"Sorry, I couldn’t find any messages from {target_user}."}
    else:
        user_msgs = message_cache  # fallback: all messages

    # Compute similarity among that user's messages
    question_emb = model.encode(question)
    similarities = [
        (msg, cosine_similarity(question_emb, msg["embedding"]))
        for msg in user_msgs
    ]
    similarities.sort(key=lambda x: x[1], reverse=True)

    if not similarities or similarities[0][1] < 0.45:
        return {"answer": "Sorry, I could not find an answer to your question."}

    top_msg = [m for m, sim in similarities[:1] if sim > 0.45]
    answer = summarize_answer(question, top_msg)
    return {"answer": answer}


def detect_user_from_question(question: str):
    """
    Identify which user name is mentioned in the question by fuzzy matching.
    """
    all_names = {m["user_name"] for m in message_cache}
    q_lower = question.lower()
    for name in all_names:
        if name.lower().split()[0] in q_lower or name.lower() in q_lower:
            return name
    return None


def summarize_answer(question, messages):
    """Summarize the relevant messages naturally."""
    if not messages:
        return "Sorry, I could not find any relevant messages."

    if is_date_related(question):
        date_text = extract_date_from_messages(messages)
        if date_text:
            name = messages[0]["user_name"].split()[0]
            return f"{name} is planning it on {date_text}."
        else:
            best = messages[0]
            ts = format_timestamp(best.get("timestamp"))
            if ts:
                name = best["user_name"].split()[0]
                return f"{name} mentioned on {ts}: {best['message']}"
            else:
                return best["message"]
    else:
        user = messages[0]["user_name"].split()[0]
        unique_msg = list({m["message"] for m in messages})
        if len(unique_msg) == 1:
            return f"{user} mentioned: {unique_msg[0]}"


def is_date_related(question):
    date_keywords = ["when", "date", "day", "time", "month", "year", "schedule", "plan", "planned"]
    return any(word in question.lower() for word in date_keywords)


def extract_date_from_messages(messages):
    date_pattern = r"([A-Z][a-z]+ \d{1,2}, \d{4})"
    for msg in messages:
        match = re.search(date_pattern, msg["message"])
        if match:
            return match.group(1)
    return None


def format_timestamp(ts):
    try:
        d = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return d.strftime("%B %-d, %Y")
    except Exception:
        return None


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

