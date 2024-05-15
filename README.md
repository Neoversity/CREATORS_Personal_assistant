# PPF_BP_Personal_assistant  (Python Programming: Foundations and Best Practices)

# Installing and launching the application

- Clone https://github.com/Neoversity/PPF_BP_Personal_assistant.git
- python -m venv venv
- venv\Scripts\activate
- pip install -r requirements.txt
- py main.py

# Branch naming  !!!!
Use feature / BotAss-Ticket## flow style Example: 
branch name to work on feature c## 
branch name for releale releale/release-1.0 major branch always main

# Фінальний проєкт​
1. Save contacts with names, addresses, phone numbers, email and birthdays to the contact book;
2. Display a list of contacts whose birthday is a specified number of days from the current date;
3. Check the correctness of the entered phone number and email when creating or editing a record and notify the user in case of incorrect entry;
4. Search for specified contacts in book contacts;
5. Edit and delete entries from the contact book;
6. Save notes with text information;
7. Search for notes;
8. Edit and delete notes;
9. Add "tags" to notes, keywords describing the topic and subject of the record;
10. Search and sort notes by keywords (tags);
11. Analyze the entered text and try to guess what the user wants from it and suggest the nearest command for execution
12. Test bug fixes


## Основні завдання, які стоятимуть перед командою:
- У заданий термін командою виконати проєкт створення “Персонального помічника” з інтерфейсом командного рядка. Мета проєкту: Створити систему для зберігання та взаємодії з записами адресної книги та нотатками.
- Отримати практичний досвіду роботи у команді
- Взаємодіяти в команді, в т.ч. при роботі з Git
- Навчитися вирішувати конфлікти при злитті гілок
- Розвинути навик модульного підходу до розробки
- Отримати досвід виконання композиції проєкту
- Отримати досвід планування та постановки завдань
- Отримати досвід роботи з Trello
- Отримати досвід на позиції Team Lead команди (додатково, за бажанням)
- Отримати досвід на позиції Scrum Master команди (додатково, за бажанням)
- Отримати досвід презентації проєктів

## Критерії прийому роботи
- Проєкт розташований у загальнодоступному репозиторії на GitHub (можна використати альтернативу таку як GitLab або BitBucket).
- Наявність коментарів та документації до коду. Присутня докладна інструкція щодо встановлення та використання застосунку описана в файлі Readme.md.
- Проєкт можна встановити як Python-пакет та викликати з будь-якого місця системи.
- Коректність реалізації всіх вимог. Всі вимоги, описані вище, хоча б частково реалізовано.
- Інтерфейс користувача реалізовано в вигляді командного рядка.
- Інтерфейс користувача базується на текстових повідомленнях та командах, які користувач вводить з клавіатури.
- Зручність та логічність інтерфейсу командного рядка.
- Програма взаємодіє з користувачем в циклі, пропонуючи вибрати команду та обробляючи її, поки користувач не введе команду для виходу.
- Дані коректно зберігаються на жорсткому диску і не втрачаються після перезапуску помічника.
- Відсутність помилок у коді при виконані застосунку.
- Програма повинна коректно обробляти некоректне введення даних користувача без закриття програми.
- Ефективність використання ООП, спадкування та композиції.
- Правильна реалізація валідації для кожного поля.
- Код повинен бути чистим, структурованим та дотримуватися стандартів PEP 8.


### Release plan
0. Release 0.1 - Start
1. Release 1.0 - implement features from 1 to 10
2. Release 1.1 - implement feature 11
3. Release 2.0 - implement user iteraction interface (replace terminal commands iteraction)

# Branch naming
Use feature / BotAss-Ticket## flow style Example: 
branch name to work on feature c## 
branch name for releale releale/release-1.0 major branch always main

1. Keep main always in working condition (No errors,failures allowed) , merge into main releale branches only after PR approves from team members , merged branch should be green .
2. Never!!!!! rename main branch
3. To start work on new feature ticket , create new branch from upcoming release branch . When work on feature done , create Pull Request into release branch , add reviewers into your PR. After work on PR comments and final approves from team merge feature branch into release branch.
4. Do not temper to add comments into your code . Team members will appreciate your work.

