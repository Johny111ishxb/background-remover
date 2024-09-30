import psutil
import os

@app.route('/memory_usage')
def memory_usage():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return f"Memory Usage: {mem_info.rss / 1024 ** 2:.2f} MB"
