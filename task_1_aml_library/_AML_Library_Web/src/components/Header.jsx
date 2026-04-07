import { Link } from 'react-router-dom'
import { Menu, Search } from 'lucide-react'

function Header({ onMenuClick }) {
  return (
    <header className="bg-white shadow-sm border-b border-stone-200 sticky top-0 z-50">
      <div className="flex items-center justify-between px-6 py-4">
        <div className="flex items-center gap-4">
          <button
            onClick={onMenuClick}
            className="p-2 rounded-lg hover:bg-stone-100 transition-colors"
            aria-label="Toggle menu"
          >
            <Menu className="w-6 h-6 text-slate-700" />
          </button>
          <Link to="/" className="flex items-center gap-2">
            <h1 className="text-2xl font-bold text-primary-600">
              AML Knowledge Library
            </h1>
          </Link>
        </div>
        <Link
          to="/search"
          className="flex items-center gap-2 px-4 py-2 rounded-lg hover:bg-stone-100 transition-colors text-slate-700"
        >
          <Search className="w-5 h-5" />
          <span className="hidden md:inline">Search</span>
        </Link>
      </div>
    </header>
  )
}

export default Header
