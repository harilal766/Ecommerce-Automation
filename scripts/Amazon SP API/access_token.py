import requests

def get_access_token(client_id, client_secret, refresh_token):
    url = "https://api.amazon.com/auth/o2/token"
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception(f"Failed to get access token: {response.text}")

# Example usage
client_id = "amzn1.application-oa2-client.440003f0ec0f4742b8a4114a6f355adc"
client_secret = "amzn1.oa2-cs.v1.3d5adf1e738e0d5ea9483c9f830ba8e304d253ff3f8d66692a1945"
refresh_token = "Atzr|IwEBIPzbHNdpkIRkPp55KydQyk3tnXDsQbxnRRolh2T34txC1XbNoD0fGp8OHQcPDHWQR1NCdw2LWNfqyrBMIclCBumAVtruJBYWijlPSjsorxvrkMrlMdGWLKTD17jV-X5cqyZ5MvAxO4fnnn2A5e521r6CvhAgABAYfOlm-VqWNhapXQAGwNQolTPJSFBPO1KtCENUpi-lKF1FvG_Pis7jjpGUn70xSM0yOqDWLvOKLLvymX6ataGyHw99kEdhIKOPX2z87k5ABE8Vl1lvUpwggRWHTMPNdP32KhEcZUht3VeLrtpnuDJD6eEEW0o59C4S_UYBAtERYuMMZgo1Fmx2T0mI"
access_token = get_access_token(client_id, client_secret, refresh_token)
print("Access Token:", access_token)
