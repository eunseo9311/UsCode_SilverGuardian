
import { Flex, Box } from '@devup-ui/react'
import { Map } from '../dashboard/Map'

import Navbar from '../../components/navbar'
import Topbar from '../../components/topbar'
import Danger from '../../components/danger'
import { VworldTable } from './table'

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
            /*h="calc(100% - 116px)"*/
          >
            {/* 좌측: Danger 컴포넌트 (195px 너비) */}
            <Danger />

            {/* 우측: 지도 영역 */}
            <Map />
          </Flex>
          <VworldTable />
        </Box>
      </Flex>
    </Box>
  )
}
