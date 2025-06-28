import { Box, Flex, Image, Text, VStack } from '@devup-ui/react'

import PatrolStartButton from '@/components/PatrolStartButton'

export default function Page() {
  return (
    <VStack alignItems="center" gap="40px">
      {/* --- 순찰 알림 섹션 */}
      <VStack alignItems="flex-start" gap="12px" w="100%">
        <Flex alignItems="center" gap="8px">
          <Image alt="alarm" boxSize="24px" src="/alarm.svg" />
          <Text color="#000" fontSize="18px" fontWeight="600">
            순찰 알림
          </Text>
        </Flex>

        <Box
          bg="#FFF"
          border="1px solid #4CAF50"
          borderRadius="14px"
          boxShadow="1px 1px 5px rgba(0,0,0,0.20)"
          px="20px"
          py="16px"
          w="100%"
        >
          <VStack alignItems="flex-start" gap="8px">
            <Text color="#000" fontSize="18px" fontWeight="600">
              순찰 지역 : 의성군 의성읍 태평리 15-3
            </Text>
            <Text color="#000" fontSize="18px" fontWeight="600">
              순찰 시간 : 6월 18일 15:00시
            </Text>
            <Text color="#000" fontSize="18px" fontWeight="600">
              순찰 인원 : 김의성, 송개발, 이코딩
            </Text>
          </VStack>
        </Box>
      </VStack>

      {/* --- 순찰 시작 버튼 */}
      <PatrolStartButton />

      {/* --- 건강 정보 섹션 */}
      <VStack alignItems="flex-start" gap="12px" w="100%">
        <Flex alignItems="center" gap="8px">
          <Image alt="health" boxSize="24px" src="/health.svg" />
          <Text color="#000" fontSize="18px" fontWeight="600">
            건강 정보
          </Text>
        </Flex>

        <Box
          bg="#FFF"
          border="1px solid #A9A7A7"
          borderRadius="12px"
          boxShadow="1px 1px 5px rgba(0,0,0,0.25)"
          px="20px"
          py="16px"
          w="100%"
        >
          <VStack alignItems="flex-start" gap="8px">
            <Text color="#000" fontSize="18px" fontWeight="600">
              걸음 수 : 4600보
            </Text>
            <Text color="#000" fontSize="18px" fontWeight="600">
              이동 거리 : 1.5km
            </Text>
          </VStack>
        </Box>
      </VStack>
    </VStack>
  )
}
