const repo = "pokala-healthops";
const isGithubPages = process.env.GITHUB_PAGES === "true";

/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "export",
  images: {
    unoptimized: true,
  },
  trailingSlash: true,
  basePath: isGithubPages ? `/${repo}` : "",
  assetPrefix: isGithubPages ? `/${repo}/` : "",
};

export default nextConfig;
