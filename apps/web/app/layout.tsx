export const metadata = {
  title: "OpenHIP Command Center",
  description: "No-PHI healthcare interface operations",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body style={{ margin: 0, background: "#0f1115", color: "#e7e9ee",
        fontFamily: "ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto" }}>
        {children}
      </body>
    </html>
  );
}
