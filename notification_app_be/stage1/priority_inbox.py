import json
import urllib.request
import urllib.error
from datetime import datetime, timezone
import heapq

AUTH_URL = "http://4.224.186.213/evaluation-service/auth"
NOTIFS_URL = "http://4.224.186.213/evaluation-service/notifications"

# Credentials (from user input)
PAYLOAD = {
    "email": "mohammedarfath.r2022@vitstudent.ac.in",
    "name": "mohammed arfath",
    "rollNo": "22mis0479",
    "accessCode": "SfFuWg",
    "clientID": "9e0eb681-ab47-4e2e-b60c-d41a43222676",
    "clientSecret": "SETQygcTkzpQFtBB"
}

WEIGHT = {
    "Placement": 3,
    "Result": 2,
    "Event": 1
}


def post(url, body):
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.getcode(), json.load(resp)


def get_auth_token():
    code, resp = post(AUTH_URL, PAYLOAD)
    if isinstance(resp, dict):
        return resp.get("access_token") or resp.get("token")
    raise RuntimeError(f"Auth failed: {code} {resp}")


def fetch_notifications(token):
    req = urllib.request.Request(NOTIFS_URL, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=15) as nf:
        return json.load(nf).get("notifications", [])


def ts_to_epoch(ts_str):
    # expected format: YYYY-MM-DD HH:MM:SS
    dt = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
    dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp())


def top_n_notifications(notifs, n=10):
    # Maintain a min-heap of size n with (score, item) so smallest score at top
    heap = []
    for it in notifs:
        weight = WEIGHT.get(it.get("Type", "Event"), 1)
        epoch = ts_to_epoch(it.get("Timestamp"))
        # score: higher is better — use weight as primary, recency as secondary
        # combine into single integer: weight * 10^12 + epoch
        score = weight * 10**12 + epoch
        entry = (score, it)
        if len(heap) < n:
            heapq.heappush(heap, entry)
        else:
            # if current score greater than smallest, replace
            if entry[0] > heap[0][0]:
                heapq.heapreplace(heap, entry)
    # return sorted descending
    return sorted([h[1] for h in heap], key=lambda x: (WEIGHT.get(x.get("Type"), 1), ts_to_epoch(x.get("Timestamp"))), reverse=True)


def main():
    print("Requesting auth token...")
    token = get_auth_token()
    print("Fetching notifications...")
    notifs = fetch_notifications(token)
    print(f"Total notifications fetched: {len(notifs)}")
    top10 = top_n_notifications(notifs, n=10)
    print("\nTop notifications (priority inbox):")
    for i, nobj in enumerate(top10, 1):
        print(f"{i}. [{nobj.get('Type')}] {nobj.get('Message')} — {nobj.get('Timestamp')} (ID: {nobj.get('ID')})")


if __name__ == '__main__':
    main()
