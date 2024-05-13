from kivy.uix.widget import Widget

from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog




class CommandLineProcessor:
    def __init__(self, address_book_app, **kwargs):
        super().__init__(**kwargs)
        self.address_book_app = address_book_app
        self.commands = {
            "add": self.add_contact,
            "change": self.change_contact,
            "phone": self.phone_search,
            "all": self.show_all_contacts,
            "add-birthday": self.add_birthday,
            "show-birthday": self.show_birthday,
            "birthdays": self.show_all_birthdays,
            "hello": self.say_hello,
            "close": self.close_app,
            "exit": self.close_app,
        }



    def on_command_entered(self, command):
        if command in self.commands:
            if command == "exit" or command == "close":
                self.address_book_app.close_app()
            else:
                self.commands[command]()
                self.address_book_app.root.ids.command_output.text = "Results of the command: " + command
        else:
            self.address_book_app.root.ids.command_output.text = "Unknown command!"

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

    def add_birthday(self):
        # Implement logic to add a birthday
        pass

    def show_birthday(self):
        # Implement logic to show a birthday
        pass

    def show_all_birthdays(self):
        # Implement logic to show all birthdays
        pass

    def say_hello(self):
        self.address_book_app.root.ids.command_output.text = "Hello!"

    def close_app(self):
        self.address_book_app.root.ids.command_output.text = "Exiting the application..."











