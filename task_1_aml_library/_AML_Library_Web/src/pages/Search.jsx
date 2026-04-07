import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Search as SearchIcon, ArrowLeft, FileText } from 'lucide-react'
import { documents } from '../data/documents'

function Search() {
  const [searchQuery, setSearchQuery] = useState('')
  const [results, setResults] = useState([])
  const [selectedCategory, setSelectedCategory] = useState('All')

  useEffect(() => {
    if (!searchQuery.trim()) {
      setResults([])
      return
    }

    // Simple search - in a real app, you'd want to search document content
    const query = searchQuery.toLowerCase()
    const filtered = documents.filter(doc => {
      const matchesQuery = 
        doc.title.toLowerCase().includes(query) ||
        doc.description.toLowerCase().includes(query) ||
        doc.category.toLowerCase().includes(query)
      
      const matchesCategory = selectedCategory === 'All' || doc.category === selectedCategory
      
      return matchesQuery && matchesCategory
    })

    setResults(filtered)
  }, [searchQuery, selectedCategory])

  const categories = ['All', ...new Set(documents.map(doc => doc.category))]

  return (
    <div className="max-w-5xl mx-auto">
      <div className="mb-6">
        <Link
          to="/"
          className="inline-flex items-center gap-2 text-primary-600 hover:text-primary-500 mb-4"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Home
        </Link>
        <h1 className="text-3xl font-bold text-slate-800 mb-2">Search Library</h1>
        <p className="text-slate-600">Find documents by title, description, or category</p>
      </div>

      {/* Search Bar */}
      <div className="bg-white rounded-lg shadow-sm border border-stone-200 p-6 mb-6">
        <div className="relative mb-4">
          <SearchIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 w-5 h-5" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search documents..."
            className="w-full pl-10 pr-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
        </div>

        {/* Category Filter */}
        <div className="flex flex-wrap gap-2">
          {categories.map(category => (
            <button
              key={category}
              onClick={() => setSelectedCategory(category)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                selectedCategory === category
                  ? 'bg-primary-500 text-white'
                  : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
              }`}
            >
              {category}
            </button>
          ))}
        </div>
      </div>

      {/* Results */}
      <div>
        {searchQuery && (
          <p className="text-slate-600 mb-4">
            Found {results.length} result{results.length !== 1 ? 's' : ''}
          </p>
        )}

        {results.length === 0 && searchQuery && (
          <div className="bg-stone-50 rounded-lg shadow-sm border border-slate-200 p-8 text-center">
            <FileText className="w-12 h-12 text-slate-400 mx-auto mb-4" />
            <p className="text-slate-600">No documents found matching your search.</p>
          </div>
        )}

        {results.length > 0 && (
          <div className="space-y-4">
            {results.map(doc => (
              <Link
                key={doc.id}
                to={`/document/${doc.id}`}
                className="block bg-white rounded-lg shadow-sm border border-slate-200 p-6 hover:shadow-md hover:border-primary-300 transition-all"
              >
                <div className="flex items-start gap-4">
                  <span className="text-2xl">{doc.icon}</span>
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-slate-800 mb-1">
                      {doc.title}
                    </h3>
                    <p className="text-sm text-slate-600 mb-2">{doc.description}</p>
                    <span className="inline-block px-3 py-1 bg-primary-100 text-primary-600 rounded-full text-xs font-medium">
                      {doc.category}
                    </span>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}

        {!searchQuery && (
          <div className="bg-white rounded-lg shadow-sm border border-stone-200 p-8 text-center">
            <SearchIcon className="w-12 h-12 text-slate-400 mx-auto mb-4" />
            <p className="text-slate-600">Enter a search query to find documents</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default Search
