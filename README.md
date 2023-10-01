# Charity Motion

---

### Решение хакатона Kokoc Hack 2023 от команды flint3s

## Веб-демо: https://kokoc.flint3s.ru/

## Приложение (apk): https://disk.yandex.ru/d/z7QERYO7OmurCg

Приложение предназначено для пользователей (сотрудников), веб-приложение для администраторов компаний и фондов

### Видеодемонстрация: https://disk.yandex.ru/i/g4d97Yggd3pe_w

### Презентация:

---

### Данные для входа:

**Суперадминистратор:**

```text
superuser
superuser
```

**Фонд:**

```text
catfund
catfund
```

**Админ компании:**

```text
companyadmin
123
```

**Пользователь:**

```text
sss
sss
```

### Установка приложения

1. Скачать apk по ссылке (https://disk.yandex.ru/d/z7QERYO7OmurCg)
2. Установить на смартфон с Android 10+
3. При установке может появиться сообщение о том, что приложение небезопасно -
   это предупреждение необходимо проигнорировать (показать больше -> все равно установить)
4. Запустить приложение
5. Войти в приложение под ролью пользователя (сотрудника)

### Развертывание проекта

Все проекты упакованы в docker-контейнеры. Для быстрого запуска можно использовать docker-compose, перед этим необходимо
указать переменные окружения в файле `docker-compose.yml`

```
docker compose up
```

