import requests

url = 'https://api.discogs.com/oauth/identity'

my_user_token = input("Enter DISCOGS user token")
my_headers={"Authorization": "Discogs token="+my_user_token}

# params = my_params
resp = requests.get(url, headers = my_headers)
RC = resp.status_code
Razao = resp.reason

url2 = "https://i.discogs.com/XTKBBBPI0_VPY3rejvaih-MxjEmif5v4NmzyBwMqd8I/rs:fit/g:sm/q:90/h:529/w:600/czM6Ly9kaXNjb2dz/LWRhdGFiYXNlLWlt/YWdlcy9SLTIwOTU3/NC0xNjczNDY4NTUw/LTU0ODMucG5n.jpeg"

resp = requests.get(url2, headers = my_headers)
RC = resp.status_code
Razao = resp.reason

if resp.status_code == 200:
    print(resp.json())
else:
    print('Error:', resp.status_code)
