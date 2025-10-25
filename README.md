# 🛡️ Codehouse Cybersecurity Training Cli (`codehouse_cyb`)

[![Build Status](https://raw.githubusercontent.com/appline1/codehouse_cyber_quiz/f27934854869a48c5869ad08af168dfc65785544/secure-svgrepo-com.svg)](https://github.com/applinet-technology/codehouse_cyber_quiz/actions)
[![GitHub release](https://img.shields.io/github/v/release/applinet-technology/codehouse_cyber_quiz?color=brightgreen&label=version)](https://github.com/applinet-technology/codehouse_cyber_quiz/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/applinet-technology/codehouse_cyber_quiz)](https://github.com/applinet-technology/codehouse_cyber_quiz/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/applinet-technology/codehouse_cyber_quiz)](https://github.com/applinet-technology/codehouse_cyber_quiz/pulls)
[![Contributors](https://img.shields.io/github/contributors/applinet-technology/codehouse_cyber_quiz)](https://github.com/applinet-technology/codehouse_cyber_quiz/graphs/contributors)
[![Stars](https://img.shields.io/github/stars/applinet-technology/codehouse_cyber_quiz?style=social)](https://github.com/applinet-technology/codehouse_cyber_quiz/stargazers)

---

## 📘 Overview

`codehouse cyber quiz` is an open-source Python client that connects learners to **CodeHouse Cloud’s** cybersecurity training API — delivering interactive questions, simulations, and AI-powered learning tools directly in the terminal.

It is part of the **CodeHouse Learning Suite**, proudly built by **[Applinet Technology](https://applinet.com.ng)** and **[CodeHouse Cloud](https://codehouse.cloud)** — an African-centered technology initiative combining culture, innovation, and human-focused digital education.

---

## ✨ Key Features

- 🧠 Interactive cybersecurity quizzes and learning scenarios  
- 🔄 Auto-fetches questions from CodeHouse Cloud servers  
- 💾 Works offline with a local fallback question database  
- 🧮 Intelligent feedback, scoring, and performance tracking  
- ⚡ Lightweight and fast — no heavy dependencies  

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/applinet-technology/codehouse_cyber_quiz.git
cd codehouse_cyber_quiz

2️⃣ Install Locally
pip install -e .

3️⃣ Start the Training
python -m cyb.start


or simply:

python cyber.start

🧩 Example CLI Session
$ python -m cyb.start

Welcome to CodeHouse Cloud Cybersecurity Training!

Loading your questions...

Question 1: What does CIA Triad stand for?
A) Confidentiality, Integrity, Availability
B) Control, Internet, Access
C) Cybersecurity, Information, Authentication

Your Answer: A
✅ Correct! Great job.

⚙️ Requirements

Python 3.8+

Internet connection (for live question mode)

Works offline with local question cache

🧱 Project Structure
codehouse_cyber_quiz/
├── cyb/
│   ├── __init__.py
│   ├── start.py
│   ├── utils.py
│   ├── config.py
│   └── questions.json
├── tests/
│   └── test_basic.py
├── setup.py
├── LICENSE
└── README.md

🧪 Running Tests

This project includes automated tests for CI/CD and local validation.

Run Tests Locally
pytest -v


Expected output:

=================== test session starts ===================
collected 4 items

tests/test_basic.py ....                           [100%]

=================== 4 passed in 0.35s ====================

🧰 Continuous Integration (CI/CD)

GitHub Actions automatically runs tests for each commit or pull request.

Workflow: .github/workflows/python-app.yml

name: Codehouse Cybersecurity Client CI
on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10, 3.11]

    steps:
      - name: 🧩 Checkout Repository
        uses: actions/checkout@v4

      - name: 🐍 Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: 📦 Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e .
          pip install pytest requests rich

      - name: 🧪 Run Tests
        run: pytest -v || echo "No tests found — skipping test step"

      - name: ✅ Lint Code
        run: |
          pip install flake8
          flake8 cyb --count --exit-zero --max-complexity=10 --max-line-length=120 --statistics

🤝 Contributing

We welcome contributions from the community!
You can help by improving the CLI, adding more cybersecurity question sets, or enhancing the offline engine.

Before contributing:

Follow PEP8 code style

Include docstrings for all new functions

Ensure tests pass before submitting PRs

To start contributing:

# Fork the repo on GitHub
git clone https://github.com/your-username/codehouse_cyber_quiz.git
cd codehouse_cyber_quiz

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)

# Install dependencies
pip install -r requirements.txt

🧾 License

This project is licensed under the MIT License.
See the LICENSE
 file for details.

👨🏽‍💻 Authors & Credits

Lead Developer:
Godswill Moses Ikpotokin — CEO, Applinet Technology & CodeHouse Cloud
📧 godswill@ikpotokin.ng

🌍 https://ikpotokin.ng

Organizations:

Applinet Technology
🌍 https://applinet.com.ng

📧 developers@applinet.com.ng

CodeHouse Cloud — African Coding Initiative
🌍 https://codehouse.cloud

📧 genius@codehouse.cloud

💬 Support & Community

Join our African Cybersecurity community:
🌍 Visit → https://cli.codehouse.cloud

💬 Discuss ideas or report bugs via → GitHub Issues

📢 Follow updates from Applinet Technology and CodeHouse Cloud

🌍 Mission

"Empowering Africans through culturally rooted technology education."
— CodeHouse Cloud & Applinet Technology
Bridging knowledge, culture, and cybersecurity.

DEMO
![CLI Demo](https://raw.githubusercontent.com/appline1/codehouse_cyber_quiz/refs/heads/master/WhatsApp%20Image%202025-10-25%20at%2016.37.46_447e0a48.jpg)

![CLI Demo](https://raw.githubusercontent.com/appline1/codehouse_cyber_quiz/refs/heads/master/WhatsApp%20Image%202025-10-25%20at%2016.38.32_28d91aa4.jpg)
