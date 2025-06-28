'use client'

import { Button } from '@devup-ui/react'
import { useRouter } from 'next/navigation'
import { useLayoutEffect } from 'react'

import { setUser } from '@/constants'
import { getUUID } from '@/utils/get-uuid'

export function StartButton() {
  const router = useRouter()
  useLayoutEffect(() => {
    if (localStorage.getItem('isAuth') === 'true') {
      router.push('/home')
    }
  }, [router])

  const handleClick = () => {
    fetch(
      `https://uscode-silverguardian-api-627770884882.europe-west1.run.app/users/${getUUID()}`,
    )
      .then((e) => e.json())
      .then((e) => {
        router.push('/home')
        localStorage.setItem('isAuth', 'true')
        setUser(e)
      })
      .catch(() => {
        alert('인증이 된 유저가 아닙니다.')
      })
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
