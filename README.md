# OTUS Petclinic Testing Project

Автоматизация тестирования веб-приложения Petclinic: реализованы API и UI тесты.

## Используемые технологии
- pytest
- Selenium
- Allure
- xdist
- requests
- PyMySQL
- black

## Установка зависимостей

```bash
pip install -r requirements.txt
```

## Запуск тестов

```bash
pytest -n 4
```

Дополнительные параметры командной строки можно посмотреть в `conftest.py` в функции `pytest_addoption`. Основные параметры имеют дефолтные значения, указанные в `pytest.ini`.


## Связанные проекты

- [Spring Petclinic REST (backend)](https://github.com/spring-petclinic/spring-petclinic-rest)
- [Spring Petclinic Angular (frontend)](https://github.com/spring-petclinic/spring-petclinic-angular)
