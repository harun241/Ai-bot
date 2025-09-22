import re
from datetime import datetime

dataset_path = "data/conversations.txt"

# Load existing conversations
conversations = {}
with open(dataset_path, "r", encoding="utf-8") as f:
    for line in f:
        if "|" in line:
            question, answer = line.strip().split("|", 1)
            question_norm = re.sub(r'[^\w\s]', '', question.lower())
            conversations[question_norm] = answer

def normalize_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip()

def add_conversation(question: str, answer: str):
    question_norm = normalize_text(question)
    conversations[question_norm] = answer
    with open(dataset_path, "a", encoding="utf-8") as f:
        f.write(f"\n{question}|{answer}")

def run_agent(user_input: str) -> str:

    # Auto-teach: check raw input first
    if user_input.lower().startswith("teach:"):
        try:
            _, qa = user_input.split("teach:", 1)
            question, answer = qa.split("|", 1)
            add_conversation(question.strip(), answer.strip())
            return f"Learned: '{question.strip()}' -> '{answer.strip()}'"
        except Exception:
            return "Invalid teach format. Use: teach: question | answer"

    normalized_input = normalize_text(user_input)

    # Date/Time queries
    if "date" in normalized_input:
        return f"Today's date is {datetime.now().strftime('%Y-%m-%d')}"
    if "time" in normalized_input:
        return f"Current time is {datetime.now().strftime('%H:%M:%S')}"

    # Exact match
    if normalized_input in conversations:
        return conversations[normalized_input]

    # Fuzzy match
    for question, answer in conversations.items():
        question_words = set(question.split())
        input_words = set(normalized_input.split())
        if len(input_words & question_words) / max(1, len(input_words)) > 0.5:
            return answer

    return "I don't understand. Teach me using: teach: question | answer"
