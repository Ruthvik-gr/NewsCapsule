import { NextResponse } from "next/server";
import { MongoClient } from "mongodb";

const MONGO_URI = process.env.MONGO_URI as string; // Use env variable
const client = new MongoClient(MONGO_URI);

interface NewsItem {
  _id: string;
  media: string;
  title: string;
  description: string;
  finetuned: string;
}

export async function GET(req: Request) {
  try {
    await client.connect();
    const db = client.db("newsapp");
    const collection = db.collection<NewsItem>("news_collection");

    const url = new URL(req.url);
    const page = parseInt(url.searchParams.get("page") || "1");
    const limit = 10; // Fetch 10 per page
    const skip = (page - 1) * limit;

    // Fetch news where `finetuned` is "y"
    const news = await collection
      .find({ finetuned: "y" })
      .sort({ _id: -1 }) // Latest first
      .skip(skip)
      .limit(limit)
      .toArray();

    return NextResponse.json(news);
  } catch (error) {
    console.error("Error fetching news:", error);
    return NextResponse.json(
      { error: "Failed to fetch news" },
      { status: 500 }
    );
  }
}
