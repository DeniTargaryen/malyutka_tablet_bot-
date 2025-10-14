# 🌐 Гайд по размещению бота на сервере

## Проблема

Сейчас бот работает только когда ваш компьютер включен. Это неудобно, так как:
- Нужно держать компьютер включенным 24/7
- Высокий расход электроэнергии
- При выключении/перезагрузке напоминания не приходят

## Решение

Разместить бота на **облачном сервере**, который работает круглосуточно.

---

## 📋 Варианты размещения

### Вариант 1: 🆓 PythonAnywhere (БЕСПЛАТНО)

⚠️ **ВНИМАНИЕ: НЕ РЕКОМЕНДУЕТСЯ ДЛЯ ЭТОГО БОТА!**

**Почему НЕ работает:**
- ❌ Бесплатная версия **НЕ поддерживает** постоянно работающие процессы
- ❌ Telegram боты с polling **не могут работать** на бесплатном аккаунте
- ❌ Always-on tasks доступны **только на платных** тарифах ($5/мес)
- ❌ Scheduled tasks запускаются **1 раз в день**, а не постоянно

**Вывод:** PythonAnywhere не подходит для этого бота. Используйте VPS.

**Если всё же хотите попробовать (платный аккаунт $5/мес):**

1. **Регистрация:**
   - https://www.pythonanywhere.com
   - Купите платный тариф ($5/мес)

2. **Загрузка файлов вручную (БЕЗ Git):**
   
   **Шаг 1:** Зайдите в Files → Browse files
   
   **Шаг 2:** Создайте папку `malyutka_bot`
   
   **Шаг 3:** Загрузите ТОЛЬКО эти файлы:
   - ✅ `bot.py` (обязательно)
   - ✅ `requirements.txt` (обязательно)
   - ✅ `db_check.py` (опционально)
   - ✅ `cleanup_jobs.py` (опционально)
   
   **НЕ загружайте:**
   - ❌ `reminders.db` (создастся автоматически)
   - ❌ `.bashrc`, `.gitconfig`, `.vimrc` и т.д. (системные файлы)
   - ❌ README.md и другие .md (только документация)

3. **Создание .env файла:**
   - Files → malyutka_bot
   - Кнопка "New file" → назовите `.env`
   - Содержимое:
     ```
     TELEGRAM_TOKEN=ваш_токен_от_BotFather
     ```
   - Save

4. **Установка зависимостей:**
   - Consoles → Bash
   ```bash
   cd malyutka_bot
   pip3 install --user -r requirements.txt
   ```

5. **Запуск (только на платном тарифе):**
   - Web → Add a new web app
   - Настройте Always-on task

⚠️ **Повторяю: это работает ТОЛЬКО на платном тарифе $5/мес. За эту же цену лучше взять VPS!**

---

### Вариант 2: 💰 VPS-сервер (от 200₽/месяц)

**Рекомендуется:** Это лучший вариант для стабильной работы бота.

#### Провайдеры:

**🇷🇺 Российские:**
- **Timeweb** — от 199₽/мес, простая панель управления
- **Selectel** — от 250₽/мес, надежный
- **Beget** — от 180₽/мес
- **RuVDS** — от 169₽/мес

**🌍 Международные:**
- **DigitalOcean** — от $4/мес (≈400₽)
- **Vultr** — от $2.5/мес (≈250₽)
- **Hetzner** — от €3.79/мес (≈400₽)

#### 📝 Пошаговая инструкция (на примере Timeweb)

**Шаг 1: Создание сервера**

1. Зарегистрируйтесь на https://timeweb.com
2. Купите VPS (тариф "Базовый" за 199₽/мес хватит)
3. При создании выберите:
   - **ОС:** Ubuntu 22.04 LTS
   - **Регион:** Любой
4. Дождитесь создания сервера (1-5 минут)
5. Получите IP-адрес и пароль root

**Шаг 2: Подключение к серверу**

Windows:
```powershell
# Используйте PuTTY или встроенный SSH:
ssh root@ваш_IP_адрес
# Введите пароль
```

**Шаг 3: Настройка сервера**

```bash
# Обновление системы
apt update && apt upgrade -y

# Установка Python и pip
apt install python3 python3-pip git -y

# Создание директории для бота
cd /opt
git clone https://ваш_репозиторий.git malyutka_bot
# ИЛИ создайте вручную:
mkdir malyutka_bot
cd malyutka_bot
```

**Шаг 4: Загрузка файлов**

**Вариант A — через SCP (РЕКОМЕНДУЕТСЯ, если проекта нет в Git):**

На вашем компьютере откройте PowerShell:

```powershell
# Перейдите в папку проекта
cd C:\Users\maksi\PycharmProjects\malyutka_tablet_bot

# Загрузите ТОЛЬКО нужные файлы на сервер:
scp bot.py root@ваш_IP:/opt/malyutka_bot/
scp requirements.txt root@ваш_IP:/opt/malyutka_bot/
scp db_check.py root@ваш_IP:/opt/malyutka_bot/
scp cleanup_jobs.py root@ваш_IP:/opt/malyutka_bot/
scp check_job.py root@ваш_IP:/opt/malyutka_bot/

# НЕ загружайте:
# - reminders.db (создастся автоматически)
# - README.md и другие .md (только документация)
# - .env (создадим на сервере)
```

⚠️ **Примечание:** Если команда `scp` не работает, установите OpenSSH:
- Settings → Apps → Optional features → Add a feature → OpenSSH Client

**Вариант B — через Git (если проект в репозитории):**
```bash
git clone https://github.com/ваш_username/malyutka_tablet_bot.git /opt/malyutka_bot
cd /opt/malyutka_bot
```

**Вариант C — вручную через nano (если SCP не работает):**

Создайте каждый файл вручную:

```bash
cd /opt/malyutka_bot

# Создаём bot.py
nano bot.py
# Скопируйте содержимое из файла на вашем ПК
# Вставьте: правая кнопка мыши или Shift+Insert
# Сохраните: Ctrl+O, Enter, Ctrl+X

# Создаём requirements.txt
nano requirements.txt
# Вставьте:
# python-telegram-bot>=20.0
# python-dotenv>=1.0.0
# Сохраните: Ctrl+O, Enter, Ctrl+X

# Опционально: db_check.py, cleanup_jobs.py и т.д.
```

**Список файлов для загрузки:**
- ✅ `bot.py` (обязательно, 15.5 KB)
- ✅ `requirements.txt` (обязательно, 60 bytes)
- ✅ `db_check.py` (опционально, 375 bytes)
- ✅ `cleanup_jobs.py` (опционально, для диагностики)
- ✅ `check_job.py` (опционально, для диагностики)

**НЕ загружайте:**
- ❌ `reminders.db` (создастся автоматически при первом запуске)
- ❌ Файлы .md (это только документация)
- ❌ Системные файлы (.bashrc, .gitconfig и т.д.)

**Шаг 5: Установка зависимостей**

```bash
cd /opt/malyutka_bot
pip3 install -r requirements.txt
```

**Шаг 6: Создание .env файла**

```bash
nano .env
```

Вставьте:
```
TELEGRAM_TOKEN=ваш_токен_от_BotFather
```

Сохраните: `Ctrl+O`, `Enter`, `Ctrl+X`

**Шаг 7: Создание systemd службы (автозапуск)**

Создайте файл службы:
```bash
nano /etc/systemd/system/malyutka-bot.service
```

Вставьте:
```ini
[Unit]
Description=Malyutka Tablet Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/malyutka_bot
ExecStart=/usr/bin/python3 /opt/malyutka_bot/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Сохраните: `Ctrl+O`, `Enter`, `Ctrl+X`

**Шаг 8: Запуск службы**

```bash
# Перезагрузить systemd
systemctl daemon-reload

# Включить автозапуск
systemctl enable malyutka-bot

# Запустить бота
systemctl start malyutka-bot

# Проверить статус
systemctl status malyutka-bot
```

**Шаг 9: Проверка работы**

```bash
# Посмотреть логи
journalctl -u malyutka-bot -f

# Должно быть: "Bot started (polling)"
```

**Шаг 10: Проверка в Telegram**

Откройте бота в Telegram:
- `/start`
- `/setme`
- `/list`

---

### Вариант 3: 🆓 Google Cloud / AWS (бесплатный tier)

**Google Cloud Platform:**
- 90 дней бесплатно с $300 кредитами
- Потом от $5-10/месяц
- Сложнее в настройке

**Amazon AWS:**
- 12 месяцев бесплатно (t2.micro)
- Потом от $5/месяц
- Требует банковскую карту

Настройка аналогична VPS выше, но через веб-интерфейс AWS/GCP.

---

### Вариант 4: 🏠 Raspberry Pi у вас дома

**Плюсы:**
- ✅ Разовая покупка (≈3000-5000₽)
- ✅ Низкое энергопотребление (≈30₽/месяц)
- ✅ Полный контроль

**Минусы:**
- ⚠️ Зависит от вашего интернета
- ⚠️ Нужно настраивать

**Что понадобится:**
1. Raspberry Pi 4 (2GB) — ≈4000₽
2. MicroSD карта 16GB — ≈500₽
3. Блок питания — обычно в комплекте

**Инструкция:**
1. Установите Raspberry Pi OS
2. Подключите к интернету
3. Выполните те же команды, что и для VPS (Шаги 3-9)

---

## 📊 Сравнение вариантов

| Вариант | Цена | Сложность | Надежность | Рекомендация |
|---------|------|-----------|------------|--------------|
| PythonAnywhere | 🆓 Бесплатно | ⭐ Простая | ⭐⭐ Средняя | ⚠️ Ограничения |
| **VPS (Timeweb)** | 💰 200₽/мес | ⭐⭐ Средняя | ⭐⭐⭐ Высокая | ✅ **Рекомендуется** |
| AWS/GCP | 🆓→💰 0-10$/мес | ⭐⭐⭐ Сложная | ⭐⭐⭐ Высокая | 👍 Хорошо |
| Raspberry Pi | 💰 4000₽ раз | ⭐⭐⭐ Сложная | ⭐⭐ Средняя | 🏠 Для энтузиастов |

---

## 🎯 Мой личный совет

**Для вашего случая:** VPS от Timeweb или Selectel

**Почему:**
1. 💰 Недорого (≈200₽/мес = стоимость 2-3 кофе)
2. ✅ Надежно и стабильно
3. ⚡ Быстрая настройка (30 минут)
4. 🇷🇺 Русская поддержка
5. 💳 Оплата российскими картами

**Альтернатива (если хотите сэкономить):**
- Raspberry Pi — разовая покупка, потом только электричество

---

## 🔧 Полезные команды для управления на VPS

```bash
# Запустить бота
systemctl start malyutka-bot

# Остановить бота
systemctl stop malyutka-bot

# Перезапустить бота
systemctl restart malyutka-bot

# Проверить статус
systemctl status malyutka-bot

# Посмотреть логи
journalctl -u malyutka-bot -f

# Посмотреть последние 100 строк логов
journalctl -u malyutka-bot -n 100

# Обновить код бота
cd /opt/malyutka_bot
# Загрузите новые файлы
systemctl restart malyutka-bot
```

---

## 📞 Нужна помощь с настройкой?

Если что-то не получается:

1. **Проверьте логи:** `journalctl -u malyutka-bot -f`
2. **Проверьте .env файл:** `cat /opt/malyutka_bot/.env`
3. **Проверьте права:** `chmod +x /opt/malyutka_bot/bot.py`
4. **Проверьте зависимости:** `pip3 list | grep telegram`

---

## ✅ Чек-лист после установки на сервер

- [ ] Бот запущен и работает (`systemctl status malyutka-bot`)
- [ ] Автозапуск включен (`systemctl is-enabled malyutka-bot`)
- [ ] Бот отвечает в Telegram (`/start`)
- [ ] Напоминания настроены (`/setme`)
- [ ] Проверили, что напоминания приходят (можно установить тестовое на +5 минут)
- [ ] Записали куда-нибудь IP и пароль от сервера

---

## 💡 Бонус: Мониторинг

Чтобы получать уведомления, если бот упал:

```bash
# Создайте скрипт проверки
nano /opt/check_bot.sh
```

Содержимое:
```bash
#!/bin/bash
if ! systemctl is-active --quiet malyutka-bot; then
    systemctl start malyutka-bot
    # Можно добавить отправку уведомления себе в Telegram
fi
```

Добавьте в cron (проверка каждые 5 минут):
```bash
chmod +x /opt/check_bot.sh
crontab -e
# Добавьте строку:
*/5 * * * * /opt/check_bot.sh
```

---

## 🎉 Готово!

Теперь ваш бот работает 24/7, и вам не нужно держать компьютер включенным!

