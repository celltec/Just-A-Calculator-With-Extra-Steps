import time
import subprocess
from PIL import Image
import pyautogui as gui
import pyperclip as clipboard

def slice(file, rows, cols, trim):
    KEYPAD = [
        None,  None,  None,  None,
        None,  None,  None, 'div',
           7,     8,     9, 'mul',
           4,     5,     6, 'sub',
           1,     2,     3, 'add',
        None,     0, 'dec',  'eq'
    ]

    image = Image.open(file)
    w, h = image.size
    x = w // rows
    y = h // cols

    buttons = [button.crop((trim, trim, x - trim, y - trim))
               for button in [row.crop((0, y * i, w, y * (i + 1))) for i in range(cols)
               for row in [image.crop((x * i, 0, x * (i + 1), h)) for i in range(rows)]]]

    return {str(KEYPAD[i]): button for i, button in enumerate(buttons) if KEYPAD[i] is not None}

KEYS = slice('keypad.png', 4, 6, 10)

def click(key):
    KEY_MAPPING = {
        '+': 'add',
        '-': 'sub',
        '*': 'mul',
        '/': 'div',
        '.': 'dec',
        '=': 'eq'
    }

    pos = gui.locateCenterOnScreen(KEYS[KEY_MAPPING.get(key, key)], confidence=0.9)
    if not pos:
        print('Error finding target')
        return
    gui.click(pos, duration=0.5, tween=gui.easeInOutQuint)

def calculate(calculation):
    subprocess.Popen("calc.exe")
    time.sleep(1)
    for digit in calculation.replace(' ', ''):
        click(digit)
    click('=')
    gui.hotkey('ctrl', 'c')
    time.sleep(1)
    gui.hotkey('alt', 'f4')
    return clipboard.paste().replace(',', '.')

def check(calculation, result):
    return abs(eval(calculation) - float(result)) < 1e-12

calculation = input('Enter calculation: ')
result = calculate(calculation)

if check(calculation, result):
    print(f'{calculation} = {result}')
else:
    print(f'Something went wrong, maybe we overdid it...')

time.sleep(5)
