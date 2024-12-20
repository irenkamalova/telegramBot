# main/commands/handle_message_command.py

from queue import Queue
from telegram import Update
from telegram.ext import ContextTypes
from main.constants import ERROR_MESSAGE, FINAL_MESSAGE, KEY_WORDS_SET, RESPONSE_QUEUE
import logging

class HandleMessageCommand:
    def __init__(self):
        # This will keep track of user states (sets and queues)
        self.user_states = {}

    # Configure logging
    logging.basicConfig(
        filename='bot.log',         # Log file name
        filemode='a',               # Append mode
        format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
        level=logging.INFO           # Minimum log level
    )

    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.message.from_user
        user_id = user.id
        first_name = user.first_name
        last_name = user.last_name if user.last_name else ''
        username = user.username if user.username else 'No username'

        user_message = update.message.text.strip().lower()

        print("User with [id: {}] and name [{}] [{}] and userName [{}] sent: [{}]".format(user_id, first_name, last_name, username, user_message))
        logging.info(f"User with [id: {user_id}] and name [name: {first_name} {last_name}] sent: [user_message: {update.message.text}]")

        # Initialize user state if it doesn't exist
        if user_id not in self.user_states:
            self.user_states[user_id] = {
                'letters': KEY_WORDS_SET.copy(),  # Create a new set for the user
                'responses': Queue()            # Create a new queue for the user
            }
            # Fill the queue with responses
            for response in RESPONSE_QUEUE:
                self.user_states[user_id]['responses'].put(response)

        if len(self.user_states[user_id]['letters']) == 0:
            await update.message.reply_text(FINAL_MESSAGE)
            return

        # Validate the user message
        if user_message in self.user_states[user_id]['letters']:
            # Remove the letter from the set
            self.user_states[user_id]['letters'].remove(user_message)

            # Get the next response from the queue
            if not self.user_states[user_id]['responses'].empty():
                next_response = self.user_states[user_id]['responses'].get()
                await update.message.reply_text(next_response) 
                if len(self.user_states[user_id]['letters']) == 0:
                    await update.message.reply_text(FINAL_MESSAGE)
        else:
            await update.message.reply_text(ERROR_MESSAGE)
