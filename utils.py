from models import User, Phone


def phone_saver(name: str, phone: str) -> bool:
    if name and phone:
        user = User.add(name)
        for phone in phones.split('\n'):
            Phone.add(phone, user.id)
        return True
    return False


# def phone_saver(name: str, phone: str, email: str, address: str, birthday: str) -> bool:
#     if name and phone and email:
#         user = User.add(name)
#         for phone in phones.split('\n'):
#             Phone.add(phone, user.id)
#         return True
#     return False