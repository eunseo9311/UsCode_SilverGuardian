import { Box, Flex, Image, Text } from '@devup-ui/react'
import Link from 'next/link'

import { RefreshUser } from './RefreshUser'

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <Box bg="#FAFAFA" h="100dvh" pt="24px" px="26px">
      <Flex alignItems="center" justifyContent="space-between" mb="20px">
        <Text
          color="#4B8853"
          fontFamily="Pretendard"
          fontSize="16px"
          fontStyle="normal"
          fontWeight="800"
          letterSpacing="0.2em"
          lineHeight="1.3em"
          textAlign="center"
        >
          SIVER GUARDIAN
        </Text>
        <Link href="/setting">
          <Image boxSize="36px" role="button" src="/setting.svg" />
        </Link>
      </Flex>
      {children}
      <RefreshUser />
    </Box>
  )
}
