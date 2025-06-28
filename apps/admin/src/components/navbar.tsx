// components/navbar.tsx
'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Box, VStack, Text, Center } from '@devup-ui/react'

const navItems = [
  { label: '대시보드', path: '/dashboard' },
  { label: '파견 관리', path: '/dispatch' },
  { label: '가디언 관리', path: '/guardian' },
]

export default function Navbar() {
  const pathname = usePathname()

  return (
    <Box
      w="250px"
      h="100vh"
      bg="#F0F0F0"               // 전체 바탕을 좀 밝은 그레이로
      display="flex"
      flexDirection="column"
      alignItems="center"
      pt="40px"
      boxShadow="2px 0 4px rgba(0,0,0,0.1)"
    >
      {/* 로고 영역 */}
      <Center mb="60px">
        <Text
          color="#4B8853"
          fontFamily="Pretendard"
          fontSize="24px"
          fontWeight="800"
          lineHeight="1.3em"
          letterSpacing="0.2em"
          textAlign="center"
        >
          SIVER<br />GUARDIAN
        </Text>
      </Center>

      {/* 네비 메뉴 */}
      <VStack w="100%" padding="20px">
        {navItems.map(({ label, path }) => {
          const isActive = pathname === path
          return (
            <Link key={path} href={path} style={{ width: '100%' }}>
              <Center
                as="button"
                w="90%"
                h="60px"
                bg={isActive ? '#D7D7D7' : '#FFFFFF'}
                boxShadow={isActive ? 'none' : '0 2px 4px rgba(0,0,0,0.1)'}
                borderRadius="8px"
                _hover={{ cursor: 'pointer', boxShadow: '0 4px 8px rgba(0,0,0,0.15)' }}
                transition="box-shadow 0.2s"
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
