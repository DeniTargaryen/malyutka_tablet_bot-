# ⚡ Быстрые ответы на ваши вопросы

## ❓ Ваши вопросы:

### 1. "Какие файлы копировать?"

**Минимум для работы бота:**
```
✅ bot.py              (15.5 KB) — ОБЯЗАТЕЛЬНО
✅ requirements.txt    (60 bytes) — ОБЯЗАТЕЛЬНО  
✅ .env                (создать!) — ОБЯЗАТЕЛЬНО (токен бота)
```

**Опционально (для диагностики):**
```
📝 db_check.py        — проверка БД
📝 cleanup_jobs.py    — диагностика джобов
📝 check_job.py       — проверка очереди
```

**НЕ нужны:**
```
❌ reminders.db          — создастся автоматически
❌ .bashrc               — системный файл Linux
❌ .gitconfig            — настройки Git
❌ .gitignore            — для Git
❌ .profile              — системный файл
❌ .pythonstartup.py     — системный файл
❌ .vimrc                — настройки редактора
❌ README.md и другие .md — только документация
```

---

### 2. "Проекта в гите нет"

**Решение:** 3 способа загрузить файлы на VPS БЕЗ Git:

#### Способ 1: SCP (быстро) ⭐
```powershell
cd C:\Users\maksi\PycharmProjects\malyutka_tablet_bot
scp bot.py root@ваш_IP:/opt/malyutka_bot/
scp requirements.txt root@ваш_IP:/opt/malyutka_bot/
```

#### Способ 2: WinSCP (удобно)
- Скачайте WinSCP
- Перетащите файлы мышкой

#### Способ 3: nano (медленно)
- Открыть файл на ПК
- Скопировать текст
- Вставить в nano на сервере

📖 **Подробная инструкция:** [WITHOUT_GIT_GUIDE.md](WITHOUT_GIT_GUIDE.md)

---

### 3. "Надо выделять по одному файлу и лить туда"

**Да, на PythonAnywhere — по одному файлу.**

**НО:** PythonAnywhere (бесплатный) **НЕ РАБОТАЕТ** для Telegram ботов!

❌ **Проблема:** Бесплатная версия не поддерживает постоянные процессы

✅ **Решение:** Используйте VPS (Timeweb — 199₽/мес)

---

## 🚨 Что вы сделали НЕПРАВИЛЬНО

### На PythonAnywhere вы загрузили:

**❌ Лишние файлы (удалите):**
- `.bashrc` — системный файл Linux (зачем?)
- `.gitconfig` — настройки Git
- `.gitignore` — для Git
- `.profile` — системный файл
- `.pythonstartup.py` — системный файл  
- `.vimrc` — настройки vim
- `reminders.db` — создастся сам

**✅ Правильные файлы (оставьте):**
- `bot.py` — хорошо
- `requirements.txt` — хорошо
- `db_check.py` — хорошо
- `README.md` — можно оставить

**❌ Чего не хватает:**
- `.env` файл с токеном бота!

### Главная проблема:

⚠️ **PythonAnywhere (бесплатный) НЕ РАБОТАЕТ для Telegram ботов!**

Бот остановится через несколько минут.

---

## ✅ Что делать ПРАВИЛЬНО

### Вариант 1: Локально (временно)

```bash
# На вашем ПК:
cd C:\Users\maksi\PycharmProjects\malyutka_tablet_bot
python bot.py
```

⚠️ Нужно держать компьютер включенным 24/7

---

### Вариант 2: VPS Timeweb (рекомендуется) ⭐

**Стоимость:** 199₽/месяц  
**Преимущества:**
- ✅ Работает 24/7
- ✅ Компьютер можно выключить
- ✅ Дешевле чем PythonAnywhere платный ($5 = ~500₽)

**Действия:**

1. **Купите VPS:**
   - https://timeweb.com
   - Тариф "Базовый" — 199₽/мес
   - Ubuntu 22.04 LTS

2. **Подключитесь:**
   ```powershell
   ssh root@ваш_IP
   ```

3. **Настройте:**
   ```bash
   apt update && apt upgrade -y
   apt install python3 python3-pip -y
   mkdir -p /opt/malyutka_bot
   ```

4. **Загрузите файлы (выберите способ):**

   **Способ A — SCP (рекомендуется):**
   ```powershell
   # На вашем ПК:
   cd C:\Users\maksi\PycharmProjects\malyutka_tablet_bot
   scp bot.py root@ваш_IP:/opt/malyutka_bot/
   scp requirements.txt root@ваш_IP:/opt/malyutka_bot/
   scp db_check.py root@ваш_IP:/opt/malyutka_bot/
   ```

   **Способ B — WinSCP (с интерфейсом):**
   - Скачайте WinSCP
   - Подключитесь к серверу
   - Перетащите файлы

   **Способ C — nano (вручную):**
   ```bash
   cd /opt/malyutka_bot
   nano bot.py
   # Скопируйте содержимое из файла
   # Вставьте: правая кнопка мыши
   # Сохраните: Ctrl+O, Enter, Ctrl+X
   ```

5. **Создайте .env:**
   ```bash
   nano /opt/malyutka_bot/.env
   ```
   Вставьте:
   ```
   TELEGRAM_TOKEN=ваш_токен_от_BotFather
   ```
   Сохраните: `Ctrl+O`, `Enter`, `Ctrl+X`

6. **Установите зависимости:**
   ```bash
   cd /opt/malyutka_bot
   pip3 install -r requirements.txt
   ```

7. **Настройте автозапуск:**
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

8. **Запустите:**
   ```bash
   systemctl daemon-reload
   systemctl enable malyutka-bot
   systemctl start malyutka-bot
   systemctl status malyutka-bot
   ```

9. **Проверьте в Telegram:**
   - `/start`
   - `/setme`
   - `/list`

10. **Выключите свой компьютер — бот работает!** 🎉

---

## 📊 Сравнение вариантов

| Вариант | Цена | Работает 24/7? | Сложность |
|---------|------|----------------|-----------|
| Локально (ваш ПК) | Электричество | ❌ Только при включенном ПК | ⭐ Просто |
| PythonAnywhere бесплатный | 0₽ | ❌ НЕТ | ⭐ Просто |
| PythonAnywhere платный | $5/мес (~500₽) | ✅ Да | ⭐ Просто |
| **VPS Timeweb** | **199₽/мес** | **✅ Да** | **⭐⭐ Средне** ⭐ |

**Вывод:** VPS дешевле и лучше!

---

## 🎯 Ваши следующие шаги

### Сейчас (на PythonAnywhere):
1. ❌ Удалите лишние файлы (.bashrc, .gitconfig и т.д.)
2. ❌ Поймите что бесплатный аккаунт **не работает**

### Правильно (на VPS):
1. ✅ Зарегистрируйтесь на Timeweb.com
2. ✅ Купите VPS за 199₽/мес
3. ✅ Следуйте инструкции выше (пункты 1-10)
4. ✅ Выберите способ загрузки:
   - SCP (если есть OpenSSH)
   - WinSCP (самый простой)
   - nano (если ничего не работает)

---

## 📚 Полезные ссылки

- 📦 **[WITHOUT_GIT_GUIDE.md](WITHOUT_GIT_GUIDE.md)** — подробная инструкция БЕЗ Git
- 🌐 **[HOSTING_GUIDE.md](HOSTING_GUIDE.md)** — полный гайд по хостингу
- 📝 **[INDEX.md](INDEX.md)** — навигация по всей документации

---

## 💡 Итог

**Ваши ошибки:**
1. ❌ Загрузили системные файлы Linux (.bashrc и т.д.)
2. ❌ Использовали PythonAnywhere (не работает для Telegram ботов)
3. ❌ Не создали .env файл с токеном

**Правильные действия:**
1. ✅ Используйте VPS (Timeweb — 199₽/мес)
2. ✅ Загрузите только: bot.py + requirements.txt
3. ✅ Создайте .env с токеном
4. ✅ Настройте автозапуск (systemd)

**Результат:**
- 🎉 Бот работает 24/7
- 💻 Компьютер можно выключить
- 💰 Дешево (199₽/мес)
- ⚡ Быстро (30 минут настройки)

---

## ❓ Остались вопросы?

Читайте **[WITHOUT_GIT_GUIDE.md](WITHOUT_GIT_GUIDE.md)** — там ВСЁ пошагово расписано!


