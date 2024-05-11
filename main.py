# import models
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.list import IRightBody, TwoLineAvatarIconListItem

from utils import phone_saver


class MainWindow(MDBoxLayout):
    pass


class RightButton(IRightBody, MDIconButton):
    pass


class SearchResultsItem(TwoLineAvatarIconListItem):
    pass


class AddressBookApp(MDApp):
    def name_search_and_populate_results_list(self, query):
        print(query + "name")

    def phone_search_and_populate_results_list(self, query):
        print(query + "phone")

    # def email_search_and_populate_results_list(self, query):
    #     print(query + "email")

    # def save_contact_and_switch_to_search(self, name, phones, emails, addresses, birthday):
    #     if phone_saver(name, phones, emails, addresses, birthday):
    #         pass

    def save_contact_and_switch_to_search(self, name, phones):
        if phone_saver(name, phones):
            pass      



    def build(self):
        return MainWindow()


if __name__ == "__main__":
    AddressBookApp().run()
