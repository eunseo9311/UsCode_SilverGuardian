'use client'

import { Button, Text } from '@devup-ui/react'
import { useRouter } from 'next/navigation'
import { useLayoutEffect, useState } from 'react'

import { setUser } from '@/constants'
import { getUUID } from '@/utils/get-uuid'

export function StartButton() {
  const [error, setError] = useState(false)
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
      .then((e) => {
        if (e.status === 404) {
          setError(true)
          throw new Error('인증이 된 유저가 아닙니다.')
        }
        return e.json()
      })
      .then((e) => {
        router.push('/home')
        localStorage.setItem('isAuth', 'true')
        setUser(e)
      })
  }

  return (
    <Button
      _hover={{ bg: '#45A049' }}
      bg={error ? '#FF0000' : '#4CAF50'}
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
      시작하기 {error && <Text color="red">인증이 된 유저가 아닙니다.</Text>}
    </Button>
  )
}
