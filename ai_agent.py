import re
from datetime import datetime
import os

dataset_path = "data/conversations.txt"

# ✅ Ensure data folder exists
os.makedirs(os.path.dirname(dataset_path), exist_ok=True)

# Load existing conversations
conversations = {}
if os.path.exists(dataset_path):
    with open(dataset_path, "r", encoding="utf-8") as f:
        for line in f:
            if "|" in line:
                question, answer = line.strip().split("|", 1)
                question_norm = re.sub(r'[^\w\s]', '', question.lower())
                conversations[question_norm] = answer

def normalize_text(text: str) -> str:
    """Lowercase, remove punctuation, strip spaces"""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip()

def add_conversation(question: str, answer: str):
    """Add new Q&A to memory and file"""
    question_norm = normalize_text(question)
    conversations[question_norm] = answer
    with open(dataset_path, "a", encoding="utf-8") as f:
        f.write(f"\n{question}|{answer}")

def run_agent(user_input: str) -> str:
    normalized_input = normalize_text(user_input)

    # ✅ Teach mode
    if user_input.lower().startswith("teach:"):
        try:
            _, qa = user_input.split("teach:", 1)
            question, answer = qa.split("|", 1)
            add_conversation(question.strip(), answer.strip())
            return f"Learned: '{question.strip()}' -> '{answer.strip()}'"
        except Exception:
            return "Invalid teach format. Use: teach: question | answer"

    # ✅ Date / Time queries (Bangla & English keywords)
    if "date" in normalized_input or "তারিখ" in normalized_input:
        return f"Today's date is {datetime.now().strftime('%Y-%m-%d')}"
    if "time" in normalized_input or "সময়" in normalized_input:
        return f"Current time is {datetime.now().strftime('%H:%M:%S')}"

    # ✅ Exact match
    if normalized_input in conversations:
        return conversations[normalized_input]

    # 🔹 Keyword match: single word match returns answer
    input_words = set(normalized_input.split())
    for question, answer in conversations.items():
        question_words = set(question.split())
        if question_words & input_words:
            return answer

    # 🔹 Fuzzy match: 50%+ word overlap
    for question, answer in conversations.items():
        question_words = set(question.split())
        if len(input_words & question_words) / max(1, len(input_words)) > 0.5:
            return answer

    # 🔹 Fallback
    bangla_unicode = re.search(r'[\u0980-\u09FF]', user_input)
    if bangla_unicode:
        return "আমি বুঝতে পারিনি। Teach me using: teach: প্রশ্ন | উত্তর"
    else:
        return "I don't understand. Teach me using: teach: question | answer"

# ✅ Test console
if __name__ == "__main__":
    print("===== AI Agent Test =====")
    print("Type 'exit' or 'quit' to stop.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = run_agent(user_input)
        print("Bot:", response)
