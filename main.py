import logging
from telegram.ext import Application, MessageHandler, filters, ConversationHandler, CallbackQueryHandler
from config import BOT_TOKEN
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import pec_api

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
    query = update.callback_query
    if query:  # юзер нажал на инлайн клаву
        city_from = query.data[6:]
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
        await context.bot.send_message(chat_id=update.effective_user.id,
                                      text=f"Напишите город получателя или выберите один из самых популярных вариантов",
                                      reply_markup=markup
                                      )
        return 3
    else:  # юзер ввел текст сам
        msg = update.message.text
        city_from = msg.lower()
        # TODO: через геокодер предлагаем варианты


async def choose_city_to(update, context):
    query = update.callback_query
    if query:  # юзер нажал на инлайн клаву
        city_to = query.data[6:]
        context.user_data['city_to'] = city_to
        await context.bot.send_message(chat_id=update.effective_user.id,
                                      text=f"Введите количество мест (неделимых грузовых объектов (коробок, связок, упаковок))"
                                      )
        return 4
    else:  # юзер ввел текст сам
        msg = update.message.text
        city_from = msg.lower()
        # TODO: через геокодер предлагаем варианты


async def read_places(update, context):
    msg = update.message.text
    try:
        places = int(msg)
        context.user_data['places'] = places
        await update.message.reply_html(
            f"Введите вес в кг на одно место"
        )
        return 5

    except ValueError:
        # TODO: некорректное значение
        pass


async def read_weight(update, context):
    msg = update.message.text
    try:
        weight = int(msg)
        context.user_data['weight'] = weight
        reply_keyboard = [[InlineKeyboardButton('мм', callback_data='#units_mm'),
                           InlineKeyboardButton('см', callback_data='#units_sm'),
                           InlineKeyboardButton('метр', callback_data='#units_m')]]
        markup = InlineKeyboardMarkup(reply_keyboard)
        await context.bot.send_message(chat_id=update.effective_user.id,
                                      text=f"Введите единицы измерения размеров груза (одно место)",
                                      reply_markup=markup)
        return 6

    except ValueError:
        # TODO: некорректное значение
        pass


async def read_units(update, context):
    query = update.callback_query
    if query.data[7:] == 'mm':
        context.user_data['volume_coef'] = 0.001
    elif query.data[7:] == 'sm':
        context.user_data['volume_coef'] = 0.01
    elif query.data[7:] == 'm':
        context.user_data['volume_coef'] = 1
    await context.bot.send_message(chat_id=update.effective_user.id,
        text=f"Введите ширину, длину, высоту груза (на одно место) через пробел\n\nПример:\n20 30 50")
    return 7


async def read_sizes(update, context):
    try:
        msg = update.message.text
        width, long, height = map(lambda x: int(x) * context.user_data['volume_coef'], msg.split(' '))
        context.user_data['sizes'] = [width, height, long]
        reply_keyboard = [[InlineKeyboardButton('да', callback_data='#gabarit_yes'),
                           InlineKeyboardButton('нет', callback_data='#gabarit_no')]]
        markup = InlineKeyboardMarkup(reply_keyboard)
        await update.message.reply_html(f"Вашему грузу нужна защитная транспортная упаковка?", reply_markup=markup)
        return 8
    except Exception:
        # TODO: некорректное значение
        pass


async def ztu(update, context):
    query = update.callback_query
    if query.data[9:] == 'yes':
        context.user_data['ztu'] = True
    elif query.data[9:] == 'no':
        context.user_data['ztu'] = False
    await calculate(update, context)


async def calculate(update, context):
    city_from = ' '.join(context.user_data['city_from'].split('_'))
    city_to = ' '.join(context.user_data['city_to'].split('_'))
    places = context.user_data['places']
    weight = context.user_data['weight']
    width, long, height = context.user_data['sizes']
    ztu = context.user_data['ztu']
    info = pec_api.get_info_delivery(city_from=city_from, city_to=city_to,
                                     weight=weight, width=width, long=long, height=height,
                                     volume=width * long * height, is_negabarit=0, need_protected_package=ztu,
                                     places=places)
    print(info)
    auto_enabled = False
    auto_cost = 0
    avia_enabled = False
    avia_cost = 0
    add_list = ['ADD', 'ADD_1', 'ADD_2', 'ADD_3', 'ADD_4']
    if 'auto' in info.keys():
        auto_enabled = True
        auto_cost = int(info['auto'][2]) + int(info['take'][2]) + int(info['deliver'][2])
        for i in add_list:
            if i in info.keys():
                auto_cost += int(info[i]['3'])
    if 'avia' in info.keys():
        avia_enabled = True
        auto_cost = int(info['take'][2]) + int(info['avia'][2]) + int(info['deliver'][2])
        for i in add_list:
            if i in info.keys():
                auto_cost += int(info[i]['3'])
    text = f'Рассчет стоимости доставки {city_from} - {city_to}\n' \
           f'Параметры груза:\n' \
           f'Количество мест: {places}\n' \
           f'Объем на место: {width * long * height} м3\n' \
           f'Вес на место: {weight} кг\n' \
           f'Защитная транспортная упаковка: {"включена" if ztu else "не включена"}\n' \
           f'----------------------------------------------\n' \
           f'Транспортная компания: ПЭК:\n' \
           f'Автоперевозка: {"недоступна" if not auto_enabled else str(auto_cost) + f"р; срок:"}{info["periods_days"]}\n' \
           f'Авиаперевозка: {"недоступна" if not avia_enabled else str(avia_cost) + "р"}' # TODO: незнаю какой здесь ключ
    await context.bot.send_message(chat_id=update.effective_user.id,
                                   text=text)


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
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, read_places)],
            5: [MessageHandler(filters.TEXT & ~filters.COMMAND, read_weight)],
            6: [CallbackQueryHandler(read_units, pattern='^' + '#units_')],
            7: [MessageHandler(filters.TEXT & ~filters.COMMAND, read_sizes)],
            8: [CallbackQueryHandler(ztu, pattern='^' + '#gabarit_')]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
