import re
import datetime

from models import User, Phone, Note


def is_valid_phone(phone):
    # Регулярний вираз для перевірки телефонного номера у форматі +380501111111
    pattern = r"^\d{10}$"
    return re.match(pattern, phone) is not None
def is_valid_phone_number(phone_number):
    # Проста валідація номера телефону за допомогою регулярних виразів
    pattern = r'^\+?[\d\s-]+$'
    return bool(re.match(pattern, phone_number))

def is_valid_email(email):
    # Проста валідація електронної пошти за допомогою регулярних виразів
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

# def is_valid_birthday(birthday):
#     try:
#         day, month, year = map(int, birthday.split('.'))
#         if day < 1 or day > 31 or month < 1 or month > 12 or year < 1900 or year > (datetime.datetime.now().year - 100):
#             return False
#         valid_date = datetime.datetime(day, month, year)
#         return True
#     except ValueError:
#         return False


def phone_saver(
    name: str, phones: str, email: str, address: str, birthday: str
) -> bool:
    if name and phones:
        user = User.add(name, email, address, birthday)
        for phone in phones.split("\n"):
            Phone.add(phone, user)
        return True
    return False


def show_all_for_name(name: str):
    return [
        tuple([user.name, ", ".join([phone.phone for phone in user.phones]), user.id])
        for user in User.find_by_name(name)
    ]


def show_all_for_phone(phone: str):
    return [
        tuple([user.name, ", ".join([phone.phone for phone in user.phones]), user.id])
        for user in User.find_by_phone(phone)
    ]


def show_all_for_email(email: str):
    return [
        tuple([user.name, ", ".join([phone.phone for phone in user.phones]), user.id])
        for user in User.find_by_email(email)
    ]


def show_all_for_phones():
    return [
        tuple([user.name, ", ".join([phone.phone for phone in user.phones]), user.id])
        for user in User.all()
    ]


def delete_by_id(user_id):
    return User.delete_by_id(user_id)


def note_saver(tag: str, description: str) -> bool:
    if tag and description:
        note = Note.add(tag, description)
        if note:
            return note.id
    return False


def show_all_for_note(tag: str):
    return [
        tuple([note.tag, note.description, note.id]) for note in Note.find_by_tag(tag)
    ]


def delete_note_by_id(note_id):
    return Note.delete_note_by_id(note_id)


Note.delete_note_by_id(1)
