from handlers.callback_data import CallbackData
from handlers.context import Ctx


def with_context(func):
    async def wrapper(update, context, *args, **kwargs):
        query = update.callback_query
        data = CallbackData.parse(query.data)

        storage = context.application.bot_data["storage"]
        broadcaster = context.application.bot_data["broadcaster"]

        game = storage.load(data.gid)

        user = update.effective_user

        ctx = Ctx(
            update=update,
            context=context,
            data=data,
            game=game,
            storage=storage,
            broadcaster=broadcaster,
            user=user,
        )

        return await func(ctx, *args, **kwargs)

    return wrapper
