import logging
import qrcode
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
import asyncio
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = ""

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def generate_qr_code(data, file_name="qrcode.png"):
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(file_name)
        return True
    except Exception as e:
        logger.error(f"Ошибка при создании QR-кода: {e}")
        return False

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    logger.info(f"Пользователь {message.from_user.id} запустил бота.")
    await message.answer("Привет! Отправь мне текст или ссылку, и я создам QR-код.")

@dp.message()
async def handle_text(message: types.Message):
    data = message.text
    file_name = "qrcode.png"
    
    logger.info(f"Пользователь {message.from_user.id} отправил: {data}")
    
    if not data:
        await message.answer("Пожалуйста, отправь текст или ссылку.")
        return
    
    if not generate_qr_code(data, file_name):
        await message.answer("Произошла ошибка при создании QR-кода.")
        return
    
    try:
        qr_file = FSInputFile(file_name)
        await message.answer_photo(qr_file, caption="Вот твой QR-код!")
        logger.info(f"QR-код отправлен пользователю {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Ошибка при отправке QR-кода: {e}")
        await message.answer("Произошла ошибка при отправке QR-кода.")
    finally:
        if os.path.exists(file_name):
            os.remove(file_name)

async def main():
    logger.info("Бот запущен.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())