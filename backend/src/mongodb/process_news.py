# from src.langchain.summary import process_url
# from src.mongodb.database import client,news_collection
# import asyncio  # Import asyncio to run the async function
# from motor.motor_asyncio import AsyncIOMotorClient
# client = AsyncIOMotorClient("mongodb://your_connection_string")
# news_collection = client.your_database.your_collection


# async def process_unprocessed_news():
#     """
#     Process news articles that haven't been finetuned yet.
#     Gets articles with finetuned='n', processes their source URLs,
#     and updates the database with summaries.
#     """
    
#     try:
#         # Find all unprocessed news articles
#         cursor = news_collection.find({'document.finetuned': 'n'})
#         unprocessed_articles = await cursor.to_list(length=None)  # Now it's valid

        
#         for article in unprocessed_articles:
#             try:
#                 # Get source URL and process it
#                 # source_url = article['source']
#                 source_url = "https://www.firstpost.com/tech/google-ai-boss-casts-doubts-on-deepseeks-efficiency-claims-calls-them-exaggerated-and-misleading-13862031.html"
#                 print("source url used:",source_url)
#                 processed_result = process_url(source_url)
                
#                 # Update the document with processed information
#                 news_collection.update_one(
#                     {'_id': article['_id']},
#                     {
#                         '$set': {
#                             'title': processed_result['title'],
#                             'description': processed_result['description'],
#                             'finetuned': 'y'
#                         }
#                     }
#                 )
#                 print(f"Successfully processed article with ID: {article['_id']}")
                
#             except Exception as e:
#                 print(f"Error processing article {article['_id']}: {str(e)}")
#                 continue
                
#     except Exception as e:
#         print(f"Database error: {str(e)}")
    
#     finally:
#         client.close()

# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(process_unprocessed_news())



from src.langchain.summary import process_url
from src.mongodb.database import client, news_collection
import asyncio

async def process_unprocessed_news():
    """Process news articles that haven't been finetuned yet."""

    try:
        # Convert cursor to list to avoid async issues
        cursor = news_collection.find({'finetuned': 'n'})
        unprocessed_articles = [article async for article in cursor]  # Async iteration


        for article in unprocessed_articles:
            try:
                source_url = article['source']
                # source_url = "https://www.firstpost.com/tech/google-ai-boss-casts-doubts-on-deepseeks-efficiency-claims-calls-them-exaggerated-and-misleading-13862031.html"
                print("Processing source URL:", source_url)

                processed_result = process_url(source_url)
                print("Processed Result:", processed_result)

                # Validate processed result
                if processed_result and "title" in processed_result and "description" in processed_result:
                    news_collection.update_one(
                        {'_id': article['_id']},
                        {
                            '$set': {
                                'title': processed_result['title'],
                                'description': processed_result['description'],
                                'finetuned': 'y'
                            }
                        }
                    )
                    print(f"Successfully processed article ID: {article['_id']}")
                else:
                    print(f"Skipping update for article {article['_id']} due to invalid processed result.")

            except Exception as e:
                print(f"Error processing article {article['_id']}: {str(e)}")

    except Exception as e:
        print(f"Database error: {str(e)}")

    finally:
        client.close()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(process_unprocessed_news())
