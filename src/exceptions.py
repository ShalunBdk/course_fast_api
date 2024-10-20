
from datetime import date

from fastapi import HTTPException


class NabronirovalException(Exception):

    detail = "Не ожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)

class NabronirovalHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class ObjectNotFoundException(NabronirovalException):
    detail = "Объект не найден"

class RoomNotFoundException(ObjectNotFoundException):
    detail = "Команта не найдена"

class HotelNotFoundException(ObjectNotFoundException):
    detail = "Отель не найден"

class AllRoomsAreBookedException(NabronirovalException):
    detail = "Не осталось свободных номеров"

class ObjectAlreadyExistsException(NabronirovalException):
    detail = "Похожий объект уже существует"

class UserAlreadyExistsException(NabronirovalException):
    detail = "Пользователь с такой почтой уже зарегистрирован"

class NullPasswordException(NabronirovalException):
    detail = "Отправлен пустой пароль"

class IncorrectTokenException(NabronirovalException):
    detail = "Некорректный токен"

class NoAccessTokenException(NabronirovalException):
    detail = "Не найден токен доступа"

class EmailNotRegisteredException(NabronirovalException):
    detail = "Пользователь с таким email не найден"

class IncorrectPasswordException(NabronirovalException):
    detail = "Введён неверный пароль"

def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_from >= date_to:
        raise HTTPException(status_code=409, detail="Дата заезда позже даты выезда")
    
class HotelNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Отель не найден"

class RoomNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Номер не найден"

class AllRoomsAreBookedHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Не осталось свободных номеров"

class UserAlreadyExistsHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Пользователь с такой почтой уже зарегистрирован"

class NullPasswordHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Отправлен пустой пароль"

class IncorrectTokenHTTPException(NabronirovalHTTPException):
    status_code = 401
    detail = "Некорректный токен"

class NoAccessTokenHTTPException(NabronirovalHTTPException):
    status_code = 401
    detail = "Вы не предоставили токен доступа"

class EmailNotRegisteredHTTPException(NabronirovalHTTPException):
    status_code = 401
    detail = "Пользователь с таким email не найден"

class IncorrectPasswordHTTPException(NabronirovalHTTPException):
    status_code = 401
    detail = "Введён неверный пароль"