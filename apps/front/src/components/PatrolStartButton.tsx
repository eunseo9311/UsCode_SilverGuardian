import { Center, Text } from '@devup-ui/react'

interface PatrolStartButtonProps {
  disabled?: boolean
  onClick?: () => void
}

export default function PatrolStartButton({
  disabled = false,
  onClick,
}: PatrolStartButtonProps) {
  return (
    <Center
      bg={disabled ? '#D9D9D9' : '#4CAF50'}
      borderRadius="14px"
      cursor="pointer"
      h="70px"
      onClick={disabled ? undefined : onClick}
      px="10px"
      py="14px"
      role="button"
      style={{ cursor: disabled ? 'not-allowed' : 'pointer' }}
      w="100%"
    >
      <Text color="#FFF" fontSize="20px" fontWeight="600" textAlign="center">
        순찰 시작
      </Text>
    </Center>
  )
}
