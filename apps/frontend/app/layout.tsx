import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Voice Sales Manager",
  description: "Commercial platform foundation for AI-assisted voice sales.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
