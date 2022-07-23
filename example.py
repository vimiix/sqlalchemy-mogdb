#!/bin/usr/env python3

# create database
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('mogdb://gaussdb:Qwer%401234@127.0.0.1:26000/postgres', echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    
    extend_existing = True
    # 定义三个列
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(64), unique=True, nullable=False)
    age  = Column(Integer)
    
        
    def __repr__(self):
        return 'User(id={}, name={}, age={})'.format(self.id, self.name, self.age)
    
    def __str__(self):
        return self.__repr__()


user_foo = User(name='foo', age='18')
user_bar = User(name='bar', age='81')


def print_users(sess):
    print("Current Users =================")
    for u in sess.query(User):
        print(u)
    print("===============================")


def insert_example(sess):
    print("Insert ['foo', 'bar'] ===============")
    sess.add(user_foo)
    sess.add(user_bar)
    try:
        sess.commit()
    except Exception as e:
        sess.rollback()
        print("add user error: ", str(e))
    print_users(sess)


def update_example(sess):
    print("Update 'bar' ========================")
    user_bar.age = '66'
    sess.add(user_bar)
    try:
        sess.commit()
    except Exception as e:
        sess.rollback()
        print("update user error: ", str(e))
    print_users(sess)


def delete_example(sess):
    print("Delete 'bar' ========================")
    sess.delete(user_bar)
    try:
        sess.commit()
    except Exception as e:
        sess.rollback()
        raise e
    print_users(sess)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    session = Session()

    insert_example(session)
    update_example(session)
    delete_example(session)

    session.close()
    Base.metadata.drop_all(engine)
