# import os
# # a = os.system("ps")
# a = os.popen("ps", mode='r', buffering=-1)
# b = a.read()
# for i in range(5):
#     print(b)

# import time

# # Печатаем начальные строки
# print("111")
# print("222")
# print(333)

# # Ждем немного времени, чтобы пользователь мог увидеть начальные строки
# time.sleep(2)

# # ANSI escape code для перемещения курсора на две строки вверх
# UP_TWO_LINES = "\033[3A"

# # ANSI escape code для очистки строки от курсора до конца строки
# CLEAR_LINE = "\033[K"

# # Перемещаем курсор на две строки вверх и перезаписываем строки
# print(f"{UP_TWO_LINES}{CLEAR_LINE}444")
# print(f"{CLEAR_LINE}555")

import subprocess

def read_top_output():
    process = subprocess.Popen(['top', '-b', '-n', '1'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        print(f"Error: {stderr.decode('utf-8')}")
    else:
        output = stdout.decode('utf-8')
        return output

top_output = read_top_output()
print(top_output)
b = ""
for i in top_output.split("\n"):
    b += f"{i}<br/>"