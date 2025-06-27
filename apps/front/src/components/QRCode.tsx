'use client'
import { Text, VStack } from '@devup-ui/react'
import { QRCodeCanvas } from 'qrcode.react'

export function QRCode() {
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
      <QRCodeCanvas value="https://reactjs.org/" />
    </VStack>
  )
}
