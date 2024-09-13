# it-company-task-manager

Project overview
--------

it_company_task_manager is a web application for organizing workflow inside a team. 
It includes a task board and a team members managing functionality.

Setup
--------
To set up the project on your local machine, follow these steps:

1. Clone the Repository
```sh
git clone https://github.com/olenazaritska/it-company-task-manager.git
cd it_company_task_manager
```
2. Create and Activate Virtual Environment
```sh
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS/Linux)
```
3. Install Dependencies
```sh
pip install -r requirements.txt
```
4. Run Migrations
```sh
python manage.py migrate
```
5. Load Data via Fixture (includes a superuser)
```sh
python manage.py loaddata it_company_task_manager_db_data.json
```
6. Run the Development Server
```sh
python manage.py runserver
```

Usage
--------
After loading data from fixture you can use following superuser (or create another one by yourself):
  - Login: `john_doe`
  - Password: `1qazcde3`

Features
--------

- Team members
    - View team members
    - Add new team member
    - View team member details (email, position, tasks count, current tasks)
    - Update personal info
    - Remove members from the team
- Task board
    - View team tasks (task name, details, deadline, completed status, priority, type, assignees)
    - Filter tasks by completed status
    - Create new task
    - Edit existing tasks
    - Delete tasks
- Admin
    - Admin members can additionally manage task types and positions
