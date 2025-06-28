// components/navbar.tsx
'use client'

import { Box, Center, Text, VStack } from '@devup-ui/react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

const navItems = [
  { label: '대시보드', path: '/dashboard' },
  { label: '파견 관리', path: '/dispatch' },
  { label: '가디언 관리', path: '/guardian' },
]

export default function Navbar() {
  const pathname = usePathname()

  return (
    <Box
      alignItems="center"
      bg="#F0F0F0"
      display="flex"
      flexDirection="column"
      h="100vh"
      justifyContent="center"
      pb="0"
      pt="0"
      transform="translateY(-70px)"
      w="260px"
    >
      {/* 로고 영역 */}
      <Center mb="80px">
        <Text
          color="#4B8853"
          fontFamily="Pretendard"
          fontSize="24px"
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

      {/* 네비 메뉴 */}
      <VStack gap="24px" padding="0" w="100%">
        {navItems.map(({ label, path }) => {
          const isActive = pathname === path
          return (
            <Link key={path} href={path} style={{ width: '100%' }}>
              <Center
                _hover={{
                  cursor: 'pointer',
                  background: '#E5E5E5',
                }}
                as="button"
                bg={isActive ? '#D7D7D7' : '#F0F0F0'}
                borderBottom="1px solid #E0E0E0"
                borderRadius="0"
                boxShadow="none"
                h="80px"
                transition="background 0.2s"
                w="100%"
              >
                <Text
                  color="#000"
                  fontFamily="Pretendard"
                  fontSize="28px"
                  fontWeight="600"
                  lineHeight="1"
                >
                  {label}
                </Text>
              </Center>
            </Link>
          )
        })}
      </VStack>
    </Box>
  )
}
