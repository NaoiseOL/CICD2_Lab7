from fastapi import FastAPI
import aio_pika
import os
import json

app = FastAPI()

RABBIT_URL = os.getenv("RABBIT_URL")

@app.post("/order")
async def  publish_order(order: dict):
    connection = await aio_pika.connect_robust(RABBIT_URL)
    channel = await connection.channel()

    message = aio_pika.Message(body=json.dumps(order.).encode())

    await channel.default_exchange.publish(
        message,
        routing_key="orders_queue"
    )

    await connection.close()

    return {"status": "Message sent", "order": order}