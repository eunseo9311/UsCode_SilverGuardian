import { Box, Center, css, Flex, Image, Text, VStack } from '@devup-ui/react'

export default function HomePage() {
  return (
    <Box bg="#F7F7F7" h="844px">
      <VStack gap="8px" w="342px">
        <Text color="$blackTitle" typography="m">
          식사
        </Text>
        <Box h="162px">
          <Box
            bg="$white"
            border="1px solid $grayPrimary"
            borderRadius="10px"
            boxShadow="0px 0px 5px 0px rgba(0, 0, 0, 0.05)"
            h="162px"
            w="100%"
          />
          <VStack gap="14px" w="276.618px">
            <Flex alignItems="center" gap="16px">
              <svg
                className={css({ color: '$orangePrimary' })}
                fill="none"
                height="30"
                viewBox="0 0 31 30"
                width="31"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M0.182343 10C0.182343 4.47715 4.6595 0 10.1823 0H20.1823C25.7052 0 30.1823 4.47715 30.1823 10V20C30.1823 25.5228 25.7052 30 20.1823 30H10.1823C4.65949 30 0.182343 25.5228 0.182343 20V10Z"
                  fill="currentColor"
                />
                <path
                  d="M8.18234 15L14.1823 22"
                  stroke="white"
                  strokeLinecap="round"
                  strokeWidth="2.5"
                />
                <path
                  d="M22.1823 8L14.1823 22"
                  stroke="white"
                  strokeLinecap="round"
                  strokeWidth="2.5"
                />
              </svg>
              <Flex alignItems="center" gap="114px">
                <Text color="$blackTitle" textAlign="center" typography="m">
                  아침식사
                </Text>
                <Text color="$blackTitle" textAlign="right" typography="s">
                  08:30
                </Text>
              </Flex>
            </Flex>
            <Flex alignItems="center" gap="16px">
              <svg
                className={css({ color: '$orangePrimary' })}
                fill="none"
                height="30"
                viewBox="0 0 31 30"
                width="31"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M0.182343 10C0.182343 4.47715 4.6595 0 10.1823 0H20.1823C25.7052 0 30.1823 4.47715 30.1823 10V20C30.1823 25.5228 25.7052 30 20.1823 30H10.1823C4.65949 30 0.182343 25.5228 0.182343 20V10Z"
                  fill="currentColor"
                />
                <path
                  d="M8.18234 15L14.1823 22"
                  stroke="white"
                  strokeLinecap="round"
                  strokeWidth="2.5"
                />
                <path
                  d="M22.1823 8L14.1823 22"
                  stroke="white"
                  strokeLinecap="round"
                  strokeWidth="2.5"
                />
              </svg>
              <Flex alignItems="center" gap="114px">
                <Text color="$blackTitle" textAlign="center" typography="m">
                  점심식사
                </Text>
                <Text color="$blackTitle" textAlign="right" typography="s">
                  12:00
                </Text>
              </Flex>
            </Flex>
            <Flex alignItems="center" gap="16px">
              <svg
                className={css({ color: '$orangePrimary' })}
                fill="none"
                height="30"
                viewBox="0 0 31 30"
                width="31"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M0.182343 10C0.182343 4.47715 4.6595 0 10.1823 0H20.1823C25.7052 0 30.1823 4.47715 30.1823 10V20C30.1823 25.5228 25.7052 30 20.1823 30H10.1823C4.65949 30 0.182343 25.5228 0.182343 20V10Z"
                  fill="currentColor"
                />
                <path
                  d="M8.18234 15L14.1823 22"
                  stroke="white"
                  strokeLinecap="round"
                  strokeWidth="2.5"
                />
                <path
                  d="M22.1823 8L14.1823 22"
                  stroke="white"
                  strokeLinecap="round"
                  strokeWidth="2.5"
                />
              </svg>
              <Flex alignItems="center" gap="114px">
                <Text color="$blackTitle" textAlign="center" typography="m">
                  저녁식사
                </Text>
                <Text color="$blackTitle" textAlign="right" typography="s">
                  17:00
                </Text>
              </Flex>
            </Flex>
          </VStack>
        </Box>
      </VStack>
      <Box h="44px" w="100%">
        <svg
          className={css({ color: '$lightInk' })}
          fill="none"
          height="13"
          viewBox="0 0 18 13"
          width="18"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M9.00049 2.69984C11.6121 2.69995 14.1239 3.70936 16.0167 5.51942C16.1592 5.65916 16.387 5.6574 16.5274 5.51547L17.8899 4.13235C17.961 4.06036 18.0006 3.96285 18 3.86139C17.9994 3.75994 17.9586 3.6629 17.8867 3.59175C12.9188 -1.19725 5.08138 -1.19725 0.113468 3.59175C0.0415041 3.66284 0.000672511 3.75985 8.9596e-06 3.86131C-0.000654709 3.96277 0.0389042 4.06031 0.109932 4.13235L1.47278 5.51547C1.61307 5.65762 1.84107 5.65938 1.98351 5.51942C3.87652 3.70924 6.38859 2.69983 9.00049 2.69984ZM9.00049 7.19971C10.4354 7.19962 11.8191 7.73611 12.8828 8.70494C13.0267 8.84243 13.2533 8.83945 13.3935 8.69822L14.7544 7.3151C14.8261 7.24255 14.8658 7.14413 14.8648 7.04186C14.8638 6.9396 14.822 6.84201 14.7489 6.77094C11.5099 3.74028 6.49385 3.74028 3.25483 6.77094C3.18166 6.84201 3.13992 6.93964 3.13896 7.04195C3.138 7.14425 3.1779 7.24266 3.24972 7.3151L4.61021 8.69822C4.75045 8.83945 4.97707 8.84243 5.12094 8.70494C6.18388 7.73675 7.56651 7.20031 9.00049 7.19971ZM11.6158 10.5006C11.6886 10.4288 11.7287 10.3299 11.7266 10.2273C11.7245 10.1248 11.6804 10.0276 11.6048 9.95883C10.1014 8.67978 7.89957 8.67978 6.39618 9.95883C6.32049 10.0276 6.27636 10.1247 6.2742 10.2272C6.27204 10.3298 6.31206 10.4287 6.38479 10.5006L8.73924 12.8902C8.80824 12.9605 8.90233 13 9.00049 13C9.09866 13 9.19274 12.9605 9.26175 12.8902L11.6158 10.5006Z"
            fill="black"
          />
        </svg>
        <svg
          className={css({ color: '$lightInk' })}
          fill="none"
          height="13"
          viewBox="0 0 27 13"
          width="27"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M1.92307 3.20515C1.92307 2.49709 2.49706 1.9231 3.20512 1.9231H20.8333C21.5414 1.9231 22.1154 2.49709 22.1154 3.20515V9.29489C22.1154 10.0029 21.5414 10.5769 20.8333 10.5769H3.20512C2.49706 10.5769 1.92307 10.0029 1.92307 9.29489V3.20515Z"
            fill="black"
          />
          <path
            d="M20.833 0C22.6031 0 24.0381 1.43496 24.0381 3.20508V9.29492C24.0381 11.065 22.6031 12.5 20.833 12.5H3.20508C1.43497 12.5 2.68974e-05 11.065 0 9.29492V3.20508C2.69574e-05 1.43497 1.43497 2.72881e-05 3.20508 0H20.833ZM3.20508 0.961914C1.96602 0.961941 0.961941 1.96602 0.961914 3.20508V9.29492C0.961941 10.534 1.96602 11.5381 3.20508 11.5381H20.833C22.0721 11.5381 23.0771 10.534 23.0771 9.29492V3.20508C23.0771 1.966 22.0721 0.961914 20.833 0.961914H3.20508ZM25 4.22559C25.9185 4.44288 26.6025 5.26513 26.6025 6.25C26.6025 7.23487 25.9185 8.05712 25 8.27441V4.22559Z"
            fill="black"
            opacity="0.4"
          />
        </svg>
        <Image h="11px" src="reception" w="18.1494140625px" />
        <Text
          color="$lightInk"
          fontFamily="Pretendard"
          fontSize="18px"
          fontStyle="normal"
          fontWeight="600"
          letterSpacing="-0.02em"
          lineHeight="1"
          textAlign="center"
        >
          19:02
        </Text>
      </Box>
      <Text color="$blackTitle" textAlign="center" typography="l">
        로그인
      </Text>
      <Text color="$blackTitle" textAlign="center" typography="m">
        실버가디언
      </Text>
      <Center
        bg="$grayThird"
        borderRadius="12px"
        gap="10px"
        h="45px"
        px="19px"
        py="12px"
        w="316px"
      >
        <Text color="$blackTitle" textAlign="center" typography="s">
          회원가입
        </Text>
      </Center>
      <Flex alignItems="center" gap="21px">
        <Text color="$blackTitle" textAlign="center" typography="s">
          아이디 찾기
        </Text>
        <Text color="$blackTitle" textAlign="center" typography="s">
          |
        </Text>
        <Text color="$blackTitle" textAlign="center" typography="s">
          비밀번호 변경
        </Text>
      </Flex>
      <VStack gap="8px" w="308px">
        <Text color="$grayText" typography="mBold">
          아이디
        </Text>
        <Flex
          alignItems="center"
          border="1px solid $gray3"
          borderRadius="5px"
          gap="10px"
          h="45px"
          px="13px"
          py="10px"
        >
          <Text color="$grayPrimary" textAlign="center" typography="m">
            아이디를 입력해주세요.
          </Text>
        </Flex>
      </VStack>
      <VStack gap="8px" w="308px">
        <Text color="$grayText" typography="mBold">
          비밀번호
        </Text>
        <Flex
          alignItems="center"
          border="1px solid $gray3"
          borderRadius="5px"
          h="45px"
          justifyContent="space-between"
          px="13px"
          py="10px"
        >
          <Text color="$grayPrimary" textAlign="center" typography="m">
            비밀번호를 입력해주세요.
          </Text>
          <Image
            h="15.193585395812988px"
            src="Group 384"
            w="18.81770896911621px"
          />
        </Flex>
      </VStack>
      <Center
        bg="$success"
        borderRadius="12px"
        gap="10px"
        h="54px"
        px="10px"
        py="14px"
        w="316px"
      >
        <Text color="$fontWhite" textAlign="center" typography="button">
          로그인
        </Text>
      </Center>
    </Box>
  )
}
