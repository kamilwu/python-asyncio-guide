import asyncio

from chat.common import readlines


HOST = '127.0.0.1'
PORT = 8080


async def handle_connection(reader: asyncio.StreamReader,
                            writer: asyncio.StreamWriter) -> None:
    addr = writer.get_extra_info('peername')
    async for data in readlines(reader):
        message = data.decode()
        print(f'{addr}: {message!r}')

        writer.write(data)
        await writer.drain()
    print(f'{addr}: Connection closed by the remote peer.')


async def start_server() -> None:
    server = await asyncio.start_server(handle_connection, HOST, PORT)
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(start_server())
