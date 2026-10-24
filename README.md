# PythonHelperAI Learning Lab

A beginner-to-intermediate Python and data structures tutor built with Tkinter.

## Project goal
This project is designed for absolute beginners. It teaches students by guiding them with questions, short explanations, and hints instead of giving away full solutions.

The system supports:
- local Ollama models for low-end machines
- Azure OpenAI for stronger demo environments
- chapter-based learning
- milestone tests after chapters 1, 3, 5, 7, and a final test in chapter 10
- beginner-focused guidance inspired by the CS50 Duck teaching style

## Core idea
Students should learn by doing:
- read a short chapter overview
- explore the concept with examples
- solve a few exercises
- ask for a hint from the AI tutor
- retry until they understand the idea
- complete chapter tests at milestone points

## Supported modes
### Local mode
- runs with Ollama
- good for testing on weak machines
- default low-end models include gemma3:1b and gemma3:2b

### Cloud mode
- Azure OpenAI fallback for better demo quality
- best when the student environment supports a strong model

## Learn by progression
The curriculum is structured as a 10-chapter path:
1. Python basics
2. Operators and expressions
3. Conditionals
4. Loops
5. Functions
6. Strings and lists
7. Dictionaries and sets
8. Intermediate Python
9. Intro to DSA
10. DSA practice and final test

## Setup

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run the app
```bash
python app.py
```

### Local model example
```bash
ollama pull gemma3:1b
```

### Azure setup
Set the environment variables before using cloud mode:
```bash
export AZURE_OPENAI_API_KEY="..."
export AZURE_OPENAI_ENDPOINT="https://<resource>.openai.azure.com/"
export AZURE_OPENAI_DEPLOYMENT="gpt-4o-mini"
```

## Important note
This project is still being built in phases. The current repo contains the beginning of the teaching app, its chapter structure, and the tutor infrastructure needed for future checkpoint and DSA progression.
