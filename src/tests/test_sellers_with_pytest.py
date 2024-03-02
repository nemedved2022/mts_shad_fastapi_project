import pytest
from fastapi import status
from sqlalchemy import select

from src.models import books, sellers


# Тест на ручку создающую продавца
@pytest.mark.asyncio
async def test_create_seller(db_session, async_client):
    data = {
        "first_name": "Scam",
        "last_name": "Mammoth",
        "email": "scam@avito.ru",
        "password": "9pae4uhgpewr9uhgi",
    }
    response = await async_client.post("/api/v1/seller/", json=data)

    assert response.status_code == status.HTTP_201_CREATED

    result_data = response.json()

    assert result_data == {
        "id": 1,
        "first_name": "Scam",
        "last_name": "Mammoth",
        "email": "scam@avito.ru",
    }


# Тест на ручку получения списка продавцов
@pytest.mark.asyncio
async def test_get_sellers(db_session, async_client):
    # Создаем продавцов вручную, а не через ручку, чтобы нам не попасться на ошибку которая
    # может случиться в POST ручке
    test_seller = sellers.Seller(
        id=1,
        first_name="Scam",
        last_name="Mammoth",
        email="scam@avito.ru",
        password_hash="9pae4uhgpewr9uhgi",
    )
    test_seller2 = sellers.Seller(
        id=2,
        first_name="Debian",
        last_name="Bookworm",
        email="debian12@bookworm.com",
        password_hash="9pae4uhgpewr9uhgi",
    )

    db_session.add_all([test_seller, test_seller2])
    await db_session.flush()

    response = await async_client.get("/api/v1/seller/")

    assert response.status_code == status.HTTP_200_OK

    assert len(response.json()["sellers"]) == 2  # Опасный паттерн! Если в БД есть данные, то тест упадет

    # Проверяем интерфейс ответа, на который у нас есть контракт.
    assert response.json() == {
        "sellers": [
            {
                "id": 1,
                "first_name": "Scam",
                "last_name": "Mammoth",
                "email": "scam@avito.ru",
            },
            {
                "id": 2,
                "first_name": "Debian",
                "last_name": "Bookworm",
                "email": "debian12@bookworm.com",
            },
        ]
    }


# Тест на ручку получения одного продавца
@pytest.mark.asyncio
async def test_get_single_seller(db_session, async_client):
    # Создаем продавцов вручную, а не через ручку, чтобы нам не попасться на ошибку которая
    # может случиться в POST ручке
    book = books.Book(author="Pushkin", title="Eugeny Onegin", year=2001, count_pages=104, seller_id=1)
    book_2 = books.Book(author="Lermontov", title="Mziri", year=1997, count_pages=104, seller_id=1)
    test_seller = sellers.Seller(
        id=1,
        first_name="Scam",
        last_name="Mammoth",
        email="scam@avito.ru",
        password_hash="9pae4uhgpewr9uhgi",
    )

    db_session.add_all([book, book_2, test_seller])
    await db_session.flush()

    response = await async_client.get(f"/api/v1/seller/{test_seller.id}")

    assert response.status_code == status.HTTP_200_OK

    # Проверяем интерфейс ответа, на который у нас есть контракт.
    assert response.json() == {
        "id": 1,
        "first_name": "Scam",
        "last_name": "Mammoth",
        "email": "scam@avito.ru",
        "books": [
            {
                "title": "Eugeny Onegin",
                "author": "Pushkin",
                "year": 2001,
                "count_pages": 104,
                "id": book.id,
            },
            {
                "title": "Mziri",
                "author": "Lermontov",
                "year": 1997,
                "count_pages": 104,
                "id": book_2.id,
            },
        ],
    }


# Тест на ручку удаления продавца
@pytest.mark.asyncio
async def test_delete_book(db_session, async_client):
    # Создаем вручную, а не через ручку, чтобы нам не попасться на ошибку которая
    # может случиться в POST ручке
    test_seller = sellers.Seller(
        id=1,
        first_name="Scam",
        last_name="Mammoth",
        email="scam@avito.ru",
        password_hash="9pae4uhgpewr9uhgi",
    )

    db_session.add(test_seller)
    await db_session.flush()

    response = await async_client.delete(f"/api/v1/seller/{test_seller.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    await db_session.flush()

    all_sellers = await db_session.execute(select(sellers.Seller))
    res = all_sellers.scalars().all()
    assert len(res) == 0


# Тест на ручку обновления продавца
@pytest.mark.asyncio
async def test_update_book(db_session, async_client):
    # Создаем продавца вручную, а не через ручку, чтобы нам не попасться на ошибку которая
    # может случиться в POST ручке
    test_seller = sellers.Seller(
        id=1,
        first_name="Scam",
        last_name="Mammoth",
        email="scam@avito.ru",
        password_hash="9pae4uhgpewr9uhgi",
    )

    db_session.add(test_seller)
    await db_session.flush()

    response = await async_client.put(
        f"/api/v1/seller/{test_seller.id}",
        json={
            "id": test_seller.id,
            "first_name": "Debian",
            "last_name": "Bookworm",
            "email": "debian12@bookworm.com",
        },
    )

    assert response.status_code == status.HTTP_200_OK
    await db_session.flush()

    # Проверяем, что обновились все поля
    res = await db_session.get(sellers.Seller, test_seller.id)
    assert res.id == test_seller.id
    assert res.first_name == "Debian"
    assert res.last_name == "Bookworm"
    assert res.email == "debian12@bookworm.com"
