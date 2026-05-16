import json, urllib.request, urllib.error

register_url = "http://4.224.186.213/evaluation-service/register"
auth_url = "http://4.224.186.213/evaluation-service/auth"
notifications_url = "http://4.224.186.213/evaluation-service/notifications"

payload = {
    "email": "mohammedarfath.r2022@vitstudent.ac.in",
    "name": "mohammed arfath",
    "rollNo": "22mis0479",
    "accessCode": "SfFuWg",
    "clientID": "9e0eb681-ab47-4e2e-b60c-d41a43222676",
    "clientSecret": "SETQygcTkzpQFtBB"
}

def post(url, body):
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type":"application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.getcode(), json.load(resp)
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.load(e)
        except Exception:
            return e.code, e.read().decode()
    except Exception as e:
        return None, str(e)

code_reg, resp_reg = post(register_url, {k:v for k,v in payload.items() if k in ["email","name","mobileNo","githubUsername","rollNo","accessCode"]})
print("REGISTER_STATUS:", code_reg)
print(json.dumps(resp_reg, indent=2))

code_auth, resp_auth = post(auth_url, payload)
print("\nAUTH_STATUS:", code_auth)
print(json.dumps(resp_auth, indent=2))

token = None
if isinstance(resp_auth, dict):
    token = resp_auth.get("access_token") or resp_auth.get("token")

if token:
    req = urllib.request.Request(notifications_url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req, timeout=15) as nf:
            notifs = json.load(nf)
            print("\nNOTIFICATIONS_FETCHED:")
            print(json.dumps(notifs, indent=2))
    except urllib.error.HTTPError as e:
        try:
            print("\nNOTIFICATIONS_ERROR:", e.code)
            print(json.dumps(json.load(e), indent=2))
        except Exception:
            print("\nNOTIFICATIONS_ERROR_RAW:", e.read().decode())
    except Exception as e:
        print("\nNOTIFICATIONS_ERROR:", str(e))
else:
    print("\nNo token obtained; skipping notifications fetch")
