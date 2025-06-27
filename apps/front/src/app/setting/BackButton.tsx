'use client'

import { Flex, Image, Text } from '@devup-ui/react'
import { useRouter } from 'next/navigation'

export function BackButton() {
  const router = useRouter()
  return (
    <Flex
      alignItems="center"
      cursor="pointer"
      gap="8px"
      mb="24px"
      onClick={() => router.back()}
      role="button"
    >
      <Image boxSize="24px" role="button" src="/arrow.svg" />
      <Text fontSize="18px" fontWeight="600">
        이전
      </Text>
    </Flex>
  )
}
