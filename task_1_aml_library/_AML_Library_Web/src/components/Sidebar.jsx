import { Link, useLocation } from 'react-router-dom'
import { X, Home, BookOpen, Search } from 'lucide-react'
import { documents, categories } from '../data/documents'

function Sidebar({ isOpen, onClose }) {
  const location = useLocation()

  const getDocumentsByCategory = (category) => {
    return documents.filter(doc => doc.category === category)
  }

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={onClose}
        />
      )}
      
      {/* Sidebar */}
      <aside className={`sidebar-scroll fixed left-0 top-16 h-[calc(100vh-4rem)] w-64 bg-white border-r border-stone-200 overflow-y-auto z-50 transition-transform duration-300 ${
        isOpen ? 'translate-x-0' : '-translate-x-full'
      }`}>
        <div className="p-4">
          {/* Close button for mobile */}
          <button
            onClick={onClose}
            className="lg:hidden mb-4 p-2 rounded-lg hover:bg-stone-100"
            aria-label="Close sidebar"
          >
            <X className="w-5 h-5" />
          </button>

          {/* Quick Links */}
          <nav className="space-y-2 mb-6">
            <Link
              to="/"
              className={`flex items-center gap-3 px-4 py-2 rounded-lg transition-colors ${
                location.pathname === '/'
                  ? 'bg-primary-100 text-primary-700 font-semibold'
                  : 'text-slate-700 hover:bg-stone-100'
              }`}
            >
              <Home className="w-5 h-5" />
              <span>Home</span>
            </Link>
            <Link
              to="/master"
              className={`flex items-center gap-3 px-4 py-2 rounded-lg transition-colors ${
                location.pathname === '/master'
                  ? 'bg-primary-100 text-primary-700 font-semibold'
                  : 'text-slate-700 hover:bg-stone-100'
              }`}
            >
              <BookOpen className="w-5 h-5" />
              <span>Master Red Flags</span>
            </Link>
            <Link
              to="/search"
              className={`flex items-center gap-3 px-4 py-2 rounded-lg transition-colors ${
                location.pathname === '/search'
                  ? 'bg-primary-100 text-primary-700 font-semibold'
                  : 'text-slate-700 hover:bg-stone-100'
              }`}
            >
              <Search className="w-5 h-5" />
              <span>Search</span>
            </Link>
          </nav>

          {/* Documents by Category */}
          <div className="space-y-6">
            {categories.map(category => {
              const categoryDocs = getDocumentsByCategory(category)
              if (categoryDocs.length === 0) return null

              return (
                <div key={category}>
                  <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2 px-4">
                    {category}
                  </h3>
                  <ul className="space-y-1">
                    {categoryDocs.map(doc => (
                      <li key={doc.id}>
                        <Link
                          to={`/document/${doc.id}`}
                          className={`flex items-start gap-2 px-4 py-2 rounded-lg transition-colors ${
                            location.pathname === `/document/${doc.id}`
                              ? 'bg-primary-100 text-primary-700 font-semibold'
                              : 'text-slate-700 hover:bg-stone-100'
                          }`}
                        >
                          <span className="text-lg mt-0.5">{doc.icon}</span>
                          <span className="text-sm leading-tight">{doc.title}</span>
                        </Link>
                      </li>
                    ))}
                  </ul>
                </div>
              )
            })}
          </div>
        </div>
      </aside>
    </>
  )
}

export default Sidebar
