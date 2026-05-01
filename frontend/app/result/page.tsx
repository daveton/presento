'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { Download, Copy, ArrowLeft, CheckCircle } from 'lucide-react'

interface Slide {
  type: string
  title: string
  points?: string[]
}

interface PPTResult {
  title: string
  slides: Slide[]
  downloadUrl?: string
}

export default function ResultPage() {
  const [result, setResult] = useState<PPTResult | null>(null)
  const [copied, setCopied] = useState(false)
  const router = useRouter()

  useEffect(() => {
    const stored = sessionStorage.getItem('pptResult')
    if (stored) setResult(JSON.parse(stored))
  }, [])

  const handleCopy = async () => {
    if (!result) return
    const text = result.slides.map(s => `${s.title}\n${s.points?.map(p => `- ${p}`).join('\n') || ''}`).join('\n\n')
    await navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  if (!result) {
    return (
      <div className="min-h-screen bg-st-bg flex items-center justify-center">
        <div className="w-12 h-12 border-4 border-st-primary/30 border-t-st-primary rounded-full animate-spin" />
      </div>
    )
  }

  return (
    <main className="min-h-screen bg-st-bg pb-20">
      <header className="px-6 py-4 flex items-center gap-4">
        <button onClick={() => router.push('/')} className="p-2 rounded-full bg-st-surface border border-st-border hover:bg-st-bg-soft">
          <ArrowLeft className="w-5 h-5 text-st-text" />
        </button>
        <h1 className="text-xl font-bold text-st-text">Your Presentation</h1>
      </header>

      <div className="px-6 max-w-3xl mx-auto">
        {/* Preview */}
        <div className="bg-st-surface rounded-st-lg shadow-st-card border border-st-border p-8 mb-6">
          <h2 className="text-2xl font-bold text-st-text mb-2">{result.title}</h2>
          <p className="text-st-text-sub mb-6">{result.slides.length} slides generated</p>
          
          <div className="space-y-4">
            {result.slides.slice(0, 3).map((slide, i) => (
              <div key={i} className="p-4 bg-st-bg-soft rounded-st-md">
                <h3 className="font-semibold text-st-text mb-2">{slide.title}</h3>
                {slide.points && (
                  <ul className="space-y-1">
                    {slide.points.map((p, j) => (
                      <li key={j} className="text-sm text-st-text-sub flex items-start gap-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-st-primary mt-2 flex-shrink-0" />
                        {p}
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            ))}
            {result.slides.length > 3 && (
              <p className="text-center text-st-text-muted text-sm">+ {result.slides.length - 3} more slides</p>
            )}
          </div>
        </div>

        {/* Actions */}
        <div className="space-y-4">
          {result.downloadUrl && (
            <a
              href={result.downloadUrl}
              download={`${result.title}.pptx`}
              className="w-full h-16 rounded-full bg-gradient-to-r from-st-primary to-st-primary-highlight text-white font-semibold flex items-center justify-center gap-2 shadow-st-button hover:shadow-lg transition-shadow"
            >
              <Download className="w-5 h-5" />
              Download PPT
            </a>
          )}
          
          <button
            onClick={handleCopy}
            className="w-full h-14 rounded-full bg-st-surface border border-st-border text-st-text font-semibold flex items-center justify-center gap-2 hover:bg-st-bg-soft transition-colors"
          >
            {copied ? <CheckCircle className="w-5 h-5 text-st-success" /> : <Copy className="w-5 h-5" />}
            {copied ? 'Copied!' : 'Copy Outline'}
          </button>
        </div>
      </div>
    </main>
  )
}
