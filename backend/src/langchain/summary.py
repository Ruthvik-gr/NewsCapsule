from dotenv import load_dotenv
import getpass
from langchain_community.document_loaders import WebBaseLoader
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.llm import LLMChain
from langchain_core.prompts import ChatPromptTemplate
import os

os.environ["USER_AGENT"] = "newscapsule/1.0"
load_dotenv()


def process_url(source_url):
    """Fetches and processes a URL to extract title and description."""
    try:
        loader = WebBaseLoader(source_url)
        docs = loader.load()

        if "GROQ_API_KEY" not in os.environ:
            os.environ["GROQ_API_KEY"] = getpass.getpass("Enter API key for Groq: ")

        from langchain.chat_models import init_chat_model

        llm = init_chat_model("llama3-8b-8192", model_provider="groq")

        # Define prompt
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Give the title and description only in json format: The title must be strictly within 8 words, and the description must be strictly within 60 words:\n\n{context}",
                )
            ]
        )

        # Instantiate chain
        chain = create_stuff_documents_chain(llm, prompt)

        # Invoke chain
        result = chain.invoke({"context": docs})

        # Validate result
        if isinstance(result, dict) and "title" in result and "description" in result:
            return result
        else:
            print("Unexpected result format:", result)
            return {"title": "Unknown", "description": "Processing failed"}

    except Exception as e:
        print("Error processing URL:", str(e))
        return {"title": "Error", "description": "Could not fetch data"}


# Test Example
result = process_url("https://www.firstpost.com/tech/google-ai-boss-casts-doubts-on-deepseeks-efficiency-claims-calls-them-exaggerated-and-misleading-13862031.html")
print(result)