### Добро пожаловать на страницу репозитория моего учебного проекта  проекта №3. 
____
### Статсус тестов:
[![Actions Status](https://github.com/K0Hb/python-project-lvl3/workflows/hexlet-check/badge.svg)](https://github.com/K0Hb/python-project-lvl3/actions)
<a href="https://codeclimate.com/github/K0Hb/python-project-lvl3/maintainability"><img src="https://api.codeclimate.com/v1/badges/2fad6650b2f651c61f97/maintainability" /></a>
<a href="https://codeclimate.com/github/K0Hb/python-project-lvl3/test_coverage"><img src="https://api.codeclimate.com/v1/badges/2fad6650b2f651c61f97/test_coverage" /></a>
______

### Описание:
page-loader - утилита, которая скачивает страницу из сети и сохраняет ее в указанную директорию (по умолчанию в директорию запуска программы).
______

### Установка:
`pip install git+https://github.com/K0Hb/python-project-lvl3.git`

### Использование:

`$ page-loader --output=/var/tmp -lelvel=error https://hexlet.io/courses`  
Где:  
`$ page-loader` - вызов утилиты  
`--output=/var/tmp` + `=/path` - указываем путь до дириектории(по умолчания сохраняет в директорию вызова)  
`-level=error` - уровень логирования (по умолчанию "info") , уровни логирования ['debug', 'info', 'error', 'warning', 'critical']  
`https://hexlet.io/courses` - любая рабочая URL ссылка  
`gendiff -h` - помощь  

__________

#### Демонстрация работы утилиты:


