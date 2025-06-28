'use client'
import { Box, Flex, Image, Text, VStack } from '@devup-ui/react'
import dayjs from 'dayjs'
import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'

import PatrolStartButton from '@/components/PatrolStartButton'
import { getUUID } from '@/utils/get-uuid'

export function PatrolPanel() {
  const [patrolData, setPatrolData] = useState<any>(null)

  useEffect(() => {
    const fetchPatrolData = async () => {
      const response = await fetch(
        `https://uscode-silverguardian-api-627770884882.europe-west1.run.app/patrols/user/${getUUID()}/scheduled`,
        {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        },
      )
      const data = await response.json()
      if (data.length && !data[0].active) {
        setPatrolData(data[0])
      }
    }
    fetchPatrolData()
  }, [])

  const router = useRouter()

  if (!patrolData) return null

  const disabled = dayjs(patrolData.start_time).isAfter(dayjs())

  return (
    <>
      <VStack alignItems="flex-start" gap="12px" w="100%">
        <Flex alignItems="center" gap="8px">
          <Image alt="alarm" boxSize="24px" src="/alarm.svg" />
          <Text color="#000" fontSize="18px" fontWeight="600">
            순찰 알림
          </Text>
        </Flex>

        <Box
          bg="#FFF"
          border="1px solid #4CAF50"
          borderRadius="14px"
          boxShadow="1px 1px 5px rgba(0,0,0,0.20)"
          px="20px"
          py="16px"
          w="100%"
        >
          <VStack alignItems="flex-start" gap="8px">
            <Text color="#000" fontSize="18px" fontWeight="600">
              순찰 지역 : {patrolData.name}
            </Text>
            <Text color="#000" fontSize="18px" fontWeight="600">
              순찰 시간 :{' '}
              {dayjs(patrolData.start_time).format('YYYY-MM-DD HH:mm:ss')}
            </Text>
            <Text color="#000" fontSize="18px" fontWeight="600">
              순찰 인원 : {patrolData.users.length}명
            </Text>
          </VStack>
        </Box>
      </VStack>
      <PatrolStartButton
        disabled={disabled}
        onClick={() => {
          if (!disabled) router.push(`/patrol?patrol_id=${patrolData.id}`)
        }}
      />
    </>
  )
}
