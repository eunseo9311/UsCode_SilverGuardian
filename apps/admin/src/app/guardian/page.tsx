// apps/admin/src/app/guardian/page.tsx
'use client'
export const runtime = 'nodejs'

import Link from 'next/link'
import { Box, Flex, Text } from '@devup-ui/react'
import Navbar from '../../components/navbar'
import Topbar from '../../components/topbar'

const sampleGuardians = Array.from({ length: 7 }).map((_, i) => ({
  id: '9f98058b-79ee-42f9-9c8a-fdcc42d90f29',
  name: '정해지지 않음',
  address: '의성리 의성읍 13-5',
  latlng: '36.3400 / 128.7200',
}))

export default function GuardianPage() {
  return (
    <Box w="1440px" h="1024px" bg="#F7F7F7">
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
              mb="16px"
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
                {sampleGuardians.map((g, idx) => (
                  <Link
                    key={idx}
                    href={`/guardian/IDpage?id=${encodeURIComponent(g.id)}`}
                    style={{ display: 'table-row', textDecoration: 'none' }}
                  >
                    <tr
                      style={
                        idx < sampleGuardians.length - 1
                          ? { borderBottom: '1px solid #DDD' }
                          : {}
                      }
                    >
                      <td style={{ padding: '12px 8px', fontSize: '14px' }}>
                        {g.id}
                      </td>
                      <td style={{ padding: '12px 8px', fontSize: '14px' }}>
                        {g.name}
                      </td>
                      <td style={{ padding: '12px 8px', fontSize: '14px' }}>
                        {g.address}
                      </td>
                      <td style={{ padding: '12px 8px', fontSize: '14px' }}>
                        {g.latlng}
                      </td>
                      <td style={{ padding: '12px 8px' }}>
                        <button
                          style={{
                            padding: '6px 12px',
                            fontSize: '14px',
                            color: '#E65C32',
                            border: '1px solid #E65C32',
                            borderRadius: '4px',
                            background: 'transparent',
                            cursor: 'pointer',
                          }}
                          onClick={(e) => {
                            e.stopPropagation()
                            e.preventDefault()
                            // TODO: 삭제 API 호출
                            console.log('Deleting', g.id)
                          }}
                        >
                          삭제
                        </button>
                      </td>
                    </tr>
                  </Link>
                ))}
              </tbody>
            </table>
          </Box>
        </Box>
      </Flex>
    </Box>
  )
}
