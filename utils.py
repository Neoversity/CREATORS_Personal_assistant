from models import User, Phone




def phone_saver(name: str, phones: str, email: str, address: str, birthday: str) -> bool:
    if name and phones:
        user = User.add(name, email, address, birthday)
        for phone in phones.split('\n'):
            Phone.add(phone, user)
        return True
    return False

def show_all_for_name(name: str):
    return [tuple([user.name, ", ".join([phone.phone for phone in user.phones]), user.id]) for user in User.find_by_name(name)]



def show_all_for_phone(phone: str):
    return [tuple([user.name, ", ".join([phone.phone for phone in user.phones]), user.id]) for user in User.find_by_phone(phone)]



def show_all_for_email(email: str):
    return [tuple([user.name, ", ".join([phone.phone for phone in user.phones]), user.id]) for user in User.find_by_email(email)]



def show_all_for_phones():
    return [tuple([user.name, ", ".join([phone.phone for phone in user.phones]), user.id]) for user in User.all()]


def delete_by_id(user_id):
    return User.delete_by_id(user_id)

