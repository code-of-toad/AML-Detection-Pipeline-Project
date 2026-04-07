import { useState, useEffect } from 'react'
import Sidebar from './Sidebar'
import Header from './Header'

function Layout({ children }) {
  // Start with sidebar closed on mobile, open on desktop
  const [sidebarOpen, setSidebarOpen] = useState(() => {
    return window.innerWidth >= 1024 // lg breakpoint
  })

  // Handle window resize to maintain proper state
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth >= 1024 && !sidebarOpen) {
        setSidebarOpen(true)
      } else if (window.innerWidth < 1024 && sidebarOpen) {
        setSidebarOpen(false)
      }
    }

    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [sidebarOpen])

  return (
    <div className="min-h-screen bg-stone-50">
      <Header onMenuClick={() => setSidebarOpen(!sidebarOpen)} />
      <div className="flex">
        <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
        <main className={`flex-1 transition-all duration-300 ${sidebarOpen ? 'lg:ml-64' : ''}`}>
          <div className="p-6">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}

export default Layout
