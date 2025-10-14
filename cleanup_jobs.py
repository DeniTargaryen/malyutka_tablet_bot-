"""
Утилита для проверки и очистки дубликатов джобов.
Запустите этот скрипт, если подозреваете, что есть дубликаты джобов.
"""
import os
import sqlite3
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
DB_PATH = "reminders.db"


def check_jobs():
    """Проверка текущих джобов в очереди"""
    if not TOKEN:
        print("TELEGRAM_TOKEN не задан!")
        return
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Получаем все джобы
    all_jobs = app.job_queue.jobs()
    print(f"\n=== Всего джобов в очереди: {len(all_jobs)} ===\n")
    
    # Группируем джобы по именам
    job_names = {}
    for job in all_jobs:
        name = job.name if job.name else "(без имени)"
        if name not in job_names:
            job_names[name] = []
        job_names[name].append(job)
    
    # Выводим статистику
    duplicates_found = False
    for name, jobs in job_names.items():
        count = len(jobs)
        status = "⚠️ ДУБЛИКАТЫ!" if count > 1 else "✓"
        print(f"{status} {name}: {count} джоб(ов)")
        
        if count > 1:
            duplicates_found = True
            for i, job in enumerate(jobs, 1):
                print(f"  - Джоб #{i}: следующий запуск в {job.next_t}")
    
    print()
    
    # Проверяем напоминания в БД
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, chat_id, time, label, active FROM reminders WHERE active = 1")
    reminders = cur.fetchall()
    conn.close()
    
    print(f"=== Активных напоминаний в БД: {len(reminders)} ===\n")
    for rem in reminders:
        rid, chat_id, time_s, label, active = rem
        expected_job_name = f"reminder_{rid}"
        job_count = len(job_names.get(expected_job_name, []))
        status = "✓" if job_count == 1 else ("⚠️" if job_count == 0 else "❌ ДУБЛИКАТ")
        print(f"{status} ID {rid}: {time_s} — {label} (джобов: {job_count})")
    
    print()
    
    if duplicates_found:
        print("⚠️  НАЙДЕНЫ ДУБЛИКАТЫ ДЖОБОВ!")
        print("Рекомендуется перезапустить бота для очистки.")
    else:
        print("✓ Дубликатов не найдено. Все в порядке!")


if __name__ == "__main__":
    check_jobs()


