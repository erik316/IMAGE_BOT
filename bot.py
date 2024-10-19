import telebot
from logic import TextToImage, base64_to_jpg
import os
from dotenv import load_dotenv
from send2trash import send2trash

def safe_remove_file(file_path):
    if os.path.exists(file_path):
        try:
            send2trash(file_path)
            print(f"Moved to trash: {file_path}")
        except Exception as e:
            print(f"Error moving {file_path} to trash: {e}")
    else:
        print(f"The file {file_path} does not exist.")

load_dotenv()

bot = telebot.TeleBot(os.getenv("TOKEN"))
url = 'https://api-key.fusionbrain.ai/'
api_key = os.getenv("API_KEY")
secret_key = os.getenv("SECRET_KEY")

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, """
uh hi
/img - put what you want after it to generate it
now use that u stupid
""")

@bot.message_handler(commands=["img"])
def image(message: telebot.types.Message):
    prompt = message.text.replace("/img", "")
    if not prompt:
        bot.send_message(message.chat.id, "No Prompt")
        return
    
    bot.send_message(message.chat.id, f'Generating image with: {prompt}, for {message.from_user.first_name}.')
    
    api = TextToImage(url, api_key, secret_key)
    model = api.get_model()
    id = api.generate(prompt, model)
    img = api.check_generation(id)
    
    image_file_path = 'picture.png'
    base64_to_jpg(img[0], image_file_path)
    
    with open(image_file_path, 'rb') as file:
        bot.send_photo(message.chat.id, file, f'Image generated with: {prompt}.')
    
    bot.delete_message(message.chat.id, message.id)
    safe_remove_file(image_file_path)

bot.infinity_polling()
