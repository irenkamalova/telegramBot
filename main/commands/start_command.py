from telegram import Update
from telegram.ext import ContextTypes
from main.constants import START_MESSAGE

class StartCommand:
    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(START_MESSAGE)

    @staticmethod
    def get_command_name():
        return "start"