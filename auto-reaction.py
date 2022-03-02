import requests
import json
import time, os
from datetime import datetime
import asyncio, aiohttp

async def dc_reaction(chanel_list, authorization):
    header = {
    "Authorization": authorization,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
    }  
    for chanel_id in chanel_list:
      url = "https://discord.com/api/v9/channels/{}/messages?limit=15".format(chanel_id)
      try:
        async with aiohttp.ClientSession() as session:
          async with session.get(url, headers=header) as res:
            if res.status == 200:
              json_results = await res.text()
              json_results = json.loads(json_results)
              for msg in json_results:
                try:
                  #3. update the lottery keyword here, eg. **GIVEAWAY**

                  msg_id = msg["id"]
                  url = "https://discord.com/api/v9/channels/{}/messages/{}/reactions/%F0%9F%8E%89/%40me".format(chanel_id,msg_id)
                  async with session.put(url, headers=header) as res2:
                    await asyncio.sleep(1)

                except Exception as e:
                  print(f'Error of put requests, exception: {e}')
                  pass
            else:
              print(f'status: {res.status}')

      except Exception as e:
        print(f'error of channel loop')
        pass

def jobs(request):
  #1. put channel id here
  channel_list = [
    "93xxxxxxxxxxxxxxxx", # soulZ wl-giveaway
  ]
  #2. load token.json format is following
  # {
  #    "account": "< your discord token here >"
  # }
  with open('token.json') as f:
    authorization_list = json.load(f)
  now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  tasks = []
  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)
  for auth in authorization_list.values():
      tasks.append(loop.create_task(dc_reaction(channel_list, auth)))
  result = asyncio.gather(*tasks)
  loop.run_until_complete(asyncio.wait(tasks))

  return f'now={now}'

if __name__ == '__main__':
  jobs(None)
