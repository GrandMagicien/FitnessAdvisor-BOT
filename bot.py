import os
import discord
from discord import app_commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get tokens from environment
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize bot with intents
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


def calculate_load_split(energy: int, sleep: int) -> tuple[int, int, str]:
    """
    Calculate mechanical/metabolic load split based on energy and sleep levels.
    
    Args:
        energy: Energy level (1-5)
        sleep: Sleep level (1-5)
    
    Returns:
        Tuple of (mechanical_percent, metabolic_percent, workout_type)
    """
    if energy >= 4 and sleep >= 4:
        return 70, 30, "Lift Weights"
    elif energy >= 3 and sleep >= 3:
        return 60, 40, "Technique Lift"
    elif energy <= 2 or sleep <= 2:
        return 40, 60, "Swim or Aqua"
    else:
        return 50, 50, "Balanced recovery"


def get_benefits(workout_type: str) -> list[str]:
    """
    Get three benefits based on workout type.
    
    Args:
        workout_type: Type of workout recommended
    
    Returns:
        List of three benefit strings
    """
    benefits_map = {
        "Lift Weights": [
            "Build strength and muscle mass",
            "Boost metabolism for hours post-workout",
            "Improve bone density and joint health"
        ],
        "Technique Lift": [
            "Refine movement patterns safely",
            "Maintain strength with reduced fatigue",
            "Perfect your form for future gains"
        ],
        "Swim or Aqua": [
            "Low-impact recovery for joints",
            "Improve cardiovascular endurance gently",
            "Reduce stress and promote relaxation"
        ],
        "Balanced recovery": [
            "Maintain fitness without overtraining",
            "Allow body to recover properly",
            "Build consistency in your routine"
        ]
    }
    return benefits_map.get(workout_type, benefits_map["Balanced recovery"])


def get_motto(workout_type: str) -> str:
    """
    Get a motivational motto based on workout type.
    
    Args:
        workout_type: Type of workout recommended
    
    Returns:
        Motivational motto string
    """
    motto_map = {
        "Lift Weights": "💪 Strong today, stronger tomorrow!",
        "Technique Lift": "🎯 Progress through precision!",
        "Swim or Aqua": "🌊 Recovery is progress too!",
        "Balanced recovery": "⚖️ Balance brings sustainable growth!"
    }
    return motto_map.get(workout_type, motto_map["Balanced recovery"])


def format_message(energy: int, sleep: int, mechanical: int, metabolic: int, 
                   workout_type: str, benefits: list[str], motto: str) -> str:
    """
    Format the response message with all components.
    
    Args:
        energy: User's energy level
        sleep: User's sleep level
        mechanical: Mechanical load percentage
        metabolic: Metabolic load percentage
        workout_type: Type of workout
        benefits: List of benefits
        motto: Motivational motto
    
    Returns:
        Formatted message string
    """
    message = f"""Hey there! 👋 Based on your current state:
**Energy Level:** {energy}/5 ⚡
**Sleep Quality:** {sleep}/5 😴

**Suggested Mechanical/Metabolic Load Split: {mechanical}% / {metabolic}%**
_({workout_type})_

**Why this is great for you:**
✨ {benefits[0]}
✨ {benefits[1]}
✨ {benefits[2]}

{motto}

Remember, listening to your body is key to long-term success! 🌟
"""
    return message


async def enhance_with_openai(message: str) -> str:
    """
    Optionally enhance the message using OpenAI API.
    
    Args:
        message: Original message
    
    Returns:
        Enhanced message or original if API is not available
    """
    if not OPENAI_API_KEY:
        return message
    
    try:
        from openai import OpenAI
        
        client_openai = OpenAI(api_key=OPENAI_API_KEY)
        response = client_openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a friendly, empathetic fitness advisor. Rephrase the given message to be warmer and more encouraging while keeping all the key information intact. Keep the same structure and formatting."
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return message


@tree.command(
    name="session",
    description="Get personalized workout session advice based on your energy and sleep"
)
@app_commands.describe(
    energy="Your current energy level (1-5, where 5 is highest)",
    sleep="Your sleep quality last night (1-5, where 5 is best)"
)
async def session(interaction: discord.Interaction, energy: int, sleep: int):
    """
    Slash command to provide session advice based on energy and sleep levels.
    
    Args:
        interaction: Discord interaction object
        energy: Energy level (1-5)
        sleep: Sleep level (1-5)
    """
    # Validate inputs
    if not (1 <= energy <= 5):
        await interaction.response.send_message(
            "⚠️ Energy level must be between 1 and 5!",
            ephemeral=True
        )
        return
    
    if not (1 <= sleep <= 5):
        await interaction.response.send_message(
            "⚠️ Sleep quality must be between 1 and 5!",
            ephemeral=True
        )
        return
    
    # Defer response as OpenAI might take time
    await interaction.response.defer()
    
    # Calculate load split
    mechanical, metabolic, workout_type = calculate_load_split(energy, sleep)
    
    # Get benefits and motto
    benefits = get_benefits(workout_type)
    motto = get_motto(workout_type)
    
    # Format base message
    message = format_message(energy, sleep, mechanical, metabolic, 
                           workout_type, benefits, motto)
    
    # Optionally enhance with OpenAI
    enhanced_message = await enhance_with_openai(message)
    
    # Send the response
    await interaction.followup.send(enhanced_message)


@client.event
async def on_ready():
    """Event handler for when the bot is ready."""
    print(f'Logged in as {client.user}')
    
    # Sync commands with Discord
    try:
        synced = await tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Error syncing commands: {e}')


def main():
    """Main function to run the bot."""
    if not DISCORD_TOKEN:
        print("Error: DISCORD_TOKEN not found in environment variables!")
        print("Please create a .env file with your DISCORD_TOKEN")
        return
    
    print("Starting Session Advisor Bot...")
    client.run(DISCORD_TOKEN)


if __name__ == '__main__':
    main()
