from models import Note, User

from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from kivy.uix.dropdown import DropDown


from models import session

from utils import is_valid_phone, is_valid_email, is_valid_phone_number


class CommandLineProcessor:

    def __init__(self, address_book_app, **kwargs):
        super().__init__(**kwargs)
        self.address_book_app = address_book_app
        self.commands = {
            "home": self.go_to_home,
            "add": self.add_contact,
            "add_phone": self.add_phone_to_contact,
            "change": self.change_contact,
            "phone": self.phone_search,
            "all": self.show_all_contacts,
            "delete": self.delete_contact,
            "add-birthday": self.add_birthday,
            "show-birthday": self.show_birthday,
            "show_all_birthdays": self.show_all_birthdays,
            "birthdays": self.show_all_birthdays,
            "hello": self.say_hello,
            "close": self.close_app,
            "exit": self.close_app,
            "add_note": self.add_note,
            "all_note": self.show_all_note,
            "delete_note": self.delete_note,
            "search_note": self.search_note,
        }
        self.dropdown = None  # Додати змінну для DropDown

    def show_suggestions(self, text):
        # Показуємо пропозиції тільки якщо введено хоча б одну літеру
        if len(text) > 0:
            suggestions = [cmd for cmd in self.commands if cmd.startswith(text)]
            self.update_dropdown(suggestions)
        else:
            if self.dropdown:
                self.dropdown.dismiss()
                self.dropdown = None

    def update_dropdown(self, suggestions):
        if self.dropdown:
            self.dropdown.dismiss()

        self.dropdown = DropDown()
        for suggestion in suggestions:
            btn = Button(text=suggestion, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.select_suggestion(btn.text))
            self.dropdown.add_widget(btn)

        self.dropdown.open(self.address_book_app.root.ids.command_input)

    def select_suggestion(self, suggestion):
        self.address_book_app.root.ids.command_input.text = suggestion
        self.execute_command(suggestion)  # Додати автоматичне виконання команди

    def execute_command(self, command):
        if command in self.commands:
            self.commands[command]()
            self.address_book_app.root.ids.command_output.text = (
                "Results of the command: " + command
            )
        else:
            self.address_book_app.root.ids.command_output.text = "Unknown command!"

    def on_command_entered(self, command):
        self.execute_command(command)

    # def add_contact(self):
    #     self.address_book_app.root.ids.command_output_result.text = (
    #         "Please enter contact details (name, email, addresses, birthday):"
    #     )
    #     self.address_book_app.root.ids.command_input.bind(
    #         on_text_validate=self.process_add_contact_input
    #     )
    #     self.address_book_app.root.ids.command_input.text = ""

    # def process_add_contact_input(self, instance):
    #     input_text = instance.text
    #     details = input_text.split()
    #     if len(details) != 4:
    #         self.address_book_app.root.ids.command_output_result.text = (
    #             "Invalid input. Please enter name, email, addresses, and birthday separated by spaces."
    #         )
    #         return True
    #     name, email, addresses, birthday = details
    #     User.add(name, email, addresses, birthday)
    #     self.address_book_app.root.ids.command_output_result.text = (
    #         f"Contact {name} added successfully."
    #     )
    #     self.address_book_app.root.ids.command_input.text = ""
    #     self.address_book_app.root.ids.command_input.unbind(
    #         on_text_validate=self.process_add_contact_input
    #     )
    #     return True
    def add_contact(self):
        self.address_book_app.root.ids.command_output_result.text = (
            "Please enter contact details <name> <email> <addresses> <birthday>:"
        )
        self.address_book_app.root.ids.command_input.bind(
            on_text_validate=self.process_add_contact_input
        )
        self.address_book_app.root.ids.command_input.text = ""

    def process_add_contact_input(self, instance):
        input_text = instance.text
        details = input_text.split()
        if len(details) != 4:
            self.address_book_app.root.ids.command_output_result.text = (
                "Invalid input. Please enter <name> <email> <addresses> <birthday> separated by spaces."
            )
            return True
        name, email, addresses, birthday = details
        if not is_valid_email(email):
            self.address_book_app.root.ids.command_output_result.text = (
                "Invalid email format. Please enter a valid email address."
            )
            return True
        # Перевірка на унікальність електронної пошти
        if User.find_by_email(email):
            self.address_book_app.root.ids.command_output_result.text = (
                "Email already exists in the database. Please use a different email."
            )
            return True
        # Додавання контакту
        user = User.add(name, email, addresses, birthday)
        self.address_book_app.root.ids.command_output_result.text = (
            f"Contact {user.name} added successfully."
        )
        self.address_book_app.root.ids.command_input.text = ""
        self.address_book_app.root.ids.command_input.unbind(
            on_text_validate=self.process_add_contact_input
        )
        return True


    def add_phone_to_contact(self):
        self.address_book_app.root.ids.command_output_result.text = (
            "Please enter the user ID and the new phone number (10 digits) <user_id> <phone_number> ....<n>:"
        )
        self.address_book_app.root.ids.command_input.bind(
            on_text_validate=self.process_add_phone_input
        )
        self.address_book_app.root.ids.command_input.text = ""

    def process_add_phone_input(self, instance):
        input_text = instance.text
        parts = input_text.split()
        if len(parts) < 2:
            self.address_book_app.root.ids.command_output_result.text = (
                "Invalid input. Please enter user_id and phone_numbers separated by space."
            )
            return True
        user_id, *new_phones = parts
        try:
            user_id = int(user_id)
        except ValueError:
            self.address_book_app.root.ids.command_output_result.text = (
                "Invalid user_id. Please enter a valid integer."
            )
            return True

        # Перевірка кожного телефонного номера на валідність
        for phone in new_phones:
            if not is_valid_phone(phone):
                self.address_book_app.root.ids.command_output_result.text = (
                    "Invalid phone number format. Please enter a valid phone number."
                )
                return True

        # Додавання телефонних номерів до контакту
        user = User.find_by_id(user_id)
        if user:
            user.add_phone_to_contact(new_phones)
            self.address_book_app.root.ids.command_output_result.text = (
                f"Phone numbers {', '.join(new_phones)} added to user {user.name} successfully."
            )
        else:
            self.address_book_app.root.ids.command_output_result.text = (
                f"User with ID {user_id} not found."
            )
        self.address_book_app.root.ids.command_input.text = ""
        self.address_book_app.root.ids.command_input.unbind(
            on_text_validate=self.process_add_phone_input
        )
        return True


    def change_contact(self):
        self.address_book_app.root.ids.command_output_result.text = (
            "Please enter the ID of the contact you want to change:"
        )
        self.address_book_app.root.ids.command_input.bind(
            on_text_validate=self.process_change_contact_input
        )

    def process_change_contact_input(self, instance):
        input_text = instance.text
        try:
            user_id = int(input_text)
            user = session.query(User).get(user_id)
            if user:
                self.edit_contact(user)
            else:
                self.address_book_app.root.ids.command_output_result.text = (
                    f"No contact found with ID {user_id}."
                )
        except ValueError:
            self.address_book_app.root.ids.command_output_result.text = (
                "Please enter a valid contact ID."
            )
        self.address_book_app.root.ids.command_input.text = ""
        self.address_book_app.root.ids.command_input.unbind(
            on_text_validate=self.process_change_contact_input
        )
        return True

    def edit_contact(self, user):
        popup = Popup(title=f"Edit Contact ID: {user.id}", size_hint=(0.8, 0.8))
        layout = BoxLayout(orientation="vertical")
        name_input = TextInput(text=user.name, multiline=False)
        email_input = TextInput(text=user.email, multiline=False)
        addresses_input = TextInput(text=user.addresses, multiline=True)
        birthday_input = TextInput(text=user.birthday, multiline=False)
        save_button = Button(text="Save")
        save_button.bind(
            on_release=lambda instance: self.save_edited_contact(
                user, name_input.text, email_input.text, addresses_input.text, birthday_input.text, popup
            )
        )
        layout.add_widget(name_input)
        layout.add_widget(email_input)
        layout.add_widget(addresses_input)
        layout.add_widget(birthday_input)
        layout.add_widget(save_button)
        popup.content = layout
        popup.open()

    def save_edited_contact(self, user, new_name, new_email, new_addresses, new_birthday, popup):
        user.name = new_name
        user.email = new_email
        user.addresses = new_addresses
        user.birthday = new_birthday
        session.commit()
        popup.dismiss()
        self.address_book_app.root.ids.command_output_result.text = (
            f"Contact ID: {user.id} has been updated."
        )

    def phone_search(self):
        self.address_book_app.root.ids.command_output_result.text = (
            "Please enter the phone number to search for:"
        )
        self.address_book_app.root.ids.command_input.bind(
            on_text_validate=self.process_phone_search_input
        )

    def process_phone_search_input(self, instance):
        input_text = instance.text
        users = User.find_by_phone(input_text)
        if users:
            user_list = "\n".join([str(user) for user in users])
            self.address_book_app.root.ids.command_output_result.text = (
                f"Users found with phone number '{input_text}':\n{user_list}"
            )
        else:
            self.address_book_app.root.ids.command_output_result.text = (
                f"No users found with phone number '{input_text}'."
            )
        self.address_book_app.root.ids.command_input.text = ""
        self.address_book_app.root.ids.command_input.unbind(
            on_text_validate=self.process_phone_search_input
        )
        return True

    def show_all_contacts(self):
        all_contacts = User.all()
        if all_contacts:
            contact_list = "\n".join(
                [
                    f"{contact.id}: {contact.name} - Email: {contact.email}, Phones: {[phone.phone for phone in contact.phones]}"
                    for contact in all_contacts
                ]
            )
            self.address_book_app.root.ids.command_output_result.text = f"All contacts:\n{contact_list}"
        else:
            self.address_book_app.root.ids.command_output_result.text = "No contacts found."
        self.address_book_app.root.ids.command_input.text = ""


    def delete_contact(self):
        self.address_book_app.root.ids.command_output_result.text = (
            "Please enter the ID of the contact you want to delete:"
        )
        self.address_book_app.root.ids.command_input.bind(
            on_text_validate=self.process_delete_contact_input
        )

    def process_delete_contact_input(self, instance):
        input_text = instance.text
        try:
            user_id = int(input_text)
            if User.delete_by_id(user_id):
                self.address_book_app.root.ids.command_output_result.text = (
                    f"Contact with ID {user_id} has been deleted."
                )
            else:
                self.address_book_app.root.ids.command_output_result.text = (
                    f"Contact with ID {user_id} does not exist."
                )
        except ValueError:
            self.address_book_app.root.ids.command_output_result.text = (
                "Invalid input. Please enter a valid contact ID."
            )
        self.address_book_app.root.ids.command_input.text = ""
        self.address_book_app.root.ids.command_input.unbind(
            on_text_validate=self.process_delete_contact_input
        )
        return True

    def add_birthday(self):
        self.address_book_app.root.ids.command_output_result.text = (
            "Please enter the ID of the contact and the birthday (format: <id> <birthday>):"
        )
        self.address_book_app.root.ids.command_input.bind(
            on_text_validate=self.process_add_birthday_input
        )
        self.address_book_app.root.ids.command_input.text = ""

    def process_add_birthday_input(self, instance):
        input_text = instance.text
        try:
            parts = input_text.split()
            if len(parts) != 2:
                raise ValueError("Invalid input format. Please enter ID and birthday separated by a space.")
            contact_id, birthday = parts
            contact_id = int(contact_id)
            contact = session.query(User).get(contact_id)
            if contact:
                contact.birthday = birthday
                session.commit()
                self.address_book_app.root.ids.command_output_result.text = (
                    f"Birthday added to contact ID {contact_id} successfully."
                )
            else:
                self.address_book_app.root.ids.command_output_result.text = (
                    f"Contact with ID {contact_id} not found."
                )
        except ValueError as e:
            self.address_book_app.root.ids.command_output_result.text = str(e)
        self.address_book_app.root.ids.command_input.text = ""
        self.address_book_app.root.ids.command_input.unbind(
            on_text_validate=self.process_add_birthday_input
        )
        return True

    def show_birthday(self):
        self.address_book_app.root.ids.command_output_result.text = (
            "Please enter the ID of the contact to show the birthday:"
        )
        self.address_book_app.root.ids.command_input.bind(
            on_text_validate=self.process_show_birthday_input
        )
        self.address_book_app.root.ids.command_input.text = ""

    def process_show_birthday_input(self, instance):
        input_text = instance.text
        try:
            contact_id = int(input_text)
            contact = session.query(User).get(contact_id)
            if contact:
                if contact.birthday:
                    self.address_book_app.root.ids.command_output_result.text = (
                        f"Birthday of contact ID {contact_id}: {contact.birthday}"
                    )
                else:
                    self.address_book_app.root.ids.command_output_result.text = (
                        f"Contact with ID {contact_id} does not have a birthday set."
                    )
            else:
                self.address_book_app.root.ids.command_output_result.text = (
                    f"Contact with ID {contact_id} not found."
                )
        except ValueError:
            self.address_book_app.root.ids.command_output_result.text = (
                "Invalid input. Please enter a valid contact ID."
            )
        self.address_book_app.root.ids.command_input.text = ""
        self.address_book_app.root.ids.command_input.unbind(
            on_text_validate=self.process_show_birthday_input
        )
        return True

    def show_all_birthdays(self):
        all_contacts = User.all()
        if all_contacts:
            birthdays_list = "\n".join(
                [
                    f"{contact.id}: {contact.name} - Birthday: {contact.birthday}"
                    for contact in all_contacts if contact.birthday
                ]
            )
            self.address_book_app.root.ids.command_output_result.text = f"All birthdays:\n{birthdays_list}"
        else:
            self.address_book_app.root.ids.command_output_result.text = "No contacts found."
        self.address_book_app.root.ids.command_input.text = ""

    def add_note(self):
        self.address_book_app.root.ids.command_output_result.text = (
            "Please enter tag and description for the note: <tag> <description>"
        )
        self.address_book_app.root.ids.command_input.bind(
            on_text_validate=self.process_note_input
        )
        self.address_book_app.root.ids.command_input.text = ""

    def process_note_input(self, instance):
        input_text = instance.text
        if input_text.lower() == "home":
            self.go_to_home()
            return True  # Повертаємо True, щоб припинити обробку події
        words = input_text.split()
        if len(words) < 2:
            self.address_book_app.root.ids.command_output_result.text = "Please enter both tag and description for the note: <tag> <description>"
            return True  # Повертаємо True, щоб припинити обробку події
        tag = words[0]
        description = " ".join(words[1:])
        Note.add(tag, description)
        self.address_book_app.root.ids.command_output_result.text = (
            "Note added successfully. \nTag: {} \nDescription: {}".format(
                tag, description
            )
        )
        self.address_book_app.root.ids.command_input.text = ""
        # Встановимо обробник on_text_validate знову
        self.address_book_app.root.ids.command_input.bind(
            on_text_validate=self.process_note_input
        )
        return True  # Повертаємо True, щоб припинити обробку події

    def show_all_note(self):
        all_notes = Note.all()
        if all_notes:
            note_list = "\n".join(
                [
                    f"{note.id}: Tag: {note.tag}, Description: {note.description}"
                    for note in all_notes
                ]
            )
            self.address_book_app.root.ids.command_output_result.text = (
                f"All notes:\n{note_list}"
            )
        else:
            self.address_book_app.root.ids.command_output_result.text = (
                "No notes found."
            )
        self.address_book_app.root.ids.command_input.text = ""

    def delete_note(self):
        self.address_book_app.root.ids.command_output_result.text = (
            "Please enter the ID of the note you want to delete: <id>"
        )
        self.address_book_app.root.ids.command_input.bind(
            on_text_validate=self.process_delete_note_input
        )

    def process_delete_note_input(self, instance):
        input_text = instance.text
        try:
            note_id = int(input_text)
            if Note.delete_note_by_id(note_id):
                self.address_book_app.root.ids.command_output_result.text = (
                    f"Note with ID {note_id} has been deleted."
                )
            else:
                self.address_book_app.root.ids.command_output_result.text = (
                    f"Note with ID {note_id} does not exist."
                )
        except ValueError:
            self.address_book_app.root.ids.command_output_result.text = (
                "Invalid input. Please enter a valid note ID."
            )
        self.address_book_app.root.ids.command_input.text = ""
        # Відмінюємо обробник події on_text_validate після додавання нотатки
        self.address_book_app.root.ids.command_input.unbind(
            on_text_validate=self.process_delete_note_input
        )
        return True

    def search_note(self):
        self.address_book_app.root.ids.command_output_result.text = "Please enter the tags to search for, separated by spaces: <tag1> <tag2> ..."
        self.address_book_app.root.ids.command_input.bind(
            on_text_validate=self.process_search_note_input
        )
        self.address_book_app.root.ids.command_input.text = ""

    def process_search_note_input(self, instance):
        input_text = instance.text
        if input_text.lower() == "home":
            self.go_to_home()
            return True  # Return True to stop event processing

        # Split the input text into tags
        tags = input_text.split()
        all_notes = []

        # Search for notes by each tag
        for tag in tags:
            notes = Note.find_by_tag(tag)
            all_notes.extend(notes)

        if all_notes:
            note_list = "\n".join(
                [
                    f"{note.id}: Tag: {note.tag}, Description: {note.description}"
                    for note in all_notes
                ]
            )
            self.address_book_app.root.ids.command_output_result.text = (
                f"Notes found for tags '{input_text}':\n{note_list}"
            )
            # Ask the user if they want to change a note
            self.address_book_app.root.ids.command_output_result.text += "\n\nDo you want to change a note? Enter its ID or type 'home' to return to the main menu:"
            self.address_book_app.root.ids.command_input.text = ""
            self.address_book_app.root.ids.command_input.bind(
                on_text_validate=self.process_change_note_input
            )
        else:
            self.address_book_app.root.ids.command_output_result.text = (
                f"No notes found for tags '{input_text}'."
            )
            # Ask the user for the next request or return to the main menu
            self.address_book_app.root.ids.command_output_result.text += "\n\nEnter next tags to search for, or type 'home' to return to the main menu:"
            self.address_book_app.root.ids.command_input.text = ""
            # Unbind the on_text_validate event handler after searching for notes
            self.address_book_app.root.ids.command_input.unbind(
                on_text_validate=self.process_search_note_input
            )
        # Return False to let Kivy continue event processing
        return False

    def process_change_note_input(self, instance):
        input_text = instance.text
        if input_text.lower() == "home":
            self.go_to_home()
            return True  # Return True to stop event processing

        try:
            note_id = int(input_text)
            note = session.query(Note).get(note_id)
            if note:
                self.edit_note(note)
            else:
                self.address_book_app.root.ids.command_output_result.text = (
                    f"No note found with ID {note_id}."
                )
        except ValueError:
            self.address_book_app.root.ids.command_output_result.text = (
                "Please enter a valid note ID."
            )

        # Ask the user for the next request or return to the main menu
        self.address_book_app.root.ids.command_output_result.text += "\n\nEnter next note ID to change, or type 'home' to return to the main menu:"
        self.address_book_app.root.ids.command_input.text = ""
        # Unbind the on_text_validate event handler after searching for notes
        self.address_book_app.root.ids.command_input.unbind(
            on_text_validate=self.process_change_note_input
        )
        # Return False to let Kivy continue event processing
        return False

    def edit_note(self, note):
        # Open a popup for editing the note
        popup = Popup(title=f"Edit Note ID: {note.id}", size_hint=(0.8, 0.8))
        layout = BoxLayout(orientation="vertical")
        tag_input = TextInput(text=note.tag, multiline=False)
        description_input = TextInput(text=note.description, multiline=True)
        save_button = Button(text="Save")
        save_button.bind(
            on_release=lambda instance: self.save_edited_note(
                note, tag_input.text, description_input.text, popup
            )
        )
        layout.add_widget(tag_input)
        layout.add_widget(description_input)
        layout.add_widget(save_button)
        popup.content = layout
        popup.open()

    def save_edited_note(self, note, new_tag, new_description, popup):
        note.tag = new_tag
        note.description = new_description
        session.commit()
        popup.dismiss()
        self.address_book_app.root.ids.command_output_result.text = (
            f"Note ID: {note.id} has been updated."
        )

    def say_hello(self):
        self.address_book_app.root.ids.command_output_result.text = (
            "Hello! \nThe 'CREATORS' team welcomes you"
        )
        self.address_book_app.root.ids.command_input.text = ""

    def close_app(self):
        self.address_book_app.stop()

    def go_to_home(self):
        # Повертаємо до початкового стану для вибору команди
        self.address_book_app.root.ids.command_output_result.text = (
            "You are returned to the main screen"
        )
        self.address_book_app.root.ids.command_input.text = ""
        # Відмінюємо обробник події on_text_validate, якщо він був встановлений
        self.address_book_app.root.ids.command_input.unbind(
            on_text_validate=self.process_note_input
        )
        self.waiting_for_note = (
            False  # Змінюємо стан, що користувач більше не очікує введення нотатки
        )
