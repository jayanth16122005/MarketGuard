import re
import json
from typing import Dict, List, Tuple
from urllib.parse import urlparse
import requests
from datetime import datetime

class RuleBasedDetector:
    def __init__(self):
        # Define fraud patterns with weights
        self.patterns = {
            "urgency_language": {
                "keywords": ["act now", "limited time", "don't miss out", "once in a lifetime", 
                            "urgent", "immediately", "today only", "before it's too late"],
                "weight": 0.8,
                "description": "Creates false urgency to pressure quick decisions"
            },
            "high_returns_promise": {
                "keywords": ["guaranteed returns", "risk-free", "high returns", "double your money",
                            "get rich quick", "no risk", "can't lose", "huge profits"],
                "weight": 0.9,
                "description": "Promises unusually high returns with low risk"
            },
            "unregistered_entities": {
                "keywords": ["unregistered", "not sec approved", "not regulated", "offshore",
                            "private investment", "secret strategy", "insider information"],
                "weight": 0.95,
                "description": "Mentions unregistered or unregulated entities"
            },
            "payment_pressure": {
                "keywords": ["wire transfer", "send money now", "bitcoin only", "crypto payment",
                            "western union", "gift cards", "prepaid cards", "urgent payment"],
                "weight": 0.85,
                "description": "Pressures specific payment methods that are hard to trace"
            },
            "grammar_errors": {
                "patterns": [r"\b[A-Z]+\b", r"!\s*!"],  # ALL CAPS, multiple exclamation marks
                "weight": 0.5,
                "description": "Excessive capitalization or punctuation typical in scams"
            },
            "celebrity_endorsement": {
                "keywords": ["elon musk", "warren buffett", "jeff bezos", "bill gates", 
                            "richard branson", "famous investor", "tv personality"],
                "weight": 0.7,
                "description": "Falsely claims celebrity endorsement"
            },
            "fake_testimonials": {
                "keywords": ["testimonials", "success stories", "people are saying", "made millions",
                            "happiest day", "life-changing", "never thought possible"],
                "weight": 0.6,
                "description": "Uses fake testimonials to build credibility"
            }
        }
        
        # Legitimacy indicators (reduce risk score)
        self.legitimacy_indicators = {
            "risk_disclosure": {
                "keywords": ["past performance", "not indicative", "risks involved", "may lose value",
                            "consult professional", "do your research", "volatility", "market risks"],
                "weight": -0.7,
                "description": "Appropriate risk disclosure"
            },
            "registered_entities": {
                "keywords": ["sec registered", "finra member", "regulated by", "license number",
                            "registration number", "nse", "bse", "authorized representative"],
                "weight": -0.8,
                "description": "Mentions proper registration and regulation"
            },
            "contact_information": {
                "patterns": [r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b", r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"],
                "weight": -0.5,
                "description": "Provides legitimate contact information"
            }
        }
        
        # Known fraudulent domains and patterns (simplified example)
        self.known_fraudulent_domains = [
            "fakeinvestment.com", 
            "getrichquick.org",
            "bitcoin-doubler.net"
        ]
        
        # Platform-specific risk modifiers
        self.platform_risk_modifiers = {
            "whatsapp": 0.2,
            "telegram": 0.3,
            "facebook": 0.1,
            "twitter": 0.1,
            "email": 0.15,
            "website": 0.0,
            "exchange": -0.2,
            "other": 0.0
        }
        
        # Content type risk modifiers
        self.content_type_modifiers = {
            "investment_advice": 0.3,
            "announcement": 0.0,
            "advertisement": 0.4,
            "video": 0.1,
            "document": -0.1,
            "other": 0.0
        }

    def analyze_text(self, text: str, source_platform: str = "", content_type: str = "") -> Dict:
        """
        Analyze text for fraud indicators and return a risk assessment
        """
        if not text:
            return {"error": "No text provided for analysis"}
        
        text_lower = text.lower()
        
        # Initialize results
        detected_indicators = []
        risk_score = 0.0
        max_possible_score = 0.0
        
        # Check for fraud patterns
        for pattern_name, pattern_data in self.patterns.items():
            pattern_weight = pattern_data["weight"]
            max_possible_score += pattern_weight
            
            # Check keyword-based patterns
            if "keywords" in pattern_data:
                for keyword in pattern_data["keywords"]:
                    if keyword in text_lower:
                        detected_indicators.append({
                            "type": "fraud",
                            "pattern": pattern_name,
                            "description": pattern_data["description"],
                            "weight": pattern_weight,
                            "evidence": keyword
                        })
                        risk_score += pattern_weight
                        break  # Only count each pattern once
            
            # Check regex patterns
            elif "patterns" in pattern_data:
                for regex_pattern in pattern_data["patterns"]:
                    if re.search(regex_pattern, text):
                        detected_indicators.append({
                            "type": "fraud",
                            "pattern": pattern_name,
                            "description": pattern_data["description"],
                            "weight": pattern_weight,
                            "evidence": "Pattern match"
                        })
                        risk_score += pattern_weight
                        break  # Only count each pattern once
        
        # Check for legitimacy indicators (reduce risk)
        for indicator_name, indicator_data in self.legitimacy_indicators.items():
            indicator_weight = indicator_data["weight"]
            
            # Check keyword-based legitimacy indicators
            if "keywords" in indicator_data:
                for keyword in indicator_data["keywords"]:
                    if keyword in text_lower:
                        detected_indicators.append({
                            "type": "legitimacy",
                            "pattern": indicator_name,
                            "description": indicator_data["description"],
                            "weight": indicator_weight,
                            "evidence": keyword
                        })
                        risk_score += indicator_weight  # This subtracts because weight is negative
                        break
            
            # Check regex patterns for legitimacy
            elif "patterns" in indicator_data:
                for regex_pattern in indicator_data["patterns"]:
                    if re.search(regex_pattern, text):
                        detected_indicators.append({
                            "type": "legitimacy",
                            "pattern": indicator_name,
                            "description": indicator_data["description"],
                            "weight": indicator_weight,
                            "evidence": "Pattern match"
                        })
                        risk_score += indicator_weight  # This subtracts because weight is negative
                        break
        
        # Apply platform and content type modifiers
        platform_modifier = self.platform_risk_modifiers.get(source_platform, 0.0)
        content_modifier = self.content_type_modifiers.get(content_type, 0.0)
        
        # Adjust risk score with modifiers (platform and content type can add up to 0.4)
        risk_score = risk_score * (1 + platform_modifier + content_modifier)
        
        # Normalize risk score to 0-100 range
        if max_possible_score > 0:
            normalized_score = max(0, min(100, (risk_score / max_possible_score) * 100))
        else:
            normalized_score = 0
        
        # Determine risk level
        if normalized_score < 30:
            risk_level = "low"
            recommendation = "This content appears to be legitimate with no significant fraud indicators detected."
        elif normalized_score < 70:
            risk_level = "medium"
            recommendation = "This content shows some suspicious patterns that require further verification."
        else:
            risk_level = "high"
            recommendation = "This content displays multiple characteristics commonly associated with fraudulent activity."
        
        # Add platform-specific advice
        if source_platform in ["whatsapp", "telegram"]:
            recommendation += " Be especially cautious of investment advice received through private messaging platforms."
        
        return {
            "risk_score": round(normalized_score, 2),
            "risk_level": risk_level,
            "indicators": detected_indicators,
            "recommendation": recommendation,
            "platform_modifier": platform_modifier,
            "content_modifier": content_modifier
        }
    
    def analyze_url(self, url: str) -> Dict:
        """
        Analyze a URL for potential fraud indicators
        """
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.lower()
            
            # Check if domain is in known fraudulent list
            domain_risk = 0
            if any(fraud_domain in domain for fraud_domain in self.known_fraudulent_domains):
                domain_risk = 80
            
            # Check for suspicious URL patterns
            suspicious_patterns = [
                r"bitcoin.*double", r"free.*money", r"investment.*secret", 
                r"stock.*tip", r"guaranteed.*return", r"millionaire.*secret"
            ]
            
            url_risk = 0
            for pattern in suspicious_patterns:
                if re.search(pattern, url.lower()):
                    url_risk += 15
            
            # Combine risks (cap at 100)
            total_risk = min(100, domain_risk + url_risk)
            
            # Determine risk level
            if total_risk < 30:
                risk_level = "low"
                recommendation = "This URL does not appear to be associated with known fraud patterns."
            elif total_risk < 70:
                risk_level = "medium"
                recommendation = "This URL shows some suspicious characteristics. Exercise caution."
            else:
                risk_level = "high"
                recommendation = "This URL matches known fraudulent patterns. Avoid interacting with this site."
            
            return {
                "risk_score": total_risk,
                "risk_level": risk_level,
                "domain": domain,
                "recommendation": recommendation
            }
            
        except Exception as e:
            return {"error": f"URL analysis failed: {str(e)}"}
    
    def check_advisor(self, name: str = None, registration_number: str = None) -> Dict:
        """
        Check if a financial advisor is legitimate
        This is a mock implementation - in a real system, you would query regulatory databases
        """
        # Mock database of legitimate advisors (in reality, this would be an external API call)
        legitimate_advisors = {
            "registration_numbers": {
                "IN123456": {"name": "John Smith", "status": "active", "type": "Equity Advisor"},
                "IN654321": {"name": "Jane Doe", "status": "active", "type": "Research Analyst"},
                "US789012": {"name": "Robert Brown", "status": "active", "type": "Investment Advisor"},
            },
            "names": {
                "john smith": "IN123456",
                "jane doe": "IN654321",
                "robert brown": "US789012",
                "sarah johnson": "IN987654"  # This one is not in registration database
            }
        }
        
        if registration_number:
            # Check by registration number
            advisor = legitimate_advisors["registration_numbers"].get(registration_number.upper())
            if advisor:
                return {
                    "registered": True,
                    "details": advisor,
                    "risk_score": 10,
                    "risk_level": "low",
                    "recommendation": "This advisor appears to be properly registered."
                }
            else:
                return {
                    "registered": False,
                    "risk_score": 90,
                    "risk_level": "high",
                    "recommendation": "This registration number was not found in our database. Verify with official regulatory authorities."
                }
        
        elif name:
            # Check by name
            normalized_name = name.lower().strip()
            registration_id = legitimate_advisors["names"].get(normalized_name)
            
            if registration_id:
                advisor = legitimate_advisors["registration_numbers"].get(registration_id)
                if advisor:
                    return {
                        "registered": True,
                        "details": advisor,
                        "risk_score": 15,
                        "risk_level": "low",
                        "recommendation": "This advisor appears to be properly registered."
                    }
            
            # Name not found or not registered
            return {
                "registered": False,
                "risk_score": 80,
                "risk_level": "high",
                "recommendation": "This advisor name was not found in our database. Verify with official regulatory authorities."
            }
        
        else:
            return {"error": "Either name or registration number must be provided"}

# Example usage and test function
if __name__ == "__main__":
    detector = RuleBasedDetector()
    
    # Test with a suspicious message
    test_message = """
    LIMITED TIME OFFER! Act NOW to double your Bitcoin in 24 hours! 
    This is a RISK-FREE opportunity with GUARANTEED RETURNS. 
    Don't miss out on this exclusive offer - wire transfer your funds TODAY!
    """
    
    result = detector.analyze_text(test_message, "whatsapp", "investment_advice")
    print("Fraud Detection Results:")
    print(f"Risk Score: {result['risk_score']}%")
    print(f"Risk Level: {result['risk_level']}")
    print(f"Recommendation: {result['recommendation']}")
    print("\nDetected Indicators:")
    for indicator in result['indicators']:
        print(f"- {indicator['description']} (Weight: {indicator['weight']})")
    
    # Test URL analysis
    print("\n" + "="*50)
    url_result = detector.analyze_url("https://bitcoin-doubler.com/get-rich-quick")
    print(f"URL Risk Score: {url_result['risk_score']}%")
    print(f"URL Risk Level: {url_result['risk_level']}")
    
    # Test advisor check
    print("\n" + "="*50)
    advisor_result = detector.check_advisor(registration_number="IN123456")
    print(f"Advisor Registered: {advisor_result['registered']}")
    print(f"Advisor Risk Score: {advisor_result['risk_score']}%")