// components/topbar.tsx
'use client'

import { Box, Flex, Image, Text } from '@devup-ui/react'

export default function Topbar() {
  return (
    <Box bg="#6F6F6F" h="100px" w="100%">
      <Flex alignItems="center" h="100%" px="24px">
        {/* 빈 공간으로 밀어내기 */}
        <Box flex={1} />

        <Text
          color="#FFF"
          fontFamily="Pretendard"
          fontSize="32px"
          fontWeight="600"
          letterSpacing="0em"
          lineHeight="1em"
        >
          환영합니다! 김의성님
        </Text>
        <Image alt="Logo" boxSize="64px" h="64px" src="/logo2.svg" />
      </Flex>
    </Box>
  )
}
