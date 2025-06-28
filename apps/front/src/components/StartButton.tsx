'use client'

import { Box, Button, Text } from '@devup-ui/react'
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
    <Box alignItems="center" display="flex" flexDirection="column" width="100%">
      <Button
        _hover={{ bg: '#45A049' }}
        bg="#4CAF50"
        border="none"
        borderRadius="12px"
        color="white"
        cursor="pointer"
        fontSize="18px"
        fontWeight="600"
        maxW="400px" // 최대 너비 지정 (필요에 따라 조정)
        mx="auto" // 가운데 정렬
        onClick={handleClick}
        px="24px" // 좌우 padding 조정
        py="16px"
        w="100%" // 부모 컨테이너에 맞춰 늘어나되, padding 덕분에 벽과 붙지 않음
      >
        시작하기
      </Button>

      {error && (
        <Text
          color="red"
          fontSize="16px"
          mt="8px" // 버튼과 약간 띄우기
          textAlign="center" // 가운데 정렬
          width="100%" // 전체 너비 사용
        >
          인증이 된 유저가 아닙니다.
        </Text>
      )}
    </Box>
  )
}
