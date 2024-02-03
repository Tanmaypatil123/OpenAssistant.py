from openassistant import OpenAssistant
import dotenv
import os
from langchain_google_genai import GoogleGenerativeAI , GoogleGenerativeAIEmbeddings

dotenv.load_dotenv()

llm = GoogleGenerativeAI(google_api_key=os.getenv("GOOGLE_API_KEY"),model="gemini-pro")
embebeddings = GoogleGenerativeAIEmbeddings(google_api_key=os.getenv("GOOGLE_API_KEY"),model="models/embedding-001")
print(embebeddings.embed_query("Hey how are you"))
print(llm.invoke("Hey"))



assistant = OpenAssistant(llm=llm,embeddings=embebeddings,name="example")
assistant.serve()