'use client'

import { Button } from '@devup-ui/react'
import { useRouter } from 'next/navigation'

export function StartButton() {
  const router = useRouter()

  const handleClick = () => {
    router.push('/home')
  }

  return (
    <Button
      _hover={{ bg: '#45A049' }}
      bg="#4CAF50"
      border="none"
      borderRadius="12px"
      color="white"
      cursor="pointer"
      fontSize="18px"
      fontWeight="600"
      onClick={handleClick}
      px="48px"
      py="16px"
      w="100%"
    >
      시작하기
    </Button>
  )
}
