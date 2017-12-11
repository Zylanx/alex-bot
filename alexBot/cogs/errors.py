import traceback
import logging

import discord
from discord.ext import commands

from ..tools import Cog

log = logging.getLogger(__name__)


class CommandErrorHandler(Cog):

    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        """The event triggered when an error is raised while invoking a command."""
        if isinstance(error, commands.CommandNotFound):
            return

        msg = None

        if isinstance(error, commands.DisabledCommand):
            msg = f'{ctx.command} has been disabled.'

        elif isinstance(error, commands.NotOwner):
            msg = f'{ctx.command} is a owner only command.'

        elif isinstance(error, commands.NoPrivateMessage):
            msg = f'{ctx.command} can not be used in Private Messages.'

        elif isinstance(error, commands.BadArgument):
            msg = f'Bad argument! {error} See {ctx.prefix}help {ctx.command} for help!'
            log.warning(f"bad argument on {ctx.command}: {error}")


        elif isinstance(error, commands.MissingRequiredArgument):
            msg = f'Parameter {error.param} is required but missing! See {ctx.prefix}help {ctx.command} for help!'

        elif isinstance(error, commands.CommandInvokeError):
            error = error.original

            if isinstance(error, discord.Forbidden):
                msg = 'A permission error occured while executing this command! ' \
                      'Make sure I have the required permissions and try again.'

        # post the error into the chat if no short error message could be generated
        if msg is None:
            trace = traceback.format_exception(type(error), error, error.__traceback__, limit=5)
            actual_trace = '\n'.join(trace)
            msg = f'congrats, you broke something teribly. contact <@108429628560924672> please'
            log.error(f"{ctx.author.id} broke bot running {ctx.command} with args {ctx.args} : {ctx.kwargs}\n"
                      f":{actual_trace}")

        try:
            await ctx.send(msg)
        except discord.HTTPException:
            await ctx.send(f'error message too long')


def setup(bot: commands.Bot):
    bot.add_cog(CommandErrorHandler(bot))
