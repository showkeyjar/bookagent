import './globals.css'
import { Inter, Crimson_Text } from 'next/font/google'
import { Toaster } from 'react-hot-toast'

const inter = Inter({ 
  subsets: ['latin'],
  variable: '--font-inter',
})

const crimsonText = Crimson_Text({ 
  weight: ['400', '600'],
  subsets: ['latin'],
  variable: '--font-crimson',
})

export const metadata = {
  title: 'BookAgent - 智能图书创作平台',
  description: '专注于思想传递的智能技术图书自动生成系统',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-CN" className={`${inter.variable} ${crimsonText.variable}`}>
      <body className="font-sans bg-gray-50 text-gray-900 antialiased">
        <div className="min-h-screen">
          {children}
        </div>
        <Toaster 
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: '#363636',
              color: '#fff',
            },
          }}
        />
      </body>
    </html>
  )
}