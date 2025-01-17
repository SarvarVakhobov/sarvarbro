from loader import tc

client = tc

async def get_all_subscribers(channel_username):
    subscribers = []  # List to store subscriber details

    async with client:
        # Get the channel object
        channel = await client.get_entity(channel_username)
        
        # Fetch all members
        async for user in client.iter_participants(channel):
            subscribers.append({
                "id": user.id,
            })

    return subscribers

def getsubs(username):
    return client.loop.run_until_complete(get_all_subscribers(username))