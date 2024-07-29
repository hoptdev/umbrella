import httpx
import requests

limits = httpx.Limits(max_keepalive_connections=100, max_connections=None)
client = httpx.AsyncClient(limits=limits, verify=False)

async def getAsync(url):
    response = await client.get(url)
    result = response.json()
    
    return result

async def postAsync(url, data, files=None):
    response = await client.post(url, data=data, files=files)
    
    result = response.json()
    
    #print(result)
    return result

def sendRpc(url, auth, data):
    response = requests.post(url, auth=auth, data=data)
    return response

def post(url, data):
    response = requests.post(url, data=data)
    result = response.json()
    
    #print(result)
    return result