# Не завершено - не коммитить!
# python3 -i manage.py runscript db_test_environment

"""Создание пустой базы данных и добавление в нее тестовых данных
для тестированния Django shell и приложения.
Команда запуска: python3 manage.py runscript <имя скрипта>"""

from ..tests.test_models import ModelsTests
import os, sys

def run():
    os.system("python3 manage.py test --keepdb")


