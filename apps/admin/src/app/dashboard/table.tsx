'use client'

import { Box } from '@devup-ui/react'
import { useEffect, useState } from 'react'

export function Table() {
  const [data, setData] = useState<Record<string, number>>({})

  // 1) vworld API 에서 실시간 데이터 가져오기
  useEffect(() => {
    fetch(
      'https://uscode-silverguardian-api-627770884882.europe-west1.run.app/vworld',
    )
      .then((res) => {
        if (!res.ok) throw new Error('네트워크 에러')
        return res.json() as Promise<Record<string, any>>
      })
      .then((json) => setData(json['message']))
      .catch(console.error)
  }, [])

  // 2) [ [ [key,val], …6개 ], [ … ], [ … ] ] 형태로 자르기
  const entries = Object.entries(data)
  const rows: [string, number][][] = []
  for (let i = 0; i < entries.length; i += 6) {
    rows.push(entries.slice(i, i + 6))
  }

  // 3) 셀 스타일 (너비 절반으로)
  const tdStyle: React.CSSProperties = {
    border: '1px solid black',
    padding: '8px 2px',
    textAlign: 'center',
    fontSize: '14px',
    color: 'black', // 전체 너비의 절반 정도(16.66% → 8.33%)
    whiteSpace: 'nowrap', // 텍스트 줄바꿈 방지
    overflow: 'hidden',
    textOverflow: 'ellipsis',
  }

  return (
    <Box minW="700px" mt="24px" mx="auto" px="30px">
      <Box
        as="table"
        borderCollapse="collapse"
        color="black"
        tableLayout="fixed"
        w="100%"
      >
        <tbody>
          {rows.map((row, ri) => (
            <tr key={ri}>
              {row.map(([region, value]) => (
                <td key={region} style={tdStyle}>
                  {region}: {value}
                </td>
              ))}
              {row.length < 6 &&
                Array.from({ length: 6 - row.length }).map((_, i) => (
                  <td key={`empty-${i}`} style={tdStyle} />
                ))}
            </tr>
          ))}
        </tbody>
      </Box>
    </Box>
  )
}
