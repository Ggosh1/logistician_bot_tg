import logging
import schedule
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, MessageHandler, filters, ConversationHandler, CallbackQueryHandler
from telegram.ext import CommandHandler
import sdek_api
import boxberry_api
import geocoder_api
import pec_api
from config import BOT_TOKEN, boxberry_acess_token
from data.users import User
from sdek_api import update_token, get_token
from data import db_session


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.WARNING
)
logger = logging.getLogger(__name__)


async def start(update, context):
    context.user_data.clear()
    user = update.effective_user
    user_db = db_sess.query(User).filter(User.tg_id == user.id).first()
    if user_db is None:
        push_data = User()
        push_data.tg_id = user.id
        push_data.feedback = None
        db_sess.add(push_data)
        db_sess.commit()
    reply_keyboard = [['Сравнить варианты доставки', 'Оценить работу бота']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_html(
        f"Привет {user.mention_html()}! Я бот-логист.\n\nЯ помогу узнать, какой курьерской службой/транспортной компанией"
        f"будет выгодно отправить посылку/груз в твоем случае.", reply_markup=markup)
    return 1


async def chosen_option(update, context):
    msg = update.message.text
    if msg.lower() == 'сравнить варианты доставки':
        inline_keyboard = [[InlineKeyboardButton('Москва', callback_data='#city_Москва'),
                            InlineKeyboardButton('Санкт-Петербург', callback_data='#city_Санкт-Петербург')],
                           [InlineKeyboardButton('Новосибирск', callback_data='#city_Новосибирск'),
                            InlineKeyboardButton('Екатеринбург', callback_data='#city_Екатеринбург')],
                           [InlineKeyboardButton('Казань', callback_data='#city_Казань'),
                            InlineKeyboardButton('Самара', callback_data='#city_Самара'),
                            InlineKeyboardButton('Уфа', callback_data='#city_Уфа')],
                           [InlineKeyboardButton('Нижний Новгород', callback_data='#city_Нижний_Новгород'),
                            InlineKeyboardButton('Красноярск', callback_data='#city_Красноярск')],
                           [InlineKeyboardButton('Челябинск', callback_data='#city_Челябинск'),
                            InlineKeyboardButton('Воронеж', callback_data='#city_Воронеж'),
                            InlineKeyboardButton('Пермь', callback_data='#city_Пермь')],
                           [InlineKeyboardButton('Ростов-на-Дону', callback_data='#city_Ростов-на-Дону'),
                            InlineKeyboardButton('Омск', callback_data='#city_Омск'),
                            InlineKeyboardButton('Краснодар', callback_data='#city_Краснодар')],
                           [InlineKeyboardButton('Волгоград', callback_data='#city_Волгоград'),
                            InlineKeyboardButton('Саратов', callback_data='#city_Саратов'),
                            InlineKeyboardButton('Тюмень', callback_data='#city_Тюмень')]]
        markup = InlineKeyboardMarkup(inline_keyboard)
        await update.message.reply_html(
            f"Напишите город отправителя или выберите один из самых популярных вариантов",
            reply_markup=markup
        )
        return 2
    elif msg.lower() == 'оценить работу бота':
        users = db_sess.query(User).all()
        rate_sum = 0
        rated_users = 0
        for el in users:
            if el.feedback is not None:
                rate_sum += el.feedback
                rated_users += 1
        if rated_users == 0:
            await update.message.reply_html(f'Пожалуйста, оцените работу бота по шкале от 0 до 10')
        else:
            await update.message.reply_html(f'Нашим ботом уже воспользовалось {len(users)} человек!\n'
                                            f'Средняя оценка наших пользователей: {round(rate_sum / rated_users, 2)}\n'
                                            f'Пожалуйста, оцените работу бота по шкале от 0 до 10')
        return 10
    else:
        reply_keyboard = [['Сравнить варианты доставки', 'Оценить работу бота']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        await update.message.reply_html('Извините, я Вас не понимаю...', reply_markup=markup)
        return 1


async def choose_city_from(update, context):
    inline_keyboard = [[InlineKeyboardButton('Москва', callback_data='#city_Москва'),
                        InlineKeyboardButton('Санкт-Петербург', callback_data='#city_Санкт-Петербург')],
                       [InlineKeyboardButton('Новосибирск', callback_data='#city_Новосибирск'),
                        InlineKeyboardButton('Екатеринбург', callback_data='#city_Екатеринбург')],
                       [InlineKeyboardButton('Казань', callback_data='#city_Казань'),
                        InlineKeyboardButton('Самара', callback_data='#city_Самара'),
                        InlineKeyboardButton('Уфа', callback_data='#city_Уфа')],
                       [InlineKeyboardButton('Нижний Новгород', callback_data='#city_Нижний_Новгород'),
                        InlineKeyboardButton('Красноярск', callback_data='#city_Красноярск')],
                       [InlineKeyboardButton('Челябинск', callback_data='#city_Челябинск'),
                        InlineKeyboardButton('Воронеж', callback_data='#city_Воронеж'),
                        InlineKeyboardButton('Пермь', callback_data='#city_Пермь')],
                       [InlineKeyboardButton('Ростов-на-Дону', callback_data='#city_Ростов-на-Дону'),
                        InlineKeyboardButton('Омск', callback_data='#city_Омск'),
                        InlineKeyboardButton('Краснодар', callback_data='#city_Краснодар')],
                       [InlineKeyboardButton('Волгоград', callback_data='#city_Волгоград'),
                        InlineKeyboardButton('Саратов', callback_data='#city_Саратов'),
                        InlineKeyboardButton('Тюмень', callback_data='#city_Тюмень')]]
    markup = InlineKeyboardMarkup(inline_keyboard)
    query = update.callback_query
    if query:  # юзер нажал на инлайн клаву
        city_from = query.data[6:]
        context.user_data['city_from'] = city_from
        await context.bot.send_message(chat_id=update.effective_user.id,
                                       text=f"Напишите город получателя или выберите один из самых популярных вариантов",
                                       reply_markup=markup
                                       )
        return 3
    else:  # юзер ввел текст сам
        msg = update.message.text
        try:
            city_from = geocoder_api.get_city_name(msg.lower())
            context.user_data['city_from'] = city_from
            await context.bot.send_message(chat_id=update.effective_user.id,
                                           text=f"Напишите город получателя или выберите один из самых популярных вариантов",
                                           reply_markup=markup
                                           )
            return 3
        except geocoder_api.CityNotFoundError:
            await not_understand(update, context)


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
        try:
            city_to = geocoder_api.get_city_name(msg.lower())
            context.user_data['city_to'] = city_to
            await context.bot.send_message(chat_id=update.effective_user.id,
                                           text=f"Введите количество мест (неделимых грузовых объектов (коробок, связок, упаковок))"
                                           )
            return 4
        except geocoder_api.CityNotFoundError:
            await not_understand(update, context)


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
        await not_understand(update, context)


async def read_weight(update, context):
    msg = update.message.text
    try:
        weight = float(msg)
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
        await not_understand(update, context)


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
        width, long, height = map(lambda x: float(x) * context.user_data['volume_coef'], msg.split(' '))
        context.user_data['sizes'] = [width, height, long]
        reply_keyboard = [[InlineKeyboardButton('да', callback_data='#gabarit_yes'),
                           InlineKeyboardButton('нет', callback_data='#gabarit_no')]]
        markup = InlineKeyboardMarkup(reply_keyboard)
        await update.message.reply_html(f"Вашему грузу нужна защитная транспортная упаковка?", reply_markup=markup)
        return 8
    except Exception:
        await not_understand(update, context)


async def ztu(update, context):
    query = update.callback_query
    if query.data[9:] == 'yes':
        context.user_data['ztu'] = True
    elif query.data[9:] == 'no':
        context.user_data['ztu'] = False
    reply_keyboard = [[InlineKeyboardButton('Забрать по адресу, доставить по адресу', callback_data='#deliv_dd')],
                      [InlineKeyboardButton('Забрать из отделения, доставить в отделение', callback_data='#deliv_pp')],
                      [InlineKeyboardButton('Забрать по адресу, доставить в отделение', callback_data='#deliv_dp')],
                      [InlineKeyboardButton('Забрать из отделения, доставить по адресу', callback_data='#deliv_pd')]]
    markup = InlineKeyboardMarkup(reply_keyboard)
    await context.bot.send_message(chat_id=update.effective_user.id,
                                   text=f"Введите единицы измерения размеров груза (одно место)",
                                   reply_markup=markup)
    return 9


async def delivery(update, context):
    query = update.callback_query
    home_take = True
    home_delive = True
    if query.data[7] == 'p':
        home_take = False
    if query.data[8] == 'p':
        home_delive = False
    context.user_data['home_take'] = home_take
    context.user_data['home_delive'] = home_delive
    await calculate(update, context)


async def calculate(update, context):
    city_from = ' '.join(context.user_data['city_from'].split('_'))
    city_to = ' '.join(context.user_data['city_to'].split('_'))
    places = context.user_data['places']
    weight = context.user_data['weight']
    width, long, height = context.user_data['sizes']
    ztu = context.user_data['ztu']
    home_take = context.user_data["home_take"]
    home_delive = context.user_data["home_delive"]
    text1 = f'Рассчет стоимости доставки {city_from} - {city_to}\n' \
            f'Параметры груза:\n' \
            f'Количество мест: {places}\n' \
            f'Объем на место: {round(width * long * height, 5)} м3\n' \
            f'Вес на место: {weight} кг\n' \
            f'Защитная транспортная упаковка: {"включена" if ztu else "не включена"}\n' \
            f'Забрать {"по адресу" if home_take else "из отделения"}\n' \
            f'Доставить {"по адресу" if home_delive else "в отделение"}\n' \
            f'----------------------------------------------\n'
    await context.bot.send_message(chat_id=update.effective_user.id,
                                   text=text1)
    try:
        info = pec_api.get_info_delivery(city_from=city_from, city_to=city_to,
                                         weight=weight, width=width, long=long, height=height,
                                         volume=width * long * height, is_negabarit=0, need_protected_package=ztu,
                                         places=places)
        auto_enabled = False
        auto_cost = 0
        avia_enabled = False
        avia_cost = 0
        add_list = ['ADD', 'ADD_1', 'ADD_2', 'ADD_3', 'ADD_4']
        if 'auto' in info.keys():
            auto_enabled = True
            auto_cost = int(info['auto'][2])
            if home_take:
                auto_cost += int(info['take'][2])
            if home_delive:
                auto_cost += int(info['deliver'][2])
            if 'autonegabarit' in info.keys():
                auto_cost += int(info['autonegabarit'][2])
            for i in add_list:
                if i in info.keys():
                    auto_cost += int(info[i]['3'])
        if 'avia' in info.keys():
            avia_enabled = True
            avia_cost = int(info['avia'][2])
            if home_take:
                avia_cost += int(info['take'][2])
            if home_delive:
                avia_cost += int(info['deliver'][2])
            for i in add_list:
                if i in info.keys():
                    avia_cost += int(info[i]['3'])
        auto_time = 'неизвестен'
        if 'periods_days' in info.keys():
            auto_time = info['periods_days']
        text2 = f'Транспортная компания: ПЭК:\n' \
                f'Автоперевозка: {"недоступна" if not auto_enabled else str(auto_cost) + f"р; срок в днях:"} {auto_time}\n' \
                f'Авиаперевозка: {"недоступна" if not avia_enabled else str(avia_cost) + "р"}'  # незнаю какой здесь ключ
        await context.bot.send_message(chat_id=update.effective_user.id,
                                       text=text2)
    except pec_api.NoDeliveryToThisCity as err:
        await context.bot.send_message(chat_id=update.effective_user.id,
                                       text=f'{str(err)}')
    try:
        if home_delive:
            is_target = False
        else:
            is_target = True
        info = boxberry_api.get_info_delivery(token=boxberry_acess_token, weight=weight * 1000, city_from=city_from,
                                              city_to=city_to, height=height * 0.01, width=width * 0.01,
                                              depth=long * 0.01, is_target=True)
        text1 = ''
        if home_take:
            text1 = '\nКомпания Boxberry осуществляет забор груза только из ПВЗ (пункта выдачи заказа)'
        if ztu:
            text1 += '\n' + '!В стоимость не включена цена защитной транспортной упаковки'
        text2 = f'\nТранспортная компания Boxberry:' \
                f'\n!Данная стоимость актуальная для одного товарного места' \
                f'{text1}' \
                f'\nАвтоперевозка: {info["price"]}р\n' \
                f'Срок доставки в днях: {info["delivery_period"]}'
        await context.bot.send_message(chat_id=update.effective_user.id, text=text2)

    except Exception as ex:
        print(ex)
        await not_understand(update, context)
    try:
        sdek_data = sdek_api.get_info_delivery(city_from, city_to, height=int(height * 100), width=int(width * 100), length=int(long * 100),
                                      amount=places, weight=int(weight * 1000))
        sdek_text = 'Транспортная компания СДЭК:\n'
        if 'errors' in sdek_data.keys():
            sdek_text += 'По данному направлению при заданных условиях нет доступных тарифов'
            await context.bot.send_message(chat_id=update.effective_user.id, text=sdek_text)
        else:
            if ztu:
                sdek_text += '!Расчет произведен без учета стоимости ЗТУ\n'
            for el in sdek_data['tariff_codes']:
                if (home_take and home_delive and 'дверь-дверь' in el['tariff_name']) or \
                        (home_take and not home_delive and 'дверь-склад' in el['tariff_name']) or\
                        (not home_take and home_delive and 'склад-дверь' in el['tariff_name']) or\
                        (not home_take and not home_delive and 'склад-склад' in el['tariff_name']):
                    sdek_text += f'{el["tariff_name"]}\n' \
                                 f'{el["tariff_description"] if "tariff_decription" in el.keys() else "Описание тарифа отсутствует"}\n' \
                                 f'{el["delivery_sum"]}р\n' \
                                 f'Максимальное время доставки в днях: {el["period_max"]}\n\n'
            await context.bot.send_message(chat_id=update.effective_user.id, text=sdek_text)
        return ConversationHandler.END
    except Exception as ex:
        print(ex)
        await not_understand(update, context)


async def feedback(update, context):
    try:
        msg = int(update.message.text)
        if msg >= 0 and msg <= 10:
            user = db_sess.query(User).filter(User.tg_id == update.effective_user.id).first()
            user.feedback = msg
            db_sess.commit()
            reply_keyboard = [['Сравнить варианты доставки', 'Оценить работу бота']]
            markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
            await update.message.reply_text("Спасибо за обратную связь!", reply_markup=markup)
            return 1
        else:
            await update.message.reply_text("Я умею считать только от 0 до 10")
    except Exception as ex:
        await not_understand(update, context)
        print(ex)


async def help(update, context):
    await update.message.reply_text("Чтобы начать диалог, напиши /start\n"
                                    "Если что-то пошло не так, пиши /stop и /start")


async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
    context.user_data.clear()
    return ConversationHandler.END


async def not_understand(update, context):
    await context.bot.send_message(chat_id=update.effective_user.id,
                                   text='Извините, я не понял вашего ответа..Попробуйте еще раз\n'
                                        'Для перезапуска напишите /stop, а после /start')


def main():
    global db_sess
    db_session.global_init("db/users.db")
    db_sess = db_session.create_session()
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
            8: [CallbackQueryHandler(ztu, pattern='^' + '#gabarit_')],
            9: [CallbackQueryHandler(delivery, pattern='^' + '#deliv_')],
            10: [MessageHandler(filters.TEXT & ~filters.COMMAND, feedback)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("help", help))
    application.run_polling()
    sdek_api.update_token()
    sdek_access_token = get_token()
    schedule.every(49).minutes.do(update_token)
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    main()