// apps/admin/src/app/guardian/page.tsx
'use client'
export const runtime = 'nodejs'

import { Box, Flex, Text } from '@devup-ui/react'

import Navbar from '../../components/navbar'
import Topbar from '../../components/topbar'
import { GuardianContent } from './GuardianContent'

export default function GuardianPage() {
  return (
    <Box bg="#F7F7F7" h="1024px" w="1440px">
      <Flex h="100%">
        {/* 좌측 내비 */}
        <Navbar />

        {/* 우측 메인 */}
        <Box flex={1} h="100%" overflowY="auto">
          {/* 상단 바 */}
          <Topbar />

          <Box px="40px" py="24px">
            {/* 제목 */}
            <Text
              color="#000"
              fontFamily="Pretendard"
              fontSize="32px"
              fontWeight="600"
              mb="20px"
            >
              가디언 관리
            </Text>

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
                  {['아이디', '이름', '주소', '위도/경도', '삭제'].map((h) => (
                    <th
                      key={h}
                      style={{
                        padding: '12px 8px',
                        textAlign: 'left',
                        fontWeight: 600,
                        color: '#000',
                      }}
                    >
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                <GuardianContent />
              </tbody>
            </table>
          </Box>
        </Box>
      </Flex>
    </Box>
  )
}
