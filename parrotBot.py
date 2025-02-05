import sys
import logging
from telegram import Update, Bot
from html import escape
import tempfile
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from pydub import AudioSegment
from gtts import gTTS
import os
from datetime import datetime
import speech_recognition as sr

BOT_USERNAME = 'username of your personal bot'
API_TOKEN = 'api token of you personal bot'
list_accepted_users = ['username1', 'username2 ', '...']

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    if update.message.from_user.username not in list_accepted_users:
        with open('lista_intrusi.txt', 'a') as intrusi:
            #  Get the current timestamp
            timestamp = datetime.now()

            # Format the timestamp as a string
            timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            intrusi.write(str(update.message.from_user) + " --- " + timestamp_str)
            intrusi.write('\n')
            return None

    await update.message.reply_text("Ciao! Sono ParrotBot e ripeterò quello che dici/scrivi")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.from_user.username not in list_accepted_users:
        with open('lista_intrusi.txt', 'a') as intrusi:
            #  Get the current timestamp
            timestamp = datetime.now()

            # Format the timestamp as a string
            timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            intrusi.write(str(update.message.from_user) + " --- " + timestamp_str)
            intrusi.write('\n')
            return None

    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")

# Function to handle the voice message
async def voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get the sent voice note
    voice = update.message.voice
    file = await voice.get_file()
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as temp_audio:
        await file.download_to_drive(temp_audio.name)
        temp_audio_path = temp_audio.name
        
    # Use pydub to convert OGG to WAV without FFmpeg
    audio = AudioSegment.from_file(temp_audio_path, format="ogg")
    wav_path = "voice.wav"
    audio.export(wav_path, format="wav")
                
    await voice_to_text(update, wav_path)
    
async def voice_to_text(update: Update, audio_path):
    wav_path = "voice.wav"
    # Create a Recognizer object
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    try:
        # Transcribe the text
        transcription = recognizer.recognize_google(audio, language="it-IT")
        await update.message.reply_text(transcription)

        # Remove the temporary WAV file
        os.remove(wav_path)
    except sr.UnknownValueError:
        await update.message.reply_text("Non è stato possibile riconoscere l'audio.")
    except sr.RequestError as e:
        await update.message.reply_text(f"Errore nella richiesta al servizio di riconoscimento: {e}")

def text_to_speech(text, output_file):
    tts = gTTS(text=text, lang='it')
    tts.save(output_file)

    if os.path.exists(output_file):
    ## Load the audio file
        audio = AudioSegment.from_mp3(output_file)

        # Modify the frequency to speed up playback
        audio = audio.speedup(playback_speed=1.2)

        # Save the modified audio file
        audio.export(output_file, format="mp3")

        print("File audio generato con successo:", output_file)
        return audio

async def text_to_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    text = update.message.text
    if update.message.from_user.username not in list_accepted_users:
        with open('lista_intrusi.txt', 'a') as intrusi:
            # Get the current timestamp
            timestamp = datetime.now()
            # Format the timestamp as a string
            timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            intrusi.write(str(update.message.from_user) + " --- " + timestamp_str)
            intrusi.write('\n')
            return None

    if text.startswith(BOT_USERNAME):
        text = text.replace(BOT_USERNAME, "")
        if len(text.strip()) == 0 :
            return
        testo_da_convertire = text
        file_audio = "output.mp3"
        text_to_speech(testo_da_convertire, file_audio)
        print("Testo convertito in audio con successo!")
        bot = Bot(API_TOKEN)
        await bot.send_voice(chat_id=context._chat_id, voice = open(file_audio, 'rb'), allow_sending_without_reply = True, caption= update.message.from_user['first_name']+':\n'+ f"<b>{escape(testo_da_convertire)}</b>", parse_mode=ParseMode.HTML )
        os.remove(file_audio)

def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(API_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT, text_to_voice))
    application.add_handler(MessageHandler(filters.VOICE, voice_message))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()
