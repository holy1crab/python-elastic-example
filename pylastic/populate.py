import json
import random
import string
import asyncio

import aiohttp


generate_text = lambda n: ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(n))


async def main(loop: asyncio.AbstractEventLoop):

    async with aiohttp.ClientSession() as session:

        index_url = 'http://localhost:9200/example'

        data = {
            'mappings': {
                'item': {
                    'properties': {
                        'key': {'type': 'long'},
                        'name': {'type': 'string'},
                        'message': {'type': 'text'},
                    }
                }
            }
        }

        # async with session.put(index_url, data=json.dumps(data)) as response:
        #
        #     print(response.status)
        #
        #     body = await response.text()
        #
        #     print(body)

        n = 1000

        for i in range(n):

            item = {
                'key': random.randint(0, 100000),
                'name': generate_text(10),
                'message': generate_text(200)
            }

            async with session.post(index_url + '/item', data=json.dumps(item)) as response:

                response_text = await response.text()

                print(response.status, response_text)

        print('inserted %s elements' % n)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
