import asyncio
import websockets


async def handle_connection(websocket, path, shared_data_obj):
    print("Connection established")
    try:
        while True:
            # Receive data from UE5
            data = await websocket.recv()
            print(f"Raw data received: {data}")

            if data:
                try:
                    shared_data_obj.update_data(data)
                    print(f"Updated shared data: {shared_data_obj.get_data()}")
                except Exception as e:
                    print(f"Error processing data: {e}")
            else:
                print("Received empty or invalid data")
    except websockets.ConnectionClosed:
        print("Connection closed")


async def start_server(shared_data_obj):
    # Start WebSocket server
    server = await websockets.serve(
        lambda ws, path: handle_connection(ws, path, shared_data_obj), '127.0.0.1', 12345)
    print("WebSocket server listening on ws://127.0.0.1:12345")
    await server.wait_closed()


def run_socket_server(shared_data_obj):
    asyncio.run(start_server(shared_data_obj))
