'use client'
import { useEffect } from 'react'

import { refreshUser } from '@/constants'

export function RefreshUser() {
  useEffect(() => {
    refreshUser()
  }, [])
  return null
}
