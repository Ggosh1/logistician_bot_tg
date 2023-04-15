import logging
from telegram.ext import Application, MessageHandler, filters, ConversationHandler, CallbackQueryHandler
from config import BOT_TOKEN
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)


async def start(update, context):
    user = update.effective_user
    reply_keyboard = [['Сравнить варианты доставки', 'чето'],
                      ['чето', 'чето']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    bot_message = await update.message.reply_html(
        f"Привет {user.mention_html()}! Я бот-логист.\n\nЯ помогу узнать, какой курьерской службой/транспортной компанией"
        f"будет выгодно отправить посылку/груз в твоем случае.",
        reply_markup=markup
    )
    context.user_data['bot_message_to_edit'] = bot_message
    return 1


async def chosen_option(update, context):
    msg = update.message.text
    if msg.lower() == 'сравнить варианты доставки':
        #reply_keyboard = [['Москва', 'Санкт-Петербург'],
        #                  ['Новосибирск', 'Екатеринбург'],
        #                  ['Казань', 'Самара', 'Уфа'],
        #                  ['Нижний Новгород', 'Красноярск'],
        #                  ['Челябинск', 'Воронеж', 'Пермь'],
        #                  ['Ростов-на-Дону', 'Омск', 'Краснодар'],
        #                  ['Волгоград', 'Саратов', 'Тюмень']]
        last_bot_markup = context.user_data['bot_message_to_edit']
        await last_bot_markup.edit_reply_markup(None)
        inline_keyboard = [[InlineKeyboardButton('Москва', callback_data='#city_москва'), InlineKeyboardButton('Санкт-Петербург', callback_data='#city_санкт-петербург')],
                          [InlineKeyboardButton('Новосибирск', callback_data='#city_новосибирск'), InlineKeyboardButton('Екатеринбург', callback_data='#city_екатеринбург')],
                          [InlineKeyboardButton('Казань', callback_data='#city_казань'), InlineKeyboardButton('Самара', callback_data='#city_самара'), InlineKeyboardButton('Уфа', callback_data='#city_уфа')],
                          [InlineKeyboardButton('Нижний Новгород', callback_data='#city_нижний_новгород'), InlineKeyboardButton('Красноярск', callback_data='#city_красноярск')],
                          [InlineKeyboardButton('Челябинск', callback_data='#city_челябинск'), InlineKeyboardButton('Воронеж', callback_data='#city_воронеж'), InlineKeyboardButton('Пермь', callback_data='#city_пермь')],
                          [InlineKeyboardButton('Ростов-на-Дону', callback_data='#city_ростов_на_дону'), InlineKeyboardButton('Омск', callback_data='#city_омск'), InlineKeyboardButton('Краснодар', callback_data='#city_краснодар')],
                          [InlineKeyboardButton('Волгоград', callback_data='#city_волгоград'), InlineKeyboardButton('Саратов', callback_data='#city_саратов'), InlineKeyboardButton('Тюмень', callback_data='#city_тюмень')],
                           [InlineKeyboardButton('В начало', callback_data='to_start')]]
        markup = InlineKeyboardMarkup(inline_keyboard)
        await update.message.reply_html(
            f"Напишите город отправителя или выберите один из самых популярных вариантов",
            reply_markup=markup
        )
        return 2

async def choose_city(update, context):
    print('bassss')


async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, chosen_option)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_city),
                CallbackQueryHandler(choose_city, pattern='^' + '#city_', )]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("start", start))
    application.run_polling()


if __name__ == '__main__':
    main()