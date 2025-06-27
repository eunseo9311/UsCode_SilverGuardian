import { Box, Flex, Image } from '@devup-ui/react'
import Link from 'next/link'

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <Box bg="#FAFAFA" h="100dvh" pt="24px" px="26px">
      <Flex justifyContent="flex-end" mb="20px">
        <Link href="/setting">
          <Image boxSize="36px" role="button" src="/setting.svg" />
        </Link>
      </Flex>
      {children}
    </Box>
  )
}
