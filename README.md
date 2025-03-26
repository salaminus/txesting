# Система тестирования
### Установка на удаленном сервере:
1. ssh -i yes -l USERNAME IP.IP.IP.IP [yes - ssh-key-file]
2. git clone https://github.com/USERNAME/REPO.git
3. sudo apt install python3.12-venv ЛИБО python3 -m venv .venv
4. source venv/bin/activate
5. python3 pip install -r requirements.txt


### Запуск
1. source venv/bin/activate
2. cd student_testing
3. python3 manage.py runserver IP.IP.IP.IP:8000
