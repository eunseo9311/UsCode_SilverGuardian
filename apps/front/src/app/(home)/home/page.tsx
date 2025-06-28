import { Box, Flex, Image, Text, VStack } from '@devup-ui/react'

import { PatrolPanel } from './PatrolPanel'

export default function Page() {
  return (
    <VStack alignItems="center" gap="40px">
      {/* --- 순찰 알림 섹션 */}
      <PatrolPanel />

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
              걸음 수 : 0보
            </Text>
            <Text color="#000" fontSize="18px" fontWeight="600">
              이동 거리 : 0km
            </Text>
          </VStack>
        </Box>
      </VStack>
    </VStack>
  )
}
