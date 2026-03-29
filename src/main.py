from __future__ import annotations

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from config import load_bot_config, load_env
from confirmations import clear_confirmation, create_confirmation, get_confirmation
from formatters.full_status_formatter import format_full_status
from formatters.help_formatter import format_help
from formatters.status_formatter import format_host_status
from logging_setup import get_logger, log_action, setup_logging
from services.host_service import get_host_status
from services.studexhub_service import (
    backup_studexhub,
    create_invite,
    list_notice_templates,
    restart_studexhub,
    send_notice,
)
from services.system_service import get_system_services_status


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


async def system_services(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user

    if user is None or not is_admin(user.id):
        logger.warning("Unauthorized access attempt on /system_services")
        if update.message:
            await update.message.reply_text("Unauthorized.")
        return

    logger.info(
        "/system_services requested by user_id=%s username=%s",
        user.id,
        user.username,
    )
    log_action(
        user_id=user.id,
        username=user.username,
        action="system_services",
        status="started",
    )

    if update.message:
        await update.message.reply_text("Checking system services...")

    try:
        output = get_system_services_status()

        logger.info(
            "/system_services succeeded for user_id=%s username=%s",
            user.id,
            user.username,
        )
        log_action(
            user_id=user.id,
            username=user.username,
            action="system_services",
            status="success",
        )

        if update.message:
            await update.message.reply_text(output)

    except Exception as error:
        logger.exception("Failed to execute /system_services: %s", error)
        log_action(
            user_id=user.id,
            username=user.username,
            action="system_services",
            status="failed",
        )

        if update.message:
            await update.message.reply_text("❌ Failed to fetch system services.")


async def full_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user

    if user is None or not is_admin(user.id):
        logger.warning("Unauthorized access attempt on /full_status")
        if update.message:
            await update.message.reply_text("Unauthorized.")
        return

    logger.info(
        "/full_status requested by user_id=%s username=%s",
        user.id,
        user.username,
    )
    log_action(
        user_id=user.id,
        username=user.username,
        action="full_status",
        status="started",
    )

    if update.message:
        await update.message.reply_text("Collecting full system status...")

    try:
        host_data = get_host_status()
        host_formatted = format_host_status(host_data)
        services_formatted = get_system_services_status()

        final_output = format_full_status(
            host_block=host_formatted,
            services_block=services_formatted,
        )

        logger.info(
            "/full_status succeeded for user_id=%s username=%s",
            user.id,
            user.username,
        )
        log_action(
            user_id=user.id,
            username=user.username,
            action="full_status",
            status="success",
        )

        if update.message:
            await update.message.reply_text(final_output)

    except Exception as error:
        logger.exception("Failed to execute /full_status: %s", error)
        log_action(
            user_id=user.id,
            username=user.username,
            action="full_status",
            status="failed",
        )

        if update.message:
            await update.message.reply_text("❌ Failed to fetch full status.")


async def studexhub_restart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user

    if user is None or not is_admin(user.id):
        logger.warning("Unauthorized access attempt on /studexhub_restart")
        if update.message:
            await update.message.reply_text("Unauthorized.")
        return

    create_confirmation(user.id, "studexhub_restart")

    logger.info(
        "/studexhub_restart requested by user_id=%s username=%s",
        user.id,
        user.username,
    )
    log_action(
        user_id=user.id,
        username=user.username,
        action="studexhub_restart",
        status="pending",
    )

    if update.message:
        await update.message.reply_text(
            "⚠️ Confirm StudexHub restart.\nReply EXACTLY YES within 180 seconds."
        )


async def studexhub_backup(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user

    if user is None or not is_admin(user.id):
        logger.warning("Unauthorized access attempt on /studexhub_backup")
        if update.message:
            await update.message.reply_text("Unauthorized.")
        return

    logger.info(
        "/studexhub_backup requested by user_id=%s username=%s",
        user.id,
        user.username,
    )
    log_action(
        user_id=user.id,
        username=user.username,
        action="studexhub_backup",
        status="started",
    )

    if update.message:
        await update.message.reply_text("Creating StudexHub backup...")

    success, output = backup_studexhub()

    if success:
        logger.info("StudexHub backup succeeded: %s", output)
        log_action(
            user_id=user.id,
            username=user.username,
            action="studexhub_backup",
            status="success",
        )
        if update.message:
            await update.message.reply_text(f"✅ {output}")
    else:
        logger.error("StudexHub backup failed: %s", output)
        log_action(
            user_id=user.id,
            username=user.username,
            action="studexhub_backup",
            status="failed",
        )
        if update.message:
            await update.message.reply_text("❌ StudexHub backup failed.\nCheck logs.")


async def studexhub_invite(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user

    if user is None or not is_admin(user.id):
        logger.warning("Unauthorized access attempt on /studexhub_invite")
        if update.message:
            await update.message.reply_text("Unauthorized.")
        return

    logger.info(
        "/studexhub_invite requested by user_id=%s username=%s",
        user.id,
        user.username,
    )
    log_action(
        user_id=user.id,
        username=user.username,
        action="studexhub_invite",
        status="started",
    )

    if update.message:
        await update.message.reply_text("Generating invite...")

    success, output = create_invite()

    if success:
        logger.info("StudexHub invite generation succeeded")
        log_action(
            user_id=user.id,
            username=user.username,
            action="studexhub_invite",
            status="success",
        )
        if update.message:
            await update.message.reply_text(f"✅ {output}")
    else:
        logger.error("StudexHub invite generation failed: %s", output)
        log_action(
            user_id=user.id,
            username=user.username,
            action="studexhub_invite",
            status="failed",
        )
        if update.message:
            await update.message.reply_text("❌ Invite generation failed.\nCheck logs.")


async def studexhub_templates(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    user = update.effective_user

    if user is None or not is_admin(user.id):
        logger.warning("Unauthorized access attempt on /studexhub_templates")
        if update.message:
            await update.message.reply_text("Unauthorized.")
        return

    logger.info(
        "/studexhub_templates requested by user_id=%s username=%s",
        user.id,
        user.username,
    )
    log_action(
        user_id=user.id,
        username=user.username,
        action="studexhub_templates",
        status="started",
    )

    if update.message:
        await update.message.reply_text("Listing StudexHub notice templates...")

    success, output = list_notice_templates()

    if success:
        logger.info("StudexHub template listing succeeded")
        log_action(
            user_id=user.id,
            username=user.username,
            action="studexhub_templates",
            status="success",
        )
        if update.message:
            await update.message.reply_text(output)
    else:
        logger.error("StudexHub template listing failed: %s", output)
        log_action(
            user_id=user.id,
            username=user.username,
            action="studexhub_templates",
            status="failed",
        )
        if update.message:
            await update.message.reply_text(
                "❌ Failed to list StudexHub notice templates."
            )


async def studexhub_notice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    message = update.message

    if user is None or not is_admin(user.id):
        logger.warning("Unauthorized access attempt on /studexhub_notice")
        if message:
            await message.reply_text("Unauthorized.")
        return

    if message is None:
        return

    args = context.args

    if not args:
        await message.reply_text("Usage: /studexhub_notice <filename> [test]")
        return

    template_name = args[0]
    mode_arg = args[1].lower() if len(args) > 1 else None
    test_mode = mode_arg == "test"

    if not template_name.endswith(".txt"):
        await message.reply_text("Notice template must be a .txt file.")
        return

    logger.info(
        "/studexhub_notice requested by user_id=%s username=%s template=%s test_mode=%s",
        user.id,
        user.username,
        template_name,
        test_mode,
    )
    log_action(
        user_id=user.id,
        username=user.username,
        action=f"studexhub_notice:{template_name}",
        status="started_test" if test_mode else "started_broadcast",
    )

    if test_mode:
        await message.reply_text(
            f"Starting StudexHub test notice...\nTemplate: {template_name}"
        )
    else:
        await message.reply_text(
            f"Starting StudexHub notice broadcast...\nTemplate: {template_name}"
        )

    success, output = send_notice(template_name, test_mode=test_mode)

    if success:
        logger.info(
            "StudexHub notice command succeeded for template=%s test_mode=%s",
            template_name,
            test_mode,
        )
        log_action(
            user_id=user.id,
            username=user.username,
            action=f"studexhub_notice:{template_name}",
            status="success_test" if test_mode else "success_broadcast",
        )
        await message.reply_text(output)
    else:
        logger.error(
            "StudexHub notice command failed for template=%s test_mode=%s: %s",
            template_name,
            test_mode,
            output,
        )
        log_action(
            user_id=user.id,
            username=user.username,
            action=f"studexhub_notice:{template_name}",
            status="failed_test" if test_mode else "failed_broadcast",
        )
        await message.reply_text("❌ Notice process failed.\nCheck logs.")


async def handle_confirmation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    user = update.effective_user
    message = update.message

    if user is None or message is None:
        return

    if not is_admin(user.id):
        logger.warning(
            "Unauthorized text message attempt from user_id=%s username=%s",
            user.id,
            user.username,
        )
        await message.reply_text("Unauthorized.")
        return

    text = message.text

    if text not in {"YES", "NO"}:
        await message.reply_text("Reply EXACTLY YES or NO (case-sensitive).")
        return

    confirmation = get_confirmation(user.id)

    if not confirmation:
        await message.reply_text("No pending action.")
        return

    if text == "NO":
        clear_confirmation(user.id)

        logger.info(
            "Action cancelled: %s by user_id=%s username=%s",
            confirmation.action,
            user.id,
            user.username,
        )
        log_action(
            user_id=user.id,
            username=user.username,
            action=confirmation.action,
            status="cancelled",
        )

        await message.reply_text("Action cancelled.")
        return

    if text == "YES":
        clear_confirmation(user.id)

        logger.info(
            "Action confirmed: %s by user_id=%s username=%s",
            confirmation.action,
            user.id,
            user.username,
        )
        log_action(
            user_id=user.id,
            username=user.username,
            action=confirmation.action,
            status="confirmed",
        )

        if confirmation.action == "studexhub_restart":
            await message.reply_text("Restarting StudexHub...")

            success, output = restart_studexhub()

            if success:
                logger.info("StudexHub restart succeeded")
                log_action(
                    user_id=user.id,
                    username=user.username,
                    action="studexhub_restart",
                    status="success",
                )
                await message.reply_text("✅ StudexHub restarted successfully.")
            else:
                logger.error("StudexHub restart failed: %s", output)
                log_action(
                    user_id=user.id,
                    username=user.username,
                    action="studexhub_restart",
                    status="failed",
                )
                await message.reply_text("❌ StudexHub restart failed.\nCheck logs.")
            return

        await message.reply_text(f"Confirmed: {confirmation.action}")


def main() -> None:
    logger.info("Starting bot: %s", bot_config["bot"]["name"])

    app = ApplicationBuilder().token(env["token"]).build()

    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("host_status", host_status))
    app.add_handler(CommandHandler("system_services", system_services))
    app.add_handler(CommandHandler("full_status", full_status))
    app.add_handler(CommandHandler("studexhub_restart", studexhub_restart))
    app.add_handler(CommandHandler("studexhub_backup", studexhub_backup))
    app.add_handler(CommandHandler("studexhub_invite", studexhub_invite))
    app.add_handler(CommandHandler("studexhub_templates", studexhub_templates))
    app.add_handler(CommandHandler("studexhub_notice", studexhub_notice))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_confirmation))

    app.run_polling()


if __name__ == "__main__":
    main()
