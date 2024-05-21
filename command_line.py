from models import Note

from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.dropdown import DropDown


from models import session


class CommandLineProcessor:

    def __init__(self, address_book_app, **kwargs):
        super().__init__(**kwargs)
        self.address_book_app = address_book_app
        self.commands = {
            "home": self.go_to_home,
            "add": self.add_contact,
            "change": self.change_contact,
            "phone": self.phone_search,
            "all": self.show_all_contacts,
            "delete": self.delete_contact,
            "add-birthday": self.add_birthday,
            "show-birthday": self.show_birthday,
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

    def add_contact(self):
        # Implement logic to add a new contact
        pass

    def change_contact(self):
        # Implement logic to change a contact
        pass

    def phone_search(self):
        # Implement logic to search for a contact by phone
        pass

    def show_all_contacts(self):
        # Implement logic to show all contacts
        pass

    def delete_contact(self):
        pass

    def add_birthday(self):
        # Implement logic to add a birthday
        pass

    def show_birthday(self):
        # Implement logic to show a birthday
        pass

    def show_all_birthdays(self):
        # Implement logic to show all birthdays
        pass

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
