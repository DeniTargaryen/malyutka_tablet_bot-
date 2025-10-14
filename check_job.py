# check_job.py
from telegram.ext import ApplicationBuilder
app = ApplicationBuilder().token("0"*10).build()
print("job_queue:", app.job_queue)
