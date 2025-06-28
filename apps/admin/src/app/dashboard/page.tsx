'use client'
export const runtime = 'nodejs' 

import { Flex, Box } from '@devup-ui/react'

import Navbar from '../../components/navbar'
import Topbar from '../../components/topbar'
import Danger from '../../components/danger'

export default function DashboardPage() {
  return (
    // 전체 화면 컨테이너 (1440×1024)
    <Box w="1440px" h="1024px" bg="#F7F7F7">
      <Flex h="100%">
        {/* 좌측 네비바 (250px) */}
        <Navbar />

        {/* 우측 메인 영역 */}
        <Box flex="1" h="100%">
          {/* 상단 바 (116px) */}
          <Topbar />

          {/* 콘텐츠 영역: 산불위험지수 + 지도 */}
          <Flex
            px="40px"
            py="24px"
            gap="40px"
            h="calc(100% - 116px)"
          >
            {/* 좌측: Danger 컴포넌트 (195px 너비) */}
            <Danger />

            {/* 우측: 지도 영역 */}
            <Box
              flex="1"
              bg="#FFF"
              borderRadius="16px"
              // 필요에 따라 그림자, overflow 등 추가 가능
            />
          </Flex>
        </Box>
      </Flex>
    </Box>
  )
}
