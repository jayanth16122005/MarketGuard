MarketGuard Lite - Fraud Detection System

MarketGuard Lite is a comprehensive fraud detection system designed to identify and prevent securities market fraud. It analyzes text content, URLs, and financial advisor credentials to detect potential fraudulent activities in investment communications.

✨ Features

Text Analysis → Scans social media posts, emails, and announcements for fraud indicators

URL Analysis → Examines websites and links for known fraudulent patterns

Advisor Verification → Checks financial advisor credentials against regulatory databases

Real-time Detection → Provides instant risk assessment with detailed indicators

Interactive Dashboard → Visualizes detection statistics and historical data

Regulatory Reporting → Facilitates reporting of suspicious activities to authorities

🛠 Technology Stack
Frontend

HTML5, CSS3, JavaScript (ES6+)

Bootstrap 5 (responsive UI)

Chart.js (data visualization)

Font Awesome (icons)

Backend

Python 3.8+

Flask web framework

Rule-based detection engine

RESTful API architecture

🚀 Installation
Prerequisites

Python 3.8+

pip (Python package manager)

A modern web browser (Chrome, Firefox, Safari, Edge)

Backend Setup
# Clone repository
git clone https://github.com/your-username/marketguard-lite.git
cd marketguard-lite

# Create virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run Flask app
python app.py


Backend runs at 👉 http://localhost:8000

Frontend Setup
cd frontend

# Open index.html directly OR run local server
python -m http.server 8080


Frontend runs at 👉 http://localhost:8080

📖 Usage
🔹 Text Analysis

Select Text Analysis tab

Paste suspicious content

Select platform + content type

Click Analyze for Fraud Indicators

🔹 URL Analysis

Select URL Analysis tab

Enter URL

Click Analyze URL

🔹 Advisor Verification

Select Advisor Check tab

Enter advisor name / registration number

Click Verify Advisor

📡 API Endpoints
Text Analysis
POST /api/analyze/text


Params:

text (string)

source_platform (string)

content_type (string)

Response: Risk score, indicators, recommendations

URL Analysis
POST /api/analyze/url


Params: url (string)
Response: Domain risk assessment

Advisor Verification
POST /api/check-advisor


Params: name (string, optional), registration_number (string, optional)
Response: Registration status, legitimacy assessment

Dashboard
GET /api/dashboard


Response: System statistics

🔎 Detection Methodology

Fraud Indicators: urgency language, unrealistic returns, fake endorsements, grammar errors, unregulated entities

Legitimacy Indicators: proper disclosures, registration mentions, legitimate contact info

Risk Scoring: weighted indicators + platform/content modifiers + historical patterns

📂 Project Structure
marketguard_lite/
├── README.md
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── rule_based_detector.py
│   └── config.py
├── data/
│   ├── regulatory_db.csv
│   ├── social_posts.jsonl
│   ├── ticks.csv
│   └── whois_mock.csv
├── frontend/
│   └── index.html
├── scripts/
│   └── run_uvicorn.sh
└── train/
    ├── train_dataset.csv
    └── train_model.py

⚙️ Customization

Add new fraud patterns → edit rule_based_detector.py

Modify risk weights → update patterns dictionary

Integrate regulatory APIs → extend advisor verification logic

🧪 Testing
python -m pytest tests/

🤝 Contributing

Fork repo

Create feature branch → git checkout -b feature/amazing-feature

Commit → git commit -m "Add amazing feature"

Push → git push origin feature/amazing-feature

Open a Pull Request

📜 License

MIT License – see LICENSE

⚠️ Disclaimer

This project is for educational purposes only. Do not rely on it as the sole means of detecting financial fraud. Always verify with official regulatory sources before making investment decisions.

🙏 Acknowledgments

SEBI (Securities and Exchange Board of India) for regulatory frameworks

Financial fraud research community

Open-source contributors to Python & web development ecosystem
