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
                    "Only Give the title and description in {{title ||| description}} format "
                    "The title must be strictly within 8-10 words, and the description must be strictly within 50-60 words.\n\n"
                    "Example format: {{title ||| description}}\n\n"
                    "Dont give extra explaination or information just give the result as specfied in Example format"
                    "{context}"
                )
            ]
        )

        # Instantiate chain
        chain = create_stuff_documents_chain(llm, prompt)

        # Invoke chain
        result = chain.invoke({"context": docs})

        # Validate result
        if isinstance(result, str) and "|||" in result:
            parts = result.split("|||", 1)  # Split into two parts at the first occurrence of "|||"
            title = parts[0].strip()
            description = parts[1].strip()

            if not title:
                title = "Unknown Title"
            if not description:
                description = "Description not available"
            return {title,description}
        else:
            # print(result)
            return {"title": "Unknown Title", "description": "Processing failed"}


    except Exception as e:
        print("Error processing URL:", str(e))
        return {"title": "Error", "description": "Could not fetch data"}


# Test Example
# result = process_url("https://www.firstpost.com/tech/google-ai-boss-casts-doubts-on-deepseeks-efficiency-claims-calls-them-exaggerated-and-misleading-13862031.html")
# print(result)