#!/usr/bin/env python3
import sys
import os

def main():
    if len(sys.argv)>1 and sys.argv[1]=="dev":
        os.environ['tg-env'] = "dev"

    from config import CONFIG
    import handler

    print(f"starting tg-bot to recive netMonitor subscribtions in {CONFIG['env']}")

    from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

    updater = Updater(CONFIG['bot_token'])
    dp = updater.dispatcher

    # job_queue = updater.job_queue
    # job_queue.run_repeating(handlers.job, CONFIG['query_interval'])

    dp.add_handler(CommandHandler('start', handler.start))
    dp.add_handler(CommandHandler('auth', handler.auth))
    dp.add_handler(CommandHandler('help', handler.help))
    dp.add_handler(CommandHandler('info', handler.info))
    dp.add_handler(CommandHandler('status', handler.status))
    dp.add_handler(CommandHandler('all', handler.all))
    dp.add_handler(CommandHandler('echo', handler.echo))
    dp.add_handler(CommandHandler('subscribe', handler.subscribe))
    dp.add_handler(CommandHandler('unsubscribe', handler.unsubscribe))
    dp.add_handler(CommandHandler('subscribtions', handler.subscribtions))
    # dp.add_handler(MessageHandler(Filters.text & (~Filters.command), handler.echo))
    dp.add_error_handler(handler.on_error)
    
    print("Bot starts")
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()