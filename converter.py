"""
Use the converter by passing the files to convert as args.

Examples:
python converter.py ./categories/animals
python converter.py ./categories/*

Outputs json in the following format:
[
    {
        "question": "Three of these animals hibernate. Which one does not?",
        "category": "animals",
        "answer": "Sloth",
        "choices": [
            "Mouse",
            "Sloth",
            "Frog",
            "Snake"
        ]
    }
]
"""


import json
import os
import string
import sys

ALPHABET = list(string.ascii_uppercase)

for file in sys.argv[1:]:
    if os.path.isdir(file):
        print(f"{file} is a directory. Skipping.")
        continue

    print(file)
    with open(file, "r", encoding='ISO-8859-1') as f:
        lines = f.readlines()

    questions = []
    question = {}
    for line in lines:
        if line.startswith("#Q "):
            question["question"] = line[3:-1]
            question["category"] = os.path.basename(file)

        elif line.startswith("^ "):
            question["answer"] = line[2:-1]

        elif line[0] in ALPHABET:
            if not question.get("choices"):
                question["choices"] = []

            question["choices"].append(line[2:-1])

        elif line.strip() == "" and question != {}:
            questions.append(question)
            question = {}

    with open(f"{file}.json", "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=4)
