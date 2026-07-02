# AI 4 Africa Workshop Starter Repo
Emmanuel

good food  here in ala
ddfd

<p align="center">
  <a href="https://github.com/AI4Africa-MBZUAI-ALA/github_tutorial/fork">
    <img src="https://img.shields.io/badge/Fork%20this%20repo-Start%20here-brightgreen?style=for-the-badge" alt="Fork this repo" />
  </a>
</p>

🚀 Welcome to the starter repo for the AI 4 Africa workshop.

This repository is designed for beginners. It teaches collaboration first and
machine learning second.

The workshop theme is aligned with the AI for Africa Bootcamp and the amazing guidance of Keisha Jemane to shape these young minds 2026 vision
AI for sustainability and agriculture in Africa. The project uses a **fully
synthetic, controlled story** so every group works from the same starting point
without needing any external dataset.

## 🌍 Project Story

Students will build a tiny pipeline for a fictional **school garden / community
farm helper** app.

The goal is to predict whether a garden plot needs:

- `low` water
- `medium` water
- `high` water

The input features stay simple and relatable:

- weather
- temperature
- soil moisture
- rainfall
- crop type
- day of week

That makes the project easy to understand while still feeling real.

## 🤝 How The GitHub Workflow Works

1. Every student creates their own GitHub account.
2. One person per group forks this repository.
3. That person adds the other group members as collaborators to the fork.
4. Each person owns one file and builds one step of the pipeline.
5. If a group has fewer people, whoever finishes early can start the next file.

This is the collaboration pattern we want students to practice:

- one fork per group
- one owner per file
- one shared pipeline at the end

## 🧩 Repo Structure

The workshop files live in `to_complete/` and are numbered so students can
identify them quickly.

- `to_complete/01_data_fetch.py` - create or load the synthetic raw records
- `to_complete/02_preprocess.py` - clean the records and split them into train/test sets
- `to_complete/03_train.py` - train a simple model
- `to_complete/04_evaluate.py` - score the model and create metrics
- `to_complete/05_visualize.py` - build plots and save them to disk
- `to_complete/06_streamlit_app.py` - prepare the interactive dashboard payload

`main.py` connects everything and reports which step is missing, stubbed, or
broken.

## ✅ Rules For The Files

- Keep the function name exactly as written in the file.
- Keep the input type and output shape exactly as documented.
- Do not change the data contract between files.
- If the step is not finished yet, leave the `NotImplementedError` in place.
- Start small. Make the simplest version work first.

## 🛠️ Setup

Before coding, every group should create a virtual environment.

Always work inside that virtual environment. Do not skip it.

Why this matters:

- it keeps the workshop tools separate from your computer’s global Python
- it makes the project easier to share and reproduce
- it helps everyone use the same package versions

Create and activate a virtual environment with `venv`.

Mac or Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If your terminal uses a different shell, use the equivalent activation command
for that shell.

Every time you add a package, update `requirements.txt`.

Always update `requirements.txt` whenever you add a new library.

Why this matters:

- `requirements.txt` is the shopping list for the project
- it tells other people what packages they need to install
- it helps the forked repos stay in sync

Example:

```bash
pip install -r requirements.txt
```

At minimum, keep `requirements.txt` up to date whenever the code needs a new
package.

If `pip` does not work on your computer, use `python -m pip` instead:

```bash
python -m pip install -r requirements.txt
```

For a single package, the same idea works:

```bash
python -m pip install pandas
```

This project expects you to create the virtual environment first, then install
the required packages, and only then start vibecoding.

## 📝 Notes For Claude

When Claude helps generate or revise code for this repo, keep these reminders
in mind:

- Always assume the student is working inside the `venv`.
- Keep the model simple, but avoid pure lookup-table solutions.
- Prefer a small real model when possible, like a basic regression model or a
  tiny neural network.
- If new libraries are used, update `requirements.txt` right away.
- When the work is finished, include the Streamlit check command so the app can
  be tested locally.

Example final app check:

```bash
streamlit run to_complete/06_streamlit_app.py
```

## 🔁 Suggested Group Flow

If the group has 6 people:

1. One person builds `to_complete/01_data_fetch.py`
2. One person builds `to_complete/02_preprocess.py`
3. One person builds `to_complete/03_train.py`
4. One person builds `to_complete/04_evaluate.py`
5. One person builds `to_complete/05_visualize.py`
6. One person builds `to_complete/06_streamlit_app.py`

If the group has 4 people:

- build the first 4 files first
- once someone finishes, they can help with visualization or Streamlit

## 🧪 Running The Demo

Once the files are implemented, run:

```bash
python main.py
```

If a step is still missing, `main.py` will tell you which one.

If the first run does not work, ask Claude for help and feedback.

- Ask: "Why is this not working?"
- Do not only ask: "Fix it."
- Use the explanation to understand the problem before changing the code.

## 👥 Workshop Inspiration

This starter is inspired by the AI for Africa Bootcamp 2026 and its mission to
connect AI with sustainability and agriculture in Africa.

## 🤝 Partners

<p align="center">
  <img src="assets/mbzuai-brand-logo.svg" alt="MBZUAI logo" height="80" />
  <img src="assets/ala-logo-horizontal.png" alt="African Leadership Academy logo" height="80" />
</p>

<p align="center">
  <strong>MBZUAI</strong> · <strong>African Leadership Academy</strong>
</p>

## 🔗 Official Site

- https://ai4africamp.com/
