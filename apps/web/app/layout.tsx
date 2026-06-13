import "./globals.css";

export const metadata = {
  title: "Pokala HealthOps Reliability Platform",
  description:
    "No-PHI healthcare interface reliability control plane for DLQ recovery, replay safety, warehouse verification, and evidence-driven incident closure."
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
