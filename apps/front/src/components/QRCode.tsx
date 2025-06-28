'use client'
import { Box, Text, VStack } from '@devup-ui/react'
import { QRCodeCanvas } from 'qrcode.react'
import { useLayoutEffect, useState } from 'react'

import { getUUID } from '@/utils/get-uuid'

export function QRCode() {
  const [uuid, setUUID] = useState<string | null>(null)

  const isLoading = uuid === null

  useLayoutEffect(() => {
    setUUID(getUUID())
  }, [])

  return (
    <VStack alignItems="center" gap="20px">
      <Text
        color="#000"
        fontFamily="Pretendard"
        fontSize="24px"
        fontStyle="normal"
        fontWeight="600"
        letterSpacing="-0.02em"
        lineHeight="1em"
        textAlign="center"
      >
        사용자 QR
      </Text>
      {isLoading ? (
        <Box aspectRatio="1" bg="gray" boxSize="100%" />
      ) : (
        <QRCodeCanvas
          value={
            'https://uscode-silverguardian-api-627770884882.europe-west1.run.app/users/qr/' +
            uuid +
            '?lat=0&lon=0'
          }
        />
      )}
    </VStack>
  )
}
