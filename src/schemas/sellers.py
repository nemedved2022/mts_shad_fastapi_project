from pydantic import BaseModel, EmailStr, Field
from .books import ReturnedBook

__all__ = ["IncomingSeller", "ReturnedAllSellers", "ReturnedSeller", "ReturnedSellerWithBooks"]


# Базовый класс "Продавца", содержащий поля, которые есть во всех классах-наследниках.
class BaseSeller(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: EmailStr = Field(max_length=100)


# Класс для валидации входящих данных. Не содержит id так как его присваивает БД.
class IncomingSeller(BaseSeller):
    password: str = Field(min_length=8)


# Класс, валидирующий исходящие данные. Он уже содержит id
class ReturnedSeller(BaseSeller):
    id: int


class ReturnedSellerWithBooks(ReturnedSeller):
    id: int
    books: list[ReturnedBook]


# Класс для возврата массива объектов "Продавец"
class ReturnedAllSellers(BaseModel):
    sellers: list[ReturnedSeller]
