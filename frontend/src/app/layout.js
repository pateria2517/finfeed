import "./globals.css";

export const metadata = {
  title: "Feedz — Hyper-Personal Financial Intelligence",
  description: "Portfolio-aware financial news intelligence with SEBI-guarded AI analysis.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-[#101820] text-[#E9EEF3] antialiased">{children}</body>
    </html>
  );
}
