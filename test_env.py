from dotenv import load_dotenv
import os
load_dotenv()
k = os.getenv("OPENAI_API_KEY")
print("Loaded:", bool(k))
if k:
    print("Preview:", k[:8] + "..." + k[-4:])
