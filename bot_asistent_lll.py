from collections import UserDict
from datetime import datetime, timedelta

class Field:
 
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass

class Birthday(Field):
    def __init__(self, value):
        if isinstance(value, datetime):
            # If value is already a datetime object, use it directly
            self.value = value
        else:
            try:
                # Try to create a datetime object from the given value
                self.value = datetime.strptime(value, "%d.%m.%Y")
            except ValueError:
                raise ValueError("Invalid date format. Try DD.MM.YYYY")

class Phone(Field):
    # phone number validation has been implemented (must be 10 digits).
     def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Invalid number. The phone number must consist of 10 digits.")
        super().__init__(value)

class Record:
    # storage of the Name object in a separate attribute has been implemented.
    # storage of the list of Phone objects in a separate attribute has been implemented.
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthdays = []

    def add_birthday(self, birthday):
        self.birthdays.append(Birthday(birthday))
           
    # implemented method for adding 
    def add_phone(self, phone): 
        self.phones.append(Phone(phone))
       
    # implemented method for removing
    def remove_phone(self, name):
        for phn in self.phones:
            if self.name.value == name:
                self.phones.remove(phn)
       
    # implemented method for editing
    def edit_phone(self, name, new_phone):
        for phn in self.phones:
            if self.name.value == name:
                phn.value = new_phone
                return new_phone
       
    # implemented method for finding Phone objects
    def find_phone(self, name):
        for phn in self.phones:
            if self.name.value == name:
                return phn.value
            
    # implemented method for showing Birthday objects
   
    def show_birthday(self, name):
        for brthd in self.birthdays:
            if self.name.value == name:
                return brthd.value

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, b-day: {'; '.join(p.value.strftime('%d.%m.%Y') for p in self.birthdays)}."

class AddressBook(UserDict):

    # add records to self.data
    def add_record(self, contact):
        self.data[contact.name.value] = contact 

    # find record by the name      
    def find(self, name):
        return self.data.get(name)
    
    # delete record by the name      
    def delete(self, name):
        if name in self.data:
            del self.data[name]

    #get birthdays that will happen in the next week.
    def get_birthdays_per_week(self):
        birthday_next_week_dict = {}
        today = datetime.today().date()

        for name, contact in self.data.items():
            for birthday in contact.birthdays:
                birthdayConverted = birthday.value.date()
                birthday_this_year = birthdayConverted.replace(year=today.year)

                if birthday_this_year < today:
                    birthday_next_year = birthdayConverted.replace(year=today.year + 1)
                    delta_days = (birthday_next_year - today).days
                else:
                    delta_days = (birthday_this_year - today).days

                birthday_weekday = birthday_this_year.weekday()

                if delta_days < 7:
                    if birthday_weekday >= 5:
                        days = 7 - birthday_weekday
                        birthday_this_year += timedelta(days=days)

                    birthday_weekday_str = birthday_this_year.strftime("%A")

                    if birthday_weekday_str not in birthday_next_week_dict:
                        birthday_next_week_dict[birthday_weekday_str] = [name]
                    else:
                        birthday_next_week_dict[birthday_weekday_str].append(name)

        for day, names in birthday_next_week_dict.items():
            names_str = ", ".join(names)
            print(f"{day}: {names_str}")


def parse_input(user_input):
    parts = user_input.split()
    command = parts[0].lower() 
    args = parts[1:] 

    return command, args

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as ve:
            print(f"ValueError: {ve}. Please check your input and try again.")
        except KeyError as ke:
            print(f"KeyError: {ke}. Contact not found. Try again.")
        except IndexError as ie:
            print(f"IndexError: {ie}. Enter user name.")
        except Exception as e:
            print(f"Error: {e}. Try again.")
    return inner

@input_error
def main():
    address_book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit", "cd"]:
            print("Good bye!")
            return
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            name, phone = args[0]

            if name not in address_book:
                contact = Record(name)    
                contact.add_phone(phone)
                address_book.add_record(contact)
                print(f"Contact {name} added successfully.")
            else:
                print(f"Contact {name} already exists. Use 'change' to update.")
        elif command == "change":
            name, phone = args[0]
            contact = address_book.find(name)

            if contact:
                result = contact.edit_phone(name, phone)
                if result:
                    address_book.add_record(contact)
                    print(f"Phone number of contact {name} was changed to {result}.")
            else:
                print(f"Contact {name} not found.")

        elif command == "phone":
            name = args[0][0]
            contact = address_book.find(name)
            
            if contact:
                phoneNumber = contact.find_phone(name)
                print(f"Phone number for contact {name}: {phoneNumber}")
            else:
                print(f"Contact {name} not found.")
                
        elif command == "add-birthday":
            name, bDay = args[0]
            contact = address_book.find(name)

            if contact:
                contact.add_birthday(bDay)
                print(f"Birthday for contact {name} added successfully.")
            else:
                print(f"Contact {name} not found.")

        elif command == "show-birthday":
            name = args[0][0]
            contact = address_book.find(name)

            if contact:
                birthday = contact.show_birthday(name)
                print(f"B-Day for contact {name}: {birthday.strftime('%d.%m.%Y')}")
            else:
                print(f"Contact {name} not found.")

        elif command == "birthdays":
            address_book.get_birthdays_per_week()     
        elif command == "all":
            result = ""
            for name, contacts in address_book.items():
                result += f" {contacts}\n"
            print(result.strip())

        elif command == "delete-phone":
            name = args[0][0]
            contact = address_book.find(name)  

            if contact:
                contact.remove_phone(name)  
                print(f"Phone number of {name} was found and deleted.")
            else:
                print(f"Contact {name} not found.")

        elif command == "delete":
            name = args[0][0]
            contact = address_book.find(name)  

            if contact:
                address_book.delete(name)  
                print(f"Contact {name} was found and deleted.")
            else:
                print(f"Contact {name} not found.")
        else:
            print("Invalid command. Try again") 

if __name__ == "__main__":
    main()