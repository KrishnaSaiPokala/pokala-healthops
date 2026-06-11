const repo = "pokala-healthops";
const isGitHubPages = process.env.GITHUB_ACTIONS === "true";

/** @type {import("next").NextConfig} */
const nextConfig = {
  output: "export",
  images: {
    unoptimized: true
  },
  basePath: isGitHubPages ? `/${repo}` : "",
  assetPrefix: isGitHubPages ? `/${repo}/` : "",
  trailingSlash: true
};

module.exports = nextConfig;
