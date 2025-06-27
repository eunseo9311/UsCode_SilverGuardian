import { Box, Center, css, Flex, Image, Text, VStack } from '@devup-ui/react'

export default function Page() {
  return (
    <VStack gap="70px">
      <VStack gap="20px">
        <VStack gap="12px">
          <Flex alignItems="center" gap="10px">
            <svg
              className={css({ color: '$success' })}
              fill="none"
              height="24"
              viewBox="0 0 20 24"
              width="20"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M10 0C4.48631 0 0.000101805 4.3068 0.000101805 9.594C-0.0361478 17.328 9.62001 23.7408 10 24C10 24 20.0362 17.328 19.9999 9.6C19.9999 4.3068 15.5137 0 10 0ZM10 14.4C7.23753 14.4 5.00005 12.252 5.00005 9.6C5.00005 6.948 7.23753 4.8 10 4.8C12.7625 4.8 15 6.948 15 9.6C15 12.252 12.7625 14.4 10 14.4Z"
                fill="currentColor"
              />
            </svg>
            <Text
              color="#000"
              fontFamily="Pretendard"
              fontSize="18px"
              fontStyle="normal"
              fontWeight="600"
              letterSpacing="0em"
              lineHeight="1em"
              textAlign="center"
            >
              지도
            </Text>
          </Flex>
          <Box filter="drop-shadow(4px 4px 4px rgba(0, 0, 0, 0.25))">
            <Box w="100%">
              <Box
                bg="#D9D9D9"
                border="1px solid $text"
                borderRadius="12px"
                w="100%"
              />
              <Image
                aspectRatio="239/518"
                bg="url(/path/to/image) lightgray 50% / cover no-repeat"
                border="1px solid $text"
                src="KakaoTalk_Photo_2025-06-27-19-33-38 1"
              />
            </Box>
          </Box>
        </VStack>
        <VStack gap="10px">
          <Flex alignItems="center" gap="6px">
            <Image alt="산불 아이콘" boxSize="24px" src="/fire.svg" />
            <Text
              color="#000"
              fontFamily="Pretendard"
              fontSize="18px"
              fontStyle="normal"
              fontWeight="600"
              letterSpacing="0em"
              lineHeight="1em"
              textAlign="center"
            >
              산불 위험도
            </Text>
          </Flex>
          <Flex
            alignItems="center"
            bg="#FFF"
            border="1px solid #FF752B"
            borderRadius="12px"
            gap="10px"
            h="64px"
            px="28px"
            py="23px"
          >
            <Text
              color="#000"
              fontFamily="Pretendard"
              fontSize="18px"
              fontStyle="normal"
              fontWeight="600"
              letterSpacing="0em"
              lineHeight="1em"
            >
              7단계 : 주의 요망
            </Text>
          </Flex>
        </VStack>
      </VStack>
      <VStack gap="40px">
        <Center
          bg="#FF752B"
          borderRadius="14px"
          cursor="pointer"
          gap="10px"
          h="70px"
          px="10px"
          py="14px"
        >
          <Text
            color="$fontWhite"
            fontFamily="Pretendard"
            fontSize="32px"
            fontStyle="normal"
            fontWeight="600"
            letterSpacing="-0.02em"
            lineHeight="1em"
            textAlign="center"
          >
            신고 버튼
          </Text>
        </Center>
        <Center
          bg="#FFF"
          border="2px solid #4B8853"
          borderRadius="14px"
          gap="10px"
          h="70px"
          px="10px"
          py="14px"
        >
          <Text
            color="#4B8853"
            fontFamily="Pretendard"
            fontSize="32px"
            fontStyle="normal"
            fontWeight="600"
            letterSpacing="-0.02em"
            lineHeight="1em"
            textAlign="center"
          >
            순찰 완료
          </Text>
        </Center>
      </VStack>
    </VStack>
  )
}
