from flask import Flask, request, jsonify
from flask_cors import CORS
from rule_based_detector import RuleBasedDetector
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the detector
detector = RuleBasedDetector()

# In-memory storage for demo purposes (in production, use a database)
detection_history = []
stats = {
    "total_scans": 0,
    "legitimate_count": 0,
    "suspicious_count": 0,
    "fraudulent_count": 0
}

@app.route('/api/analyze/text', methods=['POST'])
def analyze_text():
    try:
        data = request.get_json()
        text = data.get('text', '')
        source_platform = data.get('source_platform', '')
        content_type = data.get('content_type', '')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        result = detector.analyze_text(text, source_platform, content_type)
        
        # Update statistics
        stats["total_scans"] += 1
        if result["risk_score"] < 30:
            stats["legitimate_count"] += 1
        elif result["risk_score"] < 70:
            stats["suspicious_count"] += 1
        else:
            stats["fraudulent_count"] += 1
        
        # Add to history
        detection_history.append({
            "timestamp": datetime.now().isoformat(),
            "type": "text",
            "content": text[:100] + "..." if len(text) > 100 else text,
            "risk_score": result["risk_score"],
            "risk_level": result["risk_level"],
            "platform": source_platform
        })
        
        # Keep only last 10 detections for demo
        if len(detection_history) > 10:
            detection_history.pop(0)
            
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/analyze/url', methods=['POST'])
def analyze_url():
    try:
        data = request.get_json()
        url = data.get('url', '')
        
        if not url:
            return jsonify({"error": "No URL provided"}), 400
        
        result = detector.analyze_url(url)
        
        # Update statistics
        stats["total_scans"] += 1
        if result["risk_score"] < 30:
            stats["legitimate_count"] += 1
        elif result["risk_score"] < 70:
            stats["suspicious_count"] += 1
        else:
            stats["fraudulent_count"] += 1
        
        # Add to history
        detection_history.append({
            "timestamp": datetime.now().isoformat(),
            "type": "url",
            "content": url,
            "risk_score": result["risk_score"],
            "risk_level": result["risk_level"],
            "platform": "website"
        })
        
        # Keep only last 10 detections for demo
        if len(detection_history) > 10:
            detection_history.pop(0)
            
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/check-advisor', methods=['POST'])
def check_advisor():
    try:
        data = request.get_json()
        name = data.get('name', '')
        registration_number = data.get('registration_number', '')
        
        if not name and not registration_number:
            return jsonify({"error": "Either name or registration number must be provided"}), 400
        
        result = detector.check_advisor(name, registration_number)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/check-advisor-by-registration', methods=['POST'])
def check_advisor_by_registration():
    try:
        data = request.get_json()
        registration_number = data.get('registration_number', '')
        
        if not registration_number:
            return jsonify({"error": "Registration number must be provided"}), 400
        
        result = detector.check_advisor("", registration_number)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    try:
        total = stats["total_scans"]
        legitimate_pct = round((stats["legitimate_count"] / total * 100), 2) if total > 0 else 0
        suspicious_pct = round((stats["suspicious_count"] / total * 100), 2) if total > 0 else 0
        fraudulent_pct = round((stats["fraudulent_count"] / total * 100), 2) if total > 0 else 0
        
        return jsonify({
            "total_scans": total,
            "legitimate_percent": legitimate_pct,
            "suspicious_percent": suspicious_pct,
            "fraudulent_percent": fraudulent_pct
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/recent-detections', methods=['GET'])
def get_recent_detections():
    try:
        # Format the detections for the frontend
        formatted_detections = []
        for detection in detection_history:
            title = f"{detection['type'].upper()} Analysis"
            if detection['type'] == 'text':
                title = f"Text: {detection['content']}"
            
            formatted_detections.append({
                "title": title,
                "description": f"Detected as {detection['risk_level']} risk",
                "risk_level": detection['risk_level'],
                "time_ago": "Recently detected"
            })
        
        return jsonify(formatted_detections)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/fraud-types', methods=['GET'])
def get_fraud_types():
    try:
        # Static data for demo - in production this would come from a database
        fraud_types = [
            {"name": "Fake Advisors", "icon": "fas fa-user-secret", "count": 24},
            {"name": "Deepfakes", "icon": "fas fa-video", "count": 7},
            {"name": "Social Media Tips", "icon": "fas fa-comments", "count": 43},
            {"name": "Fake Apps", "icon": "fas fa-mobile-alt", "count": 15}
        ]
        
        return jsonify(fraud_types)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)
