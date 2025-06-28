// components/topbar.tsx
'use client'

import { Box, Flex, Text, Image } from '@devup-ui/react'

export default function Topbar() {
  return (
    <Box w="100%" h="100px" bg="#6F6F6F">
      <Flex alignItems="center" h="100%" px="24px">
        {/* 빈 공간으로 밀어내기 */}
        <Box flex={1} />

        <Text
          color="#FFF"
          fontFamily="Pretendard"
          fontSize="32px"
          fontWeight="600"
          lineHeight="1em"
          letterSpacing="0em"
        >
          환영합니다! 김의성님
        </Text>
        <Image
          src="/logo2.svg"
          alt="Logo"
          boxSize="64px"
          h="64px"
        />
      </Flex>
    </Box>
  )
}
