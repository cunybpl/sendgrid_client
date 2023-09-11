import os

ENVIRONMENT = os.environ.get("SENDGRID_API_ENVIRONMENT", "local")
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
