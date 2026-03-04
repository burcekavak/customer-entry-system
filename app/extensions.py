from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager 

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Rate limiter for controlling the rate of incoming requests
limiter = Limiter(key_func=get_remote_address)

# Database object 
db= SQLAlchemy()

# Migration tool (Alembic wrapper)
migrate = Migrate()

# Login manager for handling user sessions
login_manager = LoginManager()
login_manager.login_view = "auth.login_form"
login_manager.login_message_category = "warning" 