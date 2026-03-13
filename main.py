import json
import random
import string
from pathlib import Path


class Bank :
    database = "data.json"
    data = []
    try:
        if Path(database).exists():
            with open(database) as fs :
                data = json.loads(fs.read())
        else:
            print("No such file found!")
    except Exception as err:
        print(f"an error occured as {err}")

    @staticmethod
    def __update():
        with open(Bank.database,'w') as fs:
            fs.write(json.dumps(Bank.data))
    @classmethod
    def __acc_num_generator(cls):
        alpha = random.choices(string.ascii_letters,k=3)
        num = random.choices(string.digits,k=3)
        spchar = random.choices("!@#$%^&*",k=1)
        id = alpha + num + spchar
        random.shuffle(id)
        return"".join(id)

    def create_account(self):
        info = {
            "name" : input("Enter your name : "),
            "age" : int(input("Enter your age : ")),
            "email" : input("Enter your email : "),
            "pin" : int(input("Enter your 4 number pin : ")),
            "account_no." : Bank.__acc_num_generator(),
            "balance" : 0
        }
        if info["age"] < 18 or len(str(info["pin"]))!=4 :
            print("Sorry you can't create an account")
        else:
            print("Your account has been created successfully!")
            for i in info:
                print(f"{i} : {info[i]}")
            print("Please note down your account number carefully.")

        Bank.data.append(info)    
        Bank.__update()

    def deposit_money(self):
        account_num = input("Enter your account_num : ")
        pin = int(input("Enter your pin aswell: "))
        print(Bank.data)
        user_data = [i for i in Bank.data if i['account_no.']== account_num and i['pin'] == pin]
        if user_data == False:
            print("Sorry No data found")
        else:
            amount = int(input("Enter, how much you want to enter : "))
            if amount>10000 or amount<0:
                print("Sorry the amount is too much you can deposit only below 10000.")
            else:
                user_data[0]['balance'] += amount
                Bank.__update()
                print("Amount deposit successfully!")
        
    def withdraw_money(self):
        account_num = input("Enter your account_num : ")
        pin = int(input("Enter your pin aswell: "))
        print(Bank.data)
        user_data = [i for i in Bank.data if i['account_no.']== account_num and i['pin'] == pin]
        if user_data == False:
            print("Sorry No data found")
        else:
            amount = int(input("Enter, how much you want to withdraw : "))
            if  user_data[0]['balance']<amount:
                print("insufficient amount.")
            elif  user_data[0]['balance']==amount:
                print("Sorry ,your account will be empty,we don't allow.")
            else:
                user_data[0]['balance'] -= amount
                Bank.__update()
                print("Amount withdrawn successfully.")

    def details(self):
        account_num = input("Enter your account_num : ")
        pin = int(input("Enter your pin aswell: "))
        
        userdata = [i for i in Bank.data if i['account_no.']== account_num and i['pin'] == pin]
        print("Your informations are \n")
        for i in userdata[0] : 
            print(f"{i} : {userdata[0][i]}")
        print("Your information print successfully. ")
    
    def update_det(self):
        account_num = input("Enter your account_num : ")
        pin = int(input("Enter your pin aswell: "))
        
        userdata = [i for i in Bank.data if i['account_no.']== account_num and i['pin'] == pin]
        if userdata == False:
            print("No such user found.")
        else:
            print("You cannot change the age, account number , balance.")
            print("Fill the details for change otherwise leave it empty.")

            new_data = {
                "name" : input("Enter you modified name or press enter to skip  : "),
                "pin" : input("Enter you new pin or press enter to skip : "),
                "email" : input("Enter your changed email or press enter to skip  : ")
                }
            if new_data["name"]=="" : 
                new_data["name"] = userdata[0]['name']
            if new_data["email"]=="" : 
                new_data["email"] = userdata[0]['email']
            if new_data["pin"]=="" : 
                new_data["pin"] = userdata[0]['pin']
            
            new_data['age'] = userdata[0]['age']

            new_data['account_no.'] = userdata[0]['account_no.']
            new_data['balance'] = userdata[0]['balance']
            if type(new_data['pin']) == str :
                new_data["pin"] == int(new_data['pin'])
                
            for i in new_data:
                if new_data[i] == userdata[0][i]:
                    continue
                else:
                    userdata[0][i] == new_data[i]
                    Bank.__update()
            print("Details updated successfully.")
    def delete(self):
        account_num = input("Enter your account_num : ")
        pin = int(input("Enter your pin aswell: "))
        
        userdata = [i for i in Bank.data if i['account_no.']== account_num and i['pin'] == pin]
        if userdata == False:
            print("No such data found.")
        else:
            check = input("press y if you actually want to delete the account or press n : ")
            if check== "n" or check == "N":
                print("Bypassed!")
            else:
                index =Bank.data.index(userdata[0])
                Bank.data.pop(index)
                print("Your account deleted successfully.")
                Bank.__update()                

user = Bank()

print("press 1 for creating an account.")
print("press 2 for deposit money in account.")
print("press 3 for withdrawal money from the account.")
print("press 4 for knowing the details of the account.")
print("press 5 for updating details of your account.")
print("press 6 for delete the account.")

check = int(input("Tell your response : "))


if check == 1:
    user.create_account()

if check ==2:
    user.deposit_money()

if check ==3:
    user.withdraw_money()

if check == 4:
    user.details()

if check ==5:
    user.update_det()

if check == 6:
    user.delete() 


#give the whole code to chatgpt and give this ---> "improvise the code and also use streamlit for implementing the code"
#use this command for betterment of the project