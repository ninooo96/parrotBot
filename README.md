# ParrotBot
This project is a Telegram bot that allows users to transcribe voice notes and generate audio files from text. It can works locally, and can be added to a group or used directly via private chat.

## Features

- **Voice-to-Text**: The bot can transcribe voice messages sent in a Telegram chat.
- **Text-to-Voice**: When tagged with a message, the bot will generate an audio file from the provided text and send it back.

## Requirements

- Python 3.x
- `ffmpeg` for audio file conversions

## Setup Instructions

### Install Dependencies

Make sure you have `ffmpeg` and Python dependencies installed:

```bash
# Install ffmpeg
sudo apt install ffmpeg
```

## Python Dependencies
Make sure you have Python 3.x installed, then install the necessary Python libraries by running:
```bash
pip install -r requirements.txt
```

## Create a Telegram Bot with BotFather
To create your own Telegram bot and get the API token, follow these steps:

Open Telegram and search for the BotFather bot.
Start a chat with BotFather and type /newbot.
Follow the instructions to set a name and username for your bot.
Once the bot is created, you will receive an API token. Copy this token, as you will need it later.

## Clone the repository
First, clone the repository to your local machine. Then, modify the code to include the following:

- The username(s) of the users who are allowed to use your bot.
- our API_TOKEN (which you received from BotFather).
- The username of your bot.
Run the following commands to clone the repository:
```bash
git clone https://github.com/ninooo96/parrotBot.git
cd parrotBot
```
Once configured, the bot will be ready to use in your Telegram group or private chat.

## Using the Bot
Voice-to-Text: Send a voice note to the bot in the chat, and it will transcribe it and send you the text.

Text-to-Voice: Tag the bot with a message like:

@your_bot_username This is the text to convert to speech

The bot will respond with an audio file containing the speech.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
