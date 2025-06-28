// apps/admin/src/app/dispatch/page.tsx
'use client'

import { Box, Flex, Text } from '@devup-ui/react'
import Navbar from '../../components/navbar'
import Topbar from '../../components/topbar'
import { PatrolContent } from './PatrolContent'
import { CreatePatrol } from './CreatePatrol'

export default function DispatchPage() {
  return (
    <Box w="1440px" h="1024px" bg="#F7F7F7">
      <Flex h="100%">
        {/* 좌측 네비바 */}
        <Navbar />

        {/* 우측 메인 영역 */}
        <Box flex={1} h="100%" overflowY="auto">
          {/* 상단 바 */}
          <Topbar />

          <Box px="40px" py="24px">
            {/* 페이지 제목 */}
            <Text
              color="#000"
              fontFamily="Pretendard"
              fontSize="32px"
              fontWeight="600"
              mb="16px"
            >
              파견 관리
            </Text>
            <CreatePatrol />

            {/* 테이블 */}
            <table
              style={{
                width: '100%',
                borderCollapse: 'collapse',
                fontFamily: 'Pretendard',
                fontSize: '16px',
                color: '#000',
              }}
            >
              <thead
                style={{
                  background: '#EFEFEF',
                  borderBottom: '2px solid #CCC',
                }}
              >
                <tr>
                  {[
                    '아이디',
                    '파견 이름',
                    '유저 아이디',
                    '시작 시간',
                    '종료 시간',
                    '메모',
                    '순찰 여부',
                  ].map((header) => (
                    <th
                      key={header}
                      style={{
                        padding: '12px 8px',
                        textAlign: 'left',
                        fontWeight: 600,
                      }}
                    >
                      {header}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                <PatrolContent />
              </tbody>
            </table>
          </Box>
        </Box>
      </Flex>
    </Box>
  )
}
