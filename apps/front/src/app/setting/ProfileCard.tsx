'use client'
import { Box, Button, Center, Text, VStack } from '@devup-ui/react'
import { AnimatePresence } from 'motion/react'
import { useState } from 'react'

import { MotionBox } from '@/components/motion'
import { QRCode } from '@/components/QRCode'

export function ProfileCard() {
  const [isOpen, setIsOpen] = useState(false)
  return (
    <>
      {/* 카드 컨테이너 */}
      <Box
        bg="#FFFFFF"
        borderRadius="12px"
        boxShadow="0 2px 6px rgba(0, 0, 0, 0.1)"
        p="20px"
      >
        <VStack gap="16px">
          <Text fontSize="16px">김의성님 안녕하세요.</Text>
          <Button
            bg="#4CAF50"
            border="none"
            borderRadius="12px"
            color="#FFFFFF"
            cursor="pointer"
            fontSize="16px"
            h="48px"
            onClick={() => {
              setIsOpen(true)
            }}
            role="button"
            w="100%"
          >
            사용자 QR
          </Button>
        </VStack>
      </Box>

      {/* QR 모달 */}
      <AnimatePresence>
        {isOpen && (
          <MotionBox
            animate={{
              opacity: 1,
            }}
            exit={{
              opacity: 0,
            }}
            initial={{
              opacity: 0,
            }}
          >
            <Box
              bg="rgba(0,0,0,0.5)"
              bottom="0"
              left="0"
              onClick={() => setIsOpen(false)}
              pos="fixed"
              right="0"
              top="0"
              zIndex={1000}
            >
              <Center h="100%">
                <MotionBox
                  animate={{
                    y: 0,
                  }}
                  exit={{
                    y: 24,
                  }}
                  initial={{
                    y: 24,
                  }}
                  transition={{
                    ease: 'easeInOut',
                  }}
                >
                  <Box
                    bg="#FFFFFF"
                    borderRadius="12px"
                    onClick={(e) => {
                      e.stopPropagation()
                    }}
                    p="24px"
                    position="relative"
                    transform="scale(1.5)"
                    transformOrigin="center"
                  >
                    {/* 닫기 */}
                    <Text
                      cursor="pointer"
                      fontSize="20px"
                      onClick={() => setIsOpen(false)}
                      position="absolute"
                      right="12px"
                      role="button"
                      top="12px"
                    >
                      ×
                    </Text>
                    {/* QR 코드 */}
                    <Center>
                      <QRCode />
                    </Center>
                  </Box>
                </MotionBox>
              </Center>
            </Box>
          </MotionBox>
        )}
      </AnimatePresence>
    </>
  )
}
