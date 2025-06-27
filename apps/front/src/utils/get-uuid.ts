import { v4 as uuidv4 } from 'uuid'

export function getUUID() {
  const userId = localStorage.getItem('userId')

  if (!userId) {
    const newUUID = uuidv4()
    localStorage.setItem('userId', newUUID)
    return newUUID
  }
  return userId
}
