from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    #    def __repr__(self):
    #        return self.task

    def add_task(self, newtask, ndeadline):
        new_row = Task(task=newtask,
                       deadline=datetime.strptime(ndeadline, '%Y-%m-%d').date())
        session.add(new_row)
        session.commit()

    def todays_tasks(self):
        rows = session.query(Task).filter(Task.deadline == datetime.today().date()).all()
        if not rows:
            print('Nothing to do!')
        else:
            c = 1
            for row in rows:
                print(f"Today {datetime.today().day} {datetime.today().strftime('%b')}")
                print(f'{c}. {row.task}')
                c += 1

    def weeks_tasks(self):
        weeklist = []
        newday = datetime.today()  # Monday
#        while newday.weekday() != 0:  # get Monday
#            newday -= timedelta(days=1)
        weeklist.append(newday)
        for _ in range(1, 7):  # 建立weeklist
            newday += timedelta(days=1)
            weeklist.append(newday)
        for day in weeklist:  # 遍历打印每天的todolist
            rows = session.query(Task).filter(Task.deadline == day.date()).all()
            if not rows:
                print(f"{day.strftime('%A')} {day.day} {day.strftime('%b')}")
                print('Nothing to do!\n')
            else:
                c = 1
                for row in rows:
                    print(f"{day.strftime('%A')} {day.day} {day.strftime('%b')}")
                    print(f'{c}. {row.task}')
                    c += 1
                print('')


    def missed_tasks(self):
        print('Missed tasks:')
        rows = session.query(Task).filter(Task.deadline < datetime.today().date()).all()
        if not rows:
            print('Nothing is missed!')
        else:
            c = 1
            for row in rows:
                print(f"{c}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
                c += 1


    def all_tasks(self):
        print('All tasks:')
        rows = session.query(Task).order_by(Task.deadline).all()
        if not rows:
            print('Nothing to do!')
        else:
            c = 1
            for row in rows:
                print(f"{c}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
                c += 1

    def delete_tasks(self):
        print('Choose the number of the task you want to delete:')
        rows = session.query(Task).order_by(Task.deadline).all()
        if not rows:
            print('Nothing to delete!')
        else:
            c = 1
            for row in rows:
                print(f"{c}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
                c += 1
            session.delete(rows[int(input()) - 1])
            session.commit()
            print('The task has been deleted!')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

tl = Task()


def main_menu():
    print("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit""")
    ip = input()
    if ip == '1':
        tl.todays_tasks()
        print('')
        main_menu()
    elif ip == '2':
        tl.weeks_tasks()
        print('')
        main_menu()
    elif ip == '3':
        tl.all_tasks()
        print('')
        main_menu()
    elif ip == '5':
        print('Enter task')
        newtask = input()
        print('Enter deadline')
        ndeadline = input()
        tl.add_task(newtask, ndeadline)
        print('The task has been added!\n')
        main_menu()
    elif ip == '4':
        tl.missed_tasks()
        print('')
        main_menu()
    elif ip == '6':
        tl.delete_tasks()
        print('')
        main_menu()
    elif ip == '0':
        print('Bye!')
        exit(0)


main_menu()
