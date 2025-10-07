import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Consultor de Viagens",
  description: "Planeje sua viagem com checklist e clima",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="pt-BR" className="h-full">
      <body className="min-h-full bg-white text-neutral-900 dark:bg-neutral-950 dark:text-neutral-100">
        {children}
      </body>
    </html>
  );
}
