# Домашнее задание №1 QA.GURU | Python Advanced | Автоматизация
## Задача

1. Разработать несколько API-автотестов на https://reqres.in (если обучались на основном курсе python - можно взять код автотестов из домашнего задания) Можно также за основу взять https://github.com/qa-guru/qa_guru_python_9_19

2. Вместо https://reqres.in разработать свой микросервис в стеке Python + FastAPI (допускается также Flask, Django).
Пример - https://github.com/qa-guru/python-advanced-intro

    - Автотесты должны также успешно проходить.

    - В коде микросервиса не должно быть хардкода. Например, не должно быть эндпоинтов типа /api/users/2 -  правильнее /api/users/{user_id}

3. Данные для ответа пока что можно хранить в текстовом файле, в следующих занятиях мы перенесем их в базу данных

4. Оформить README.md - https://school.qa.guru/teach/control/stream/view/id/465999013 в тренинге есть несколько занятий по оформлению красивой документации.

## Технологии
1. Микросервис: Python + FastAPI
2. Тесты: Python + Pytest + Requests

## Запуск проекта (локально)
1. python -m venv venv
2. source venv/Scripts/activate
3. pip install -r requirements.txt
4. uvicorn main:app —reload
5. pytest

## Автор 
Мокрушин Евгений

