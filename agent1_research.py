from langchain_openai import ChatOpenAI
import chromadb
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
from serpapi import GoogleSearch

# Load environment variables
load_dotenv()

# Initialize LLM
llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o")

# Initialize shared memory (ChromaDB)
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(name="shared_memory")

def fetch_search_results(query: str) -> str:
    search = GoogleSearch({
        "q": query,
        "api_key": os.getenv("SERPAPI_API_KEY"),
        "num": 5
    })
    results = search.get_dict()
    summaries = []
    for result in results.get("organic_results", []):
        summaries.append(f"- {result.get('title')}: {result.get('snippet')}")
    return "\n".join(summaries)

def research_and_summarize(topic: str) -> str:
    search_results = fetch_search_results(topic)

    if not search_results.strip():
        return "⚠️ No search results found!"

    prompt = f"""
You are given real search results (these were fetched using an API).

Do not say you cannot search the web.  
Directly read these search results and summarize them in 5 bullet points.

Here’s the data:

{search_results}
"""
    response = llm.invoke(prompt)

    final_summary = response.content.strip()
    collection.add(
        documents=[final_summary],
        ids=[f"summary_{topic}"]
    )
    print("✅ Research summary stored in shared memory!")
    return final_summary
