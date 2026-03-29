from __future__ import annotations

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from config import load_bot_config, load_env


env = load_env()
bot_config = load_bot_config()


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user

    if user is None or user.id != env["admin_id"]:
        if update.message:
            await update.message.reply_text("Unauthorized.")
        return

    if update.message:
        await update.message.reply_text("pong")


def main() -> None:
    app = ApplicationBuilder().token(env["token"]).build()
    app.add_handler(CommandHandler("ping", ping))

    print(f"{bot_config['bot']['name']} is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
