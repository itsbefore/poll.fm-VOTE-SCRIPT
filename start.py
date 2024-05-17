import subprocess
import threading
import time
import os
import platform

def kill_process(process):
    if process.poll() is None:  # 如果进程仍在运行
        try:
            # 尝试温和地终止进程
            process.terminate()
            # 等待一段时间看进程是否响应
            time.sleep(1)
            if process.poll() is None:
                # 进程没有响应，强制结束
                if platform.system() == "Windows":
                    # 使用taskkill命令强制结束进程
                    os.system(f"taskkill /F /PID {process.pid} /T")
                    print(f"taskkill /F /PID {process.pid} /T")
        except Exception as e:
            print(f"Error killing process: {e}")

def run_script_with_timeout(script_path, timeout_seconds):
    process = subprocess.Popen(["python3", script_path])

    def timeout_handler():
        kill_process(process)

    # 设置一个定时器在timeout_seconds秒后执行timeout_handler函数
    timer = threading.Timer(timeout_seconds, timeout_handler)
    try:
        timer.start()
        # 等待进程完成（但由于设置了定时器，它可能永远不会真正完成）
        process.wait()
    finally:
        # 无论进程是否完成，都取消定时器
        timer.cancel()

    print("Script finished or was terminated. Restarting...(5min)\n")
    time.sleep(300)

current_directory = os.getcwd()
while True:
    run_script_with_timeout(f"{current_directory}/mlvote.py",300)  # 300秒 = 5分钟