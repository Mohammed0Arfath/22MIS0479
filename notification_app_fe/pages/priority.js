import Link from 'next/link'

const WEIGHT = { Placement:3, Result:2, Event:1 }

function computeScore(n){
  const epoch = Math.floor(new Date(n.Timestamp.replace(' ', 'T')+'Z').getTime()/1000)
  return (WEIGHT[n.Type]||1) * 1e12 + epoch
}

export default function Priority({ notifications, topN, filter }){
  const filtered = filter? notifications.filter(n => n.Type === filter) : notifications
  const sorted = filtered.slice().sort((a,b) => computeScore(b) - computeScore(a))
  const top = sorted.slice(0, topN)

  return (
    <div className="container">
      <div className="topbar">
        <h2>Priority Inbox — Top {topN} {filter? `(${filter})`:''}</h2>
        <div className="controls">
          <Link href="/"><a className="btn">All Notifications</a></Link>
        </div>
      </div>

      {top.map((n,i) => (
        <div key={n.ID} className="card">
          <strong>{i+1}. {n.Type}</strong> — {n.Message}
          <div className="meta">{n.Timestamp} — ID: {n.ID}</div>
        </div>
      ))}
    </div>
  )
}

export async function getServerSideProps(ctx){
  const fs = require('fs')
  const path = require('path')
  const root = path.resolve(process.cwd(), '..', '..')
  const tokenPath = path.join(root, 'stage1', 'token.json')
  let token = null
  try{ token = JSON.parse(fs.readFileSync(tokenPath,'utf8')).access_token }catch(e){}

  const res = await fetch('http://4.224.186.213/evaluation-service/notifications', { headers: token?{ Authorization: `Bearer ${token}` }:{} })
  const data = await res.json()
  const q = ctx.query || {}
  const topN = parseInt(q.n||'10',10) || 10
  const filter = q.type || null
  return { props: { notifications: data.notifications || [], topN, filter } }
}
