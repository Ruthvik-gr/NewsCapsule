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
    """Fetches and processes a URL to extract description only."""
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
                    "You are a top-tier news channel known for compelling summaries. Use your best copywriting skills to craft concise, impactful descriptions. Provide only the summary strictly within 50-60 words, without additional formatting, quotation marks, or explanations.{context}"
                ),
            ]
        )

        # Instantiate chain
        chain = create_stuff_documents_chain(llm, prompt)

        # Invoke chain
        result = chain.invoke({"context": docs})

        # Validate result
        if isinstance(result, str):
            description = result.strip()
            if not description:
                return "Description not available"  # Return a string directly
            return description  # Return the description string directly
        else:
            return "Processing failed"  # Return a string for failure

    except Exception as e:
        print("Error processing URL:", str(e))
        return "Could not fetch data"  # Return a string for error


# Test Example
# result = process_url("https://www.firstpost.com/tech/google-ai-boss-casts-doubts-on-deepseeks-efficiency-claims-calls-them-exaggerated-and-misleading-13862031.html")
# print(result)
