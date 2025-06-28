// apps/admin/src/app/guardian/[id]/page.tsx
'use client'
export const runtime = 'nodejs'

import Link from 'next/link'
import { useState, useEffect } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { Box, Flex, Text } from '@devup-ui/react'
import Navbar from '../../../components/navbar'
import Topbar from '../../../components/topbar'

export default function GuardianDetailPage() {
  const { id } = useParams()
  const router = useRouter()

  // 가디언 이름 상태 (나중에 API에서 불러올 것)
  const [name, setName] = useState('')

  useEffect(() => {
    // TODO: 실제 API 호출하여 초기값 세팅
    setName('정해지지 않음')
  }, [id])

  const handleSave = () => {
    // TODO: API 호출하여 저장
    console.log(`Saving guardian ${id}: ${name}`)
    router.back()
  }

  const handleDelete = () => {
    // TODO: API 호출하여 삭제
    console.log(`Deleting guardian ${id}`)
    router.back()
  }

  return (
    <Box w="1440px" h="1024px" bg="#F7F7F7">
      <Flex h="100%">
        {/* 좌측 내비 */}
        <Navbar />

        {/* 우측 메인 */}
        <Box flex={1} h="100%" overflowY="auto">
          <Topbar />

          <Box px="40px" py="24px">
            {/* 뒤로 가기 버튼 */}
            <Link href="/guardian">
              <Text
                color="#4B8853"
                fontFamily="Pretendard"
                fontSize="16px"
                fontWeight="500"
                mb="16px"
                style={{ cursor: 'pointer' }}
              >
                &lt; 이전
              </Text>
            </Link>

            {/* 페이지 타이틀 */}
            <Text
              color="#000"
              fontFamily="Pretendard"
              fontSize="32px"
              fontWeight="600"
              mb="16px"
            >
              가디언 상세 관리
            </Text>

            {/* 편집 테이블 */}
            <table
              style={{
                width: '100%',
                borderCollapse: 'collapse',
                fontFamily: 'Pretendard',
              }}
            >
              <thead
                style={{
                  background: '#EFEFEF',
                  borderBottom: '2px solid #CCC',
                }}
              >
                <tr>
                  <th
                    style={{
                      padding: '12px 8px',
                      textAlign: 'left',
                      fontSize: '16px',
                      fontWeight: 600,
                    }}
                  >
                    이름
                  </th>
                  <th
                    style={{
                      padding: '12px 8px',
                      textAlign: 'left',
                      fontSize: '16px',
                      fontWeight: 600,
                    }}
                  >
                    삭제
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr style={{ borderBottom: '1px solid #DDD' }}>
                  <td style={{ padding: '12px 8px' }}>
                    <input
                      type="text"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      style={{
                        width: '60%',
                        padding: '6px 8px',
                        fontSize: '16px',
                        fontFamily: 'Pretendard',
                        border: '1px solid #CCC',
                        borderRadius: '4px',
                      }}
                    />
                    <button
                      onClick={handleSave}
                      style={{
                        marginLeft: '12px',
                        padding: '6px 12px',
                        fontSize: '14px',
                        color: '#FFF',
                        background: '#4B8853',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: 'pointer',
                      }}
                    >
                      저장
                    </button>
                  </td>
                  <td style={{ padding: '12px 8px' }}>
                    <button
                      onClick={handleDelete}
                      style={{
                        padding: '6px 12px',
                        fontSize: '14px',
                        color: '#E65C32',
                        border: '1px solid #E65C32',
                        borderRadius: '4px',
                        background: 'transparent',
                        cursor: 'pointer',
                      }}
                    >
                      삭제
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </Box>
        </Box>
      </Flex>
    </Box>
  )
}
