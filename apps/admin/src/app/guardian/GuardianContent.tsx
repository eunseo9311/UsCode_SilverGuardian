'use client'
import { Input } from '@devup-ui/react'
import { useEffect, useState } from 'react'

export function GuardianContent() {
  const [guardians, setGuardians] = useState<any[]>([])
  useEffect(() => {
    fetch(
      'https://uscode-silverguardian-api-627770884882.europe-west1.run.app/users',
    )
      .then((e) => e.json())
      .then((e) => setGuardians(e))
  }, [])
  return guardians.map((g, idx) => (
    <tr
      key={g.id}
      style={
        idx < guardians.length - 1 ? { borderBottom: '1px solid #DDD' } : {}
      }
    >
      <td style={{ padding: '10px', fontSize: '14px' }}>{g.id}</td>
      <td style={{ padding: '10px', fontSize: '14px' }}>
        <Input
          bg="#DFDFDF"
          borderRadius="5px"
          color="#000"
          defaultValue={g.name}
          fontSize="14px"
          h="36px"
          onBlur={(e) => {
            e.stopPropagation()
            e.preventDefault()

            fetch(
              `https://uscode-silverguardian-api-627770884882.europe-west1.run.app/users/${g.id}`,
              {
                method: 'PUT',
                body: JSON.stringify({
                  name: e.target.value,
                  id: g.id,
                  lat: 0,
                  lon: 0,
                }),
                headers: {
                  'content-type': 'application/json',
                },
              },
            )
              .then((e) => e.json())
              .then((e) => {
                setGuardians(guardians.map((g) => (g.id === e.id ? e : g)))
              })
          }}
        />
      </td>
      <td style={{ padding: '10px', fontSize: '14px' }}>{g.address}</td>
      <td style={{ padding: '10px', fontSize: '14px' }}>{g.latlng}</td>
      <td style={{ padding: '12px 8px' }}>
        <button
          onClick={(e) => {
            e.stopPropagation()
            e.preventDefault()
            // TODO: 삭제 API 호출
            console.info('Deleting', g.id)
          }}
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
  ))
}
