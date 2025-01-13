from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from main_bot import admins_id

def main_keyboard(user_id):
    kb_list = [
        [KeyboardButton(text='🐱 Смотреть питомцев'), KeyboardButton(text='➕ Добавить питомца')],
        [KeyboardButton(text='🏅 Рейтинг'), KeyboardButton(text='👤 Мой аккаунт')]
    ]
    if user_id in admins_id:
        kb_list.append([KeyboardButton(text='⚙️ Админ панель 📄')])
    return ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, input_field_placeholder='Мяукнуть...')


watching_pets = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='🎲 Случайный питомец'), KeyboardButton(text='🔎 Поиск питомца')],
    [KeyboardButton(text='⬅️ В Главное меню')]
    ],
    resize_keyboard=True, input_field_placeholder='Мяукнуть...')


search_pet_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='👤 По имени пользователя')], [KeyboardButton(text='🐱 По имени питомца')],
    [KeyboardButton(text='⬅️ Назад')]
    ],
    resize_keyboard=True)


def pets_keyboard(pet_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='❤️ Лайк', callback_data=f'like_{pet_id}'),
            InlineKeyboardButton(text='💛 В избранное', callback_data=f'favorite_{pet_id}')
        ],
        [InlineKeyboardButton(text='🐱 Следующий питомец', callback_data='next_pet')]
    ])


def pets_keyboard_without_next(pet_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='❤️ Лайк', callback_data=f'like_{pet_id}'),
            InlineKeyboardButton(text='💛 В избранное', callback_data=f'favorite_{pet_id}')
        ]
    ])


def my_account_keyboard(user_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Мои питомцы', callback_data=f'my_pets_{user_id}')],
        [InlineKeyboardButton(text='💛 Моё избранное', callback_data=f'my_favorites_{user_id}')]
    ])


exit_search_pet = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отменить поиск', callback_data='exit_search_pet')]
    ])


exit_pet_add = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отменить добавление', callback_data='exit_pet_add')]
    ])


def delete_pet(pet_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='❌ Удалить питомца', callback_data=f'delete_pet_{pet_id}')]
    ])


def delete_pet_check(pet_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='✅ Да', callback_data=f'delete_yes_{pet_id}'),
            InlineKeyboardButton(text='❌ Нет', callback_data=f'delete_no_{pet_id}')
        ]
    ])


def delete_favorite(pet_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='❌ Удалить из избранного', callback_data=f'delete_favorite_{pet_id}')]
    ])


def delete_favorite_check(pet_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='✅ Да', callback_data=f'delfavorite_yes_{pet_id}'),
            InlineKeyboardButton(text='❌ Нет', callback_data=f'delfavorite_no_{pet_id}')
        ]
    ])


def admin_keyboard(pet_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='✅ Добавить', callback_data=f'true_{pet_id}'),
            InlineKeyboardButton(text='🚫 Отклонить', callback_data=f'false_{pet_id}')
        ]
    ])


link_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сайт Telegram-бота', url='https://nikosvex.github.io/Web-site/')]
    ])
