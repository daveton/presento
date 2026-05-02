"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"

interface Slide {
  type: string
  title: string
  points?: string[]
}

interface PPTResult {
  title: string
  slides: Slide[]
  download_url?: string
}

export default function ResultPage() {
  const [result, setResult] = useState<PPTResult | null>(null)
  const [loading, setLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    const stored = sessionStorage.getItem("pptResult")
    if (stored) {
      setResult(JSON.parse(stored))
    }
    setLoading(false)
  }, [])

  const handleDownload = () => {
    if (!result?.download_url) return
    
    // 构建完整下载链接
    const downloadUrl = result.download_url.startsWith("http") 
      ? result.download_url 
      : `http://localhost:8000${result.download_url}`
    
    window.open(downloadUrl, "_blank")
  }

  const handleBack = () => {
    router.push("/")
  }

  if (loading) {
    return (
      <main className="min-h-screen bg-white flex items-center justify-center">
        <div className="text-center">
          <div className="w-8 h-8 border-2 border-gray-300 border-t-black rounded-full animate-spin mx-auto mb-4" />
          <p className="text-gray-500">Loading...</p>
        </div>
      </main>
    )
  }

  if (!result) {
    return (
      <main className="min-h-screen bg-white flex items-center justify-center px-6">
        <div className="text-center max-w-md">
          <h1 className="text-2xl font-bold mb-4">No Result Found</h1>
          <p className="text-gray-500 mb-6">Please generate a PPT first.</p>
          <button
            onClick={handleBack}
            className="px-6 py-3 bg-black text-white rounded-xl font-medium hover:opacity-90 transition"
          >
            Back to Home
          </button>
        </div>
      </main>
    )
  }

  return (
    <main className="min-h-screen bg-white">
      {/* Header */}
      <div className="absolute top-6 left-6 text-lg font-semibold">
        Presento
      </div>

      <div className="max-w-2xl mx-auto px-6 pt-24 pb-12">
        {/* Title */}
        <div className="text-center mb-12">
          <h1 className="text-3xl md:text-4xl font-bold mb-2">{result.title}</h1>
          <p className="text-gray-500">{result.slides.length} slides • Ready to present</p>
        </div>

        {/* Preview Cards */}
        <div className="space-y-4 mb-12">
          {result.slides.slice(0, 3).map((slide, i) => (
            <div key={i} className="border border-gray-200 rounded-xl p-5">
              <h3 className="font-semibold text-lg mb-3">{slide.title}</h3>
              {slide.points && slide.points.length > 0 && (
                <ul className="space-y-2">
                  {slide.points.map((point, j) => (
                    <li key={j} className="text-gray-600 text-sm flex items-start gap-2">
                      <span className="w-1 h-1 rounded-full bg-gray-400 mt-2 flex-shrink-0" />
                      {point}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          ))}
          
          {result.slides.length > 3 && (
            <p className="text-center text-sm text-gray-400 py-4">
              + {result.slides.length - 3} more slides
            </p>
          )}
        </div>

        {/* Actions */}
        <div className="space-y-4">
          {result.download_url && (
            <button
              onClick={handleDownload}
              className="w-full py-4 rounded-xl bg-black text-white font-medium text-lg hover:opacity-90 transition"
            >
              Download PPT
            </button>
          )}
          
          <button
            onClick={handleBack}
            className="w-full py-4 rounded-xl border border-gray-300 text-gray-700 font-medium hover:bg-gray-50 transition"
          >
            Generate Another
          </button>
        </div>

        {/* Trust badges */}
        <div className="mt-8 text-center text-sm text-gray-400 flex justify-center gap-4">
          <span>✓ Auto structured</span>
          <span>✓ Clean layout</span>
          <span>✓ Ready to present</span>
        </div>
      </div>
    </main>
  )
}
