import os
import ast

# List your credentials and tokens here instead for security reasons
# NOTE: I know that this is not super-safe, but it's good enough for this project
# For real production, I will use Azure Key Vault
ADMIN_LIST = ast.literal_eval(os.environ['ADMIN_LIST'])  # Insert telegram user ID-s here to enable admin-only commands for them
BOT_TOKEN = os.environ['BOT_TOKEN']  # Insert your Telegram bot token here
WEBHOOK_URL = os.environ['WEBHOOK_URL']  # For upcoming webhook implementation
MONGODB_ATLAS_CONNECTION_STRING = os.environ['MONGODB_ATLAS_CONNECTION_STRING']  # For MongoDB Atlas connection
EMAIL = os.environ['EMAIL']  # Not important for now
main_chat = ast.literal_eval(os.environ['main_chat'])  # Insert your main Telegram group chat ID here
private_chat = ast.literal_eval(os.environ['private_chat'])  # Insert your personal/private Telegram chat ID here for testing purposes
