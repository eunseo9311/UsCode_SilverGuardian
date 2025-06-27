import { Box, Text } from '@devup-ui/react'

import { BackButton } from './BackButton'
import { ProfileCard } from './ProfileCard'

export default function SettingPage() {
  return (
    <Box bg="#F5F5F5" h="100dvh" p="24px">
      {/* 상단 뒤로가기 */}
      <BackButton />

      {/* 회원 정보 타이틀 */}
      <Text fontSize="16px" fontWeight="600" mb="32px">
        회원 정보
      </Text>
      <Box pt="20px">
        <ProfileCard />
      </Box>
    </Box>
  )
}
