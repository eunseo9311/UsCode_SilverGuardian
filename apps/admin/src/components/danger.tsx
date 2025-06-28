'use client'

import { Box, Flex, Text, VStack } from '@devup-ui/react'

export default function Danger() {
  return (
    <VStack gap="41px" w="195px">
      {/* 제목 */}
      <Text
        color="#000"
        fontFamily="Pretendard"
        fontSize="32px"
        fontWeight="600"
        letterSpacing="0em"
        lineHeight="1em"
      >
        산불위험지수
      </Text>

      {/* 색상 막대 + 단계 레이블 */}
      <Flex alignItems="center" gap="18px">
        {/* 컬러 바 */}
        <VStack border="3px solid #000" gap="0" h="500px" w="124px">
          <Box bg="#002673" h="50px" />
          <Box bg="#004DA8" h="50px" />
          <Box bg="#0084A8" h="50px" />
          <Box bg="#00C5FF" h="50px" />
          <Box bg="#A3FF73" h="50px" />
          <Box bg="#D3FFBE" h="50px" />
          <Box bg="#FFFF73" h="50px" />
          <Box bg="#FFD37F" h="50px" />
          <Box bg="#FA0" h="50px" />
          <Box bg="#E60000" h="50px" />
        </VStack>

        {/* 단계 텍스트 */}
        <VStack gap="25px" w="53px">
          {Array.from({ length: 10 }, (_, i) => (
            <Text
              key={i}
              color="#000"
              fontFamily="Pretendard"
              fontSize="18px"
              fontWeight="600"
              letterSpacing="0em"
              lineHeight="1em"
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
