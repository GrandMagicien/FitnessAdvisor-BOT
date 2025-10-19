# Session Advisor Bot 🏋️‍♂️

A friendly Discord bot that provides personalized workout session advice based on your energy level and sleep quality.

## Features

- 💬 Slash command `/session` to get workout recommendations
- ⚡ Energy and sleep-based workout load split calculations
- 🎯 Four different workout types based on your current state
- ✨ Three personalized benefits for each recommendation
- 💪 Motivational mottos to keep you inspired
- 🤖 Optional OpenAI integration for warmer, more empathetic messages

## Workout Recommendations

The bot suggests a mechanical/metabolic load split based on your inputs:

| Energy | Sleep | Split | Workout Type |
|--------|-------|-------|--------------|
| ≥4 | ≥4 | 70% / 30% | Lift Weights |
| ≥3 | ≥3 | 60% / 40% | Technique Lift |
| ≤2 or ≤2 | ≤2 or ≤2 | 40% / 60% | Swim or Aqua |
| Other | Other | 50% / 50% | Balanced recovery |

## Prerequisites

- Python 3.8 or higher
- A Discord Bot Token
- (Optional) OpenAI API Key for enhanced messages

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/GrandMagicien/FitnessAdvisor-BOT.git
cd FitnessAdvisor-BOT
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Create a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section and click "Add Bot"
4. Under "Privileged Gateway Intents", enable:
   - Presence Intent (optional)
   - Server Members Intent (optional)
   - Message Content Intent (optional)
5. Copy the bot token

### 4. Invite the Bot to Your Server

1. In the Developer Portal, go to "OAuth2" → "URL Generator"
2. Select scopes:
   - `bot`
   - `applications.commands`
3. Select bot permissions:
   - `Send Messages`
   - `Use Slash Commands`
4. Copy the generated URL and open it in your browser
5. Select your server and authorize the bot

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your tokens:

```env
DISCORD_TOKEN=your_discord_bot_token_here
OPENAI_API_KEY=your_openai_api_key_here  # Optional
```

### 6. Run the Bot

```bash
python bot.py
```

You should see:
```
Starting Session Advisor Bot...
Logged in as YourBotName#1234
Synced 1 command(s)
```

## Usage

In any channel where the bot has access, use the slash command:

```
/session energy:4 sleep:5
```

Parameters:
- `energy`: Your current energy level (1-5, where 5 is highest)
- `sleep`: Your sleep quality last night (1-5, where 5 is best)

The bot will respond with:
- Your current state
- Recommended mechanical/metabolic load split
- Workout type
- Three personalized benefits
- A motivational motto

### Example Response

```
Hey there! 👋 Based on your current state:
Energy Level: 4/5 ⚡
Sleep Quality: 5/5 😴

Suggested Mechanical/Metabolic Load Split: 70% / 30%
(Lift Weights)

Why this is great for you:
✨ Build strength and muscle mass
✨ Boost metabolism for hours post-workout
✨ Improve bone density and joint health

💪 Strong today, stronger tomorrow!

Remember, listening to your body is key to long-term success! 🌟
```

## Optional: OpenAI Integration

To enable AI-powered message rephrasing:

1. Get an API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Add it to your `.env` file:
   ```env
   OPENAI_API_KEY=sk-...
   ```
3. Restart the bot

The bot will now use GPT-3.5 to rephrase messages with a warmer, more empathetic tone while keeping all the information intact.

## Project Structure

```
FitnessAdvisor-BOT/
├── bot.py              # Main bot implementation
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## Troubleshooting

### Bot doesn't respond to /session command

1. Make sure the bot has proper permissions in your server
2. Try restarting the bot to sync commands
3. Commands may take up to an hour to propagate globally (instantly in development servers)

### ImportError: No module named 'discord'

Install dependencies:
```bash
pip install -r requirements.txt
```

### Bot token is invalid

1. Regenerate the token in Discord Developer Portal
2. Update your `.env` file
3. Restart the bot

### OpenAI API errors

- Check that your API key is valid
- Ensure you have credits in your OpenAI account
- The bot will fallback to default messages if OpenAI fails

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

Made with ❤️ for fitness enthusiasts
