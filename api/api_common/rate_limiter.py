from flask_limiter import Limiter # type: ignore
from flask_limiter.util import get_remote_address # type: ignore
import json

# Load rate limit configurations from a JSON file
with open('monitoring/logs/rate_limiter_config.json') as config_file:
    RATE_LIMIT_CONFIG = json.load(config_file)

# Initialize Limiter with IP-based rate limiting
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=RATE_LIMIT_CONFIG.get("default_limits", ["50 per second"]),
)

def set_rate_limits(app):
    """Applies rate limits to Flask app."""
    limiter.init_app(app)
    print("Rate limiter initialized with default limits:", RATE_LIMIT_CONFIG.get("default_limits", ["50 per second"]))

