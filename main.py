import models
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.list import IRightBody, TwoLineAvatarIconListItem

# from kivy.uix.widget import Widget


from utils import (
    phone_saver,
    show_all_for_name,
    show_all_for_phone,
    show_all_for_email,
    show_all_for_phones,
    delete_by_id,
)


class MainWindow(MDBoxLayout):
    pass


class RightButton(IRightBody, MDIconButton):
    pass


class SearchResultsItem(TwoLineAvatarIconListItem):

    def __init__(self, user_id, **kwargs):
        super(SearchResultsItem, self).__init__(**kwargs)
        self.user_id = user_id

    def delete_phone(self):
        if delete_by_id(self.user_id):
            self.parent.remove_widget(self)


class AddressBookApp(MDApp):

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
                SearchResultsItem(text=f"{contact[0]}", secondary_text=f"{contact[1]}")
            )

    def save_contact_and_switch_to_search(
        self, name, phones, email, addresses, birthday
    ):
        if phone_saver(name, phones, email, addresses, birthday):
            app = MDApp.get_running_app()
            sm = app.root.ids.bottom_nav
            sm.switch_tab("screen search")

    def build(self):
        return MainWindow()


if __name__ == "__main__":
    AddressBookApp().run()
