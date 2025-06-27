import { Center, css, Image, Text, VStack } from '@devup-ui/react'

import { MotionBox } from '@/components/motion'
import { QRCode } from '@/components/QRCode'
import { StartButton } from '@/components/StartButton'

export default function HomePage() {
  return (
    <Center h="100dvh">
      <VStack alignItems="center" mx="auto" transform="translateY(-80px)">
        <MotionBox
          animate={{
            scale: 0.8,
            y: -40,
          }}
          initial={{
            scale: 1,
          }}
          transition={{
            ease: 'easeInOut',
          }}
        >
          <Image boxSize="180px" src="logo.svg" />
        </MotionBox>

        <MotionBox
          animate={{
            scale: [0, 1.1, 1],
            height: [0, 100, 100],
          }}
          initial={{
            scale: 0,
            height: 0,
          }}
          transition={{
            delay: 0.3,
          }}
        >
          <Center>
            <QRCode />
          </Center>
        </MotionBox>

        <MotionBox
          animate={{
            scale: 0.8,
            y: 100,
            marginTop: 0,
          }}
          initial={{
            scale: 1,
            marginTop: 60,
          }}
          transition={{
            ease: 'easeInOut',
          }}
        >
          <Center>
            <Text
              color="#4B8853"
              fontFamily="Pretendard"
              fontSize="36px"
              fontStyle="normal"
              fontWeight="800"
              letterSpacing="0.2em"
              lineHeight="1.3em"
              textAlign="center"
            >
              SILVER
              <br />
              GUARDIAN
            </Text>
          </Center>
        </MotionBox>

        {/* ✅ "시작하기" 버튼 */}
        <MotionBox
          animate={{
            opacity: 1,
            y: 120,
          }}
          className={css({ w: '100%' })}
          initial={{
            opacity: 0,
            y: 140,
          }}
          transition={{
            delay: 0.6,
            ease: 'easeInOut',
          }}
        >
          <StartButton />
        </MotionBox>
      </VStack>
    </Center>
  )
}
