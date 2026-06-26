import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from openai import OpenAI

print("start")
print("GROQ:", repr(os.getenv("GROQ_API_KEY")))
print("TOKEN:", os.getenv("TELEGRAM_BOT_TOKEN"))


client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "user", "content": user_message}
        ]
    )

    await update.message.reply_text(
        response.choices[0].message.content
    )

app = ApplicationBuilder().token(
    os.getenv("TELEGRAM_BOT_TOKEN")
).build()

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, chat)
)

print("Bot started!")
app.run_polling()