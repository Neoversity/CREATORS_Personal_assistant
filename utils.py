import re

from models import User, Phone, Note


def is_valid_phone(phone):
    # Регулярний вираз для перевірки телефонного номера у форматі +380501111111
    pattern = r"^\d{10}$"
    return re.match(pattern, phone) is not None


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
