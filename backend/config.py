from dotenv import load_dotenv
import os
load_dotenv()
class Config:
    GROQ_API_KEY = os.environ.get('GROQ_AI_KEY')
    SERPER_API_KEY = os.environ.get('SERPER_API_KEY')