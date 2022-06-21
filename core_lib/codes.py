# # coding=utf-8
SYSTEM_ERROR = -1
NO_DATA_FOUND = -5
INVALID_LOGIN_PASS = -7
INTEGRITY_ERROR = -18
OBJECT_DOES_NOT_EXIST = -10
USER_BLOCKED = -16

MESSAGES = {
    'ru': {
        SYSTEM_ERROR: 'Системная ошибка, попробуйте позже',
        NO_DATA_FOUND: 'Данные не найдены',
        OBJECT_DOES_NOT_EXIST: 'Запрашиваемого обьекта в БД не существует',
        INVALID_LOGIN_PASS: 'Неправильный логин или пароль',
        INTEGRITY_ERROR: 'Ошибка при обработке данных!',
        USER_BLOCKED: 'Доступ заблокирован!',
    },
    'en': {},
    'kg': {}
}
