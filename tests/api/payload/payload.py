from sqlalchemy import Boolean, false

valid_created_payload = {
   "username": "newUser",
   "password": "validPassword",
}

api_payload = {
   "username": "newUser1",
   "password": "validPassword1",
}

invalid_create_payload = {
   "username": 1,
   "password": "validPassword",
}

invalid_password_less_than_6_digits = {
   "username": "hello",
   "password": "short"
}

valid_task_template = {
   "title": "Trial task",
   "description": "some description",
   "completed": True
}

valid_edited_task_template = {
   "title": "Updated task",
   "description": "new description",
   "completed": True
}

invalid_task_template_no_title = {
   "title": "",
   "description": "12123",
   "completed": True
}

invalid_task_template_no_description = {
   "title": "asdassd",
   "description": "",
   "completed": True
}