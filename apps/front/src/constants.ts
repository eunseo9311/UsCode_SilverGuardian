import { getUUID } from './utils/get-uuid'

export let GlobalUser: {
  name: string
} | null = null
export function refreshUser() {
  fetch(
    `https://uscode-silverguardian-api-627770884882.europe-west1.run.app/users/${getUUID()}`,
  )
    .then((e) => e.json())
    .then((e) => {
      GlobalUser = e
    })
}
export function setUser(user: any) {
  GlobalUser = user
}
