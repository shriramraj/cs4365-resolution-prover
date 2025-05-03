# CS 4365: Resolution-Based Theorem Prover

This project implements a resolution-based theorem prover for clause logic, as part of Assignment 3 for CS 4365: Artificial Intelligence.

## 🔧 Features

- Parses input clauses from a text file using disjunctive form.
- Applies the resolution principle to determine clause validity.
- Supports proof by contradiction via resolution until `False` is deduced.
- Outputs proof trace and size of final clause set.

## 📁 Files

- `main.py` – Entry point for running the resolution prover.
- `facts.txt` – Contains base knowledge (initial valid clauses).
- `task1.in`, `task2.in`, `task3.in` – Test inputs for clause validity checking.

## 📜 Usage

```bash
python3 main.py facts.txt task1.in
