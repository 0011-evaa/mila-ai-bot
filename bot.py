import os
from dotenv import load_dotenv
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from memory import get_user_memory, update_user_memory, remember_interaction
from teacher import ask_teacher

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is missing. Add it to your .env file.")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing. Add it to your .env file.")

client = OpenAI(api_key=OPENAI_API_KEY)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_memory = get_user_memory(user_id)
    update_user_memory(user_id, user_memory)

    await update.message.reply_text(
        "Привіт 🌿 Я Mila AI — твій серйозний викладач чеської та англійської.\n\n"
        "Перш ніж почати уроки, я визначу твій рівень окремо з чеської та англійської.\n\n"
        "З якої мови почнемо діагностику? Напиши: «чеська» або «англійська»."
    )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_memory = get_user_memory(user_id)

    await update.message.reply_text(
        f"📊 Твій поточний профіль:\n\n"
        f"🇨🇿 Чеська: {user_memory.get('czech_level')}\n"
        f"🇬🇧 Англійська: {user_memory.get('english_level')}\n"
        f"📚 Уроків: {user_memory.get('lesson_count')}\n"
        f"📝 Помилок у пам'яті: {len(user_memory.get('mistakes', []))}\n"
        f"📖 Слів у словнику: {len(user_memory.get('vocabulary', []))}"
    )


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    update_user_memory(user_id, {})
    await update.message.reply_text("Пам'ять очищено. Напиши /start, щоб почати заново.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text.strip()

    user_memory = get_user_memory(user_id)

    lower_text = user_text.lower()
    if lower_text in ["чеська", "ческа", "почнемо чеську", "czech"]:
        user_memory["current_language"] = "czech"
        update_user_memory(user_id, user_memory)
    elif lower_text in ["англійська", "английская", "почнемо англійську", "english"]:
        user_memory["current_language"] = "english"
        update_user_memory(user_id, user_memory)

    try:
        bot_text = ask_teacher(client, user_text, user_memory)
        remember_interaction(user_id, user_text, bot_text)
        await update.message.reply_text(bot_text)
    except Exception as error:
        await update.message.reply_text(
            "Сталася помилка 😅 Але це нормально на етапі розробки.\n\n"
            f"Технічна деталь: {error}"
        )


def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Mila AI is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
