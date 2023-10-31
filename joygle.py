import os
import random
import discord
import openai
from textblob import TextBlob
from dotenv import load_dotenv
from discord.ext import commands
import random

# Load environment variables
load_dotenv()
openai.api_key=os.getenv('API_Key')
token=os.getenv('DISCORD_TOKEN')



# Setup OpenAI and Discord
intents = discord.Intents.default()
intents.messages = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    username = str(message.author).split("#")[0]
    user_message = str(message.content)
    channel = 'Direct Message' if isinstance(message.channel, discord.DMChannel) else str(message.channel.name)

    print(f"{username} said {user_message.lower()} in {channel}")

    # Feature 1: Add reactions to all server messages
    if not isinstance(message.channel, discord.DMChannel):
        blob = TextBlob(user_message)
        sentiment = blob.sentiment.polarity
        positive_emojis = ["😀", "😊", "👍", "❤️", "😍", "🥰", "✨", "🎉", "😁", "🙌"]
        negative_emojis = ["😢", "😠", "👎", "💔", "😞",  "😔", "😒", "👿"]
        neutral_emojis = ["🧐", "🙂"]


        # Determine which list of emojis to use based on the sentiment
        if sentiment > 0.1:  # You might want to adjust the threshold
            emoji_list = positive_emojis
        elif sentiment < -0.1:  # You might want to adjust the threshold
            emoji_list = negative_emojis
        else:
            emoji_list = neutral_emojis  # Use neutral emojis for neutral sentiment

        # Choose a random emoji from the appropriate list
        emoji = random.choice(emoji_list)
        await message.add_reaction(emoji)




    # Feature 2: Reply to the user
    if message.content.startswith(f"<@{client.user.id}>") or isinstance(message.channel, discord.DMChannel):
        question = message.content[len(f"<@{client.user.id}> "):] if message.content.startswith(f"<@{client.user.id}>") else user_message
        print(question)
        async with message.channel.typing():
            try:
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=question,
                    max_tokens=150,  # Adjust to your needs but be cautious of usage limits
                    temperature=0.7
                )
                output = response.choices[0].text.strip()  # Updated to use attribute access for readability
            except openai.error.OpenAIError as e:
                print(f"OpenAI Error: {e}")
                output = "I'm sorry, I can't process your request right now."

            print(output)
            await message.channel.send(output)



    # Feature 3: Auto reply to the user
        if message.author == client.user:
            return

    user_message = str(message.content)

    # Feature 3: Auto-reply cheerfully in the channel
    if not isinstance(message.channel, discord.DMChannel):
        # We'll use the sentiment of the message to decide if we should respond cheerfully
        blob = TextBlob(user_message)
        sentiment = blob.sentiment.polarity
        print(sentiment)
        # Let's say we only respond to negative messages, to prevent inappropriate cheerful responses
        if sentiment < 0:  # feel free to adjust this threshold
            prompt = f"If a person says this {user_message} what should reply cheer up in literally. Only give me the one sentence that I need to reply without quotation marks, no anything else"
            # Use GPT-3 to generate a cheerful response
            async with message.channel.typing():
                try:
                    # Adding some cheerful keywords to the prompt
                    
                    response = openai.Completion.create(
                        model="text-davinci-003",
                        prompt=prompt,
                        max_tokens=200,  # Adjust to your needs but be cautious of usage limits
                        temperature=0.7
                    )
                    # Extracting the cheerful response
                    cheerful_response = response.choices[0].text
                    # split_text = cheerful_response.split("\n")
                    # cheerful_response = split_text[1].strip() if len(split_text) > 1 else "Keep smiling! 😊"  # Fallback reply
                    print(response.choices[0].text)
                
                    
                    # Making sure the response is not too long for a Discord message
                    if len(cheerful_response) > 2000:  # Discord limit is 2000 characters
                        cheerful_response = "You're awesome! Keep being positive! 😊🎉"  # Default message
                except openai.error.OpenAIError as e:
                    print(f"OpenAI Error: {e}")
                    cheerful_response = "Keep up the good vibes! 😄👍"  # Default message in case of an error


                
                await message.channel.send(cheerful_response)

client.run(token)
