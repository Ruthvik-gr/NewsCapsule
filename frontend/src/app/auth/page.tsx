'use client'

import { useEffect } from 'react';
import { useSession, signIn, signOut } from "next-auth/react"
import { useRouter } from 'next/navigation';

export default function Component() {
    const { data: session } = useSession()
    const router = useRouter();

    useEffect(() => {
        if (session) {
            router.push('/feed');
        }
    }, [session, router]);

    if (!session) {
        return (
            <div className="p-4 flex flex-col items-center justify-center min-h-screen bg-black text-white ">
                Not signed in <br />
                <button onClick={() => signIn()}>Sign in</button>
            </div>
        )
    }

    return null;
}