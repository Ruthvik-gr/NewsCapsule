import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  env: {
    MONGO_URI: process.env.MONGO_URI, // Expose MONGO_URI
  },
};

export default nextConfig;
