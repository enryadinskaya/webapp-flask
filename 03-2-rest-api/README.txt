GET the list (�������� ������ �������������):
curl http://localhost:5000/contacts


GET a single task (�������� ������ ������������ �� id):
curl http://localhost:5000/contacts/4


DELETE a task (������� ������������ �� id):
curl http://localhost:5000/contacts/6 -X DELETE -v


Add a new task (�������� ������ ������������):
curl http://localhost:5000/contacts -d "name=Svetlana&surname=Ivanova&mail=mail3@mail.ru&tel=8757657447" -X POST -v


Update a task (�������� ������ ������������ �� id):
curl http://localhost:5000/contacts/4 -d "surname=Ivanova" -X PUT -v



