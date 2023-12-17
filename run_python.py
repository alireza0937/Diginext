import subprocess
import multiprocessing


def run_django():
    django_command = "python manage.py runserver 0.0.0.0:8000"
    try:
        subprocess.run(django_command, shell=True)
    except KeyboardInterrupt:
        print("Django server interrupted")


def run_background_script():
    try:
        subprocess.run("python manage.py cars_async", shell=True)
    except KeyboardInterrupt:
        print("Background script interrupted")


def run_background_script2():
    try:
        subprocess.run("python manage.py subscribe", shell=True)
    except KeyboardInterrupt:
        print("Background script 2 interrupted")


def run_background_script3():
    try:
        subprocess.run("python manage.py catching", shell=True)
    except KeyboardInterrupt:
        print("Background script 3 interrupted")


if __name__ == "__main__":
    django_process = multiprocessing.Process(target=run_django)

    background_process = multiprocessing.Process(target=run_background_script, daemon=True)
    background_process2 = multiprocessing.Process(target=run_background_script2, daemon=True)
    background_process3 = multiprocessing.Process(target=run_background_script3, daemon=True)

    try:
        django_process.start()
        background_process.start()
        background_process2.start()
        background_process3.start()

        django_process.join()
    except KeyboardInterrupt:
        print("Main process interrupted")

        # Terminate background processes gracefully
        background_process.terminate()
        background_process2.terminate()
        background_process3.terminate()

        # Wait for the background processes to finish
        background_process.join()
        background_process2.join()
        background_process3.join()
