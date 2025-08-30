import os

class Config:
    # Database configuration
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), '../data/regulatory_db.csv')
    SOCIAL_POSTS_PATH = os.path.join(os.path.dirname(__file__), '../data/social_posts.jsonl')
    TICKS_PATH = os.path.join(os.path.dirname(__file__), '../data/ticks.csv')
    
    # API configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max content length
    
    # Detection thresholds
    HIGH_RISK_THRESHOLD = 70
    MEDIUM_RISK_THRESHOLD = 30
    
    # External API keys (if needed in the future)
    # WHOIS_API_KEY = os.getenv('WHOIS_API_KEY', '')