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
      bg="#F0F0F0" // 전체 바탕을 좀 밝은 그레이로
      boxShadow="2px 0 4px rgba(0,0,0,0.1)"
      display="flex"
      flexDirection="column"
      h="100vh"
      pt="40px"
      w="250px"
    >
      {/* 로고 영역 */}
      <Center mb="60px">
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
      <VStack padding="20px" w="100%">
        {navItems.map(({ label, path }) => {
          const isActive = pathname === path
          return (
            <Link key={path} href={path} style={{ width: '100%' }}>
              <Center
                _hover={{
                  cursor: 'pointer',
                  boxShadow: '0 4px 8px rgba(0,0,0,0.15)',
                }}
                as="button"
                bg={isActive ? '#D7D7D7' : '#FFFFFF'}
                borderRadius="8px"
                boxShadow={isActive ? 'none' : '0 2px 4px rgba(0,0,0,0.1)'}
                h="60px"
                transition="box-shadow 0.2s"
                w="90%"
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
