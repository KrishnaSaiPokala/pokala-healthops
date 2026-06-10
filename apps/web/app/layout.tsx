export const metadata = {
  title: "OpenHIP Command Center",
  description: "No-PHI EHR InterfaceOps platform"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
