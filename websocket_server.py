import asyncio
import websockets
import openai

# OpenAI API Key
openai.api_key = "your-api-key"
# need to set up authorizing api

async def handle_connection(websocket, path):
    async for message in websocket:
        print(f"Received from NAO: {message}")
        # Process the message with LLM elaborate on this
        response = await get_response_from_llm(message)
        print(f"Response from LLM: {response}")
        await websocket.send(response)

async def get_response_from_llm(message):
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=message,
            max_tokens=150
        )
        return response["choices"][0]["text"].strip()
    except Exception as e:
        print(f"Error querying LLM: {e}")
        return "Sorry, I couldn't process your request."

start_server = websockets.serve(handle_connection, "localhost", 8765)

print("WebSocket Server is running...")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
