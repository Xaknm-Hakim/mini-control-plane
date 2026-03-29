from __future__ import annotations

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from config import load_bot_config, load_env
from formatters.help_formatter import format_help
from formatters.status_formatter import format_host_status
from services.host_service import get_host_status


env = load_env()
bot_config = load_bot_config()


def is_admin(user_id: int) -> bool:
    return user_id == env["admin_id"]


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user

    if user is None or not is_admin(user.id):
        if update.message:
            await update.message.reply_text("Unauthorized.")
        return

    if update.message:
        await update.message.reply_text("pong")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user

    if user is None or not is_admin(user.id):
        if update.message:
            await update.message.reply_text("Unauthorized.")
        return

    if update.message:
        await update.message.reply_text(format_help())


async def host_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user

    if user is None or not is_admin(user.id):
        if update.message:
            await update.message.reply_text("Unauthorized.")
        return

    status = get_host_status()
    message = format_host_status(status)

    if update.message:
        await update.message.reply_text(message)


def main() -> None:
    app = ApplicationBuilder().token(env["token"]).build()

    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("host_status", host_status))

    print(f"{bot_config['bot']['name']} is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
