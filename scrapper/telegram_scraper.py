from telethon import TelegramClient
import csv
import os
from dotenv import load_dotenv

# Load environment variables once
load_dotenv('.env')
api_id = os.getenv('TG_API_ID')
api_hash = os.getenv('TG_API_HASH')
phone = os.getenv('phone')

# Function to scrape data from a single channel
async def scrape_channel(client, channel_username, writer):
    entity = await client.get_entity(channel_username)
    async for message in client.iter_messages(entity, limit=10000):
        writer.writerow([channel_username, message.id, message.message, message.date])

# Initialize the client once
client = TelegramClient('scraping_session', api_id, api_hash)

async def main():
    await client.start()
    # Open the CSV file and prepare the writer
    with open('telegram_data2.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Channel', 'id', 'message', 'date'])  # Include channel name in the header
        
        # List of channels to scrape
        channels = [
            'Eliasmeserett',
            'ICS_Ethiopia',
            'forfreemarket',
            'mr_trump_poems',
            'tikvahethiopia',
            'amharic_poems',
            'MinTEthiopia',
            'tikvahethmagazine',
            'tikvahethsport',
            'amharicq'
            'Bisrat_Sport_433et',
            'Manchester_Unitedfansz',
            'ethio_telecom',
            'EBCNEWSNOW'
,
        ]
        
        # Iterate over channels and scrape data into the single CSV file
        for channel in channels:
            await scrape_channel(client, channel, writer)
            print(f"Scraped data from {channel}")

with client:
    client.loop.run_until_complete(main())