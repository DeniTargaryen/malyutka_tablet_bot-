# 📦 Инструкция по загрузке БЕЗ Git

## 🎯 Ваша ситуация

У вас нет проекта в Git, и вы хотите загрузить файлы на сервер вручную.

---

## ⚠️ ВАЖНО: PythonAnywhere НЕ подходит!

**Вы загрузили файлы на PythonAnywhere, но:**
- ❌ Бесплатная версия **НЕ работает** с Telegram ботами
- ❌ Боты с polling **не могут работать** постоянно
- ❌ Платная версия стоит $5/мес (дороже VPS!)

**Решение:** Удалите всё с PythonAnywhere и используйте **VPS за 199₽/мес**

---

## 📋 Какие файлы нужны для бота?

### ✅ Обязательные (минимум для работы):
```
malyutka_tablet_bot/
├── bot.py              (15.5 KB) ← Основной файл
├── requirements.txt    (60 bytes) ← Зависимости
└── .env                (создать!) ← Токен бота
```

### 📝 Опциональные (для удобства):
```
malyutka_tablet_bot/
├── db_check.py         (375 bytes) ← Проверка БД
├── cleanup_jobs.py     ← Диагностика джобов
└── check_job.py        ← Проверка очереди
```

### ❌ НЕ нужны:
- `reminders.db` — создастся автоматически
- `.bashrc`, `.gitconfig`, `.vimrc` — системные файлы Linux (не трогать!)
- `README.md` и другие .md — только документация

---

## 🗑️ Что вы загрузили ЛИШНЕГО?

Можно удалить:
- ❌ `.bashrc` — системный файл
- ❌ `.gitconfig` — настройки Git
- ❌ `.profile` — системный файл
- ❌ `.pythonstartup.py` — системный файл
- ❌ `.vimrc` — настройки редактора
- ❌ `.gitignore` — для Git
- ❌ `reminders.db` — создастся автоматически
- 📚 `README.md` — можно оставить для справки

**Оставить:**
- ✅ `bot.py`
- ✅ `requirements.txt`
- ✅ `db_check.py`

**Создать:**
- 🆕 `.env` файл с токеном!

---

## 🚀 Правильный способ: VPS с Timeweb

### Шаг 1: Зарегистрируйтесь на Timeweb
1. Зайдите на https://timeweb.com
2. Зарегистрируйтесь
3. Купите VPS "Базовый" за 199₽/мес
4. Выберите Ubuntu 22.04 LTS
5. Получите IP-адрес и пароль

### Шаг 2: Подключитесь к серверу

Windows PowerShell:
```powershell
ssh root@ваш_IP_адрес
# Введите пароль
```

### Шаг 3: Настройте сервер

```bash
# Обновление
apt update && apt upgrade -y

# Установка Python
apt install python3 python3-pip -y

# Создание папки
mkdir -p /opt/malyutka_bot
```

### Шаг 4: Загрузите файлы (3 способа)

#### Способ 1: SCP с вашего компьютера (БЫСТРО) ⭐

На вашем компьютере (Windows PowerShell):

```powershell
# Перейдите в папку проекта
cd C:\Users\maksi\PycharmProjects\malyutka_tablet_bot

# Создайте папку на сервере
ssh root@ваш_IP "mkdir -p /opt/malyutka_bot"

# Загрузите файлы
scp bot.py root@ваш_IP:/opt/malyutka_bot/
scp requirements.txt root@ваш_IP:/opt/malyutka_bot/
scp db_check.py root@ваш_IP:/opt/malyutka_bot/
scp cleanup_jobs.py root@ваш_IP:/opt/malyutka_bot/
```

Если `scp` не работает:
- Settings → Apps → Optional features → Add a feature → OpenSSH Client
- Перезапустите PowerShell

#### Способ 2: Вручную через nano (МЕДЛЕННО)

На сервере:

```bash
cd /opt/malyutka_bot

# Создаём bot.py
nano bot.py
```

Затем:
1. Откройте `bot.py` на вашем ПК в блокноте
2. Скопируйте ВЕСЬ текст (Ctrl+A, Ctrl+C)
3. В окне SSH кликните правой кнопкой мыши (вставится)
4. Нажмите `Ctrl+O`, затем `Enter` (сохранить)
5. Нажмите `Ctrl+X` (выйти)

Повторите для `requirements.txt`:

```bash
nano requirements.txt
```

Вставьте:
```
python-telegram-bot>=20.0
python-dotenv>=1.0.0
```

Сохраните: `Ctrl+O`, `Enter`, `Ctrl+X`

#### Способ 3: WinSCP (С ИНТЕРФЕЙСОМ)

1. Скачайте WinSCP: https://winscp.net/
2. Установите и откройте
3. Подключитесь:
   - Host: ваш_IP
   - Username: root
   - Password: ваш_пароль
4. Перетащите файлы из левой панели (ваш ПК) в правую (сервер)
5. Перетащите в папку `/opt/malyutka_bot/`:
   - `bot.py`
   - `requirements.txt`
   - `db_check.py` (опционально)
   - `cleanup_jobs.py` (опционально)

### Шаг 5: Создайте .env файл

На сервере:

```bash
cd /opt/malyutka_bot
nano .env
```

Вставьте (замените на ваш настоящий токен):
```
TELEGRAM_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

Сохраните: `Ctrl+O`, `Enter`, `Ctrl+X`

### Шаг 6: Установите зависимости

```bash
cd /opt/malyutka_bot
pip3 install -r requirements.txt
```

### Шаг 7: Проверьте что всё на месте

```bash
ls -lh /opt/malyutka_bot
```

Должно быть:
```
bot.py
requirements.txt
.env
db_check.py (опционально)
```

### Шаг 8: Протестируйте запуск

```bash
cd /opt/malyutka_bot
python3 bot.py
```

Должно появиться:
```
Bot started (polling)
```

Проверьте бота в Telegram:
- Найдите своего бота
- Отправьте `/start`
- Должен ответить!

Если работает — нажмите `Ctrl+C` чтобы остановить.

### Шаг 9: Настройте автозапуск

Создайте службу:

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

Включите автозапуск:

```bash
systemctl daemon-reload
systemctl enable malyutka-bot
systemctl start malyutka-bot
systemctl status malyutka-bot
```

Должно быть: `active (running)`

### Шаг 10: Проверьте в Telegram

1. Откройте бота в Telegram
2. Отправьте `/start`
3. Отправьте `/setme`
4. Отправьте `/list`

Должно быть:
```
1: 06:00 — Эсциталопрам (утро) [активно]
2: 19:00 — Ярина плюс (вечер) [активно]
```

---

## ✅ Готово!

Теперь:
- ✅ Бот работает 24/7
- ✅ Можно выключить свой компьютер
- ✅ Напоминания приходят автоматически

---

## 🔧 Полезные команды

```bash
# Проверить статус бота
systemctl status malyutka-bot

# Посмотреть логи
journalctl -u malyutka-bot -f

# Перезапустить бота
systemctl restart malyutka-bot

# Остановить бота
systemctl stop malyutka-bot

# Запустить бота
systemctl start malyutka-bot
```

---

## 📊 Что у вас сейчас на PythonAnywhere?

Вы загрузили:
- ✅ `bot.py` — нужен
- ✅ `requirements.txt` — нужен
- ✅ `db_check.py` — опционально
- ✅ `README.md` — документация
- ❌ `.bashrc`, `.gitconfig`, `.vimrc` и т.д. — НЕ нужны
- ❌ `reminders.db` — создастся сам

**Чего не хватает:**
- ❌ `.env` файл с токеном!

**Но главное:** PythonAnywhere (бесплатный) **не работает** для Telegram ботов!

---

## 💰 Сравнение

| Вариант | Цена | Работает? |
|---------|------|-----------|
| PythonAnywhere (бесплатный) | 0₽ | ❌ НЕТ |
| PythonAnywhere (платный) | $5/мес ≈ 500₽ | ✅ Да |
| **VPS Timeweb** | **199₽/мес** | **✅ Да** ⭐ |

**Вывод:** VPS дешевле и работает лучше!

---

## 🎯 Ваши следующие шаги

1. ✅ Зарегистрируйтесь на Timeweb.com
2. ✅ Купите VPS за 199₽/мес
3. ✅ Следуйте инструкции выше (Шаги 1-10)
4. ✅ Выберите способ загрузки файлов:
   - **SCP** — если установлен OpenSSH (быстро)
   - **WinSCP** — если хотите с интерфейсом (удобно)
   - **nano** — если ничего не работает (медленно)
5. ✅ Не забудьте создать `.env` с токеном!
6. ✅ Протестируйте бота
7. ✅ Выключите свой компьютер — бот работает! 🎉

---

## ❓ Вопросы?

**Q: Почему не работает на PythonAnywhere?**  
A: Бесплатная версия не поддерживает постоянные процессы. Нужен платный аккаунт или VPS.

**Q: Безопасно ли хранить токен в .env?**  
A: Да, файл .env находится на сервере и недоступен извне.

**Q: Что если я случайно удалю reminders.db?**  
A: Ничего страшного, создастся новая. Но потеряете историю подтверждений.

**Q: Можно ли использовать другой VPS?**  
A: Да! Selectel, Beget, DigitalOcean, Vultr и т.д. Инструкция аналогична.

**Q: Нужно ли загружать README.md и другие .md?**  
A: Нет, это только документация для вас. Бот работает без них.

---

## 🎉 Удачи!

После настройки VPS бот будет работать 24/7, и вам не придется держать компьютер включенным!


