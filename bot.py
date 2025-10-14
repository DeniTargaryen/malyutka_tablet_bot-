import datetime
import os
import sqlite3
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
)

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
DB_PATH = "reminders.db"
MOSCOW = ZoneInfo("Europe/Moscow")


# ---------- DB ----------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS reminders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER NOT NULL,
        time TEXT NOT NULL,
        label TEXT DEFAULT '',
        active INTEGER DEFAULT 1
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS confirmations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reminder_id INTEGER,
        chat_id INTEGER,
        ts TEXT,
        note TEXT
    )""")
    conn.commit()
    conn.close()


def add_reminder(chat_id: int, time_str: str, label: str) -> int:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO reminders (chat_id, time, label) VALUES (?, ?, ?)",
                (chat_id, time_str, label))
    rid = cur.lastrowid
    conn.commit()
    conn.close()
    return rid


def get_reminder(rem_id: int):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, chat_id, time, label, active FROM reminders WHERE id = ?", (rem_id,))
    r = cur.fetchone()
    conn.close()
    return r


def all_active_reminders():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, chat_id, time, label FROM reminders WHERE active = 1")
    rows = cur.fetchall()
    conn.close()
    return rows


def list_reminders_for(chat_id: int):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, time, label, active FROM reminders WHERE chat_id = ?", (chat_id,))
    rows = cur.fetchall()
    conn.close()
    return rows


def delete_reminder(rem_id: int):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM reminders WHERE id = ?", (rem_id,))
    conn.commit()
    conn.close()


def record_confirmation(reminder_id: int, chat_id: int, note: str = ""):
    ts = datetime.datetime.now(tz=MOSCOW).isoformat()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO confirmations (reminder_id, chat_id, ts, note) VALUES (?, ?, ?, ?)",
                (reminder_id, chat_id, ts, note))
    conn.commit()
    conn.close()


# ---------- Bot handlers ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = (
        "Привет! Я бот-напоминалка про таблетки.\n\n"
        "Я уже настроен отправлять:\n"
        "• Эсциталопрам — 06:00 МСК\n"
        "• Ярина плюс — 19:00 МСК\n\n"
        "Команды:\n"
        "/setme — настроить напоминания для меня\n"
        "/list — показать напоминания\n"
        "/delete <id> — удалить напоминание\n"
        "/update <id> HH:MM — изменить время напоминания\n"
        "/settime HH:MM [метка] — добавить новое напоминание\n"
    )
    await update.message.reply_text(txt)


async def list_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    rows = list_reminders_for(chat_id)
    if not rows:
        await update.message.reply_text("У вас нет напоминаний.")
        return
    lines = []
    for r in rows:
        rid, time_s, label, active = r
        status = "активно" if active else "выключено"
        lines.append(f"{rid}: {time_s} — {label or '(без метки)'} [{status}]")
    await update.message.reply_text("\n".join(lines))


def update_reminder_time(rem_id: int, time_str: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("UPDATE reminders SET time = ? WHERE id = ?", (time_str, rem_id))
    conn.commit()
    conn.close()


# /settime HH:MM [метка] — создаёт новое напоминание для текущего чата
async def settime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Использование: /settime HH:MM [метка]")
        return
    timestr = context.args[0]
    try:
        h, m = map(int, timestr.split(":"))
        if not (0 <= h < 24 and 0 <= m < 60):
            raise ValueError
    except Exception:
        await update.message.reply_text("Неправильный формат времени. Пример: 06:00")
        return
    label = " ".join(context.args[1:]) if len(context.args) > 1 else ""
    chat_id = update.effective_chat.id
    rid = add_reminder(chat_id, timestr, label)
    # планируем job с уникальным именем
    context.application.job_queue.run_daily(
        callback=send_reminder,
        time=datetime.time(hour=h, minute=m, tzinfo=MOSCOW),
        context={"reminder_id": rid, "chat_id": chat_id},
        name=f"reminder_{rid}"
    )
    await update.message.reply_text(f"Добавлено напоминание id={rid} в {timestr} — {label}")


async def delete_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Нужно: /delete <id>")
        return
    try:
        rid = int(context.args[0])
    except ValueError:
        await update.message.reply_text("id должен быть числом")
        return
    
    # Удаляем из базы данных
    delete_reminder(rid)
    
    # Удаляем связанный джоб из очереди (чтобы избежать "мертвых" джобов)
    job_name = f"reminder_{rid}"
    jobs = context.application.job_queue.get_jobs_by_name(job_name)
    for job in jobs:
        job.schedule_removal()
    
    await update.message.reply_text(f"Удалил напоминание {rid} (если было).")


# отправка напоминания (job)
async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    job_ctx = context.job.context
    rem_id = job_ctx.get("reminder_id")
    chat_id = job_ctx.get("chat_id")
    rem = get_reminder(rem_id)
    if not rem:
        return
    _, _, time_s, label, active = rem
    if not active:
        return
    nickname = "Котик"  # можно сделать персонализацию позже
    label_text = f" — {label}" if label else ""
    text = f"{nickname}, выпей, пожалуйста, таблеточку{label_text}"
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Выпила", callback_data=f"took:{rem_id}")],
        [InlineKeyboardButton("⏰ Отложить на 10 минут", callback_data=f"snooze:{rem_id}:10")]
    ])
    await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)


# повторное однократное напоминание через X минут (run_once)
async def send_snooze(context: ContextTypes.DEFAULT_TYPE):
    job_ctx = context.job.context
    rem_id = job_ctx.get("reminder_id")
    chat_id = job_ctx.get("chat_id")
    note = job_ctx.get("note", "")
    text = f"Напоминание (отложенное): пожалуйста, примите таблеточку — {note}"
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Выпила", callback_data=f"took:{rem_id}")],
        [InlineKeyboardButton("⏰ Отложить ещё 10 минут", callback_data=f"snooze:{rem_id}:10")]
    ])
    await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)


# обработка нажатия кнопки
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if not data:
        return
    parts = data.split(":")
    if parts[0] == "took":
        rem_id = int(parts[1])
        chat_id = query.message.chat_id
        record_confirmation(rem_id, chat_id, note="confirmed via button")
        try:
            await query.edit_message_text("✅ Выпила")
        except Exception:
            pass
        await context.bot.send_message(chat_id=chat_id,
                                       text="Отлично, что ты выпила таблеточку — ты настоящая героиня!")
    elif parts[0] == "snooze":
        rem_id = int(parts[1])
        minutes = int(parts[2])
        chat_id = query.message.chat_id
        # подтвердим пользователю, что отложили
        try:
            await query.edit_message_text(f"Отложено на {minutes} минут.")
        except Exception:
            pass
        # ставим одноразовое напоминание через minutes
        when = datetime.timedelta(minutes=minutes)
        context.job_queue.run_once(
            callback=send_snooze,
            when=when,
            context={"reminder_id": rem_id, "chat_id": chat_id, "note": get_reminder(rem_id)[3]}
        )
        await context.bot.send_message(chat_id=chat_id, text=f"Хорошо — напоминание придёт через {minutes} минут.")


# при старте приложения — планируем напоминания
def schedule_all(app):
    rows = all_active_reminders()
    for rid, chat_id, time_s, label in rows:
        try:
            h, m = map(int, time_s.split(":"))
        except Exception:
            continue
        time_obj = datetime.time(hour=h, minute=m, tzinfo=MOSCOW)
        # Проверяем, нет ли уже джоба с таким именем (защита от дубликатов)
        job_name = f"reminder_{rid}"
        existing_jobs = app.job_queue.get_jobs_by_name(job_name)
        if not existing_jobs:
            app.job_queue.run_daily(callback=send_reminder, time=time_obj,
                                    context={"reminder_id": rid, "chat_id": chat_id},
                                    name=job_name)


# ---------- main ----------
def main():
    if not TOKEN:
        print("TELEGRAM_TOKEN не задан. Создайте .env с TELEGRAM_TOKEN=...")
        return
    init_db()
    app = ApplicationBuilder().token(TOKEN).build()

    # handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("list", list_cmd))
    app.add_handler(CommandHandler("delete", delete_cmd))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(CommandHandler("setme", setme))
    app.add_handler(CommandHandler("settime", settime))
    app.add_handler(CommandHandler("update", update_cmd))
    # Если БД пустая — создаём два напоминания по умолчанию для текущего пользователя.
    # Тут логика: при первом запуске бот не знает chat_id — поэтому добавляем напоминания
    # только когда пользователь напишет /start: ниже простой способ — если хочешь, можно добавить команду для регистрации.
    # Для удобства: если таблица reminders пустая, добавим "шаблон" для демонстрации (chat_id = 0 — потом удалим).
    if not all_active_reminders():
        # Создадим «шаблонные» записи. В реальной эксплуатации лучше сделать /register или /settime.
        print("No reminders in DB. Creating default template entries (need to register real chat_id via /settime).")

    # schedule any existing reminders
    schedule_all(app)

    print("Bot started (polling)")
    app.run_polling()


async def setme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # команда /setme — регистрирует два напоминания для текущего чата
    chat_id = update.effective_chat.id
    # Проверим, есть ли уже записи для этого chat_id
    existing = list_reminders_for(chat_id)
    if existing:
        await update.message.reply_text("Похоже, напоминания уже настроены. Используйте /list или /delete.")
        return
    # добавим необходимые напоминания
    rid1 = add_reminder(chat_id, "06:00", "Эсциталопрам (утро)")
    rid2 = add_reminder(chat_id, "19:00", "Ярина плюс (вечер)")
    # спланируем их немедленно с уникальными именами
    context.application.job_queue.run_daily(callback=send_reminder,
                                            time=datetime.time(hour=6, minute=0, tzinfo=MOSCOW),
                                            context={"reminder_id": rid1, "chat_id": chat_id},
                                            name=f"reminder_{rid1}")
    context.application.job_queue.run_daily(callback=send_reminder,
                                            time=datetime.time(hour=19, minute=0, tzinfo=MOSCOW),
                                            context={"reminder_id": rid2, "chat_id": chat_id},
                                            name=f"reminder_{rid2}")
    await update.message.reply_text("Добавлены напоминания: 06:00 — Эсциталопрам, 19:00 — Ярина плюс.")


async def update_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # /update <id> HH:MM
    if len(context.args) < 2:
        await update.message.reply_text("Использование: /update <id> HH:MM")
        return
    try:
        rid = int(context.args[0])
    except ValueError:
        await update.message.reply_text("id должен быть числом")
        return
    timestr = context.args[1]
    try:
        h, m = map(int, timestr.split(":"))
        if not (0 <= h < 24 and 0 <= m < 60):
            raise ValueError
    except Exception:
        await update.message.reply_text("Неправильный формат времени. Пример: 20:00")
        return

    # обновляем в БД
    update_reminder_time(rid, timestr)

    # ВАЖНО: удаляем старый джоб перед созданием нового, чтобы избежать дубликатов
    job_name = f"reminder_{rid}"
    current_jobs = context.application.job_queue.get_jobs_by_name(job_name)
    for job in current_jobs:
        job.schedule_removal()
    
    # Создаем новый джоб с обновленным временем
    context.application.job_queue.run_daily(
        callback=send_reminder,
        time=datetime.time(hour=h, minute=m, tzinfo=MOSCOW),
        context={"reminder_id": rid, "chat_id": update.effective_chat.id},
        name=job_name
    )
    await update.message.reply_text(f"Обновлено напоминание {rid} на {timestr}")


if __name__ == "__main__":
    main()
