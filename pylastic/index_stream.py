from pprint import pprint
import json
import timeit
import asyncio

import aiohttp


async def main(loop: asyncio.AbstractEventLoop):

    index_url = 'http://localhost:9200/example'

    async with aiohttp.ClientSession() as session:

        body = {
            'size': 200,
            'query': {}
        }

        url = index_url + '/item/_search?scroll=1m'

        async with session.post(url, data=json.dumps(body)) as response:

            response_data = await response.json()

            scroll_id = response_data['_scroll_id']

        c = 0

        for i in range(200):

            body = {
                'scroll': '1m',
                'scroll_id': scroll_id
            }

            async with session.get('http://localhost:9200/_search/scroll', data=json.dumps(body)) as response:

                response_data = await response.json()

                scroll_id = response_data['_scroll_id']

                hits = response_data['hits']['hits']

                if len(hits) == 0:
                    break

                for el in hits:

                    c += 1

                    print(str(c) + '.', el)


def run():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))


if __name__ == '__main__':
    print(timeit.timeit(run, number=1))

