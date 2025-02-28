import type { Metadata } from "next";
import { Inconsolata } from "next/font/google";
import "./globals.css";
import { Navbar } from "@/components/navbar";
import SessionWrapper from "../components/sessionWrapper"

const inconsolata = Inconsolata({
  weight: "400",
  variable: "--font-inconsolata",
  subsets: ["latin"],
});


export const metadata: Metadata = {
  applicationName: "News Capsule",
  title: "News Capsule - AI-Powered News Summaries in Seconds",
  description: "Stay informed in seconds! NewsCapsule curates and delivers AI-powered, concise news summaries, keeping you updated with the latest headlines effortlessly.",
  authors: { name: "Ruthvik Ghagarwale", url: "https://ruthvikghagarwaleportfolio.netlify.app/" },
  keywords: [
    "AI news summarizer",
    "AI-powered news app",
    "News summary app",
    "Real-time news summaries",
    "Smart news aggregator",
    "AI news insights",
    "Quick news updates",
    "Best news app",
    "Daily news summary",
    "Fast news highlights",
    "AI-powered app for news updates",
    "Best app to read summarized news",
    "How to get quick news summaries?",
    "AI-driven news curation app"
  ]
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head><meta name="google-site-verification" content="_JOLkDNnFGSg_Yn__hoJdlf_gr74eRFz5n1a7O4XtMA" /></head>
      <SessionWrapper>
        <body
          className={` ${inconsolata.variable} antialiased`}
        >
          <Navbar className="bg-[#022439] rounded-xl" />
          {children}
        </body>
      </SessionWrapper>
    </html>
  );
}
