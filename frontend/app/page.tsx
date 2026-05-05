"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://192.168.10.105:3301"

export default function Home() {
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const router = useRouter()

  const handleGenerate = async () => {
    if (!input) {
      alert("Please paste a video link or text first")
      return
    }

    setLoading(true)

    try {
      const res = await fetch(`${API_BASE}/api/generate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ input })
      })

      if (!res.ok) {
        const error = await res.json()
        alert(error.detail || "Generation failed")
        setLoading(false)
        return
      }

      const data = await res.json()

      // 存储结果并跳转
      sessionStorage.setItem("pptResult", JSON.stringify(data))
      router.push("/result")

    } catch (err) {
      console.error(err)
      alert("Network error, please try again")
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen bg-white flex flex-col items-center justify-center px-6">

      {/* Logo */}
      <div className="absolute top-6 left-6 text-lg font-semibold">
        Presento
      </div>

      {/* 核心区 */}
      <div className="max-w-2xl w-full text-center space-y-8">

        {/* 标题 */}
        <h1 className="text-3xl md:text-4xl font-bold leading-tight">
          Turn any video into a <br />
          <span className="text-gray-500">
            ready-to-use presentation
          </span>
        </h1>

        {/* 输入框 */}
        <div className="w-full">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Paste video link or transcript..."
            className="w-full h-32 p-4 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-black resize-none"
          />
        </div>

        {/* 按钮 */}
        <button
          onClick={handleGenerate}
          disabled={loading}
          className="w-full py-4 rounded-xl bg-black text-white font-medium text-lg hover:opacity-90 transition"
        >
          {loading ? "Generating..." : "🔥 Generate Ready-to-Use PPT"}
        </button>

        {/* 辅助说明 */}
        <div className="text-sm text-gray-500 flex justify-center gap-4">
          <span>• Auto structured</span>
          <span>• Clean layout</span>
          <span>• Ready to present</span>
        </div>

      </div>

    </main>
  )
}
