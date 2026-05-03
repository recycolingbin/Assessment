import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'PortfolioIQ - Professional Investment Management',
  description: 'Secure and elegant portfolio management platform for tracking your investments',
  icons: {
    icon: '/favicon.svg',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
