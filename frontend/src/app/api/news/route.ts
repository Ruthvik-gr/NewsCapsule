import { NextResponse } from "next/server";
import { MongoClient } from "mongodb";

const MONGO_URI = process.env.MONGO_URI as string;
if (!MONGO_URI) {
  throw new Error("MONGO_URI is not defined in environment variables");
}

// Optimize MongoDB connection
let client: MongoClient;
let clientPromise: Promise<MongoClient>;

if (!(globalThis as any).mongoClientPromise) {
  client = new MongoClient(MONGO_URI);
  (globalThis as any).mongoClientPromise = client.connect();
}
clientPromise = (globalThis as any).mongoClientPromise;

interface NewsItem {
  _id: string;
  media: string;
  title: string;
  description: string;
  finetuned: string;
}

export async function GET(req: Request) {
  try {
    const dbClient = await clientPromise;
    const db = dbClient.db("newsapp");
    const collection = db.collection<NewsItem>("news_collection");
    const url = new URL(req.url);
    const page = parseInt(url.searchParams.get("page") || "1");
    const limit = 10;
    const skip = (page - 1) * limit;

    // Fetch news where `finetuned` is "y"
    const news = await collection
      .find({ finetuned: "y" })
      .sort({ _id: -1 })
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
