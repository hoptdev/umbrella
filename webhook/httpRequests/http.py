import httpx
import requests

limits = httpx.Limits(max_keepalive_connections=100, max_connections=None)
client = httpx.AsyncClient(limits=limits, verify=False)

async def getAsync(url):
    response = await client.get(url)
    return response.json()

async def postAsync(url, data, files=None):
    response = await client.post(url, data=data, files=files)
    return response.json()

def post(url, data):
    response = requests.post(url, data=data)
    return response.json()