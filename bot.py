import aiohttp, asyncio, warnings, pytz, datetime
import logging, logging.config, glob, sys, importlib, importlib.util, pyromod
from pathlib import Path
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from config import Config
from plugins.web_support import web_server
from plugins.file_rename import app

# Get logging configurations
logging.config.fileConfig("logging.conf")
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("cinemagoer").setLevel(logging.ERROR)


class Digital_FileRenameBot(Client):
    def __init__(self):
        super().__init__(
            name="Digital_FileRenameBot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=200,
            plugins={"root": "plugins"},
            sleep_threshold=15,
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username
        self.uptime = Config.BOT_UPTIME

        # Start web server
        app_runner = aiohttp.web.AppRunner(await web_server())
        await app_runner.setup()
        bind_address = "0.0.0.0"
        await aiohttp.web.TCPSite(app_runner, bind_address, Config.PORT).start()

        # Load plugins manually
        path = "plugins/*.py"
        files = glob.glob(path)
        for name in files:
            patt = Path(name)
            plugin_name = patt.stem
            plugins_path = Path(f"plugins/{plugin_name}.py")
            import_path = f"plugins.{plugin_name}"

            spec = importlib.util.spec_from_file_location(import_path, plugins_path)
            load = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(load)

            sys.modules[f"plugins.{plugin_name}"] = load
            print("Digital Botz Imported " + plugin_name)

        print(f"{me.first_name} Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️")

        # Notify admins
        for id in Config.ADMIN:
            if Config.STRING_SESSION:
                try:
                    await self.send_message(
                        id,
                        f"𝟮𝗚𝗕+ ғɪʟᴇ sᴜᴘᴘᴏʀᴛ ʜᴀs ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ᴛᴏ ʏᴏᴜʀ ʙᴏᴛ.\n\n"
                        f"Note: 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦 𝐩𝐫𝐞𝐦𝐢𝐮𝐦 𝐚𝐜𝐜𝐨𝐮𝐧𝐭 𝐬𝐭𝐫𝐢𝐧𝐠 𝐬𝐞𝐬𝐬𝐢𝐨𝐧 𝐫𝐞𝐪𝐮𝐢𝐫𝐞𝐝 "
                        f"𝐓𝐡𝐞𝐧 𝐬𝐮𝐩𝐩𝐨𝐫𝐭𝐬 𝟐𝐆𝐁+ 𝐟𝐢𝐥𝐞𝐬.\n\n"
                        f"**__{me.first_name}  Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️__**",
                    )
                except:
                    pass
            else:
                try:
                    await self.send_message(
                        id,
                        f"𝟮𝗚𝗕- ғɪʟᴇ sᴜᴘᴘᴏʀᴛ ʜᴀs ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ᴛᴏ ʏᴏᴜʀ ʙᴏᴛ.\n\n"
                        f"**__{me.first_name}  Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️__**",
                    )
                except:
                    pass

        # Log channel message
        if Config.LOG_CHANNEL:
            try:
                curr = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
                date = curr.strftime("%d %B, %Y")
                time = curr.strftime("%I:%M:%S %p")
                await self.send_message(
                    Config.LOG_CHANNEL,
                    f"**__{me.mention} Iꜱ Rᴇsᴛᴀʀᴛᴇᴅ !!**\n\n"
                    f"📅 Dᴀᴛᴇ : `{date}`\n"
                    f"⏰ Tɪᴍᴇ : `{time}`\n"
                    f"🌐 Tɪᴍᴇᴢᴏɴᴇ : `Asia/Kolkata`\n\n"
                    f"🉐 Vᴇʀsɪᴏɴ : `v{__version__} (Layer {layer})`",
                )
            except:
                print("Pʟᴇᴀꜱᴇ Mᴀᴋᴇ Tʜɪꜱ Iꜱ Aᴅᴍɪɴ Iɴ Yᴏᴜʀ Lᴏɢ Cʜᴀɴɴᴇʟ")

    async def stop(self, *args):
        await super().stop()
        print("Bot Stopped 🙄")


bot_instance = Digital_FileRenameBot()


def main():
    async def start_services():
        if Config.STRING_SESSION:
            await asyncio.gather(
                app.start(),  # Start the Pyrogram Client
                bot_instance.start(),  # Start the bot instance
            )
        else:
            await asyncio.gather(bot_instance.start())

    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_services())
    loop.run_forever()


if __name__ == "__main__":
    warnings.filterwarnings("ignore", message="There is no current event loop")
    main()
