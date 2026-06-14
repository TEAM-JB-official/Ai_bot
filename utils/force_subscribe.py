from config import config

async def check_force_subscribe(client, user_id):
    if not config.FORCE_SUBSCRIBE_CHANNEL:
        return True
    
    try:
        member = await client.get_chat_member(config.FORCE_SUBSCRIBE_CHANNEL, user_id)
        if member.status in ["member", "administrator", "creator"]:
            return True
        else:
            await client.send_message(
                user_id,
                f"⚠️ Please join our [channel](https://t.me/{config.FORCE_SUBSCRIBE_CHANNEL}) to use this bot.",
                disable_web_page_preview=True
            )
            return False
    except:
        return False
