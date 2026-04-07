import { Link } from 'react-router-dom'
import { BookOpen, Search, FileText, Shield } from 'lucide-react'
import { documents } from '../data/documents'

function Home() {
  const featuredDocs = documents.filter(doc => doc.priority === 1 || doc.priority === 2).slice(0, 4)

  return (
    <div className="max-w-6xl mx-auto">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-700 rounded-xl p-8 mb-8 text-white shadow-lg">
        <h1 className="text-4xl font-bold mb-4">AML Knowledge Library</h1>
        <p className="text-xl text-primary-50 mb-6">
          A standalone, comprehensive knowledge base containing Money Laundering (ML) and 
          Terrorist Financing (TF) red flags, indicators, and intelligence, with a special 
          focus on <strong>Organized Crime Groups (OCGs)</strong>.
        </p>
        <div className="flex gap-4">
          <Link
            to="/master"
            className="bg-white text-primary-600 px-6 py-3 rounded-lg font-semibold hover:bg-primary-50 transition-colors shadow-sm"
          >
            View Master Red Flags
          </Link>
          <Link
            to="/search"
            className="bg-primary-500 text-white px-6 py-3 rounded-lg font-semibold hover:bg-primary-400 transition-colors shadow-sm"
          >
            Search Library
          </Link>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white rounded-lg p-6 shadow-sm border border-stone-200">
          <div className="flex items-center gap-3 mb-2">
            <Shield className="w-8 h-8 text-primary-600" />
            <h3 className="text-2xl font-bold text-slate-800">147+</h3>
          </div>
          <p className="text-slate-600">Red Flags & Indicators</p>
        </div>
        <div className="bg-white rounded-lg p-6 shadow-sm border border-stone-200">
          <div className="flex items-center gap-3 mb-2">
            <FileText className="w-8 h-8 text-primary-600" />
            <h3 className="text-2xl font-bold text-slate-800">8</h3>
          </div>
          <p className="text-slate-600">Authoritative Sources</p>
        </div>
        <div className="bg-white rounded-lg p-6 shadow-sm border border-stone-200">
          <div className="flex items-center gap-3 mb-2">
            <BookOpen className="w-8 h-8 text-primary-600" />
            <h3 className="text-2xl font-bold text-slate-800">11</h3>
          </div>
          <p className="text-slate-600">Document Categories</p>
        </div>
      </div>

      {/* Featured Documents */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-slate-800 mb-4">Featured Documents</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {featuredDocs.map(doc => (
            <Link
              key={doc.id}
              to={`/document/${doc.id}`}
              className="bg-white rounded-lg p-6 shadow-sm border border-stone-200 hover:shadow-md hover:border-primary-300 transition-all"
            >
              <div className="flex items-start gap-3">
                <span className="text-2xl">{doc.icon}</span>
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-slate-800 mb-1">
                    {doc.title}
                  </h3>
                  <p className="text-sm text-slate-600 mb-2">{doc.description}</p>
                  <span className="text-xs text-primary-600 font-medium">
                    {doc.category}
                  </span>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>

      {/* Use Cases */}
      <div className="bg-white rounded-lg p-6 shadow-sm border border-stone-200">
        <h2 className="text-2xl font-bold text-slate-800 mb-4">Use Cases</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <h3 className="font-semibold text-slate-800 mb-2">Standalone Use</h3>
            <ul className="space-y-1 text-slate-600 text-sm">
              <li>• AML Investigation</li>
              <li>• Risk Assessment</li>
              <li>• Training and Education</li>
              <li>• Research and Analysis</li>
            </ul>
          </div>
          <div>
            <h3 className="font-semibold text-slate-800 mb-2">Facilitation Use</h3>
            <ul className="space-y-1 text-slate-600 text-sm">
              <li>• Model Development</li>
              <li>• Feature Engineering</li>
              <li>• Model Explainability</li>
              <li>• Risk Pattern Understanding</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home
