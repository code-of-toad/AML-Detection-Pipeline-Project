import { useParams, Link } from 'react-router-dom'
import { useState, useEffect } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { ArrowLeft, FileText } from 'lucide-react'
import { documents } from '../data/documents'

function DocumentViewer() {
  const { docId } = useParams()
  const [content, setContent] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const document = documents.find(doc => doc.id === docId)

  useEffect(() => {
    if (!document) {
      setError('Document not found')
      setLoading(false)
      return
    }

    // Get base path from Vite's import.meta.env
    const baseUrl = import.meta.env.BASE_URL || '/'
    
    // Load markdown file from public directory
    // Remove trailing slash from baseUrl if present, then add the path
    const basePath = baseUrl.endsWith('/') ? baseUrl.slice(0, -1) : baseUrl
    fetch(`${basePath}/AML_Library/${document.filename}`)
      .then(response => {
        if (!response.ok) throw new Error('Failed to load document')
        return response.text()
      })
      .then(text => {
        setContent(text)
        setLoading(false)
      })
      .catch(err => {
        setError(err.message)
        setLoading(false)
      })
  }, [docId, document])

  if (loading) {
    return (
      <div className="max-w-5xl mx-auto">
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
            <p className="text-slate-600">Loading document...</p>
          </div>
        </div>
      </div>
    )
  }

  if (error || !document) {
    return (
      <div className="max-w-5xl mx-auto">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6">
          <h2 className="text-xl font-semibold text-red-800 mb-2">Error</h2>
          <p className="text-red-600">{error || 'Document not found'}</p>
          <Link
            to="/"
            className="mt-4 inline-flex items-center gap-2 text-primary-600 hover:text-primary-500"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Home
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-5xl mx-auto">
      {/* Header */}
      <div className="mb-6">
        <Link
          to="/"
          className="inline-flex items-center gap-2 text-primary-600 hover:text-primary-500 mb-4"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Home
        </Link>
        <div className="flex items-start gap-3">
          <span className="text-3xl">{document.icon}</span>
          <div>
            <h1 className="text-3xl font-bold text-slate-800 mb-2">
              {document.title}
            </h1>
            <p className="text-slate-600 mb-2">{document.description}</p>
            <span className="inline-block px-3 py-1 bg-primary-100 text-primary-600 rounded-full text-sm font-medium">
              {document.category}
            </span>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="bg-white rounded-lg shadow-sm border border-stone-200 p-8">
        <div className="markdown-content">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {content}
          </ReactMarkdown>
        </div>
      </div>
    </div>
  )
}

export default DocumentViewer
