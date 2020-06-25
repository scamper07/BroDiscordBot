import aiohttp
import json
from base_logger import logger


async def get_advice(message_channel):
    logger.debug("advice")
    wait_message = await message_channel.send("Let me think...")

    try:
        session = aiohttp.ClientSession()
        async with session.get("https://api.adviceslip.com/advice") as resp:
            data = await resp.read()
        json_response = json.loads(data)
        await session.close()
        await wait_message.delete()
        await message_channel.send('*\"{}\"*'.format(json_response['slip']['advice']))
    except Exception as e:
        logger.exception(e)
        await message_channel.send('Sorry can\'t think of anything')
