import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Presento - Turn any video into a ready-to-use presentation',
  description: 'One-click to transform your video content into professional presentations',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="antialiased min-h-screen bg-st-bg">
        {children}
      </body>
    </html>
  )
}
