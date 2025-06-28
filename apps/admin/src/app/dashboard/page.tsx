import { Box, Flex, VStack } from '@devup-ui/react'

import Danger from '../../components/danger'
import Navbar from '../../components/navbar'
import Topbar from '../../components/topbar'
import { Map } from '../dashboard/Map'
import { Table } from './table'

export default function DashboardPage() {
  return (
    // 전체 화면 컨테이너 (1440×1024)
    <Box bg="#F7F7F7">
      <Flex h="100%">
        {/* 좌측 네비바 (250px) */}
        <Navbar />

        {/* 우측 메인 영역 */}
        <Box flex="1" h="100%">
          {/* 상단 바 (116px) */}
          <Topbar />

          {/* 콘텐츠 영역: Danger + Map + Table 세로 배치 */}
          <Flex
            flexDirection="column"
            gap="40px"
            px="40px"
            py="24px"
            /* h="calc(100% - 116px)"*/
          >
            {/* Danger + Map 가로 배치 */}
            <Flex gap="40px">
              {/* 좌측: Danger 컴포넌트 (195px 너비) */}
              <Danger />
              {/* 우측: 지도 영역 */}
              <VStack flex="1">
                <Map />
                <Table />
              </VStack>
            </Flex>
          </Flex>
        </Box>
      </Flex>
    </Box>
  )
}
