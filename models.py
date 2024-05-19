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
    email = Column(String)
    addresses = Column(String)
    birthday = Column(String)

    def __str__(self):
        return self.name

    @classmethod
    def add(cls, name, email, addresses, birthday):
        user = cls(name=name, email=email, addresses=addresses, birthday=birthday)
        session.add(user)
        session.commit()
        return user

    @classmethod
    def find_by_name(cls, name):
        return session.query(cls).filter(cls.name.ilike(f"%{name}%"))

    @classmethod
    def find_by_phone(cls, phone):
        return session.query(cls).join(Phone).filter(Phone.phone.ilike(f"%{phone}%"))

    @classmethod
    def find_by_email(cls, email):
        return session.query(cls).filter(cls.email.ilike(f"%{email}%"))

    @classmethod
    def all(cls):
        return session.query(cls).all()

    @classmethod
    def delete_by_id(cls, user_id):
        user = session.query(cls).filter_by(id=user_id).first()
        if user:
            session.delete(user)
            session.commit()
            return True
        return False


class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    tag = Column(String, nullable=False)
    description = Column(String, nullable=False)

    def __str__(self):
        return self.tag

    @classmethod
    def add(cls, tag, description):
        note = cls(tag=tag, description=description)
        session.add(note)
        session.commit()
        return note

    @classmethod
    def find_by_tag(cls, tag):
        return session.query(cls).filter(cls.tag.ilike(f"%{tag}%"))

    @classmethod
    def all(cls):
        return session.query(cls).all()

    @classmethod
    def delete_note_by_id(cls, note_id):
        note = session.query(cls).filter_by(id=note_id).first()
        if note:
            session.delete(note)
            session.commit()
            return True
        return False
    


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


Base.metadata.create_all(engine)
