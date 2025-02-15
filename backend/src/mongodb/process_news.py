from src.langchain.summary import process_url
from src.mongodb.database import client, news_collection
import asyncio


async def process_unprocessed_news():
    """Process news articles that haven't been finetuned yet."""

    try:
        # Convert cursor to list to avoid async issues
        cursor = news_collection.find({"finetuned": "n"})
        unprocessed_articles = [article async for article in cursor]  # Async iteration

        for article in unprocessed_articles:
            try:
                source_url = article["source"]
                # source_url = "https://www.firstpost.com/tech/google-ai-boss-casts-doubts-on-deepseeks-efficiency-claims-calls-them-exaggerated-and-misleading-13862031.html"
                print("Processing source URL:", source_url)

                title, description = process_url(source_url)
                title = title.strip('{}')  # Remove curly brackets
                description = description.strip('{}')  # Remove curly brackets
                # Validate processed result
                
                if title and description:
                    print({"title": title, "description": description})

                    news_collection.update_one(
                        {"_id": article["_id"]},
                        {
                            "$set": {
                                "title": title,
                                "description": description,
                                "finetuned": "y",
                            }
                        },
                    )
                    print(f"Successfully processed article ID: {article['_id']}")
                else:
                    print(
                        f"Skipping update for article {article['_id']} due to invalid processed result."
                    )

            except Exception as e:
                print(f"Error processing article {article['_id']}: {str(e)}")

    except Exception as e:
        print(f"Database error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(process_unprocessed_news())
