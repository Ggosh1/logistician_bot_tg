import logging
from telegram.ext import Application, MessageHandler, filters, ConversationHandler, CallbackQueryHandler
from config import BOT_TOKEN
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)


async def start(update, context):
    user = update.effective_user
    reply_keyboard = [['Сравнить варианты доставки', 'чето'],
                      ['чето', 'чето']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    # await update.message.reply_html(
    #    f"Привет {user.mention_html()}! Я бот-логист.\n\nЯ помогу узнать, какой курьерской службой/транспортной компанией"
    #    f"будет выгодно отправить посылку/груз в твоем случае.",
    #    reply_markup=markup
    # )
    await update.message.reply_html(
        f"Привет {user.mention_html()}! Я бот-логист.\n\nЯ помогу узнать, какой курьерской службой/транспортной компанией"
        f"будет выгодно отправить посылку/груз в твоем случае.", reply_markup=markup)
    return 1


async def chosen_option(update, context):
    msg = update.message.text
    if msg.lower() == 'сравнить варианты доставки':
        # reply_keyboard = [['Москва', 'Санкт-Петербург'],
        #                  ['Новосибирск', 'Екатеринбург'],
        #                  ['Казань', 'Самара', 'Уфа'],
        #                  ['Нижний Новгород', 'Красноярск'],
        #                  ['Челябинск', 'Воронеж', 'Пермь'],
        #                  ['Ростов-на-Дону', 'Омск', 'Краснодар'],
        #                  ['Волгоград', 'Саратов', 'Тюмень']]
        inline_keyboard = [[InlineKeyboardButton('Москва', callback_data='#city_москва'),
                            InlineKeyboardButton('Санкт-Петербург', callback_data='#city_санкт-петербург')],
                           [InlineKeyboardButton('Новосибирск', callback_data='#city_новосибирск'),
                            InlineKeyboardButton('Екатеринбург', callback_data='#city_екатеринбург')],
                           [InlineKeyboardButton('Казань', callback_data='#city_казань'),
                            InlineKeyboardButton('Самара', callback_data='#city_самара'),
                            InlineKeyboardButton('Уфа', callback_data='#city_уфа')],
                           [InlineKeyboardButton('Нижний Новгород', callback_data='#city_нижний_новгород'),
                            InlineKeyboardButton('Красноярск', callback_data='#city_красноярск')],
                           [InlineKeyboardButton('Челябинск', callback_data='#city_челябинск'),
                            InlineKeyboardButton('Воронеж', callback_data='#city_воронеж'),
                            InlineKeyboardButton('Пермь', callback_data='#city_пермь')],
                           [InlineKeyboardButton('Ростов-на-Дону', callback_data='#city_ростов_на_дону'),
                            InlineKeyboardButton('Омск', callback_data='#city_омск'),
                            InlineKeyboardButton('Краснодар', callback_data='#city_краснодар')],
                           [InlineKeyboardButton('Волгоград', callback_data='#city_волгоград'),
                            InlineKeyboardButton('Саратов', callback_data='#city_саратов'),
                            InlineKeyboardButton('Тюмень', callback_data='#city_тюмень')],
                           [InlineKeyboardButton('В начало', callback_data='to_start')]]
        markup = InlineKeyboardMarkup(inline_keyboard)
        await update.message.reply_html(
            f"Напишите город отправителя или выберите один из самых популярных вариантов",
            reply_markup=markup
        )
        return 2
    else:
        reply_keyboard = [['Сравнить варианты доставки', 'чето'],
                          ['чето', 'чето']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        await update.message.reply_html('Извините, я Вас не понимаю...', reply_markup=markup)
        return 1


async def choose_city_from(update, context):
    msg = update.message.text
    query = update.callback_query
    if query:  # юзер нажал на инлайн клаву
        city_from = query.data
        context.user_data['city_from'] = city_from
        inline_keyboard = [[InlineKeyboardButton('Москва', callback_data='#city_москва'),
                            InlineKeyboardButton('Санкт-Петербург', callback_data='#city_санкт-петербург')],
                           [InlineKeyboardButton('Новосибирск', callback_data='#city_новосибирск'),
                            InlineKeyboardButton('Екатеринбург', callback_data='#city_екатеринбург')],
                           [InlineKeyboardButton('Казань', callback_data='#city_казань'),
                            InlineKeyboardButton('Самара', callback_data='#city_самара'),
                            InlineKeyboardButton('Уфа', callback_data='#city_уфа')],
                           [InlineKeyboardButton('Нижний Новгород', callback_data='#city_нижний_новгород'),
                            InlineKeyboardButton('Красноярск', callback_data='#city_красноярск')],
                           [InlineKeyboardButton('Челябинск', callback_data='#city_челябинск'),
                            InlineKeyboardButton('Воронеж', callback_data='#city_воронеж'),
                            InlineKeyboardButton('Пермь', callback_data='#city_пермь')],
                           [InlineKeyboardButton('Ростов-на-Дону', callback_data='#city_ростов_на_дону'),
                            InlineKeyboardButton('Омск', callback_data='#city_омск'),
                            InlineKeyboardButton('Краснодар', callback_data='#city_краснодар')],
                           [InlineKeyboardButton('Волгоград', callback_data='#city_волгоград'),
                            InlineKeyboardButton('Саратов', callback_data='#city_саратов'),
                            InlineKeyboardButton('Тюмень', callback_data='#city_тюмень')],
                           [InlineKeyboardButton('В начало', callback_data='to_start')]]
        markup = InlineKeyboardMarkup(inline_keyboard)
        await update.message.reply_html(
            f"Напишите город получателя или выберите один из самых популярных вариантов",
            reply_markup=markup
        )
        return 3

    else:  # юзер ввел текст сам
        city_from = msg.lower()
        # TODO: через геокодер предлагаем варианты


async def choose_city_to(update, context):
    msg = update.message.text
    query = update.callback_query
    if query:  # юзер нажал на инлайн клаву
        city_to = query.data
        context.user_data['city_to'] = city_to
        await update.message.reply_html(
            f"Введите суммарный вес посылки"
        )
        return 4
    else:  # юзер ввел текст сам
        city_from = msg.lower()
        # TODO: через геокодер предлагаем варианты


async def read_weight(update, context):
    msg = update.message.text
    try:
        weight = int(msg)

    except ValueError:
        # TODO: некорректное значение
        pass


async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, chosen_option)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_city_from),
                CallbackQueryHandler(choose_city_from, pattern='^' + '#city_', )],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_city_to),
                CallbackQueryHandler(choose_city_to, pattern='^' + '#city_')],
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, read_weight)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
