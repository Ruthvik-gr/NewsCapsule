"use client";
import { useState, useEffect, useRef, useCallback } from "react";

interface NewsItem {
    _id: string;
    media: string;
    title: string;
    summary: string;
}

const Page: React.FC = () => {
    const [news, setNews] = useState<NewsItem[]>([]);
    const [page, setPage] = useState<number>(1);
    const [loading, setLoading] = useState<boolean>(false);
    const [hasMore, setHasMore] = useState<boolean>(true);
    const observer = useRef<IntersectionObserver | null>(null);

    // Fetch news data from API
    const fetchNews = useCallback(async () => {
        if (!hasMore) return;
        setLoading(true);

        try {
            const res = await fetch(`/api/news?page=${page}`);
            const data: NewsItem[] = await res.json();

            if (data.length === 0) {
                setHasMore(false);
            } else {
                setNews((prev) => [...prev, ...data]);
                setPage((prev) => prev + 1);
            }
        } catch (error) {
            console.error("Error fetching news:", error);
        }

        setLoading(false);
    }, [page, hasMore]);

    // Intersection Observer for infinite scrolling
    const lastNewsRef = useCallback(
        (node: HTMLDivElement | null) => {
            if (loading) return;
            if (observer.current) observer.current.disconnect();

            observer.current = new IntersectionObserver(
                (entries) => {
                    if (entries[0].isIntersecting) {
                        fetchNews();
                    }
                },
                { threshold: 1.0 }
            );

            if (node) observer.current.observe(node);
        },
        [loading, fetchNews]
    );

    useEffect(() => {
        fetchNews();
    }, []); // Initial fetch

    return (
        <div className="flex pt-24 flex-col items-center min-h-screen bg-[#022439] p-4">
            <div className="w-full max-w-md space-y-4">
                {news.map((item, index) => (
                    <div
                        key={item._id}
                        ref={index === news.length - 1 ? lastNewsRef : null}
                        className="bg-white text-black p-4 rounded-2xl shadow-lg"
                    >
                        <img
                            src={item.media}
                            alt={item.title}
                            className="w-full h-48 object-cover rounded-lg"
                            loading="lazy"
                        />
                        <h3 className="text-lg font-semibold mt-2">{item.title}</h3>
                        <p className="text-sm text-gray-700 mt-1">{item.summary}</p>
                    </div>
                ))}

                {loading && (
                    <div className="flex items-center justify-center min-h-screen">
                        <div className="w-12 h-12 border-4 border-gray-300 border-t-blue-500 rounded-full animate-spin"></div>
                    </div>
                )}
                {!hasMore && (
                    <p className="text-white text-center text-lg font-semibold mt-4 bg-gradient-to-r from-gray-700 via-gray-900 to-gray-700 py-2 rounded-lg shadow-lg">
                        You've seen it all
                    </p>
                )}

            </div>
        </div>
    );
};

export default Page;
