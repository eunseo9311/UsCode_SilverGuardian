'use client'

import { VStack, Flex, Box, Text, Center, css, Image } from '@devup-ui/react'

export default function Danger() {
  return (
    <VStack w="195px" gap="41px">
      {/* 제목 */}
      <Text
        color="#000"
        fontFamily="Pretendard"
        fontSize="32px"
        fontWeight="600"
        lineHeight="1em"
        letterSpacing="0em"
      >
        산불위험지수
      </Text>

      {/* 색상 막대 + 단계 레이블 */}
      <Flex alignItems="center" gap="18px">
        {/* 컬러 바 */}
        <VStack w="124px" h="500px" border="3px solid #000" gap="0">
          <Box h="50px" bg="#002673" />
          <Box h="50px" bg="#004DA8" />
          <Box h="50px" bg="#0084A8" />
          <Box h="50px" bg="#00C5FF" />
          <Box h="50px" bg="#A3FF73" />
          <Box h="50px" bg="#D3FFBE" />
          <Box h="50px" bg="#FFFF73" />
          <Box h="50px" bg="#FFD37F" />
          <Box h="50px" bg="#FA0" />
          <Box h="50px" bg="#E60000" />
        </VStack>

        {/* 단계 텍스트 */}
        <VStack w="53px" gap="25px">
          {Array.from({ length: 10 }, (_, i) => (
            <Text
              key={i}
              color="#000"
              fontFamily="Pretendard"
              fontSize="18px"
              fontWeight="600"
              lineHeight="1em"
              letterSpacing="0em"
              textAlign={i === 0 || i === 8 ? 'center' : 'left'}
            >
              {i + 1}단계
            </Text>
          ))}
        </VStack>
      </Flex>
    </VStack>
  )
}
