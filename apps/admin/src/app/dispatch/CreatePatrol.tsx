'use client'

import { Button, Input, Text, VStack } from "@devup-ui/react"
import { useState } from "react"

export function CreatePatrol() {
    const [name, setName] = useState('')
    const [start_lat, setStartLat] = useState(0)
    const [start_lon, setStartLon] = useState(0)
    const [start_time, setStartTime] = useState('')
    const [users, setUsers] = useState<string[]>([])


    return <VStack gap={2}>

        <Text color="gray">이름</Text>
        <Input
            value={name}
            onChange={(e) => setName(e.target.value)}
        />
        <Text color="gray">위도</Text>
        <Input
            value={start_lat}
            onChange={(e) => setStartLat(Number(e.target.value))}
        />
        <Text color="gray">경도</Text>
        <Input
            value={start_lon}
            onChange={(e) => setStartLon(Number(e.target.value))}
        />
        <Text color="gray">시작 시간</Text>
        <Input
            value={start_time}
            onChange={(e) => setStartTime(e.target.value)}
        />
        <Text color="gray">유저</Text>
        <Input
            value={users}
            onChange={(e) => setUsers(e.target.value.split(','))}
        />
        <Button
            onClick={() => {
                fetch('https://uscode-silverguardian-api-627770884882.europe-west1.run.app/patrols/start', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ name, start_lat, start_lon, start_time, users }),
                })
            }}
        >
            생성
        </Button>
    </VStack>
}