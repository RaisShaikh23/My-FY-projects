class Account:
    def __init__(self , account_no , password_no):
        self.account_no = account_no
        self.password = password_no
        self.filename = f"{account_no}_account.csv"
        self.passfle = f"{account_no}_password.txt"
        try:
            k = open(self.filename)
            k.close()
        except:
            print(f"File {self.filename} Not Exist")
        else:
            print(f"Account {self.filename} Exist")

        try:
            with open(self.passfle , "r") as file:
                k = file.read()
            if k==password_no:
                print("Password Verified")
            else :
                print("incorrect password")
        except:
            print(f"Account {self.passfle} Not Exists")

    def credit(self):
         import time as tm
         td = tm.ctime()
         with open(self.passfle,"r") as rp:
             k = rp.read()
             if self.password == k and self.password !="":
                while True:
                    try:
                        Amount = int(input("\n----------------------\nEnter The credit Amount :"))
                        if Amount>0:
                            with open(self.filename,"a") as mile:
                                 k = mile.write(f"{Amount}\n")
                                 print(f"----------------------\n₹{Amount} :Credited To Your Account\n----------------------\n{td}")
                            break
                        else:
                            print("credit Amount Must Be > 0")
                    except ValueError :
                        print("Enter Amount In Integer Only !")
                    except:
                        print("Server Down !")
             else:
                 print("\nIncorrect Password Credit Fail\nCancel And Try Again !\n",td)

    def debit(self):
         import time as tm
         td = tm.ctime()
         with open(self.passfle,"r") as rp:
             k = rp.read()
             if self.password == k and self.password!="":
                 l1 = []
                 with open(self.filename) as file:
                      for i in file:
                           num = int(i.strip())
                           l1.append(num)
                 sum1 = 0
                 for j in l1:
                     sum1+=j
                 print(f"----------------------\nTotal Amount In Bank : ₹{sum1}")
                 while True:
                      try:
                          Amount = int(input("----------------------\nEnter The debit Amount :"))
                          if Amount>0 and Amount<sum1:
                              with open(self.filename,"a") as mile:
                                  k = mile.write(f"{-Amount}\n")
                                  print(f"----------------------\n₹{Amount} debited From Your Account\n----------------------\n{td}")
                                  break
                          elif sum1==0 and Amount>=0:
                              print("No Balance In Your Account !")
                          else:
                              print(f"Amount Must Be Less Than {sum1}")
                      except ValueError :
                          print("Enter Amount In Integer Only !")
                      except:
                          print("Server Down !")
             else:
                 print("\nIncorrect Password Debit Fail\nTry Again!\n",td)

    def final(self):
         import time as tm
         td = tm.ctime()
         with open(self.passfle,"r") as rp:
             k = rp.read()
             if self.password == k and self.password!="":
                 l1 = []
                 with open(self.filename) as file:
                      for i in file:
                           num = int(i.strip())
                           l1.append(num)
                 print(f"\n----------------------\nPast Transactions:\n{l1}\n----------------------\n")
                 sum2 = 0
                 for j in l1:
                     sum2+=j
                 print(f"Total Balance In Account : ₹{sum2}\n----------------------\n{td}")
             else:
                 print("\nIncorrect Password Balance Check Fail.\nCancel And Try Again!\n",td)

    def create_account(self):
         try:
              k = open(self.filename,"x")
              m = open(self.passfle,"x+")
              m.write(self.password)
              m.close()
              k.close()
         except:
              print(f"\nCustomer File {self.filename} Already Exists\n")
         else:
              print(f"Customer Account File Created :-{self.filename}")
 
print("\n**Welcome To Our Bank**")
print("\nPlz Enter Your Account No To Verify U Are New To Us Or Already Our Member ?")
User = input("Enter Account No :-")
pin = input("! Pin Should Not Empty !\nEnter Pin Here:-")
j = Account(User,pin)
print(f"\nFollowing Command Will Guide U\nEnter 1.Create Account For {User}\nEnter 2.Credit Balance\nEnter 3.Debit\nEnter 4.Total_Balance\n")
while True:
     Ask = int(input("Enter Query  Her :-"))
     if Ask==1:j.create_account()
     elif Ask==2:j.credit()
     elif Ask==3:j.debit()
     elif Ask==4:j.final()
     else:
          print("\n------------------------------\nThank You For Visiting !\n\n*** Plz Visit Again ***\n")
          break

