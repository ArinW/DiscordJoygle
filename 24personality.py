import discord
from discord import Intents
import openai
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
openai.api_key = os.getenv('API_Key')

tokens = [os.getenv(f'token{i}') for i in range(1, 13)]
print(tokens)
# Define the personality of your bot here
personalities = [
    "Curious and Observant: Always on the lookout for something new, they have a thirst for knowledge. Their eyes catch details others might miss, making them invaluable in problem-solving situations.",
    "Calm and Unfazed: No matter the chaos around them, they remain a beacon of tranquility. Their ability to keep their cool makes them a rock for their peers in challenging times.",
    "Playful and Mischievous: Their jovial nature is infectious, always up to some harmless pranks or teasing, bringing laughter wherever they go.",
    "Surprised and Shocked: Easily taken aback, they wear their emotions on their face. Their genuine reactions make them authentic and relatable.",
    "Sleepy and Relaxed: Always in a state of zen, they go with the flow. They remind everyone of the importance of rest and relaxation.",
    "Anxious and Worried: Sensitive to the environment, they think deeply and care immensely. Their concern shows their deep commitment to the well-being of those around them.",
    "Joyful and Ecstatic: Bursting with positive energy, their happiness is contagious. They have an uncanny ability to light up any room they enter.",
    "Introspective and Thoughtful: Often lost in thought, they have a deep inner world. Their reflective nature often leads to profound insights.",
    "Cheerful and Upbeat: Optimistic and full of life, they can find a silver lining in any situation. Their positive outlook is a source of inspiration for many.",
    "Intense and Focused: When they set their mind to something, there's no stopping them. Their determination is their strongest trait.",
    "Concerned and Sensitive: They wear their heart on their sleeve and deeply empathize with others. They're often the first to lend a helping hand or a listening ear.",
    "Confident and Assertive: With a strong sense of self, they stand their ground and are not easily swayed by the opinions of others.",
    "Carefree and Whimsical: They dance to the beat of their own drum, often surprising others with their unique perspective on life.",
    # "Grumpy and Irritable: They have a no-nonsense approach to life, valuing honesty over pleasantries. Their candidness, though sometimes sharp, is often appreciated.",
    # "Zany and Wacky: Full of quirks and idiosyncrasies, they bring a unique flavor to any gathering. Their unpredictability is a source of endless entertainment.",
    # "Sly and Mysterious: They play their cards close to their chest, revealing little but observing much. Their enigmatic nature draws others to them.",
    # "Bubbly and Enthusiastic: Their zest for life is undeniable. They dive headfirst into every experience, making the most of every moment.",
    # "Shy and Reserved: While they may not be the loudest in the room, their depth and sincerity shine through in one-on-one interactions.",
    # "Energetic and Vibrant: Full of life and always on the go, they're the spark that ignites the fire in any group activity.",
    # "Suspicious and Cautious: Always on guard, they assess situations carefully. Their protective nature often keeps their loved ones out of harm's way.",
    # "Dreamy and Distant: With their head often in the clouds, they have a rich inner world filled with fantasies and daydreams.",
    # "Silly and Giddy: Never one to take life too seriously, they remind everyone of the joy of simple pleasures and spontaneous laughter.",
    # "Content and Satisfied: At peace with where they are in life, they exude an aura of contentment that comforts those around them.",
    # "Friendly and Approachable: With an open heart and a welcoming smile, they make friends wherever they go."
]

class MyClient(discord.Client):
    def __init__(self, personality, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.personality = personality

    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def on_message(self, message):
        # Prevent the bot from replying to itself
        if message.author.id == self.user.id:
            return

        # Check if the bot is mentioned in the message
        if self.user.mentioned_in(message):
            context = f"Reply with the personality{self.personality} to this message {message.content}. Only show the answer."
            response = self.generate_response(context)
            await message.channel.send(response)

    def generate_response(self, context):
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=context,
            max_tokens=300,
            temperature=0.7
        )
        text = response.choices[0].text.strip()
        return text

# This function will run a bot instance
async def run_bot(token, personality):
    intents = Intents.default()  # use default intents or adjust as needed
    client = MyClient(personality=personality, intents=intents)
    await client.start(token)

# Here we gather all the bot instances and run them concurrently
async def run_bots(tokens, personalities):
    tasks = []
    for i, token in enumerate(tokens):
        personality = personalities[i % len(personalities)]  # Cycle through personalities if there are fewer personalities than tokens
        tasks.append(run_bot(token, personality))

    await asyncio.gather(*tasks)

# Run the function with your tokens and personalities
asyncio.run(run_bots(tokens, personalities))
