#  AI Study Flashcard Quiz — Adaptive Learning CLI

A command-line flashcard quiz application that uses **AI-powered adaptive learning** via the **SM-2 Spaced Repetition Algorithm** to help you study smarter. Cards you struggle with appear more often; cards you know well are shown less frequently.

Built for the *Fundamentals of AI and ML (CSA2001)* course project.

---

##  Features

- **Adaptive Quiz Engine** — SM-2 spaced repetition algorithm schedules reviews based on your confidence ratings
- **Self-Rating System** — Rate your recall (0–5) after each card; the algorithm adjusts intervals accordingly
- **15 Built-in AI/ML Cards** — Topics: Machine Learning, Neural Networks, NLP, Algorithms, Reinforcement Learning, AI Fundamentals
- **Hint System** — Ask for a hint (with a small score penalty)
- **Per-topic Statistics** — Visual accuracy bars per topic
- **Full CRUD** — Add, list, and delete your own custom flashcards
- **Data Persistence** — Progress and cards saved to JSON files
- **Clean Terminal UI** — Colored output, progress bars, session summaries

---

##  Requirements

- Python **3.7+** (no external libraries required — uses only the standard library)

Check your Python version:
```bash
python3 --version
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/ai-flashcard-quiz.git
cd ai-flashcard-quiz
```

### 2. (Optional) Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. No dependencies to install!
This project uses only Python's built-in standard library (`json`, `os`, `random`, `time`, `math`, `datetime`).

---

##  Running the Application

```bash
python3 main.py
```

On Windows:
```bash
python main.py
```

---

##  How to Use

When the app launches, you'll see the main menu:

```
╔══════════════════════════════════════════════╗
║        AI Study Flashcard Quiz               ║
║        Adaptive Learning with Spaced Reps    ║
╚══════════════════════════════════════════════╝

  1.  Start Quiz
  2.  View Stats
  3.  List All Cards
  4.  Add Card
  5.  Delete Card
  6.  Reset Progress
  7.  Help
  8.  Exit
```

### Starting a Quiz
- Select **1** to begin
- A card's question is shown — press **Enter** to reveal the answer
- Type `hint` before revealing to get a clue (small penalty applied)
- Rate your recall from **0 (no idea)** to **5 (perfect)**
- The algorithm schedules the next review automatically

### Rating Guide
| Rating | Meaning |
|--------|---------|
| 0 | Complete blackout — no idea |
| 1 | Wrong answer but recalled on seeing it |
| 2 | Wrong but close |
| 3 | Correct but difficult |
| 4 | Correct after slight hesitation |
| 5 | Perfect recall |

### Adding Your Own Cards
- Select **4** from the menu
- Enter topic, question, answer, and optional hint
- Cards are saved to `data/flashcards.json`

---

##  Project Structure

```
ai-flashcard-quiz/
├── main.py              # Main CLI application
├── README.md            # This file
└── data/                # Auto-created on first run
    ├── flashcards.json  # Card database
    └── progress.json    # User progress & spaced repetition state
```

---

##  AI Concept: SM-2 Spaced Repetition

The SM-2 algorithm (SuperMemo 2) is a well-known algorithm in AI-assisted learning:

1. Each card has an **easiness factor (EF)** starting at 2.5
2. After each review, EF is updated based on recall quality
3. The **review interval** (days until next review) grows for well-known cards
4. Poorly recalled cards are reset to short intervals (1 day)

This mimics how human memory works — reinforcing information just before it's forgotten, which is proven to maximize retention.

---

##  Data Storage

All data is stored locally in JSON format:
- `data/flashcards.json` — Your card library
- `data/progress.json` — Per-card SM-2 state (interval, easiness factor, review history)

---

##  Course

**Fundamentals of AI and ML — CSA2001**  
Vellore Institute of Technology

---

##  License

MIT License — free to use and modify.
