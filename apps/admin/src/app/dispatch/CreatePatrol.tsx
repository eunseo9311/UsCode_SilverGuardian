'use client'

import { Button, Input, Text, VStack } from '@devup-ui/react'
import { useState } from 'react'

export function CreatePatrol() {
  const [name, setName] = useState('')
  const [start_lat, setStartLat] = useState(0)
  const [start_lon, setStartLon] = useState(0)
  const [start_time, setStartTime] = useState('')
  const [users, setUsers] = useState<string[]>([])

  return (
    <VStack gap={2} mb={8}>
      <Text color="#000" fontSize="18px" mt="10px">
        이름
      </Text>
      <Input
        bg="#FFFFFF"
        border="1px solid #333333"
        borderRadius="8px"
        color="#000"
        fontSize="16px"
        h="42px"
        onChange={(e) => setName(e.target.value)}
        value={name}
        w="100%"
      />
      <Text color="#000" fontSize="18px">
        위도
      </Text>
      <Input
        bg="#FFFFFF"
        border="1px solid #333333"
        borderRadius="8px"
        color="#000"
        fontSize="16px"
        h="42px"
        onChange={(e) => setStartLat(Number(e.target.value))}
        value={start_lat}
        w="100%"
      />
      <Text color="#000" fontSize="18px">
        경도
      </Text>
      <Input
        bg="#FFFFFF"
        border="1px solid #333333"
        borderRadius="8px"
        color="#000"
        fontSize="16px"
        h="42px"
        onChange={(e) => setStartLon(Number(e.target.value))}
        value={start_lon}
        w="100%"
      />
      <Text color="#000" fontSize="18px">
        시작 시간
      </Text>
      <Input
        bg="#FFFFFF"
        border="1px solid #333333"
        borderRadius="8px"
        color="#000"
        fontSize="16px"
        h="42px"
        onChange={(e) => setStartTime(e.target.value)}
        value={start_time}
        w="100%"
      />
      <Text color="#000" fontSize="18px">
        유저
      </Text>
      <Input
        bg="#FFFFFF"
        border="1px solid #333333"
        borderRadius="8px"
        color="#000"
        fontSize="16px"
        h="42px"
        onChange={(e) => setUsers(e.target.value.split(','))}
        value={users}
        w="100%"
      />
      <Button
        bg="#4CAF50"
        borderRadius="10px"
        color="#fff"
        fontSize="20px"
        h="60px"
        mb={6}
        mt={2}
        onClick={() => {
          fetch(
            'https://uscode-silverguardian-api-627770884882.europe-west1.run.app/patrols/start',
            {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({
                name,
                start_lat,
                start_lon,
                start_time,
                users,
              }),
            },
          )
        }}
        w="100%"
      >
        생성
      </Button>
    </VStack>
  )
}
