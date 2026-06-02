'use client'

import { useEffect, useRef } from 'react'

interface Particle {
  x: number
  y: number
  vx: number
  vy: number
}

export default function NeuralBackgroundInteractive() {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const mouseRef = useRef({ x: 0, y: 0 })

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    let width = canvas.width = window.innerWidth
    let height = canvas.height = window.innerHeight

    const particleCount = 50
    const maxDistance = 180
    const particles: Particle[] = Array.from({ length: particleCount }).map(() => ({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * 0.7,
      vy: (Math.random() - 0.5) * 0.7,
    }))

    const draw = () => {
      ctx.clearRect(0, 0, width, height)

      // Move particles
      particles.forEach(p => {
        p.x += p.vx
        p.y += p.vy
        if (p.x < 0 || p.x > width) p.vx *= -1
        if (p.y < 0 || p.y > height) p.vy *= -1
      })

      // Draw connections
      for (let i = 0; i < particleCount; i++) {
        for (let j = i + 1; j < particleCount; j++) {
          const dx = particles[i].x - particles[j].x
          const dy = particles[i].y - particles[j].y
          const dist = Math.sqrt(dx * dx + dy * dy)

          // Plus la souris est proche, plus la ligne est opaque
          const mdx = (particles[i].x + particles[j].x) / 2 - mouseRef.current.x
          const mdy = (particles[i].y + particles[j].y) / 2 - mouseRef.current.y
          const mouseDist = Math.sqrt(mdx * mdx + mdy * mdy)

          if (dist < maxDistance && mouseDist < 300) {
            ctx.strokeStyle = `rgba(0,255,255,${1 - dist / maxDistance})`
            ctx.lineWidth = 1
            ctx.beginPath()
            ctx.moveTo(particles[i].x, particles[i].y)
            ctx.lineTo(particles[j].x, particles[j].y)
            ctx.stroke()
          }
        }
      }

      // Draw particles
      particles.forEach(p => {
        const dx = p.x - mouseRef.current.x
        const dy = p.y - mouseRef.current.y
        const distToMouse = Math.sqrt(dx * dx + dy * dy)
        const size = distToMouse < 150 ? 6 : 4
        const alpha = distToMouse < 150 ? 1 : 0.7
        ctx.fillStyle = `rgba(255,0,255,${alpha})`
        ctx.beginPath()
        ctx.arc(p.x, p.y, size, 0, Math.PI * 2)
        ctx.fill()
      })

      requestAnimationFrame(draw)
    }

    draw()

    const handleResize = () => {
      width = canvas.width = window.innerWidth
      height = canvas.height = window.innerHeight
    }

    const handleMouseMove = (e: MouseEvent) => {
      mouseRef.current.x = e.clientX
      mouseRef.current.y = e.clientY
    }

    window.addEventListener('resize', handleResize)
    window.addEventListener('mousemove', handleMouseMove)
    return () => {
      window.removeEventListener('resize', handleResize)
      window.removeEventListener('mousemove', handleMouseMove)
    }

  }, [])

  return <canvas ref={canvasRef} className="absolute inset-0 -z-10" />
}