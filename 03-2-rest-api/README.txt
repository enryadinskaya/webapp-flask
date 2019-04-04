GET the list (получить список пользователей):
curl http://localhost:5000/contacts


GET a single task (получить одного пользователя по id):
curl http://localhost:5000/contacts/4


DELETE a task (удалить пользователя по id):
curl http://localhost:5000/contacts/6 -X DELETE -v


Add a new task (добавить нового пользователя):
curl http://localhost:5000/contacts -d "name=Svetlana&surname=Ivanova&mail=mail3@mail.ru&tel=8757657447" -X POST -v


Update a task (обновить данные пользователя по id):
curl http://localhost:5000/contacts/4 -d "surname=Ivanova" -X PUT -v



