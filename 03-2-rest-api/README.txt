GET the list (�������� ������ �������������):
curl http://localhost:5000/todos


GET a single task (�������� ������ ������������ �� id):
curl http://localhost:5000/todos/4


DELETE a task (������� ������������ �� id):
curl http://localhost:5000/todos/6 -X DELETE -v


Add a new task (�������� ������ ������������):
curl http://localhost:5000/todos -d "name=Svetlana&surname=Ivanova&mail=mail3@mail.ru&tel=8757657447" -X POST -v


Update a task (�������� ������ ������������ �� id):
curl http://localhost:5000/todos/4 -d "surname=Ivanova" -X PUT -v



