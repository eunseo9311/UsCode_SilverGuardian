'use client'
import { useEffect, useRef } from 'react'

export const Map = () => {
  const mapEl = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const { kakao } = window as any
    if (!kakao) return

    kakao.maps.load(() => {
      if (!mapEl.current) return
      const center = new kakao.maps.LatLng(36.3852, 128.4362)
      const options = {
        center,
        level: 3,
      }

      new kakao.maps.Map(mapEl.current!, options)
    })
  }, [])

  return (
    <div
      ref={mapEl}
      style={{ width: '100%', height: '100%', minHeight: '300px' }}
    ></div>
  )
}
