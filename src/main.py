from __future__ import annotations

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from config import load_bot_config, load_env
from formatters.help_formatter import format_help
from formatters.status_formatter import format_host_status
from logging_setup import get_logger, log_action, setup_logging
from services.host_service import get_host_status


setup_logging()
logger = get_logger()

env = load_env()
bot_config = load_bot_config()


def is_admin(user_id: int) -> bool:
    return user_id == env["admin_id"]


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user

    if user is None or not is_admin(user.id):
        logger.warning("Unauthorized access attempt on /ping")
        if update.message:
            await update.message.reply_text("Unauthorized.")
        return

    logger.info("/ping executed by user_id=%s username=%s", user.id, user.username)
    log_action(
        user_id=user.id,
        username=user.username,
        action="ping",
        status="success",
    )

    if update.message:
        await update.message.reply_text("pong")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user

    if user is None or not is_admin(user.id):
        logger.warning("Unauthorized access attempt on /help")
        if update.message:
            await update.message.reply_text("Unauthorized.")
        return

    logger.info("/help executed by user_id=%s username=%s", user.id, user.username)
    log_action(
        user_id=user.id,
        username=user.username,
        action="help",
        status="success",
    )

    if update.message:
        await update.message.reply_text(format_help())


async def host_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user

    if user is None or not is_admin(user.id):
        logger.warning("Unauthorized access attempt on /host_status")
        if update.message:
            await update.message.reply_text("Unauthorized.")
        return

    try:
        status = get_host_status()
        message = format_host_status(status)

        logger.info(
            "/host_status executed by user_id=%s username=%s",
            user.id,
            user.username,
        )
        log_action(
            user_id=user.id,
            username=user.username,
            action="host_status",
            status="success",
        )

        if update.message:
            await update.message.reply_text(message)

    except Exception as error:
        logger.exception("Failed to execute /host_status: %s", error)
        log_action(
            user_id=user.id,
            username=user.username,
            action="host_status",
            status="failed",
        )

        if update.message:
            await update.message.reply_text("Failed to fetch host status.")


def main() -> None:
    logger.info("Starting bot: %s", bot_config["bot"]["name"])

    app = ApplicationBuilder().token(env["token"]).build()

    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("host_status", host_status))

    app.run_polling()


if __name__ == "__main__":
    main()
