from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///phones.sqlite", echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phones = relationship("Phone", cascade="all, delete", back_populates="user")

    def __str__(self):
        return self.name
    

    @classmethod
    def add(cls,name):
        user = cls(name=name)
        session.add(user)
        session.commit()
        return user
    

# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     phones = relationship("Phone", cascade="all, delete", back_populates="user")
#     emails = relationship("Email", cascade="all, delete", back_populates="user")
#     addresses = Column(String)
#     birthday = Column(String)

#     def __str__(self):
#         return self.name
    

#     @classmethod
#     def add(cls,name, addresses, birthday):
#         user = cls(name=name, addresses=addresses, birthday=birthday)
#         session.add(user)
#         session.commit()
#         return user    


class Phone(Base):
    __tablename__ = "phones"
    id = Column(Integer, primary_key=True)
    phone = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="phones")

    def __str__(self):
        return self.phone
    

    @classmethod
    def add(cls, phone, user):
        phone = cls(phone=phone, user=user)
        session.add(phone)
        session.commit()
        return phone
    

# class Email(Base):
#     __tablename__ = "emails"
#     id = Column(Integer, primary_key=True)
#     email = Column(String, nullable=False)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     user = relationship("User", back_populates="emails")

#     def __str__(self):
#         return self.email    

#     @classmethod
#     def add(cls, email, user):
#         email = cls(email=email, user=user)
#         session.add(email)
#         session.commit()
#         return email


Base.metadata.create_all(engine)