from dataclasses import dataclass
from telegram import Update, User
from telegram.ext import CallbackContext
from domain.models import Game
from infrastructure.storage.sqlite import Storage
from infrastructure.telegram.broadcaster import Broadcaster
from handlers.callback_data import CallbackData


@dataclass
class Ctx:
    update: Update
    context: CallbackContext
    data: CallbackData
    game: Game
    storage: Storage
    broadcaster: Broadcaster
    user: User

    @property
    def user_str(self):
        if self.user.username:
            return f"{self.user.username} ({self.user.id})"
        return f"{self.user.first_name} {self.user.last_name} ({self.user.id})"
