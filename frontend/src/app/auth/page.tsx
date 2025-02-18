"use client";

import { useEffect } from "react";
import { useSession, signIn, signOut } from "next-auth/react";
import { useRouter } from "next/navigation";
import LampDemo from "@/components/ui/lamp"; // Ensure this component exists

export default function Component() {
    const { data: session, status } = useSession();
    const router = useRouter();

    // Redirect authenticated users to /feed
    useEffect(() => {
        if (session) {
            router.push("/feed");
        }
    }, [session, router]);

    // Show loading state while session is being checked
    if (status === "loading") {
        return (
            <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-gray-900 to-black text-white">
                <p className="text-lg font-medium">Loading...</p>
            </div>
        );
    }

    // If user is not authenticated, show the sign-in UI
    if (!session) {
        return (
            <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-gray-900 to-black text-white">
                <LampDemo words={["Welcome back! We’ve missed you.",
                    "It’s great to have you back with us!",
                    "Glad to see you again!",
                    "Welcome back, buddy!",
                ]} />
                <button
                    onClick={() => signIn()}
                    aria-label="Sign In"
                    className="fixed bottom-20 bg-[#16c6e2] text-white px-6 py-2 rounded-lg shadow-md hover:bg-[#022439] transition focus:outline-none focus:ring-2 focus:ring-[#12616d]"

                >
                    Sign In
                </button>
            </div>
        );
    }

    return null;
}
