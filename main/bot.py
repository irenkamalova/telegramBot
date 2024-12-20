import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from collections import defaultdict
from main.command_scanner import CommandsScanner
from main.commands.start_command import StartCommand
from main.commands.hint_command import HintCommand
from main.messages.handle_message_command import HandleMessageCommand

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.user_remind_counts = defaultdict(int)

        # Initialize the bot application
        self.app = Application.builder().token(self.token).build()

        # Register command handlers
        self.register_commands()
        self.register_message_handlers()

    def register_commands(self):
        self.app.add_handler(CommandHandler("start", StartCommand().execute))
        self.app.add_handler(CommandHandler("hint", HintCommand().execute))
    
    def register_message_handlers(self):
        handle_message_command = HandleMessageCommand()
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message_command.execute))

    def run(self):
        """Run the bot application with polling."""
        import asyncio
        asyncio.run(self.app.run_polling())

    @classmethod
    def main(cls, token):
        """Main entry point for running the bot."""
        bot_instance = cls(token)
        bot_instance.run()

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
