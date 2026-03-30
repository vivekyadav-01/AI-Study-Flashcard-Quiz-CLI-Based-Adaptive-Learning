#!/usr/bin/env python3
"""
AI Study Flashcard Quiz - Adaptive Learning CLI
Uses spaced repetition and confidence-based scoring to optimize learning.
"""

import json
import os
import random
import time
import math
from datetime import datetime, timedelta

# ─────────────────────────────────────────────
#  DATA FILES
# ─────────────────────────────────────────────
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
CARDS_FILE = os.path.join(DATA_DIR, "flashcards.json")
PROGRESS_FILE = os.path.join(DATA_DIR, "progress.json")

os.makedirs(DATA_DIR, exist_ok=True)


# ─────────────────────────────────────────────
#  SPACED REPETITION (SM-2 Algorithm)
# ─────────────────────────────────────────────
def sm2_update(card_progress, quality: int) -> dict:
    """
    SM-2 spaced repetition algorithm.
    quality: 0-5 (0=complete blackout, 5=perfect recall)
    """
    n = card_progress.get("n", 0)
    ef = card_progress.get("ef", 2.5)
    interval = card_progress.get("interval", 1)

    if quality >= 3:
        if n == 0:
            interval = 1
        elif n == 1:
            interval = 6
        else:
            interval = round(interval * ef)
        n += 1
    else:
        n = 0
        interval = 1

    ef = ef + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    ef = max(1.3, ef)

    next_review = (datetime.now() + timedelta(days=interval)).isoformat()

    return {
        "n": n,
        "ef": round(ef, 4),
        "interval": interval,
        "next_review": next_review,
        "last_reviewed": datetime.now().isoformat(),
        "total_reviews": card_progress.get("total_reviews", 0) + 1,
        "correct": card_progress.get("correct", 0) + (1 if quality >= 3 else 0),
    }


def is_due(card_progress: dict) -> bool:
    """Check if a card is due for review."""
    next_review = card_progress.get("next_review")
    if not next_review:
        return True
    return datetime.now() >= datetime.fromisoformat(next_review)


# ─────────────────────────────────────────────
#  PERSISTENCE
# ─────────────────────────────────────────────
def load_cards() -> list:
    if not os.path.exists(CARDS_FILE):
        return get_default_cards()
    with open(CARDS_FILE, "r") as f:
        return json.load(f)


def save_cards(cards: list):
    with open(CARDS_FILE, "w") as f:
        json.dump(cards, f, indent=2)


def load_progress() -> dict:
    if not os.path.exists(PROGRESS_FILE):
        return {}
    with open(PROGRESS_FILE, "r") as f:
        return json.load(f)


def save_progress(progress: dict):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2)


# ─────────────────────────────────────────────
#  DEFAULT FLASHCARDS  (AI / ML topics)
# ─────────────────────────────────────────────
def get_default_cards() -> list:
    return [
        {
            "id": "1",
            "topic": "Machine Learning",
            "question": "What is supervised learning?",
            "answer": "A type of ML where the model is trained on labeled data — input-output pairs — so it can learn to map inputs to correct outputs.",
            "hint": "Think: teacher provides correct answers during training.",
        },
        {
            "id": "2",
            "topic": "Machine Learning",
            "question": "What is the difference between overfitting and underfitting?",
            "answer": "Overfitting: model learns training data too well, poor on new data. Underfitting: model is too simple, poor on both training and new data.",
            "hint": "Think about bias-variance tradeoff.",
        },
        {
            "id": "3",
            "topic": "Machine Learning",
            "question": "What is a confusion matrix?",
            "answer": "A table showing True Positives, True Negatives, False Positives, and False Negatives to evaluate classification model performance.",
            "hint": "2x2 table for binary classification.",
        },
        {
            "id": "4",
            "topic": "Neural Networks",
            "question": "What is an activation function and why is it needed?",
            "answer": "A function applied to a neuron's output to introduce non-linearity, allowing neural networks to learn complex patterns. Examples: ReLU, Sigmoid, Tanh.",
            "hint": "Without it, neural nets collapse into linear models.",
        },
        {
            "id": "5",
            "topic": "Neural Networks",
            "question": "What is backpropagation?",
            "answer": "An algorithm that calculates gradients of the loss function with respect to weights by propagating errors backwards through the network, enabling gradient descent.",
            "hint": "Chain rule applied layer by layer.",
        },
        {
            "id": "6",
            "topic": "Neural Networks",
            "question": "What is a Convolutional Neural Network (CNN)?",
            "answer": "A deep learning architecture that uses convolutional layers to automatically detect spatial features (edges, textures) from data like images.",
            "hint": "Mainly used for image tasks.",
        },
        {
            "id": "7",
            "topic": "AI Fundamentals",
            "question": "What is the Turing Test?",
            "answer": "A test proposed by Alan Turing where a machine is considered intelligent if a human judge cannot distinguish its responses from a human's in a text conversation.",
            "hint": "Proposed in 1950.",
        },
        {
            "id": "8",
            "topic": "AI Fundamentals",
            "question": "What is the difference between AI, ML, and Deep Learning?",
            "answer": "AI is the broad field of making machines intelligent. ML is a subset using data to learn. Deep Learning is a subset of ML using multi-layer neural networks.",
            "hint": "Think of nested circles.",
        },
        {
            "id": "9",
            "topic": "AI Fundamentals",
            "question": "What is a heuristic in AI?",
            "answer": "A practical approach or rule of thumb used to find a solution faster when an exact method is too slow. It trades off optimality for speed.",
            "hint": "Used in search algorithms like A*.",
        },
        {
            "id": "10",
            "topic": "Algorithms",
            "question": "What is gradient descent?",
            "answer": "An optimization algorithm that iteratively adjusts model parameters in the direction of the negative gradient of the loss function to minimize error.",
            "hint": "Like walking downhill to find the lowest point.",
        },
        {
            "id": "11",
            "topic": "Algorithms",
            "question": "What is the k-Nearest Neighbors (kNN) algorithm?",
            "answer": "A classification algorithm that predicts the label of a new point by finding the k closest training examples and taking a majority vote.",
            "hint": "No training phase — lazy learner.",
        },
        {
            "id": "12",
            "topic": "Algorithms",
            "question": "What is a decision tree?",
            "answer": "A tree-shaped model where each internal node is a feature test, each branch is a decision, and each leaf is a class label or output value.",
            "hint": "Like a flowchart for decisions.",
        },
        {
            "id": "13",
            "topic": "NLP",
            "question": "What is tokenization in NLP?",
            "answer": "The process of splitting text into individual units (tokens) such as words, subwords, or characters, as the first step in text processing.",
            "hint": "Splitting 'Hello world' → ['Hello', 'world'].",
        },
        {
            "id": "14",
            "topic": "NLP",
            "question": "What is TF-IDF?",
            "answer": "Term Frequency–Inverse Document Frequency. A numerical statistic reflecting how important a word is in a document relative to a collection of documents.",
            "hint": "Rare words get higher scores.",
        },
        {
            "id": "15",
            "topic": "Reinforcement Learning",
            "question": "What is reinforcement learning?",
            "answer": "An ML paradigm where an agent learns by interacting with an environment, receiving rewards or penalties, and maximizing cumulative reward over time.",
            "hint": "Like training a dog with treats.",
        },
    ]


# ─────────────────────────────────────────────
#  UI HELPERS
# ─────────────────────────────────────────────
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"


def clr(text, color):
    return f"{color}{text}{RESET}"


def divider(char="─", width=60):
    print(clr(char * width, DIM))


def header(title):
    print()
    divider("═")
    print(clr(f"  {title}", BOLD + CYAN))
    divider("═")
    print()


def pause(msg="Press Enter to continue..."):
    input(clr(f"\n  {msg}", DIM))


# ─────────────────────────────────────────────
#  QUIZ ENGINE
# ─────────────────────────────────────────────
def pick_cards_for_session(cards, progress, count=10):
    """
    Adaptive selection:
    1. Due cards first (spaced repetition)
    2. New cards next
    3. Fill rest randomly
    """
    due = []
    new_cards = []
    others = []

    for card in cards:
        cid = card["id"]
        if cid not in progress:
            new_cards.append(card)
        elif is_due(progress[cid]):
            due.append(card)
        else:
            others.append(card)

    random.shuffle(new_cards)
    random.shuffle(others)

    selected = due[:count]
    remaining = count - len(selected)
    selected += new_cards[:remaining]
    remaining = count - len(selected)
    selected += others[:remaining]

    random.shuffle(selected)
    return selected[:count]


def run_quiz(cards, progress):
    """Run an interactive quiz session."""
    session_cards = pick_cards_for_session(cards, progress)

    if not session_cards:
        print(clr("  No cards available for review!", YELLOW))
        return progress

    header(f"📚 Quiz Session  —  {len(session_cards)} cards")
    print(clr("  Rate your answer: 0=No idea  1=Wrong  2=Close  3=Hard  4=Good  5=Easy\n", DIM))

    session_correct = 0
    session_total = len(session_cards)

    for i, card in enumerate(session_cards, 1):
        cid = card["id"]
        card_prog = progress.get(cid, {})

        # Show question
        print(clr(f"  [{i}/{session_total}]  Topic: {card['topic']}", DIM))
        divider()
        print(f"\n  {clr('Q:', BOLD + YELLOW)}  {card['question']}\n")

        # Hint option
        hint_used = False
        user_input = input(clr("  Press Enter to reveal answer, or type 'hint': ", CYAN)).strip().lower()
        if user_input == "hint":
            print(clr(f"\n  💡 Hint: {card['hint']}", YELLOW))
            hint_used = True
            input(clr("  Press Enter to reveal answer...", DIM))

        # Show answer
        print(f"\n  {clr('A:', BOLD + GREEN)}  {card['answer']}\n")
        divider()

        # Self-rating
        while True:
            try:
                rating_str = input(clr("  How well did you know this? (0-5): ", CYAN)).strip()
                rating = int(rating_str)
                if 0 <= rating <= 5:
                    break
                print(clr("  Enter a number between 0 and 5.", RED))
            except ValueError:
                print(clr("  Please enter a valid number (0-5).", RED))

        # Penalize slightly for hint use
        effective_rating = max(0, rating - 1) if hint_used else rating
        progress[cid] = sm2_update(card_prog, effective_rating)

        if rating >= 3:
            session_correct += 1
            print(clr("  ✓ Marked as known!", GREEN))
        else:
            print(clr("  ✗ Will review again soon.", RED))

        next_rev = progress[cid]["interval"]
        print(clr(f"  Next review in: {next_rev} day(s)\n", DIM))

    # Session summary
    header("📊 Session Summary")
    pct = round((session_correct / session_total) * 100)
    bar_filled = int(pct / 5)
    bar = "█" * bar_filled + "░" * (20 - bar_filled)
    print(f"  Score:    {clr(f'{session_correct}/{session_total}', BOLD)}  ({pct}%)")
    print(f"  Progress: {clr(bar, GREEN if pct >= 70 else YELLOW if pct >= 40 else RED)}")
    print()

    if pct >= 80:
        print(clr("  🔥 Excellent session! Keep it up!", GREEN + BOLD))
    elif pct >= 50:
        print(clr("  👍 Good effort! Review weak cards again.", YELLOW))
    else:
        print(clr("  📖 Keep studying — you'll get there!", CYAN))

    save_progress(progress)
    pause()
    return progress


# ─────────────────────────────────────────────
#  STATS VIEW
# ─────────────────────────────────────────────
def view_stats(cards, progress):
    header("📈 Learning Statistics")

    if not progress:
        print(clr("  No progress data yet. Complete a quiz first!\n", YELLOW))
        pause()
        return

    total = len(cards)
    reviewed = len(progress)
    never = total - reviewed
    due_now = sum(1 for cid, p in progress.items() if is_due(p))

    total_reviews = sum(p.get("total_reviews", 0) for p in progress.values())
    total_correct = sum(p.get("correct", 0) for p in progress.values())
    accuracy = round((total_correct / total_reviews) * 100) if total_reviews > 0 else 0

    print(f"  {'Total cards:':<25} {clr(str(total), BOLD)}")
    print(f"  {'Cards reviewed:':<25} {clr(str(reviewed), BOLD + GREEN)}")
    print(f"  {'Never reviewed:':<25} {clr(str(never), BOLD + YELLOW)}")
    print(f"  {'Due for review now:':<25} {clr(str(due_now), BOLD + RED)}")
    print(f"  {'Total reviews done:':<25} {clr(str(total_reviews), BOLD)}")
    print(f"  {'Overall accuracy:':<25} {clr(f'{accuracy}%', BOLD + (GREEN if accuracy >= 70 else YELLOW))}")

    # Per-topic breakdown
    print()
    divider()
    print(clr("  Per-Topic Breakdown:", BOLD))
    divider()

    topics = {}
    for card in cards:
        t = card["topic"]
        cid = card["id"]
        if t not in topics:
            topics[t] = {"total": 0, "reviewed": 0, "correct": 0, "reviews": 0}
        topics[t]["total"] += 1
        if cid in progress:
            p = progress[cid]
            topics[t]["reviewed"] += 1
            topics[t]["correct"] += p.get("correct", 0)
            topics[t]["reviews"] += p.get("total_reviews", 0)

    for topic, data in sorted(topics.items()):
        acc = round((data["correct"] / data["reviews"]) * 100) if data["reviews"] > 0 else 0
        bar = "█" * int(acc / 10) + "░" * (10 - int(acc / 10))
        color = GREEN if acc >= 70 else YELLOW if acc >= 40 else RED
        print(f"  {topic:<22} {clr(bar, color)}  {acc}%  ({data['reviewed']}/{data['total']} cards)")

    print()
    pause()


# ─────────────────────────────────────────────
#  MANAGE CARDS
# ─────────────────────────────────────────────
def add_card(cards):
    header("➕ Add New Flashcard")
    topic = input(clr("  Topic: ", CYAN)).strip()
    if not topic:
        print(clr("  Topic cannot be empty.", RED))
        pause()
        return cards

    question = input(clr("  Question: ", CYAN)).strip()
    if not question:
        print(clr("  Question cannot be empty.", RED))
        pause()
        return cards

    answer = input(clr("  Answer: ", CYAN)).strip()
    if not answer:
        print(clr("  Answer cannot be empty.", RED))
        pause()
        return cards

    hint = input(clr("  Hint (optional): ", CYAN)).strip()

    new_id = str(max(int(c["id"]) for c in cards) + 1) if cards else "1"
    cards.append({
        "id": new_id,
        "topic": topic,
        "question": question,
        "answer": answer,
        "hint": hint or "No hint available.",
    })
    save_cards(cards)
    print(clr(f"\n  ✓ Card added! (ID: {new_id})", GREEN))
    pause()
    return cards


def list_cards(cards, progress):
    header("📋 All Flashcards")
    topics = sorted(set(c["topic"] for c in cards))

    for topic in topics:
        print(clr(f"  ── {topic} ──", BOLD + CYAN))
        for card in cards:
            if card["topic"] != topic:
                continue
            cid = card["id"]
            p = progress.get(cid, {})
            if not p:
                status = clr("NEW", YELLOW)
            elif is_due(p):
                status = clr("DUE", RED)
            else:
                days = p.get("interval", 1)
                status = clr(f"in {days}d", GREEN)

            print(f"    [{clr(cid, DIM)}] {card['question'][:55]:<55}  {status}")
        print()

    pause()


def delete_card(cards, progress):
    header("🗑  Delete Flashcard")
    card_id = input(clr("  Enter card ID to delete: ", CYAN)).strip()
    match = next((c for c in cards if c["id"] == card_id), None)
    if not match:
        print(clr("  Card not found.", RED))
        pause()
        return cards, progress

    confirm = input(clr(f"  Delete card: '{match['question'][:50]}'? (y/n): ", YELLOW)).strip().lower()
    if confirm == "y":
        cards = [c for c in cards if c["id"] != card_id]
        progress.pop(card_id, None)
        save_cards(cards)
        save_progress(progress)
        print(clr("  ✓ Card deleted.", GREEN))
    else:
        print(clr("  Cancelled.", DIM))
    pause()
    return cards, progress


def reset_progress(progress):
    header("🔄 Reset Progress")
    confirm = input(clr("  Reset ALL progress? This cannot be undone. (yes/no): ", RED)).strip().lower()
    if confirm == "yes":
        progress = {}
        save_progress(progress)
        print(clr("  ✓ Progress reset.", GREEN))
    else:
        print(clr("  Cancelled.", DIM))
    pause()
    return progress


# ─────────────────────────────────────────────
#  HELP
# ─────────────────────────────────────────────
def show_help():
    header("❓ Help")
    rows = [
        ("1. Start Quiz",       "Begin an adaptive quiz session"),
        ("2. View Stats",       "See your learning progress & accuracy"),
        ("3. List Cards",       "Browse all flashcards with their status"),
        ("4. Add Card",         "Create a new flashcard"),
        ("5. Delete Card",      "Remove a flashcard by ID"),
        ("6. Reset Progress",   "Clear all spaced-repetition data"),
        ("7. Help",             "Show this help screen"),
        ("8. Exit",             "Quit the application"),
    ]
    for cmd, desc in rows:
        print(f"  {clr(cmd, BOLD + CYAN):<30}  {desc}")
    print()
    print(clr("  About Adaptive Learning:", BOLD))
    print("  Cards you struggle with appear more often.")
    print("  Cards you know well are shown less frequently.")
    print("  This uses the SM-2 spaced repetition algorithm.")
    print()
    pause()


# ─────────────────────────────────────────────
#  MAIN MENU
# ─────────────────────────────────────────────
def main_menu(cards, progress):
    due_count = sum(1 for cid, p in progress.items() if is_due(p))
    new_count = sum(1 for c in cards if c["id"] not in progress)

    print()
    divider("═")
    print(clr("  🧠  AI Study Flashcard Quiz", BOLD + CYAN))
    print(clr("       Adaptive Spaced Repetition", DIM))
    divider("═")
    print(f"  Cards due:  {clr(str(due_count), RED + BOLD)}   New: {clr(str(new_count), YELLOW + BOLD)}   Total: {clr(str(len(cards)), BOLD)}")
    divider()
    options = [
        ("1", "Start Quiz"),
        ("2", "View Stats"),
        ("3", "List All Cards"),
        ("4", "Add Card"),
        ("5", "Delete Card"),
        ("6", "Reset Progress"),
        ("7", "Help"),
        ("8", "Exit"),
    ]
    for num, label in options:
        print(f"  {clr(num, BOLD + CYAN)}.  {label}")
    divider()
    return input(clr("  Enter choice: ", CYAN)).strip()


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
def main():
    os.system("clear" if os.name == "posix" else "cls")

    print(clr("""
  ╔══════════════════════════════════════════════╗
  ║   🧠  AI Study Flashcard Quiz               ║
  ║       Adaptive Learning with Spaced Reps    ║
  ╚══════════════════════════════════════════════╝
    """, CYAN + BOLD))
    print(clr("  Loading flashcards...", DIM))
    time.sleep(0.6)

    cards = load_cards()
    if not os.path.exists(CARDS_FILE):
        save_cards(cards)

    progress = load_progress()

    while True:
        choice = main_menu(cards, progress)

        if choice == "1":
            progress = run_quiz(cards, progress)
        elif choice == "2":
            view_stats(cards, progress)
        elif choice == "3":
            list_cards(cards, progress)
        elif choice == "4":
            cards = add_card(cards)
        elif choice == "5":
            cards, progress = delete_card(cards, progress)
        elif choice == "6":
            progress = reset_progress(progress)
        elif choice == "7":
            show_help()
        elif choice == "8":
            print(clr("\n  👋 Goodbye! Keep studying!\n", CYAN + BOLD))
            break
        else:
            print(clr("  ⚠  Invalid choice. Enter 1–8.", RED))
            time.sleep(0.8)


if __name__ == "__main__":
    main()
