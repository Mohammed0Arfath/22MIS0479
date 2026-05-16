import { useEffect, useState } from 'react'
import Link from 'next/link'

function NotificationCard({ n, markViewed }){
  return (
    <div className="card">
      <div style={{display:'flex', justifyContent:'space-between'}}>
        <div>
          <strong>{n.Type}</strong> — {n.Message}
          <div className="meta">{n.Timestamp} — ID: {n.ID}</div>
        </div>
        <div>
          <button onClick={() => markViewed(n.ID)} className="btn">Mark viewed</button>
        </div>
      </div>
    </div>
  )
}

export default function Index({ notifications }){
  const [viewed, setViewed] = useState(new Set())

  useEffect(()=>{
    try{
      const v = JSON.parse(localStorage.getItem('viewed')||'[]')
      setViewed(new Set(v))
    }catch(e){ }
  },[])

  function markViewed(id){
    const s = new Set(viewed)
    s.add(id)
    setViewed(s)
    localStorage.setItem('viewed', JSON.stringify(Array.from(s)))
  }

  return (
    <div className="container">
      <div className="topbar">
        <h2>All Notifications</h2>
        <div className="controls">
          <Link href="/priority"><a className="btn">Priority Inbox</a></Link>
        </div>
      </div>

      {notifications.map(n => (
        <div key={n.ID} style={{opacity: viewed.has(n.ID)?0.6:1}}>
          <NotificationCard n={n} markViewed={markViewed} />
        </div>
      ))}
    </div>
  )
}

export async function getServerSideProps(){
  const fs = require('fs')
  const path = require('path')
  const root = path.resolve(process.cwd(), '..', '..') // project root C:\Users\moham\Afford
  // token path relative to repo root
  const tokenPath = path.join(root, 'stage1', 'token.json')
  let token = null
  try{
    const raw = fs.readFileSync(tokenPath, 'utf8')
    token = JSON.parse(raw).access_token
  }catch(e){ }

  const res = await fetch('http://4.224.186.213/evaluation-service/notifications', { headers: token?{ Authorization: `Bearer ${token}` }:{} })
  const data = await res.json()
  return { props: { notifications: data.notifications || [] } }
}
