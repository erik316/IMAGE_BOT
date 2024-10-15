import telebot
from logic import TextToImage, base64_to_jpg
import os
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv("TOKEN"))

url = 'https://api-key.fusionbrain.ai/'
api_key = os.getenv("API_KEY")
secret_key = os.getenv("SECRET_KEY")

@bot.message_handler(commands=["img"])
def image(message: telebot.typeSs.Message):
    prompt = message.text.replace("/img", "")
    if not prompt:
        bot.send_message(message.chat.id, "No Prompt")
        return
    bot.send_message(message.chat.id, f'Generating image... with: {prompt}.')

    api = TextToImage(url,api_key, secret_key)
    model = api.get_model()
    id = api.generate(prompt, model)
    img = api.check_generation(id)
    base64_to_jpg(img[0], 'picture.jpeg')
    with open('picture.jpeg', 'rb') as file:
        bot.send_photo(message.chat.id, file, f'image generated with: {prompt}.')
    bot.delete_message(message.chat.id, message.id)
bot.infinity_polling()