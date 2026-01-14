import telebot
from collections import Counter
import re

# ТОКЕН ОТ @BotFather
TOKEN = '8277517885:AAGi-WqPeMICYTc52ZsA6LLg1_dgs7lSlX0'

bot = telebot.TeleBot(TOKEN)

# Распознавание разных вариантов написания
skill_mapping = {
    'пах': 'пах',
    'ухо': 'ухо',
    'колено': 'ухо',
    'коленом': 'ухо',
    'глаза': 'глаз',
    'глаз': 'глаз',
    'грудь': 'грудь',
    'яд': 'яд',
    'яды': 'яд',
    'самопал': 'пал',
    'пал': 'пал',
    'финка': 'финка',
    'фин': 'финка',
    'финк': 'финка'
}

base_skills = {'пах', 'ухо', 'глаз', 'грудь'}     # за повторы +3 монеты
special_skills = {'яд', 'пал', 'финка'}

@bot.message_handler(func=lambda message: True)
def calculate_combo(message):
    text = message.text.lower()
    words = re.findall(r'[а-я]+', text)

    combo = [skill_mapping[word] for word in words if word in skill_mapping]

    if not combo:
        bot.reply_to(message, "Не распознал ни одного удара 😕\nПришли комбо ещё разок.")
        return

    counts = Counter(combo)

    # Монеты от повторов базовых ударов
    coins = 0
    for skill in base_skills:
        if counts[skill] > 1:
            coins += (counts[skill] - 1) * 3

    # Специальные предметы
    needed = []
    for skill in special_skills:
        if counts[skill] > 0:
            needed.append(f"{skill.capitalize()}: {counts[skill]} шт.")

    # Ответ
    answer = f"Комбо: {' → '.join(combo)}\n\n"
    answer += f"💰 Потребуется рублей: **{coins}**\n"

    if needed:
        answer += "\nДополнительно:\n" + "\n".join(f"• {item}" for item in needed)
    else:
        answer += "\nБез специальных предметов."

    bot.reply_to(message, answer, parse_mode='Markdown')

print("Бот запущен...")
bot.infinity_polling(allowed_updates=["message"])