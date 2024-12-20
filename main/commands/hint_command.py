from telegram import Update
from telegram.ext import ContextTypes
from main.constants import HINT_MESSAGE

class HintCommand:
    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(HINT_MESSAGE)

    @staticmethod
    def get_command_name():
        return "hint"