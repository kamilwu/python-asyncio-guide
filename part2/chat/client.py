import asyncio
import sys
from typing import IO

from chat.common import read_until_eol


HOST = '127.0.0.1'
PORT = 8080


async def connect(file: IO[str]) -> None:
    reader, writer = await asyncio.open_connection(HOST, PORT)

    for message in file:
        writer.write(message.encode())
        await writer.drain()

        echoed = await read_until_eol(reader)
        if echoed:
            print(f'{echoed.decode()!r}')
        else:
            print('EOF received. The server may be dead.')
            break

    writer.close()
    await writer.wait_closed()
    print('Connection closed.')


if __name__ == '__main__':
    asyncio.run(connect(sys.stdin))
