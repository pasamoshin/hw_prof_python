from pprint import pprint
from application.data import *
from application.parsing import *



if __name__ == "__main__":
    contacts_list = get_raw(r'data/phonebook_raw.csv')
    contacts_list = mod_fio(contacts_list)
    contacts_list = change_number(contacts_list)
    contacts_list = remove_duplicates(contacts_list)
    # print(contacts_list)
    save("phonebook.csv", contacts_list)
        