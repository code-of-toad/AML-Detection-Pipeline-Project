import { Link } from 'react-router-dom'
import { ArrowLeft, BookOpen } from 'lucide-react'

function MasterRedFlags() {
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
        <div className="flex items-center gap-3 mb-4">
          <BookOpen className="w-8 h-8 text-primary-500" />
          <h1 className="text-3xl font-bold text-slate-800">
            Comprehensive Red Flags Master
          </h1>
        </div>
        <p className="text-slate-600">
          All 147+ red flags organized in tables - Quick reference format with data signals and feature mappings.
        </p>
      </div>

      <div className="bg-primary-50 border border-primary-200 rounded-lg p-4 mb-6">
        <p className="text-primary-800">
          <strong>Note:</strong> This page displays the master document. For the best experience, 
          view the <Link to="/document/00" className="underline font-semibold">full document</Link> with complete formatting.
        </p>
      </div>

      <Link
        to="/document/00"
        className="inline-block bg-primary-500 text-white px-6 py-3 rounded-lg font-semibold hover:bg-primary-400 transition-colors mb-6"
      >
        View Full Master Document
      </Link>

      <div className="bg-white rounded-lg shadow-sm border border-stone-200 p-6">
        <p className="text-slate-600">
          The Comprehensive Red Flags Master document contains all 147+ red flags organized by category:
        </p>
        <ul className="list-disc list-inside mt-4 space-y-2 text-slate-700">
          <li>Professional Money Laundering (Trade & MSB)</li>
          <li>Bulk Cash Smuggling (Mexico TCOs)</li>
          <li>Oil Smuggling (Mexico Cartels)</li>
          <li>Chinese ML Networks (Mexico TCOs)</li>
          <li>Synthetic Opioids Proceeds</li>
          <li>Underground Banking Schemes</li>
          <li>Human Trafficking Proceeds</li>
          <li>General ML/TF Indicators</li>
        </ul>
      </div>
    </div>
  )
}

export default MasterRedFlags
