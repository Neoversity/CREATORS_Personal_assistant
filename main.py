# import models

# from kivy.uix.widget import Widget
from kivymd.app import MDApp
# from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.list import IRightBody, TwoLineAvatarIconListItem

# from kivymd.uix.button import MDFlatButton
# from kivymd.uix.dialog import MDDialog

from models import Note, User

from command_line import CommandLineProcessor

# from models import session


from utils import (
    phone_saver,
    show_all_for_name,
    show_all_for_phone,
    show_all_for_email,
    show_all_for_phones,
    delete_by_id,
    is_valid_phone,
    note_saver,
    show_all_for_note,
    # delete_note_by_id,
)


class MainWindow(MDBoxLayout):
    pass


class RightButton(IRightBody, MDIconButton):
    pass


class SearchResultsItem(TwoLineAvatarIconListItem):

    def __init__(self, note_id=None, user_id=None, **kwargs):
        super(SearchResultsItem, self).__init__(**kwargs)
        self.note_id = note_id
        self.user_id = user_id

    def delete(self):
        if self.note_id:
            note = Note.find_by_tag(self.note_id)
            if note:
                if Note.delete_note_by_id(self.note_id):
                    self.parent.remove_widget(self)
                    print(f"Note {self.note_id} deleted successfully")
                else:
                    print(f"Failed to delete note {self.note_id}")
            else:
                print(f"Note {self.note_id} does not exist")
        elif self.user_id:
            print(f"Deleting user {self.user_id}")
            user = User.find_by_name(self.user_id)
            if user:
                if delete_by_id(self.user_id):
                    self.parent.remove_widget(self)
                    print(f"User {self.user_id} deleted successfully")
                else:
                    print(f"Failed to delete user {self.user_id}")
            else:
                print(f"User {self.user_id} does not exist")


class AddressBookApp(MDApp):

    def process_command(self, command):
        self.command_processor.on_command_entered(command)

    def show_all(self):
        app = MDApp.get_running_app()
        result_list_widget = app.root.ids.search_results
        result_list_widget.clear_widgets()
        for contact in show_all_for_phones():
            result_list_widget.add_widget(
                SearchResultsItem(
                    text=f"{contact[0]}",
                    secondary_text=f"{contact[1]}",
                    user_id=contact[2],
                )
            )

    def name_search_and_populate_results_list(self, query):
        app = MDApp.get_running_app()
        result_list_widget = app.root.ids.search_results
        result_list_widget.clear_widgets()
        for contact in show_all_for_name(query):
            result_list_widget.add_widget(
                SearchResultsItem(
                    text=f"{contact[0]}",
                    secondary_text=f"{contact[1]}",
                    user_id=contact[2],
                )
            )

    def phone_search_and_populate_results_list(self, query):
        app = MDApp.get_running_app()
        result_list_widget = app.root.ids.search_results
        result_list_widget.clear_widgets()
        for contact in show_all_for_phone(query):
            result_list_widget.add_widget(
                SearchResultsItem(
                    text=f"{contact[0]}",
                    secondary_text=f"{contact[1]}",
                    user_id=contact[2],
                )
            )

    def email_search_and_populate_results_list(self, query):
        app = MDApp.get_running_app()
        result_list_widget = app.root.ids.search_results
        result_list_widget.clear_widgets()
        for contact in show_all_for_email(query):
            result_list_widget.add_widget(
                SearchResultsItem(
                    text=f"{contact[0]}",
                    secondary_text=f"{contact[1]}",
                    user_id=contact[2],
                )
            )

    def birthday_search_and_populate_results_list(self, query):
        print("birthday_search_and_populate_results_list")

    def save_contact_and_switch_to_search(
        self, name, phones, email, addresses, birthday
    ):
        if not is_valid_phone(phones):
            self.root.ids.message_label.text = (
                "Invalid format phone \nPhone must be : 1234567890"
            )
            return
        else:
            self.root.ids.message_label.text = ""
        if phone_saver(name, phones, email, addresses, birthday):
            app = MDApp.get_running_app()
            sm = app.root.ids.bottom_nav
            sm.switch_tab("screen search")

    def show_all_note(self):
        app = MDApp.get_running_app()
        result_list_widget = app.root.ids.search_results
        result_list_widget.clear_widgets()
        for note in show_all_for_note(""):
            result_list_widget.add_widget(
                SearchResultsItem(
                    text=f"{note[0]}",
                    secondary_text=f"{note[1]}",
                    note_id=note[2],
                )
            )

    def note_search_and_populate_results_list(self, query):
        app = MDApp.get_running_app()
        result_list_widget = app.root.ids.search_results
        result_list_widget.clear_widgets()
        try:
            notes = show_all_for_note(query)
            for note in notes:
                result_list_widget.add_widget(
                    SearchResultsItem(
                        text=f"{note[0]}",
                        secondary_text=f"{note[1]}",
                        note_id=note[2],
                    )
                )
        except Exception as e:
            print(f"Error loading notes from the database: {e}")

    def save_note_and_switch_to_search(self, tag, description):
        last_note_id = note_saver(tag, description)
        if last_note_id:
            self.note_id = last_note_id  # Зберігаємо id нотатки як атрибут класу
            app = MDApp.get_running_app()
            sm = app.root.ids.bottom_nav
            sm.switch_tab("screen search")
            print(f"Last note saved with id: {self.note_id}")

    def build(self):
        self.command_processor = CommandLineProcessor(self)
        return MainWindow()

    def close_app(self, *args):
        self.stop()


if __name__ == "__main__":
    app = AddressBookApp()
    command_line_processor = CommandLineProcessor(app)
    app.run()
