'use client'
import { useEffect, useState } from "react"

export function PatrolContent() {
    const [patrols, setPatrols] = useState<any[]>([])
    useEffect(() => {
        fetch('https://uscode-silverguardian-api-627770884882.europe-west1.run.app/patrols')
            .then(e => e.json())
            .then(e => setPatrols(e))
    }, [])
    return patrols.map((d) =>
        d.users.map((user: any, idx: number) => (
            <tr
                key={`${d.id}-${idx}`}
                style={
                    idx < d.users.length - 1
                        ? { borderBottom: '1px solid #DDD' }
                        : {}
                }
            >
                {idx === 0 && (
                    <td
                        rowSpan={d.users.length}
                        style={{ padding: '12px 8px' }}
                    >
                        {d.id}
                    </td>
                )}
                {idx === 0 && (
                    <td
                        rowSpan={d.users.length}
                        style={{ padding: '12px 8px' }}
                    >
                        {d.location}
                    </td>
                )}
                <td style={{ padding: '12px 8px' }}>{user.user_id}</td>
                {idx === 0 && (
                    <td style={{ padding: '12px 8px' }}>{d.start}</td>
                )}
                {idx === 0 && (
                    <td style={{ padding: '12px 8px' }}>{d.end}</td>
                )}
                {idx === 0 && (
                    <td style={{ padding: '12px 8px' }}>{d.memo}</td>
                )}
                {idx === 0 && (
                    <td style={{ padding: '12px 8px' }}>
                        {d.patrol ? 'true' : 'false'}
                    </td>
                )}
            </tr>
        ))
    )
}

