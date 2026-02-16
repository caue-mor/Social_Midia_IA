export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR">
      <body className="antialiased">
        <div className="min-h-screen flex items-center justify-center bg-[var(--background)]">
          {children}
        </div>
      </body>
    </html>
  );
}
