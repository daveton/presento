'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Sparkles, FileText, Zap } from 'lucide-react'

export default function Home() {
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const router = useRouter()

  const handleGenerate = async () => {
    if (!input.trim()) {
      alert('Please paste a video link or text first')
      return
    }
    
    setIsLoading(true)
    
    try {
      const response = await fetch('http://localhost:8000/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input: input.trim() }),
      })
      
      if (!response.ok) throw new Error('Failed to generate')
      
      const data = await response.json()
      
      // Store result in session storage for result page
      sessionStorage.setItem('pptResult', JSON.stringify(data))
      router.push('/result')
    } catch (error) {
      console.error('Error:', error)
      alert('生成失败，请重试')
    } finally {
      setIsLoading(false)
    }
  }

  const handlePaste = async () => {
    try {
      const text = await navigator.clipboard.readText()
      setInput(text)
    } catch {
      alert('无法访问剪贴板，请手动粘贴')
    }
  }

  return (
    <main className="min-h-screen bg-st-bg flex flex-col">
      {/* Header */}
      <header className="px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-st-primary to-st-primary-highlight flex items-center justify-center">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <span className="text-xl font-bold text-st-text">Presento</span>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex-1 flex flex-col items-center justify-center px-6 py-12 max-w-2xl mx-auto w-full">
        {/* Hero */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-st-text mb-4 leading-tight">
            Turn any video into a
            <span className="bg-gradient-to-r from-st-primary to-st-primary-highlight bg-clip-text text-transparent">
              {' '}ready-to-use{' '}
            </span>
            presentation
          </h1>
          <p className="text-st-text-sub text-lg">
            Paste a video link or transcript, get a professional PPT in seconds
          </p>
        </div>

        {/* Input Card */}
        <div className="w-full bg-st-surface rounded-st-lg shadow-st-card border border-st-border p-6 mb-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <FileText className="w-5 h-5 text-st-primary" />
              <span className="font-semibold text-st-text">Input</span>
            </div>
            <div className="flex gap-2">
              <button
                onClick={handlePaste}
                className="px-4 py-2 rounded-full bg-st-bg-soft text-st-primary text-sm font-semibold hover:bg-st-primary-soft transition-colors"
              >
                Paste
              </button>
              {input && (
                <button
                  onClick={() => setInput('')}
                  className="px-4 py-2 rounded-full bg-st-bg-soft text-st-text-sub text-sm font-semibold hover:bg-st-risk-soft hover:text-st-risk transition-colors"
                >
                  Clear
                </button>
              )}
            </div>
          </div>
          
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Paste video link or transcript here..."
            className="w-full min-h-[180px] p-4 rounded-st-md bg-st-bg-soft border border-st-border resize-none focus:outline-none focus:border-st-primary focus:ring-2 focus:ring-st-primary-soft transition-all text-st-text placeholder:text-st-placeholder"
          />
        </div>

        {/* Generate Button */}
        <button
          onClick={handleGenerate}
          disabled={!input.trim() || isLoading}
          className={`
            w-full h-[72px] rounded-full font-semibold text-lg text-white
            flex items-center justify-center gap-3
            transition-all duration-200
            ${input.trim() && !isLoading
              ? 'bg-gradient-to-r from-st-primary to-st-primary-highlight shadow-st-button hover:shadow-lg hover:scale-[1.02] active:scale-[0.98]'
              : 'bg-st-placeholder cursor-not-allowed'
            }
          `}
        >
          {isLoading ? (
            <>
              <div className="w-6 h-6 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              Generating...
            </>
          ) : (
            <>
              <Zap className="w-6 h-6" />
              Generate Ready-to-Use PPT
            </>
          )}
        </button>

        {/* Features */}
        <div className="flex flex-wrap justify-center gap-6 mt-8 text-st-text-muted text-sm">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-st-success" />
            Auto structured
          </div>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-st-success" />
            Clean layout
          </div>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-st-success" />
            Ready to present
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="px-6 py-4 text-center text-st-text-muted text-sm">
        <p>Generated presentations are ready to use immediately</p>
      </footer>
    </main>
  )
}
