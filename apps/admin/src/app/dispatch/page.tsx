// apps/admin/src/app/dispatch/page.tsx
'use client'
export const runtime = 'nodejs'

import { Box, Flex, Text } from '@devup-ui/react'
import Navbar from '../../components/navbar'
import Topbar from '../../components/topbar'

const sampleDispatches = [
  {
    id: 1,
    location: '의성체육관',
    users: ['이코딩'],
    start: '05:20',
    end: '06:30',
    memo: '',
    patrol: true,
  },
  {
    id: 2,
    location: '의성시청',
    users: ['김코드', '이코딩'],
    start: '12:00',
    end: '12:40',
    memo: '',
    patrol: true,
  },
  {
    id: 3,
    location: '공원',
    users: ['송개발', '차맥북', '김그램'],
    start: '14:10',
    end: '15:30',
    memo: '',
    patrol: false,
  },
  {
    id: 4,
    location: '보건소',
    users: ['박깃헙', '유이썬'],
    start: '15:40',
    end: '16:50',
    memo: '',
    patrol: true,
  },
]

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
                    '유저 이름',
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
                {sampleDispatches.map((d) =>
                  d.users.map((user, idx) => (
                    <tr
                      key={`${d.id}-${idx}`}
                      style={
                        idx < d.users.length - 1
                          ? { borderBottom: '1px solid #DDD' }
                          : {}
                      }
                    >
                      {idx === 0 && (
                        <td
                          rowSpan={d.users.length}
                          style={{ padding: '12px 8px' }}
                        >
                          {d.id}
                        </td>
                      )}
                      {idx === 0 && (
                        <td
                          rowSpan={d.users.length}
                          style={{ padding: '12px 8px' }}
                        >
                          {d.location}
                        </td>
                      )}
                      <td style={{ padding: '12px 8px' }}>{user}</td>
                      {idx === 0 && (
                        <td style={{ padding: '12px 8px' }}>{d.start}</td>
                      )}
                      {idx === 0 && (
                        <td style={{ padding: '12px 8px' }}>{d.end}</td>
                      )}
                      {idx === 0 && (
                        <td style={{ padding: '12px 8px' }}>{d.memo}</td>
                      )}
                      {idx === 0 && (
                        <td style={{ padding: '12px 8px' }}>
                          {d.patrol ? 'true' : 'false'}
                        </td>
                      )}
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </Box>
        </Box>
      </Flex>
    </Box>
  )
}
