
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import os

# Import the rule-based detector from the project
from rule_based_detector import RuleBasedDetector

app = Flask(__name__)
CORS(app)  # allow the frontend to talk to this backend from any origin

detector = RuleBasedDetector()

# In-memory store for "recent detections" so the UI can show something
RECENT = [
    {
        "risk_level": "high",
        "title": "WhatsApp tip promising 'Guaranteed 50% in 7 days'",
        "summary": "Contained urgency and guaranteed returns keywords.",
        "time_ago": "2 hours ago"
    },
    {
        "risk_level": "medium",
        "title": "New website sharing 'secret stock tips'",
        "summary": "Suspicious wording and very new domain.",
        "time_ago": "yesterday"
    }
]

@app.route('/api/analyze/text', methods=['POST'])
def analyze_text():
    try:
        data = request.get_json(force=True) or {}
        text = data.get('text', '')
        source_platform = data.get('source_platform', '')  # e.g., whatsapp/telegram/twitter
        content_type = data.get('content_type', '')        # e.g., investment_advice/advertisement

        result = detector.analyze_text(text=text, source_platform=source_platform, content_type=content_type)

        # Add to RECENT for the dashboard
        RECENT.insert(0, {
            "risk_level": result.get("risk_level", "low"),
            "title": f"Text scan from {source_platform or 'unknown source'}",
            "summary": (result.get("recommendation") or "Scanned text."),
            "time_ago": "just now"
        })
        # cap the list
        if len(RECENT) > 20:
            RECENT.pop()

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/analyze/url', methods=['POST'])
def analyze_url():
    try:
        data = request.get_json(force=True) or {}
        url = data.get('url', '')
        result = detector.analyze_url(url)

        RECENT.insert(0, {
            "risk_level": result.get("risk_level", "low"),
            "title": f"URL scan: {url}",
            "summary": "URL was analyzed for suspicious patterns and domain risk.",
            "time_ago": "just now"
        })
        if len(RECENT) > 20:
            RECENT.pop()

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/fraud-types', methods=['GET'])
def fraud_types():
    # Map a few common types to icons expected by the UI (Font Awesome classes)
    data = [
        {"name": "Guaranteed Returns", "icon": "fas fa-certificate", "count": 18},
        {"name": "Pump & Dump", "icon": "fas fa-bullhorn", "count": 11},
        {"name": "Insider Tips", "icon": "fas fa-user-secret", "count": 9},
        {"name": "Penny Stock Hype", "icon": "fas fa-coins", "count": 7},
        {"name": "New Domain Scam", "icon": "fas fa-globe", "count": 6},
        {"name": "Celebrity Endorsement", "icon": "fas fa-star", "count": 5},
    ]
    return jsonify(data), 200

@app.route('/api/recent-detections', methods=['GET'])
def recent_detections():
    return jsonify(RECENT), 200

@app.route('/api/dashboard', methods=['GET'])
def dashboard():
    # Very simple fake stats so the UI doesn't break
    total = max(10, len(RECENT) + 10)
    high = sum(1 for r in RECENT if r["risk_level"] == "high")
    medium = sum(1 for r in RECENT if r["risk_level"] == "medium")
    low = sum(1 for r in RECENT if r["risk_level"] == "low")

    # Convert to percentages
    def pct(x): 
        return int(round((x / total) * 100)) if total else 0

    data = {
        "total_scans": total,
        "legitimate_percent": pct(low),
        "suspicious_percent": pct(medium),
        "fraudulent_percent": pct(high),
    }
    return jsonify(data), 200

if __name__ == "__main__":
    # Run on port 8000 to match the frontend's API_BASE_URL
    app.run(host="0.0.0.0", port=8000, debug=True)
