import httpx

limits = httpx.Limits(max_keepalive_connections=100, max_connections=None)
client = httpx.AsyncClient(limits=limits, verify=False)

async def getAsync(url):
    response = await client.get(url)
    return response.json()

async def postAsync(url, data):
    response = await client.post(url, data=data)
    return response.json()