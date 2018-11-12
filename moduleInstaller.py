import os

while True:
    try:
        import re
        break
    except ModuleNotFoundError:
        os.system('py -m pip install re')
        os.system('python -m pip install re')

while True:
    try:
        import requests
        break
    except ModuleNotFoundError:
        os.system('py -m pip install requests')
        os.system('python -m pip install requests')
