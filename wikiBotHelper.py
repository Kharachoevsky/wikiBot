import logging
import wikipedia
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext


wikipedia.set_lang("ru")


logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)


async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Привет! Задай мне вопрос, и я найду ответ в Википедии.")


async def search_wiki(update: Update, context: CallbackContext):
    query = update.message.text.strip()

    try:
        summary = wikipedia.summary(query, sentences=3)
        await update.message.reply_text(summary)
    except wikipedia.exceptions.PageError:
        await update.message.reply_text("Я не нашел информации по этому запросу.")
    except wikipedia.exceptions.DisambiguationError as e:
        await update.message.reply_text(f"Уточните запрос: {e.options[:5]}")


def main():
    token = "8123260907:AAEHmmzEke8i33sjwYrAPXIpxuvSbeZ0WfM"
    app = Application.builder().token(token).build()


    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_wiki))


    app.run_polling()


if __name__ == "__main__":
    main()