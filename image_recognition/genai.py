from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

gemini_key=os.getenv("GEMINI_API_KEY")
print("API KEY: ", gemini_key)

genai.configure(api_key=gemini_key)

model = genai.GenerativeModel(model_name="gemini-1.5-flash")
# response = model.generate_content("The opposite of hot is")
# print(response.text)
